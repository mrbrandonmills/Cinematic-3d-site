#!/usr/bin/env python3
"""
Generate Cinematic Train Station
Creates high-quality 3D train stations with advanced materials and geometry
Usage: blender -b -P generate_cinematic_station.py -- --id station-home --section home
"""

import bpy
import json
import sys
import argparse
from pathlib import Path
from math import radians, pi
import mathutils

def hex_to_rgb(hex_color):
    """Convert hex color to RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def clear_scene():
    """Clear all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    # Clear meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


def create_cinematic_material(name, base_color, roughness=0.4, metallic=0.1, emission_strength=0):
    """Create photorealistic PBR material"""
    mat = bpy.data.materials.new(name=name)
    if not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Specular IOR Level'].default_value = 0.5

    # Add emission if needed
    if emission_strength > 0:
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (0, -300)
        emission.inputs['Color'].default_value = (*base_color, 1.0)
        emission.inputs['Strength'].default_value = emission_strength

        add_shader = nodes.new(type='ShaderNodeAddShader')
        add_shader.location = (300, 0)
        links.new(bsdf.outputs['BSDF'], add_shader.inputs[0])
        links.new(emission.outputs['Emission'], add_shader.inputs[1])

        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (600, 0)
        links.new(add_shader.outputs['Shader'], output.inputs['Surface'])
    else:
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def add_subdivision_modifier(obj, levels=2, render_levels=3):
    """Add subdivision surface for smooth geometry"""
    mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.levels = levels
    mod.render_levels = render_levels
    mod.subdivision_type = 'CATMULL_CLARK'
    return mod


def add_bevel_modifier(obj, width=0.02, segments=3):
    """Add bevel for smooth edges"""
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    mod.angle_limit = radians(30)
    return mod


def create_detailed_platform(style):
    """Create detailed platform with inset panels and edge details"""
    # Main platform
    bpy.ops.mesh.primitive_cube_add(size=2)
    platform = bpy.context.active_object
    platform.name = "platform_main"
    platform.scale = (12, 6, 0.3)
    bpy.ops.object.transform_apply(scale=True)

    # Add bevels for smooth edges
    add_bevel_modifier(platform, width=0.05, segments=4)

    # Add subtle subdivision
    add_subdivision_modifier(platform, levels=1, render_levels=2)

    # Material
    color = hex_to_rgb(style['color_palette']['tertiary']['hex']) if 'color_palette' in style else (0.85, 0.85, 0.87)
    mat = create_cinematic_material("platform_concrete", color, roughness=0.7, metallic=0.05)
    platform.data.materials.append(mat)

    # Add platform trim
    bpy.ops.mesh.primitive_cube_add(size=2)
    trim = bpy.context.active_object
    trim.name = "platform_trim"
    trim.scale = (12.2, 6.2, 0.05)
    trim.location = (0, 0, -0.3)
    bpy.ops.object.transform_apply(scale=True)

    add_bevel_modifier(trim, width=0.01, segments=2)
    trim_mat = create_cinematic_material("platform_trim_metal", (0.3, 0.3, 0.35), roughness=0.3, metallic=0.8)
    trim.data.materials.append(trim_mat)

    # Join trim to platform
    bpy.ops.object.select_all(action='DESELECT')
    platform.select_set(True)
    trim.select_set(True)
    bpy.context.view_layer.objects.active = platform
    bpy.ops.object.join()

    return platform


def create_modern_bench(style, position):
    """Create modern bench with metal frame and wooden seat"""
    # Seat
    bpy.ops.mesh.primitive_cube_add(size=2)
    seat = bpy.context.active_object
    seat.name = "bench_seat"
    seat.scale = (2, 0.5, 0.08)
    seat.location = position
    bpy.ops.object.transform_apply(scale=True)

    add_bevel_modifier(seat, width=0.015, segments=3)
    add_subdivision_modifier(seat, levels=1, render_levels=2)

    wood_mat = create_cinematic_material("bench_wood", (0.4, 0.25, 0.15), roughness=0.6, metallic=0.0)
    seat.data.materials.append(wood_mat)

    # Back support
    bpy.ops.mesh.primitive_cube_add(size=2)
    back = bpy.context.active_object
    back.name = "bench_back"
    back.scale = (2, 0.08, 0.7)
    back.location = (position[0], position[1] - 0.4, position[2] + 0.4)
    bpy.ops.object.transform_apply(scale=True)

    add_bevel_modifier(back, width=0.015, segments=3)
    add_subdivision_modifier(back, levels=1, render_levels=2)
    back.data.materials.append(wood_mat)

    # Metal legs (4 legs)
    legs = []
    leg_positions = [
        (position[0] - 0.8, position[1] + 0.15, position[2] - 0.2),
        (position[0] + 0.8, position[1] + 0.15, position[2] - 0.2),
        (position[0] - 0.8, position[1] - 0.35, position[2] - 0.2),
        (position[0] + 0.8, position[1] - 0.35, position[2] - 0.2)
    ]

    metal_mat = create_cinematic_material("bench_metal", (0.15, 0.15, 0.17), roughness=0.25, metallic=0.9)

    for leg_pos in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.5)
        leg = bpy.context.active_object
        leg.location = leg_pos
        add_bevel_modifier(leg, width=0.005, segments=2)
        leg.data.materials.append(metal_mat)
        legs.append(leg)

    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    seat.select_set(True)
    back.select_set(True)
    for leg in legs:
        leg.select_set(True)
    bpy.context.view_layer.objects.active = seat
    bpy.ops.object.join()

    return seat


def create_elegant_sign(style, text="HOME"):
    """Create elegant LED sign with metal frame"""
    # Sign frame
    bpy.ops.mesh.primitive_cube_add(size=2)
    frame = bpy.context.active_object
    frame.name = "sign_frame"
    frame.scale = (1.5, 0.1, 0.4)
    frame.location = (0, 0, 2.5)
    bpy.ops.object.transform_apply(scale=True)

    add_bevel_modifier(frame, width=0.03, segments=4)
    add_subdivision_modifier(frame, levels=1, render_levels=2)

    frame_mat = create_cinematic_material("sign_frame", (0.1, 0.1, 0.12), roughness=0.2, metallic=0.95)
    frame.data.materials.append(frame_mat)

    # LED sign panel
    bpy.ops.mesh.primitive_cube_add(size=2)
    led_panel = bpy.context.active_object
    led_panel.name = "sign_led"
    led_panel.scale = (1.4, 0.05, 0.35)
    led_panel.location = (0, 0.05, 2.5)
    bpy.ops.object.transform_apply(scale=True)

    color = hex_to_rgb(style['color_palette']['accent']['hex']) if 'color_palette' in style else (0.95, 0.7, 0.2)
    led_mat = create_cinematic_material("sign_led", color, roughness=0.1, metallic=0.3, emission_strength=5.0)
    led_panel.data.materials.append(led_mat)

    # Join
    bpy.ops.object.select_all(action='DESELECT')
    frame.select_set(True)
    led_panel.select_set(True)
    bpy.context.view_layer.objects.active = frame
    bpy.ops.object.join()

    return frame


def create_modern_light_post(style, position):
    """Create modern street lamp with glass dome"""
    # Post (tapered cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=3)
    post = bpy.context.active_object
    post.name = "light_post"
    post.location = (position[0], position[1], 1.5)

    # Taper the post slightly
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(1, 1, 1), constraint_axis=(False, False, True))
    bpy.ops.object.mode_set(mode='OBJECT')

    add_bevel_modifier(post, width=0.01, segments=3)
    post_mat = create_cinematic_material("light_post_metal", (0.15, 0.15, 0.17), roughness=0.3, metallic=0.85)
    post.data.materials.append(post_mat)

    # Light housing (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(position[0], position[1], 3.2))
    housing = bpy.context.active_object
    housing.name = "light_housing"

    add_subdivision_modifier(housing, levels=2, render_levels=3)

    # Glass material with emission
    color = hex_to_rgb(style['color_palette']['accent']['hex']) if 'color_palette' in style else (0.98, 0.85, 0.5)
    glass_mat = create_cinematic_material("light_glass", color, roughness=0.05, metallic=0.0, emission_strength=8.0)
    housing.data.materials.append(glass_mat)

    # Join
    bpy.ops.object.select_all(action='DESELECT')
    post.select_set(True)
    housing.select_set(True)
    bpy.context.view_layer.objects.active = post
    bpy.ops.object.join()

    return post


def create_cinematic_station(asset_id, section, style):
    """Assemble complete cinematic train station"""
    print(f"\n{'='*60}")
    print(f"Creating CINEMATIC Station: {asset_id}")
    print(f"Section: {section}")
    print(f"{'='*60}\n")

    objects = []

    # Platform
    platform = create_detailed_platform(style)
    objects.append(platform)

    # Benches (2)
    bench1 = create_modern_bench(style, (-3, -1, 0.05))
    bench2 = create_modern_bench(style, (3, -1, 0.05))
    objects.append(bench1)
    objects.append(bench2)

    # Sign
    sign = create_elegant_sign(style, section.upper())
    objects.append(sign)

    # Light posts (2)
    light1 = create_modern_light_post(style, (-5, 2, 0))
    light2 = create_modern_light_post(style, (5, 2, 0))
    objects.append(light1)
    objects.append(light2)

    # Join all into one object
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = platform
    bpy.ops.object.join()

    final_obj = bpy.context.active_object
    final_obj.name = asset_id

    # Center origin
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    return final_obj


def setup_hdri_lighting(style):
    """Setup HDRI environment for photorealistic lighting"""
    world = bpy.context.scene.world
    if not world.use_nodes:
        world.use_nodes = True

    nodes = world.node_tree.nodes
    links = world.node_tree.links

    # Clear existing nodes
    nodes.clear()

    # Background shader
    bg = nodes.new(type='ShaderNodeBackground')
    bg.location = (0, 0)

    # Use solid color for now (can be replaced with HDRI texture)
    ambient_color = hex_to_rgb(style['lighting']['ambient']['color']) if 'lighting' in style else (0.25, 0.27, 0.35)
    ambient_intensity = style['lighting']['ambient']['intensity'] if 'lighting' in style else 0.8

    bg.inputs['Color'].default_value = (*ambient_color, 1.0)
    bg.inputs['Strength'].default_value = ambient_intensity

    # Output
    output = nodes.new(type='ShaderNodeOutputWorld')
    output.location = (300, 0)

    links.new(bg.outputs['Background'], output.inputs['Surface'])

    # Add sun lamp for key light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.data.angle = radians(5)
    sun.rotation_euler = (radians(45), radians(30), radians(45))


def export_cinematic_glb(filepath, obj):
    """Export as optimized GLB (no Draco for web compatibility)"""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # CRITICAL: Enable smooth shading before export
    bpy.ops.object.shade_smooth()
    print("[Export] ✓ Applied smooth shading")

    # Calculate normals for all meshes
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    print("[Export] ✓ Recalculated normals")

    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.export_scene.gltf(
        filepath=str(filepath),
        export_format='GLB',
        use_selection=True,
        export_draco_mesh_compression_enable=False,
        export_texture_dir='',
        export_apply=True,  # Apply modifiers (subdivision becomes real geometry)
        export_yup=True,
        export_force_sampling=False,
        export_cameras=False,
        export_lights=True,  # Export lights for better rendering
        export_materials='EXPORT',
        export_normals=True,  # CRITICAL: Export vertex normals
        export_tangents=True  # For normal mapping
    )

    print(f"\n✓ Exported cinematic GLB: {filepath}")

    # Get file size
    file_size = Path(filepath).stat().st_size / 1024
    print(f"  File size: {file_size:.1f} KB")


def generate_metadata(asset_id, section, glb_path, style):
    """Generate asset metadata"""
    section_positions = {
        'home': [0, 0, 0],
        'store': [30, 0, 0],
        'gallery': [60, 0, 0],
        'blog': [90, 0, 0]
    }

    position = section_positions.get(section, [0, 0, 0])

    metadata = {
        "id": asset_id,
        "category": "cinematic_station",
        "file": f"models/{glb_path.name}",
        "scale": [1.0, 1.0, 1.0],
        "position": position,
        "rotation": [0, 0, 0],
        "animation": {
            "type": "cinematic_idle",
            "params": {
                "subtle_sway": True,
                "light_flicker": True,
                "duration": 6.0,
                "ease": "sine.inOut"
            }
        },
        "section": section,
        "visibility": {
            "default": True if section == "home" else False,
            "fadeIn": True,
            "fadeOut": True,
            "transitionDuration": 1.5
        },
        "quality": "cinematic",
        "features": [
            "subdivision_surfaces",
            "pbr_materials",
            "emission_lights",
            "beveled_edges",
            "photorealistic"
        ]
    }

    return metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True, help='Asset ID')
    parser.add_argument('--section', required=True, help='Section name')

    # Parse args after --
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = parser.parse_args(argv)

    # Load style guide
    project_root = Path(__file__).parent.parent.parent
    style_path = project_root / 'assets' / 'meta' / 'style-guide.json'

    with open(style_path) as f:
        style = json.load(f)

    # Clear scene
    clear_scene()

    # Create cinematic station
    asset_obj = create_cinematic_station(args.id, args.section, style)

    # Setup lighting
    setup_hdri_lighting(style)

    # Export paths
    glb_path = project_root / 'assets' / 'models' / f'{args.id}.glb'
    meta_path = project_root / 'assets' / 'meta' / f'{args.id}.json'

    # Export GLB
    export_cinematic_glb(glb_path, asset_obj)

    # Generate and save metadata
    metadata = generate_metadata(args.id, args.section, glb_path, style)
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"✓ Generated metadata: {meta_path}")

    print(f"\n{'='*60}")
    print("✓ CINEMATIC ASSET COMPLETE!")
    print(f"  GLB: {glb_path}")
    print(f"  Metadata: {meta_path}")
    print(f"  Quality: CINEMA-GRADE")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
