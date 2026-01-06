"""
SVG Export Module

Handles exporting flow field visualizations to SVG format,
optimized for pen plotting.
"""

import svgwrite
from typing import List, Tuple, Optional


class SVGExporter:
    """
    Export flow fields and other patterns to SVG format.
    
    SVG files are vector-based and ideal for pen plotters like AxiDraw.
    """
    
    def __init__(
        self,
        width: int = 800,
        height: int = 800,
        stroke_width: float = 0.5,
        stroke_color: str = 'black',
        background_color: Optional[str] = 'white'
    ):
        """
        Initialize the SVG exporter.
        
        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
            stroke_width: Line thickness
            stroke_color: Line color
            background_color: Background color (None for transparent)
        """
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.background_color = background_color
    
    def export_lines(
        self,
        lines: List[List[Tuple[float, float]]],
        filename: str,
        add_border: bool = False
    ) -> None:
        """
        Export a list of lines to an SVG file.
        
        Args:
            lines: List of lines, where each line is a list of (x, y) points
            filename: Output filename (should end with .svg)
            add_border: Whether to add a border around the canvas
        """
        # Create SVG drawing
        dwg = svgwrite.Drawing(
            filename,
            size=(f'{self.width}px', f'{self.height}px'),
            viewBox=f'0 0 {self.width} {self.height}'
        )
        
        # Add background if specified
        if self.background_color:
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill=self.background_color
            ))
        
        # Add border if requested
        if add_border:
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill='none',
                stroke=self.stroke_color,
                stroke_width=self.stroke_width * 2
            ))
        
        # Add all lines
        for line in lines:
            if len(line) < 2:
                continue
            
            # Convert points to SVG path
            path_data = []
            path_data.append(f'M {line[0][0]:.2f},{line[0][1]:.2f}')
            
            for point in line[1:]:
                path_data.append(f'L {point[0]:.2f},{point[1]:.2f}')
            
            dwg.add(dwg.path(
                d=' '.join(path_data),
                stroke=self.stroke_color,
                stroke_width=self.stroke_width,
                fill='none',
                stroke_linecap='round',
                stroke_linejoin='round'
            ))
        
        # Save the file
        dwg.save()
    
    def export_circles(
        self,
        circles: List[Tuple[float, float, float]],
        filename: str,
        filled: bool = False
    ) -> None:
        """
        Export circles to an SVG file.
        
        Args:
            circles: List of (x, y, radius) tuples
            filename: Output filename
            filled: Whether circles should be filled
        """
        dwg = svgwrite.Drawing(
            filename,
            size=(f'{self.width}px', f'{self.height}px'),
            viewBox=f'0 0 {self.width} {self.height}'
        )
        
        if self.background_color:
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill=self.background_color
            ))
        
        for x, y, r in circles:
            dwg.add(dwg.circle(
                center=(x, y),
                r=r,
                stroke=self.stroke_color,
                stroke_width=self.stroke_width,
                fill=self.stroke_color if filled else 'none'
            ))
        
        dwg.save()
    
    def export_mixed(
        self,
        filename: str,
        lines: Optional[List[List[Tuple[float, float]]]] = None,
        circles: Optional[List[Tuple[float, float, float]]] = None,
        add_border: bool = False
    ) -> None:
        """
        Export a mix of lines and circles to an SVG file.
        
        Args:
            filename: Output filename
            lines: Optional list of lines
            circles: Optional list of circles
            add_border: Whether to add a border
        """
        dwg = svgwrite.Drawing(
            filename,
            size=(f'{self.width}px', f'{self.height}px'),
            viewBox=f'0 0 {self.width} {self.height}'
        )
        
        if self.background_color:
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill=self.background_color
            ))
        
        if add_border:
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill='none',
                stroke=self.stroke_color,
                stroke_width=self.stroke_width * 2
            ))
        
        if lines:
            for line in lines:
                if len(line) < 2:
                    continue
                
                path_data = []
                path_data.append(f'M {line[0][0]:.2f},{line[0][1]:.2f}')
                
                for point in line[1:]:
                    path_data.append(f'L {point[0]:.2f},{point[1]:.2f}')
                
                dwg.add(dwg.path(
                    d=' '.join(path_data),
                    stroke=self.stroke_color,
                    stroke_width=self.stroke_width,
                    fill='none',
                    stroke_linecap='round',
                    stroke_linejoin='round'
                ))
        
        if circles:
            for x, y, r in circles:
                dwg.add(dwg.circle(
                    center=(x, y),
                    r=r,
                    stroke=self.stroke_color,
                    stroke_width=self.stroke_width,
                    fill='none'
                ))
        
        dwg.save()
