#!/usr/bin/env python3
"""
Generate Asset Template
Creates parametric 3D assets for train stations based on style guide
Usage: blender -b -P generate_asset_template.py -- --id station-home --section home
"""

import bpy
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from mathutils import Vector

# Get the directory containing this script
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
META_DIR = ASSETS_DIR / "meta"
MODELS_DIR = ASSETS_DIR / "models"


def load_style_guide():
    """Load the style guide JSON"""
    style_path = META_DIR / "style-guide.json"
    if not style_path.exists():
        print(f"Warning: Style guide not found at {style_path}")
        return {}

    with open(style_path) as f:
        return json.load(f)


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple (0-1 range)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def create_pbr_material(name, base_color, roughness=0.6, metalness=0.2, emissive=False):
    """Create a PBR material with given properties"""
    mat = bpy.data.materials.new(name=name)
    if not mat.use_nodes:
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)

    # Set properties
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metalness

    # Add Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (600, 0)

    if emissive:
        # For Blender 5.0+, use separate Emission shader
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (0, -300)
        emission.inputs['Color'].default_value = (*base_color, 1.0)
        emission.inputs['Strength'].default_value = 2.0

        # Add shader to mix BSDF with Emission
        add_shader = nodes.new(type='ShaderNodeAddShader')
        add_shader.location = (300, 0)

        links.new(bsdf.outputs['BSDF'], add_shader.inputs[0])
        links.new(emission.outputs['Emission'], add_shader.inputs[1])
        links.new(add_shader.outputs['Shader'], output.inputs['Surface'])
    else:
        # Link nodes normally
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def create_platform(style):
    """Create a train platform"""
    # Platform base
    bpy.ops.mesh.primitive_cube_add(size=2)
    platform = bpy.context.active_object
    platform.name = "platform_base"
    platform.scale = (10, 5, 0.2)

    # Apply scale
    bpy.ops.object.transform_apply(scale=True)

    # Add bevel modifier for smooth edges
    bevel = platform.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 2

    # Create material
    if 'color_palette' in style and 'tertiary' in style['color_palette']:
        color = hex_to_rgb(style['color_palette']['tertiary']['hex'])
    else:
        color = (0.9, 0.9, 0.9)  # Light gray default

    mat = create_pbr_material("platform_material", color, roughness=0.8, metalness=0.0)
    platform.data.materials.append(mat)

    return platform


def create_bench(style, position):
    """Create a simple bench"""
    # Bench seat
    bpy.ops.mesh.primitive_cube_add(size=2)
    seat = bpy.context.active_object
    seat.name = "bench_seat"
    seat.scale = (1.5, 0.4, 0.05)
    seat.location = position

    bpy.ops.object.transform_apply(scale=True)

    # Bench back
    bpy.ops.mesh.primitive_cube_add(size=2)
    back = bpy.context.active_object
    back.name = "bench_back"
    back.scale = (1.5, 0.05, 0.6)
    back.location = (position[0], position[1] - 0.35, position[2] + 0.3)

    bpy.ops.object.transform_apply(scale=True)

    # Create material
    if 'color_palette' in style and 'primary' in style['color_palette']:
        color = hex_to_rgb(style['color_palette']['primary']['hex'])
    else:
        color = (0.2, 0.3, 0.4)  # Dark blue-gray default

    mat = create_pbr_material("bench_material", color, roughness=0.6, metalness=0.2)
    seat.data.materials.append(mat)
    back.data.materials.append(mat)

    # Join seat and back
    bpy.context.view_layer.objects.active = seat
    back.select_set(True)
    bpy.ops.object.join()

    return seat


def create_light_post(style, position):
    """Create a light post with emissive top"""
    # Post
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=3)
    post = bpy.context.active_object
    post.name = "light_post"
    post.location = (position[0], position[1], position[2] + 1.5)

    # Light top
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2)
    light = bpy.context.active_object
    light.name = "light_bulb"
    light.location = (position[0], position[1], position[2] + 3.2)

    # Materials
    if 'color_palette' in style and 'primary' in style['color_palette']:
        post_color = hex_to_rgb(style['color_palette']['primary']['hex'])
    else:
        post_color = (0.2, 0.2, 0.2)

    if 'color_palette' in style and 'accent' in style['color_palette']:
        light_color = hex_to_rgb(style['color_palette']['accent']['hex'])
    else:
        light_color = (0.95, 0.6, 0.1)

    post_mat = create_pbr_material("post_material", post_color, roughness=0.3, metalness=0.9)
    light_mat = create_pbr_material("light_material", light_color, roughness=0.1, metalness=0.0, emissive=True)

    post.data.materials.append(post_mat)
    light.data.materials.append(light_mat)

    # Join
    bpy.context.view_layer.objects.active = post
    light.select_set(True)
    bpy.ops.object.join()

    return post


def create_station_sign(style, text="STATION", position=(0, 0, 2)):
    """Create a station sign"""
    # Create text
    bpy.ops.object.text_add(location=position)
    sign = bpy.context.active_object
    sign.name = "station_sign"
    sign.data.body = text
    sign.data.align_x = 'CENTER'
    sign.data.align_y = 'CENTER'
    sign.data.size = 0.5
    sign.data.extrude = 0.05

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')

    # Create emissive material
    if 'color_palette' in style and 'accent' in style['color_palette']:
        color = hex_to_rgb(style['color_palette']['accent']['hex'])
    else:
        color = (0.95, 0.6, 0.1)

    mat = create_pbr_material("sign_material", color, roughness=0.2, metalness=0.5, emissive=True)
    sign.data.materials.append(mat)

    return sign


def setup_lighting(style):
    """Setup scene lighting for baking"""
    # Remove default light
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            obj.select_set(True)
            bpy.ops.object.delete()

    # Add ambient light (world)
    world = bpy.context.scene.world
    if not world.use_nodes:
        world.use_nodes = True
    bg = world.node_tree.nodes['Background']

    if 'lighting' in style and 'ambient' in style['lighting']:
        ambient_color = hex_to_rgb(style['lighting']['ambient']['color'])
        ambient_intensity = style['lighting']['ambient']['intensity']
    else:
        ambient_color = (0.25, 0.25, 0.31)
        ambient_intensity = 0.4

    bg.inputs['Color'].default_value = (*ambient_color, 1.0)
    bg.inputs['Strength'].default_value = ambient_intensity

    # Add directional light (sun)
    bpy.ops.object.light_add(type='SUN')
    sun = bpy.context.active_object
    sun.name = "sun"

    if 'lighting' in style and 'directional' in style['lighting']:
        sun_color = hex_to_rgb(style['lighting']['directional']['color'])
        sun_intensity = style['lighting']['directional']['intensity']
        if 'position' in style['lighting']['directional']:
            sun.location = style['lighting']['directional']['position']
    else:
        sun_color = (1.0, 0.96, 0.88)
        sun_intensity = 0.8

    sun.data.color = sun_color
    sun.data.energy = sun_intensity
    sun.rotation_euler = (0.8, 0.2, 0.5)


def create_station_asset(asset_id, section, style):
    """Create a complete station asset"""
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Setup lighting
    setup_lighting(style)

    # Create platform
    platform = create_platform(style)

    # Create benches
    bench1 = create_bench(style, (-3, 0, 0.2))
    bench2 = create_bench(style, (3, 0, 0.2))

    # Create light posts
    light1 = create_light_post(style, (-5, 2, 0.2))
    light2 = create_light_post(style, (5, 2, 0.2))

    # Create station sign
    sign_text = section.upper()
    sign = create_station_sign(style, sign_text, (0, -2, 2.5))

    # Join all objects
    bpy.ops.object.select_all(action='SELECT')
    # Deselect lights
    for obj in bpy.context.selected_objects:
        if obj.type == 'LIGHT':
            obj.select_set(False)

    # Set platform as active
    bpy.context.view_layer.objects.active = platform
    bpy.ops.object.join()

    final_obj = bpy.context.active_object
    final_obj.name = asset_id

    return final_obj


def export_glb(filepath, obj):
    """Export object as GLB without Draco compression (for web compatibility)"""
    # Select only the object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Ensure output directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # Export with settings from style guide
    # Draco disabled - requires decoder files in web app
    bpy.ops.export_scene.gltf(
        filepath=str(filepath),
        export_format='GLB',
        use_selection=True,
        export_draco_mesh_compression_enable=False,  # Disabled for web compatibility
        export_draco_mesh_compression_level=6,
        export_texture_dir='',
        export_apply=True,
        export_yup=True,  # Y up
        export_force_sampling=False,
        export_cameras=False,
        export_lights=False
    )

    print(f"Exported GLB to: {filepath}")


def calculate_polycount(obj):
    """Calculate triangle count for object"""
    polycount = 0
    if obj.type == 'MESH':
        polycount += len(obj.data.polygons)

    # Include children
    for child in obj.children:
        if child.type == 'MESH':
            polycount += len(child.data.polygons)

    return polycount


def generate_metadata(asset_id, section, glb_path, obj):
    """Generate metadata JSON for the asset"""
    # Calculate stats
    polycount = calculate_polycount(obj)
    filesize = glb_path.stat().st_size if glb_path.exists() else 0

    # Position based on section
    section_positions = {
        'home': [0, 0, 0],
        'store': [30, 0, 0],
        'gallery': [60, 0, 0],
        'blog': [90, 0, 0]
    }

    position = section_positions.get(section, [0, 0, 0])

    metadata = {
        "id": asset_id,
        "category": "hero_stop",
        "file": f"models/{glb_path.name}",
        "scale": [1.0, 1.0, 1.0],
        "position": position,
        "rotation": [0, 0, 0],
        "animation": {
            "type": "idle",
            "params": {
                "duration": 4.0,
                "ease": "sine.inOut",
                "loop": True
            }
        },
        "section": section,
        "visibility": {
            "default": True if section == "home" else False,
            "fadeIn": True,
            "fadeOut": False if section == "home" else True
        },
        "lighting": {
            "baked": True,
            "castShadow": False,
            "receiveShadow": False
        },
        "optimization": {
            "dracoCompressed": False,
            "ktx2Textures": False,
            "lodLevels": 1
        },
        "metadata": {
            "author": "Asset Agent",
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "version": "1.0.0",
            "polycount": polycount,
            "fileSize": filesize,
            "tags": ["station", section, "hero", "generated"]
        }
    }

    # Write metadata
    meta_path = META_DIR / f"{asset_id}.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)

    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Generated metadata: {meta_path}")
    return metadata


def main():
    """Main execution"""
    # Parse arguments (after --)
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []

    parser = argparse.ArgumentParser(description='Generate train station asset')
    parser.add_argument('--id', required=True, help='Asset ID (e.g., station-home)')
    parser.add_argument('--section', required=True, help='Section name (e.g., home)')
    parser.add_argument('--output-dir', default=str(MODELS_DIR), help='Output directory for GLB')

    args = parser.parse_args(argv)

    print(f"\n{'='*60}")
    print(f"Generating Asset: {args.id}")
    print(f"Section: {args.section}")
    print(f"{'='*60}\n")

    # Load style guide
    style = load_style_guide()

    # Create asset
    asset_obj = create_station_asset(args.id, args.section, style)

    # Export GLB
    glb_path = Path(args.output_dir) / f"{args.id}.glb"
    export_glb(glb_path, asset_obj)

    # Generate metadata
    metadata = generate_metadata(args.id, args.section, glb_path, asset_obj)

    print(f"\n{'='*60}")
    print(f"✓ Asset generated successfully!")
    print(f"  GLB: {glb_path}")
    print(f"  Polycount: {metadata['metadata']['polycount']:,}")
    print(f"  File size: {metadata['metadata']['fileSize'] / 1024:.1f} KB")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
