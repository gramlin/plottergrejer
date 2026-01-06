# plottergrejer

A Python tool for generating beautiful noise field visualizations optimized for pen plotting with AxiDraw plotters.

## Features

- **Noise Field Generation**: Creates flow fields based on Perlin noise patterns
- **SVG Export**: Outputs vector graphics optimized for pen plotting
- **AxiDraw Integration**: Direct integration with AxiDraw pen plotters
- **Customizable**: Extensive parameters for creating unique patterns
- **Easy to Use**: Simple API and command-line interface

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### AxiDraw API (Optional)

For plotter integration, install the AxiDraw software:

```bash
# Visit https://axidraw.com/doc/py_api/#installation for detailed instructions
# or install directly (requires AxiDraw software package)
pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
```

## Quick Start

### Generate Example Patterns

```bash
# Generate all example patterns
python example.py --all

# Generate specific patterns
python example.py --flow-lines
python example.py --grid-field
python example.py --organic

# Generate custom pattern
python example.py --custom --output my_art.svg --num-lines 1000
```

### Using as a Library

```python
from noise_field import NoiseFieldGenerator
from svg_export import SVGExporter

# Create a noise field generator
generator = NoiseFieldGenerator(
    width=800,
    height=800,
    resolution=20,
    noise_scale=0.005,
    seed=42
)

# Generate flow lines
lines = generator.generate_flow_lines(
    num_lines=500,
    line_length=150,
    step_size=2.0
)

# Export to SVG
exporter = SVGExporter(width=800, height=800)
exporter.export_lines(lines, "output.svg", add_border=True)
```

### Plotting with AxiDraw

```bash
# Generate and plot in one command
python example.py --flow-lines --plot

# Plot an existing SVG file
python example.py --plot my_art.svg
```

Or use the library directly:

```python
from axidraw_plotter import plot_svg_file

# Plot an SVG file
plot_svg_file("output.svg", pen_down_speed=25, pen_up_speed=75)
```

## API Reference

### NoiseFieldGenerator

Main class for generating noise-based flow fields.

**Parameters:**
- `width` (int): Canvas width in pixels (default: 800)
- `height` (int): Canvas height in pixels (default: 800)
- `resolution` (int): Grid spacing - smaller values = more detail (default: 20)
- `noise_scale` (float): Scale factor for noise - smaller = smoother (default: 0.01)
- `octaves` (int): Number of noise octaves - more = more detail (default: 1)
- `persistence` (float): Amplitude multiplier per octave (default: 0.5)
- `lacunarity` (float): Frequency multiplier per octave (default: 2.0)
- `seed` (int): Random seed for reproducibility (default: random)

**Methods:**
- `generate_flow_lines(num_lines, line_length, step_size)`: Generate continuous flow lines
- `generate_grid_lines(line_length)`: Generate directional indicators at grid points
- `get_angle_at(x, y)`: Get flow direction at specific coordinates

### SVGExporter

Handles SVG export for pen plotting.

**Parameters:**
- `width` (int): Canvas width (default: 800)
- `height` (int): Canvas height (default: 800)
- `stroke_width` (float): Line thickness (default: 0.5)
- `stroke_color` (str): Line color (default: 'black')
- `background_color` (str): Background color or None (default: 'white')

**Methods:**
- `export_lines(lines, filename, add_border)`: Export lines to SVG
- `export_circles(circles, filename, filled)`: Export circles to SVG
- `export_mixed(filename, lines, circles, add_border)`: Export mixed content

### AxiDrawPlotter

Interface for AxiDraw pen plotters.

**Methods:**
- `connect()`: Connect to plotter
- `plot_svg(svg_file, pen_down_speed, pen_up_speed, ...)`: Plot an SVG file
- `preview_svg(svg_file)`: Preview without plotting
- `disconnect()`: Disconnect from plotter
- `is_available()`: Check if AxiDraw library is installed

**Convenience Function:**
- `plot_svg_file(svg_file, pen_down_speed, pen_up_speed)`: Quick plotting

## Examples

### Flow Lines Pattern
Creates continuous lines that follow the noise field:
```python
generator = NoiseFieldGenerator(width=800, height=800, noise_scale=0.005)
lines = generator.generate_flow_lines(num_lines=500, line_length=150)
```

### Grid Field Pattern
Shows the direction of flow at each grid point:
```python
generator = NoiseFieldGenerator(resolution=30, noise_scale=0.008)
lines = generator.generate_grid_lines(line_length=25)
```

### Organic Pattern
Dense, organic-looking patterns with multiple octaves:
```python
generator = NoiseFieldGenerator(
    noise_scale=0.003,
    octaves=4,
    persistence=0.5
)
lines = generator.generate_flow_lines(num_lines=1500, line_length=80)
```

## Customization Tips

### Smooth vs. Chaotic
- **Smooth**: Lower `noise_scale` (0.001-0.005), fewer `octaves` (1-2)
- **Chaotic**: Higher `noise_scale` (0.01-0.02), more `octaves` (3-5)

### Dense vs. Sparse
- **Dense**: More `num_lines` (1000+), shorter `line_length` (50-100)
- **Sparse**: Fewer `num_lines` (100-300), longer `line_length` (150-300)

### Resolution
- Lower `resolution` (10-15): More detail, slower generation
- Higher `resolution` (30-50): Less detail, faster generation

## Troubleshooting

### AxiDraw Not Found
If you get "AxiDraw library not available":
1. Install the AxiDraw software from Evil Mad Scientist
2. Install the Python API: Follow instructions at https://axidraw.com/doc/py_api/

### SVG Looks Wrong
- Ensure your canvas dimensions match your paper size
- Check that `stroke_width` is appropriate for your pen
- Try adding a border with `add_border=True`

### Slow Generation
- Increase `resolution` (less dense grid)
- Reduce `num_lines` or `line_length`
- Reduce `octaves` for simpler noise

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [noise](https://github.com/caseman/noise) for Perlin noise generation
- Uses [svgwrite](https://github.com/mozman/svgwrite) for SVG export
- Integrates with [AxiDraw](https://axidraw.com/) pen plotters from Evil Mad Scientist