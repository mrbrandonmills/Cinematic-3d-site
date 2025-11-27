#!/usr/bin/env python3
"""
Bake and Export Script
Processes Blender files: UV unwrap, bake textures, export GLB
Usage: blender -b your_file.blend -P bake_and_export.py
"""

import bpy
import json
import sys
from pathlib import Path
from datetime import datetime


def ensure_uvs(obj):
    """Ensure object has UV coordinates"""
    if obj.type != 'MESH':
        return

    mesh = obj.data

    # Check if UV map exists
    if not mesh.uv_layers:
        print(f"  Creating UV map for {obj.name}")
        # Select object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Smart UV project
        bpy.ops.uv.smart_project(
            angle_limit=66.0,
            island_margin=0.02,
            area_weight=0.0,
            correct_aspect=True,
            scale_to_bounds=False
        )

        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        print(f"  ✓ UV map created for {obj.name}")
    else:
        print(f"  ✓ UV map exists for {obj.name}")


def setup_bake_settings():
    """Configure bake settings"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'  # Change to 'GPU' if available
    scene.cycles.samples = 128
    scene.cycles.max_bounces = 3
    scene.cycles.bake_type = 'COMBINED'

    # Set bake settings
    scene.render.bake.use_pass_direct = True
    scene.render.bake.use_pass_indirect = True
    scene.render.bake.use_pass_color = True
    scene.render.bake.margin = 16  # 16px margin to prevent seams

    print("  ✓ Bake settings configured")


def create_bake_image(name, resolution=1024):
    """Create an image for baking"""
    img = bpy.data.images.new(
        name=name,
        width=resolution,
        height=resolution,
        alpha=True,
        float_buffer=False
    )
    img.colorspace_settings.name = 'sRGB'
    return img


def bake_lighting(obj, resolution=1024):
    """Bake lighting for an object"""
    if obj.type != 'MESH':
        return None

    print(f"  Baking lighting for {obj.name}...")

    # Ensure UVs exist
    ensure_uvs(obj)

    # Create bake image
    bake_img = create_bake_image(f"{obj.name}_baked", resolution)

    # Setup material for baking
    mat = obj.data.materials[0] if obj.data.materials else None

    if not mat:
        print(f"  Warning: No material on {obj.name}, skipping bake")
        return None

    if not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes

    # Create image texture node for baking
    img_node = nodes.new(type='ShaderNodeTexImage')
    img_node.image = bake_img
    img_node.select = True
    nodes.active = img_node

    # Select object and bake
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    try:
        bpy.ops.object.bake(type='COMBINED')
        print(f"  ✓ Bake complete for {obj.name}")

        # Pack image into blend file
        bake_img.pack()

        return bake_img

    except Exception as e:
        print(f"  ✗ Bake failed for {obj.name}: {e}")
        return None


def export_glb(filepath):
    """Export scene as GLB"""
    # Deselect lights and cameras
    for obj in bpy.context.scene.objects:
        if obj.type in ['LIGHT', 'CAMERA', 'EMPTY']:
            obj.select_set(False)
        else:
            obj.select_set(True)

    # Ensure output directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # Export with optimal settings
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(filepath),
            export_format='GLB',
            use_selection=False,  # Export all visible objects
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
            export_texture_dir='',
            export_texcoords=True,
            export_normals=True,
            export_tangents=False,
            export_apply=True,
            export_yup=True,
            export_animations=True,
            export_frame_range=True,
            export_force_sampling=False,
            export_cameras=False,
            export_lights=False,
            export_colors=True,
            export_extras=True
        )

        print(f"✓ Exported GLB to: {filepath}")
        return True

    except Exception as e:
        print(f"✗ Export failed: {e}")
        return False


def process_blend_file(blend_path, output_dir, bake=True):
    """Process a single blend file"""
    print(f"\n{'='*60}")
    print(f"Processing: {blend_path.name}")
    print(f"{'='*60}\n")

    # Open blend file
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))

    # Get all mesh objects
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    if not mesh_objects:
        print("  Warning: No mesh objects found in scene")
        return False

    print(f"Found {len(mesh_objects)} mesh object(s)")

    # Ensure UVs for all objects
    for obj in mesh_objects:
        ensure_uvs(obj)

    # Bake if requested
    if bake:
        print("\n--- Baking Phase ---")
        setup_bake_settings()

        for obj in mesh_objects:
            bake_lighting(obj, resolution=1024)

    # Export GLB
    print("\n--- Export Phase ---")
    output_path = Path(output_dir) / f"{blend_path.stem}.glb"
    success = export_glb(output_path)

    if success:
        filesize = output_path.stat().st_size
        print(f"\nFile size: {filesize / 1024:.1f} KB ({filesize / (1024*1024):.2f} MB)")

    return success


def main():
    """Main execution"""
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent.parent
    models_dir = project_root / "assets" / "models"

    # Parse arguments
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []

    # Get current blend file
    current_file = bpy.data.filepath

    if not current_file:
        print("Error: No blend file is open")
        print("Usage: blender -b your_file.blend -P bake_and_export.py")
        return

    blend_path = Path(current_file)

    # Check if --no-bake flag is present
    bake = "--no-bake" not in argv

    # Check if custom output directory is specified
    output_dir = models_dir
    if "--output" in argv:
        idx = argv.index("--output")
        if idx + 1 < len(argv):
            output_dir = Path(argv[idx + 1])

    print(f"\n{'='*60}")
    print(f"Bake and Export Script")
    print(f"{'='*60}")
    print(f"Input: {blend_path}")
    print(f"Output: {output_dir}")
    print(f"Baking: {'Yes' if bake else 'No'}")
    print(f"{'='*60}")

    # Process the file
    success = process_blend_file(blend_path, output_dir, bake=bake)

    if success:
        print(f"\n{'='*60}")
        print("✓ Processing complete!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print("✗ Processing failed")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
