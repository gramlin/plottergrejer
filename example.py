#!/usr/bin/env python3
"""
Example Script: Noise Field Generator

This script demonstrates how to use the noise field generator to create
beautiful flow field visualizations suitable for pen plotting.
"""

import sys
import os

# Check Python version before importing anything else
if sys.version_info[:2] < (3, 7):
    script_name = os.path.basename(__file__)
    print("Error: This script requires Python 3.7 or higher.")
    print("You are running Python {}.{}.{}".format(*sys.version_info[:3]))
    print("\nPlease run with Python 3.7+:")
    print("  python3 {} --all".format(script_name))
    print("or make the script executable and run it directly:")
    print("  chmod +x {}".format(script_name))
    print("  ./{} --all".format(script_name))
    sys.exit(1)

import argparse
from noise_field import NoiseFieldGenerator
from svg_export import SVGExporter
from axidraw_plotter import AxiDrawPlotter, plot_svg_file


def example_flow_lines(output_file: str = "flow_lines.svg"):
    """
    Generate a flow field with continuous lines following the noise pattern.
    
    Args:
        output_file: Output SVG filename
    """
    print("Generating flow lines visualization...")
    
    # Create noise field generator
    generator = NoiseFieldGenerator(
        width=800,
        height=800,
        resolution=20,
        noise_scale=0.005,
        octaves=2,
        seed=42
    )
    
    # Generate flow lines
    lines = generator.generate_flow_lines(
        num_lines=500,
        line_length=150,
        step_size=2.0
    )
    
    # Export to SVG
    exporter = SVGExporter(
        width=800,
        height=800,
        stroke_width=0.5,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Generated {len(lines)} flow lines")


def example_grid_field(output_file: str = "grid_field.svg"):
    """
    Generate a grid showing the direction of the flow field at each point.
    
    Args:
        output_file: Output SVG filename
    """
    print("Generating grid field visualization...")
    
    # Create noise field generator
    generator = NoiseFieldGenerator(
        width=800,
        height=800,
        resolution=30,
        noise_scale=0.008,
        octaves=1,
        seed=123
    )
    
    # Generate grid lines
    lines = generator.generate_grid_lines(line_length=25)
    
    # Export to SVG
    exporter = SVGExporter(
        width=800,
        height=800,
        stroke_width=1.0,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Generated {len(lines)} directional indicators")


def example_organic_pattern(output_file: str = "organic_pattern.svg"):
    """
    Generate an organic-looking pattern with varied parameters.
    
    Args:
        output_file: Output SVG filename
    """
    print("Generating organic pattern...")
    
    # Create noise field generator with multiple octaves for complexity
    generator = NoiseFieldGenerator(
        width=800,
        height=800,
        resolution=15,
        noise_scale=0.003,
        octaves=4,
        persistence=0.5,
        lacunarity=2.0,
        seed=999
    )
    
    # Generate many short flow lines for a dense pattern
    lines = generator.generate_flow_lines(
        num_lines=1500,
        line_length=80,
        step_size=1.5
    )
    
    # Export to SVG
    exporter = SVGExporter(
        width=800,
        height=800,
        stroke_width=0.3,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Generated {len(lines)} flow lines with organic feel")


def example_custom(
    output_file: str = "custom.svg",
    width: int = 800,
    height: int = 800,
    resolution: int = 20,
    noise_scale: float = 0.005,
    num_lines: int = 500,
    line_length: int = 100,
    seed: int = None
):
    """
    Generate a custom flow field with user-specified parameters.
    
    Args:
        output_file: Output SVG filename
        width: Canvas width
        height: Canvas height
        resolution: Grid resolution
        noise_scale: Noise scale factor
        num_lines: Number of flow lines
        line_length: Steps per line
        seed: Random seed (None for random)
    """
    print("Generating custom flow field...")
    
    generator = NoiseFieldGenerator(
        width=width,
        height=height,
        resolution=resolution,
        noise_scale=noise_scale,
        seed=seed
    )
    
    lines = generator.generate_flow_lines(
        num_lines=num_lines,
        line_length=line_length,
        step_size=2.0
    )
    
    exporter = SVGExporter(
        width=width,
        height=height,
        stroke_width=0.5,
        stroke_color='black'
    )
    exporter.export_lines(lines, output_file, add_border=True)
    
    print(f"✓ Saved to {output_file}")
    print(f"  Canvas: {width}x{height}")
    print(f"  Lines: {len(lines)}")
    print(f"  Seed: {generator.seed}")


def plot_to_axidraw(svg_file: str):
    """
    Send an SVG file to AxiDraw plotter.
    
    Args:
        svg_file: Path to SVG file to plot
    """
    print(f"Preparing to plot {svg_file}...")
    
    plotter = AxiDrawPlotter()
    
    if not plotter.is_available():
        print("ERROR: AxiDraw library not installed.")
        print("Visit: https://axidraw.com/doc/py_api/#installation")
        return False
    
    print("Connecting to AxiDraw...")
    if not plotter.connect():
        print("ERROR: Could not connect to AxiDraw plotter.")
        print("Make sure the plotter is connected and powered on.")
        return False
    
    try:
        success = plotter.plot_svg(
            svg_file,
            pen_down_speed=25,
            pen_up_speed=75
        )
        
        if success:
            print("✓ Plotting complete!")
        else:
            print("✗ Plotting failed")
        
        return success
    finally:
        plotter.disconnect()


def main():
    """Main entry point for the example script."""
    parser = argparse.ArgumentParser(
        description="Generate noise field visualizations for pen plotting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all example patterns
  python example.py --all
  
  # Generate a specific pattern
  python example.py --flow-lines
  python example.py --grid-field
  python example.py --organic
  
  # Generate custom pattern
  python example.py --custom --output my_art.svg --width 1000 --height 1000
  
  # Plot to AxiDraw
  python example.py --flow-lines --plot
  python example.py --plot flow_lines.svg
        """
    )
    
    # Pattern selection
    parser.add_argument('--all', action='store_true',
                        help='Generate all example patterns')
    parser.add_argument('--flow-lines', action='store_true',
                        help='Generate flow lines pattern')
    parser.add_argument('--grid-field', action='store_true',
                        help='Generate grid field pattern')
    parser.add_argument('--organic', action='store_true',
                        help='Generate organic pattern')
    parser.add_argument('--custom', action='store_true',
                        help='Generate custom pattern with parameters')
    
    # Custom parameters
    parser.add_argument('--output', '-o', default='output.svg',
                        help='Output SVG filename (default: output.svg)')
    parser.add_argument('--width', type=int, default=800,
                        help='Canvas width (default: 800)')
    parser.add_argument('--height', type=int, default=800,
                        help='Canvas height (default: 800)')
    parser.add_argument('--resolution', type=int, default=20,
                        help='Grid resolution (default: 20)')
    parser.add_argument('--noise-scale', type=float, default=0.005,
                        help='Noise scale factor (default: 0.005)')
    parser.add_argument('--num-lines', type=int, default=500,
                        help='Number of flow lines (default: 500)')
    parser.add_argument('--line-length', type=int, default=100,
                        help='Steps per line (default: 100)')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducibility')
    
    # Plotting
    parser.add_argument('--plot', nargs='?', const=True,
                        help='Send to AxiDraw plotter (optionally specify SVG file)')
    
    args = parser.parse_args()
    
    # If no options specified, show help
    if not any([args.all, args.flow_lines, args.grid_field, 
                args.organic, args.custom, args.plot]):
        parser.print_help()
        return
    
    # Handle plotting
    if args.plot and args.plot is not True:
        # User specified an SVG file to plot
        plot_to_axidraw(args.plot)
        return
    
    # Generate patterns
    if args.all:
        example_flow_lines()
        example_grid_field()
        example_organic_pattern()
        generated_file = "flow_lines.svg"
    elif args.flow_lines:
        example_flow_lines(args.output)
        generated_file = args.output
    elif args.grid_field:
        example_grid_field(args.output)
        generated_file = args.output
    elif args.organic:
        example_organic_pattern(args.output)
        generated_file = args.output
    elif args.custom:
        example_custom(
            output_file=args.output,
            width=args.width,
            height=args.height,
            resolution=args.resolution,
            noise_scale=args.noise_scale,
            num_lines=args.num_lines,
            line_length=args.line_length,
            seed=args.seed
        )
        generated_file = args.output
    else:
        generated_file = None
    
    # Plot if requested
    if args.plot is True and generated_file:
        print()
        plot_to_axidraw(generated_file)


if __name__ == "__main__":
    main()
