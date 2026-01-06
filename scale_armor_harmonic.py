"""
Scale Armor Harmonized Example

Creates a tiled scale pattern with smoother size variation and harmonic rotation.
"""

import math
import os
import random
import shutil
import subprocess
import tempfile

from noise_field import NoiseFieldGenerator
from svg_export import SVGExporter


def _square_path(
    center_x: float,
    center_y: float,
    size: float,
    angle: float
):
    half = size / 2.0
    corners = [
        (-half, -half),
        (half, -half),
        (half, half),
        (-half, half),
        (-half, -half)
    ]
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points = []
    for x, y in corners:
        rot_x = x * cos_a - y * sin_a
        rot_y = x * sin_a + y * cos_a
        points.append((center_x + rot_x, center_y + rot_y))
    return points


def _smooth_angle(generator: NoiseFieldGenerator, x: float, y: float, offset: float) -> float:
    angles = [
        generator.get_angle_at(x, y),
        generator.get_angle_at(x + offset, y),
        generator.get_angle_at(x - offset, y),
        generator.get_angle_at(x, y + offset),
        generator.get_angle_at(x, y - offset)
    ]
    avg_sin = sum(math.sin(angle) for angle in angles)
    avg_cos = sum(math.cos(angle) for angle in angles)
    return math.atan2(avg_sin, avg_cos)


def example_scale_armor_harmonic(output_file: str = "scale_armor.svg"):
    """
    Generate a tiled scale armor pattern with balanced size and rotation.

    Args:
        output_file: Output SVG filename
    """
    print("Generating scale armor tile pattern (harmonic)...")

    width = 900
    height = 900
    panels = 3
    tiles_per_panel = 10
    panel_gap = 40
    margin = 40

    panel_size = (width - (2 * margin) - (panel_gap * (panels - 1))) / panels
    tile_step = panel_size / tiles_per_panel
    base_tile_size = tile_step * 0.95
    border_width = tile_step * 1.4
    stack_offset = tile_step * 0.25
    smooth_offset = tile_step * 0.6

    generator = NoiseFieldGenerator(
        width=width,
        height=height,
        resolution=20,
        noise_scale=0.007,
        octaves=1,
        seed=2024
    )
    rng = random.Random(2024)

    lines_with_depth = []

    for panel_y in range(panels):
        for panel_x in range(panels):
            origin_x = margin + panel_x * (panel_size + panel_gap)
            origin_y = margin + panel_y * (panel_size + panel_gap)
            panel_center = panel_size / 2.0

            for row in range(tiles_per_panel):
                for col in range(tiles_per_panel):
                    center_x = origin_x + (col + 0.5) * tile_step
                    center_y = origin_y + (row + 0.5) * tile_step

                    angle = _smooth_angle(generator, center_x, center_y, smooth_offset)
                    size_angle = _smooth_angle(
                        generator,
                        center_x + tile_step * 1.2,
                        center_y - tile_step * 1.1,
                        smooth_offset
                    )
                    size_noise = (math.sin(size_angle) + 1) / 2
                    size = base_tile_size * (0.9 + 0.25 * size_noise)

                    local_x = (col + 0.5) * tile_step
                    local_y = (row + 0.5) * tile_step
                    center_dist = math.hypot(local_x - panel_center, local_y - panel_center)
                    center_norm = min(1.0, center_dist / (panel_size * 0.5))
                    center_scale = 0.75 + 0.35 * center_norm
                    size *= center_scale

                    edge_dist = min(
                        local_x,
                        local_y,
                        panel_size - local_x,
                        panel_size - local_y
                    )
                    border_factor = max(0.0, 1.0 - (edge_dist / border_width))
                    size *= 1.0 + border_factor * 0.2
                    angle += border_factor * 0.35

                    depth_noise = (math.sin(angle * 0.8) + math.cos(size_angle * 1.1)) * 0.5
                    depth = (depth_noise + 1.0) / 2.0
                    depth += rng.uniform(-0.03, 0.03)
                    depth = max(0.0, min(1.0, depth))
                    offset = depth * stack_offset
                    stacked_x = center_x + offset
                    stacked_y = center_y - offset

                    lines_with_depth.append((
                        depth,
                        _square_path(stacked_x, stacked_y, size, angle)
                    ))

    exporter = SVGExporter(
        width=width,
        height=height,
        stroke_width=1.2,
        stroke_color='black'
    )
    lines_with_depth.sort(key=lambda item: item[0])
    lines = [line for _, line in lines_with_depth]
    vpype_path = shutil.which("vpype")
    if vpype_path:
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as temp_svg:
            temp_path = temp_svg.name
        exporter.export_lines(lines, temp_path, add_border=False)
        result = subprocess.run(
            [vpype_path, "read", temp_path, "occult", "write", output_file],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print("Warning: vpype occult failed, keeping raw SVG output.")
            print(result.stderr.strip())
            os.replace(temp_path, output_file)
        else:
            os.remove(temp_path)
    else:
        print("Warning: vpype not found, exporting without occult.")
        exporter.export_lines(lines, output_file, add_border=False)

    print(f"✓ Saved to {output_file}")
    print(f"  Generated {len(lines)} tiles across {panels}x{panels} panels")
