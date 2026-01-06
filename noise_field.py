"""
Noise Field Tile Generator

A tool for generating flow field visualizations based on Perlin noise,
with SVG export for pen plotting.
"""

import noise
import numpy as np
import math
from typing import List, Tuple, Optional


class NoiseFieldGenerator:
    """
    Generate flow fields based on Perlin noise patterns.
    
    The generator creates a grid of points and calculates noise-based
    angles for each point, which can be used to draw flow lines.
    """
    
    def __init__(
        self,
        width: int = 800,
        height: int = 800,
        resolution: int = 20,
        noise_scale: float = 0.01,
        octaves: int = 1,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
        seed: Optional[int] = None
    ):
        """
        Initialize the noise field generator.
        
        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
            resolution: Grid spacing (smaller = more detail)
            noise_scale: Scale factor for noise (smaller = smoother)
            octaves: Number of noise octaves (more = more detail)
            persistence: Amplitude multiplier per octave
            lacunarity: Frequency multiplier per octave
            seed: Random seed for reproducible results
        """
        self.width = width
        self.height = height
        self.resolution = resolution
        self.noise_scale = noise_scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed if seed is not None else np.random.randint(0, 10000)
        
        # Calculate grid dimensions
        self.cols = int(width / resolution) + 1
        self.rows = int(height / resolution) + 1
        
        # Generate the noise field
        self.field = self._generate_field()
    
    def _generate_field(self) -> np.ndarray:
        """
        Generate the noise field grid.
        
        Returns:
            2D array of angles (in radians) for each grid point
        """
        field = np.zeros((self.rows, self.cols))
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.resolution
                y = row * self.resolution
                
                # Generate Perlin noise value
                noise_val = noise.pnoise3(
                    x * self.noise_scale,
                    y * self.noise_scale,
                    self.seed,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=0
                )
                
                # Convert noise value (-1 to 1) to angle (0 to 2π)
                angle = (noise_val + 1) * math.pi
                field[row, col] = angle
        
        return field
    
    def get_angle_at(self, x: float, y: float) -> float:
        """
        Get the flow field angle at a specific position using bilinear interpolation.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Angle in radians
        """
        # Get grid position
        col = x / self.resolution
        row = y / self.resolution
        
        # Get integer parts
        col0 = int(col)
        row0 = int(row)
        
        # Clamp to valid range
        col0 = max(0, min(col0, self.cols - 2))
        row0 = max(0, min(row0, self.rows - 2))
        
        # Get fractional parts
        col_frac = col - col0
        row_frac = row - row0
        
        # Bilinear interpolation
        angle00 = self.field[row0, col0]
        angle10 = self.field[row0, col0 + 1]
        angle01 = self.field[row0 + 1, col0]
        angle11 = self.field[row0 + 1, col0 + 1]
        
        angle0 = angle00 * (1 - col_frac) + angle10 * col_frac
        angle1 = angle01 * (1 - col_frac) + angle11 * col_frac
        angle = angle0 * (1 - row_frac) + angle1 * row_frac
        
        return angle
    
    def generate_flow_lines(
        self,
        num_lines: int = 1000,
        line_length: int = 100,
        step_size: float = 2.0
    ) -> List[List[Tuple[float, float]]]:
        """
        Generate flow lines that follow the noise field.
        
        Args:
            num_lines: Number of flow lines to generate
            line_length: Number of steps per line
            step_size: Distance to move at each step
            
        Returns:
            List of lines, where each line is a list of (x, y) points
        """
        lines = []
        
        for _ in range(num_lines):
            # Random starting point
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)
            
            line = [(x, y)]
            
            for _ in range(line_length):
                # Get angle from noise field
                angle = self.get_angle_at(x, y)
                
                # Move in the direction of the angle
                x += math.cos(angle) * step_size
                y += math.sin(angle) * step_size
                
                # Check if still within bounds
                if x < 0 or x > self.width or y < 0 or y > self.height:
                    break
                
                line.append((x, y))
            
            # Only keep lines with at least 2 points
            if len(line) >= 2:
                lines.append(line)
        
        return lines
    
    def generate_grid_lines(
        self,
        line_length: float = 30.0,
    ) -> List[List[Tuple[float, float]]]:
        """
        Generate lines at each grid point showing the flow direction.
        
        Args:
            line_length: Length of each directional line
            
        Returns:
            List of lines, where each line is a list of (x, y) points
        """
        lines = []
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.resolution
                y = row * self.resolution
                
                # Skip if outside canvas
                if x > self.width or y > self.height:
                    continue
                
                angle = self.field[row, col]
                
                # Create a line segment
                half_len = line_length / 2
                x1 = x - math.cos(angle) * half_len
                y1 = y - math.sin(angle) * half_len
                x2 = x + math.cos(angle) * half_len
                y2 = y + math.sin(angle) * half_len
                
                lines.append([(x1, y1), (x2, y2)])
        
        return lines
