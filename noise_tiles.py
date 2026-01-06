#!/usr/bin/env python3
"""
Noise Tiles: Scale Armor Pattern Generator

A noise field drives rotation and scaling in a grid of square tiles.
Along panel borders, larger tiles overlap and interlock with their neighbours,
creating localized "scale armor" structures.
"""

import math
import numpy as np
from typing import List, Tuple
from noise_field import NoiseFieldGenerator
from svg_export import SVGExporter


class TileGenerator:
    """Generate rotated and scaled square tiles based on a noise field."""
    
    def __init__(
        self,
        width: int = 800,
        height: int = 800,
        panel_cols: int = 3,
        panel_rows: int = 3,
        tiles_per_panel: int = 10,
        gap_ratio: float = 0.05,
        noise_scale: float = 0.15,
        rotation_intensity: float = 0.8,
        scale_intensity: float = 0.6,
        seed: int = None
    ):
        """
        Initialize the tile generator.
        
        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
            panel_cols: Number of panel columns (e.g., 3)
            panel_rows: Number of panel rows (e.g., 3)
            tiles_per_panel: Number of tiles per panel side (e.g., 10 for 10x10)
            gap_ratio: Gap between panels as ratio of total size (e.g., 0.05 for 5%)
            noise_scale: Scale factor for noise (larger = more variation)
            rotation_intensity: How much rotation to apply (0-1)
            scale_intensity: How much scaling to apply (0-1)
            seed: Random seed for reproducible results
        """
        self.width = width
        self.height = height
        self.panel_cols = panel_cols
        self.panel_rows = panel_rows
        self.tiles_per_panel = tiles_per_panel
        self.gap_ratio = gap_ratio
        self.rotation_intensity = rotation_intensity
        self.scale_intensity = scale_intensity
        
        # Calculate panel dimensions
        total_gap_width = width * gap_ratio * (panel_cols - 1)
        total_gap_height = height * gap_ratio * (panel_rows - 1)
        self.panel_width = (width - total_gap_width) / panel_cols
        self.panel_height = (height - total_gap_height) / panel_rows
        self.gap_width = width * gap_ratio
        self.gap_height = height * gap_ratio
        
        # Calculate tile size within each panel
        self.tile_width = self.panel_width / tiles_per_panel
        self.tile_height = self.panel_height / tiles_per_panel
        
        # Create noise field generators for rotation and scale
        self.noise_rotation = NoiseFieldGenerator(
            width=width,
            height=height,
            resolution=int(self.tile_width * 2),
            noise_scale=noise_scale,
            octaves=3,
            persistence=0.5,
            seed=seed if seed else np.random.randint(0, 10000)
        )
        
        self.noise_scale = NoiseFieldGenerator(
            width=width,
            height=height,
            resolution=int(self.tile_width * 2),
            noise_scale=noise_scale * 0.8,
            octaves=2,
            persistence=0.6,
            seed=self.noise_rotation.seed + 1000
        )
    
    def _create_grid_tile(
        self,
        center_x: float,
        center_y: float,
        size: float,
        rotation: float,
        grid_divisions: int = 5
    ) -> List[List[Tuple[float, float]]]:
        """
        Create a tile with internal grid lines.
        
        Args:
            center_x: X coordinate of tile center
            center_y: Y coordinate of tile center
            size: Size of the tile
            rotation: Rotation angle in radians
            grid_divisions: Number of grid divisions (e.g., 5 creates 5x5 grid)
            
        Returns:
            List of line segments forming the grid
        """
        half_size = size / 2
        lines = []
        
        # Create horizontal lines
        for i in range(grid_divisions + 1):
            y = -half_size + (i / grid_divisions) * size
            x1, y1 = -half_size, y
            x2, y2 = half_size, y
            
            # Rotate points
            rx1 = x1 * math.cos(rotation) - y1 * math.sin(rotation)
            ry1 = x1 * math.sin(rotation) + y1 * math.cos(rotation)
            rx2 = x2 * math.cos(rotation) - y2 * math.sin(rotation)
            ry2 = x2 * math.sin(rotation) + y2 * math.cos(rotation)
            
            # Translate
            lines.append([
                (center_x + rx1, center_y + ry1),
                (center_x + rx2, center_y + ry2)
            ])
        
        # Create vertical lines
        for i in range(grid_divisions + 1):
            x = -half_size + (i / grid_divisions) * size
            x1, y1 = x, -half_size
            x2, y2 = x, half_size
            
            # Rotate points
            rx1 = x1 * math.cos(rotation) - y1 * math.sin(rotation)
            ry1 = x1 * math.sin(rotation) + y1 * math.cos(rotation)
            rx2 = x2 * math.cos(rotation) - y2 * math.sin(rotation)
            ry2 = x2 * math.sin(rotation) + y2 * math.cos(rotation)
            
            # Translate
            lines.append([
                (center_x + rx1, center_y + ry1),
                (center_x + rx2, center_y + ry2)
            ])
        
        return lines
    
    def _is_border_tile(self, panel_row: int, panel_col: int, tile_row: int, tile_col: int) -> bool:
        """Check if a tile is on the border of its panel."""
        # Check if at edge of panel
        if tile_row == 0 or tile_row == self.tiles_per_panel - 1:
            return True
        if tile_col == 0 or tile_col == self.tiles_per_panel - 1:
            return True
        
        # Check if near center dividing lines
        mid = self.tiles_per_panel // 2
        if abs(tile_row - mid) <= 1 or abs(tile_col - mid) <= 1:
            return True
        
        return False
    
    def generate_tiles(self) -> List[List[Tuple[float, float]]]:
        """
        Generate all tiles based on the noise field.
        
        Returns:
            List of lines (each line is a list of points)
        """
        all_lines = []
        
        for panel_row in range(self.panel_rows):
            for panel_col in range(self.panel_cols):
                # Calculate panel offset
                panel_x = panel_col * (self.panel_width + self.gap_width)
                panel_y = panel_row * (self.panel_height + self.gap_height)
                
                # Generate tiles within this panel
                for tile_row in range(self.tiles_per_panel):
                    for tile_col in range(self.tiles_per_panel):
                        # Calculate tile center within panel
                        center_x = panel_x + (tile_col + 0.5) * self.tile_width
                        center_y = panel_y + (tile_row + 0.5) * self.tile_height
                        
                        # Get noise values for rotation and scale
                        rotation_noise = self.noise_rotation.get_angle_at(center_x, center_y)
                        scale_noise = self.noise_scale.get_angle_at(center_x, center_y)
                        
                        # Map noise to rotation
                        rotation = (rotation_noise - math.pi) * self.rotation_intensity
                        
                        # Map noise to scale - wider range for more variation
                        base_scale = 0.3 + (scale_noise / (2 * math.pi)) * 1.4
                        scale_factor = 0.5 + base_scale * self.scale_intensity
                        
                        # Border tiles get larger scale
                        if self._is_border_tile(panel_row, panel_col, tile_row, tile_col):
                            scale_factor *= 1.4 + scale_noise / (2 * math.pi) * 0.6
                        
                        # Calculate tile size with more variation
                        tile_size = min(self.tile_width, self.tile_height) * scale_factor
                        
                        # Create the tile with internal grid
                        grid_lines = self._create_grid_tile(center_x, center_y, tile_size, rotation)
                        all_lines.extend(grid_lines)
        
        return all_lines
    
    def generate_nested_tiles(self) -> List[List[Tuple[float, float]]]:
        """
        Generate tiles with nested grid squares for more detail.
        
        Returns:
            List of lines forming tiles with nested grids
        """
        all_lines = []
        
        for panel_row in range(self.panel_rows):
            for panel_col in range(self.panel_cols):
                # Calculate panel offset
                panel_x = panel_col * (self.panel_width + self.gap_width)
                panel_y = panel_row * (self.panel_height + self.gap_height)
                
                # Generate tiles within this panel
                for tile_row in range(self.tiles_per_panel):
                    for tile_col in range(self.tiles_per_panel):
                        # Calculate tile center within panel
                        center_x = panel_x + (tile_col + 0.5) * self.tile_width
                        center_y = panel_y + (tile_row + 0.5) * self.tile_height
                        
                        # Get noise values
                        rotation_noise = self.noise_rotation.get_angle_at(center_x, center_y)
                        scale_noise = self.noise_scale.get_angle_at(center_x, center_y)
                        
                        # Map noise to rotation
                        rotation = (rotation_noise - math.pi) * self.rotation_intensity
                        
                        # Map noise to scale - wider range for more variation
                        base_scale = 0.3 + (scale_noise / (2 * math.pi)) * 1.4
                        scale_factor = 0.5 + base_scale * self.scale_intensity
                        
                        # Border tiles get special treatment
                        is_border = self._is_border_tile(panel_row, panel_col, tile_row, tile_col)
                        if is_border:
                            scale_factor *= 1.4 + scale_noise / (2 * math.pi) * 0.6
                        
                        # Calculate base tile size with more variation
                        base_size = min(self.tile_width, self.tile_height) * scale_factor
                        
                        # Determine grid density based on scale
                        if scale_factor > 1.3:
                            grid_div = 8  # More grid lines for larger tiles
                        elif scale_factor > 1.1:
                            grid_div = 6
                        else:
                            grid_div = 5
                        
                        # Create main tile with grid
                        grid_lines = self._create_grid_tile(center_x, center_y, base_size, rotation, grid_div)
                        all_lines.extend(grid_lines)
        
        return all_lines


def example_scale_armor(output_file: str = "scale_armor.svg", tiles_per_panel: int = 20):
    """
    Generate a scale armor pattern with noise-driven tiles.
    
    Args:
        output_file: Output SVG filename
        tiles_per_panel: Number of tiles per panel side (default: 20)
    """
    print(f"Generating scale armor pattern ({tiles_per_panel}x{tiles_per_panel} tiles per panel)...")
    
    generator = TileGenerator(
        width=800,
        height=800,
        panel_cols=3,
        panel_rows=3,
        tiles_per_panel=tiles_per_panel,
        gap_ratio=0.04,
        noise_scale=0.04,
        rotation_intensity=0.7,
        scale_intensity=0.8,
        seed=42
    )
    
    lines = generator.generate_nested_tiles()
    
    # Export to SVG
    exporter = SVGExporter(
        width=800,
        height=800,
        stroke_width=0.5,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Total panels: 3×3 = 9 panels")
    print(f"  Tiles per panel: {tiles_per_panel}×{tiles_per_panel} = {tiles_per_panel**2} tiles")
    print(f"  Total tiles: {9 * tiles_per_panel**2} tiles")
    print(f"  Generated {len(lines)} lines")


def example_simple_tiles(output_file: str = "simple_tiles.svg"):
    """
    Generate a simpler tile pattern with consistent grid density.
    
    Args:
        output_file: Output SVG filename
    """
    print("Generating simple tiles pattern...")
    
    generator = TileGenerator(
        width=800,
        height=800,
        tile_cols=12,
        tile_rows=12,
        noise_scale=0.18,
        rotation_intensity=1.0,
        scale_intensity=0.5,
        seed=123
    )
    
    lines = generator.generate_tiles()
    
    # Export to SVG
    exporter = SVGExporter(
        width=800,
        height=800,
        stroke_width=0.8,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Generated {len(lines)} lines")


def example_dense_armor(output_file: str = "dense_armor.svg"):
    """
    Generate a dense scale armor pattern with many tiles.
    
    Args:
        output_file: Output SVG filename
    """
    print("Generating dense armor pattern...")
    
    generator = TileGenerator(
        width=800,
        height=800,
        tile_cols=15,
        tile_rows=15,
        noise_scale=0.08,
        rotation_intensity=0.6,
        scale_intensity=0.7,
        seed=999
    )
    
    lines = generator.generate_nested_tiles()
    
    # Export to SVG
    exporter = SVGExporter(
        width=800,
        height=800,
        stroke_width=0.6,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Generated {len(lines)} lines")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate noise-driven tile patterns for pen plotting"
    )
    
    parser.add_argument('--all', action='store_true',
                        help='Generate all example patterns')
    parser.add_argument('--scale-armor', action='store_true',
                        help='Generate scale armor pattern')
    parser.add_argument('--simple', action='store_true',
                        help='Generate simple tiles pattern')
    parser.add_argument('--dense', action='store_true',
                        help='Generate dense armor pattern')
    parser.add_argument('--output', '-o', default='tiles.svg',
                        help='Output SVG filename')
    parser.add_argument('--tiles', type=int, default=20,
                        help='Number of tiles per panel side (default: 20)')
    
    args = parser.parse_args()
    
    if not any([args.all, args.scale_armor, args.simple, args.dense]):
        parser.print_help()
    else:
        if args.all:
            example_scale_armor('scale_armor_10.svg', 10)
            example_scale_armor('scale_armor_15.svg', 15)
            example_scale_armor('scale_armor_20.svg', 20)
            example_simple_tiles()
            example_dense_armor()
        elif args.scale_armor:
            example_scale_armor(args.output, args.tiles)
        elif args.simple:
            example_simple_tiles(args.output)
        elif args.dense:
            example_dense_armor(args.output)
