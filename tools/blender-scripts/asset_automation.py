#!/usr/bin/env python3
"""
Asset Automation Script
Reads asset-list.json and generates all planned assets
Usage: python asset_automation.py --config assets/meta/asset-list.json
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import argparse


def load_asset_list(config_path):
    """Load the asset list configuration"""
    with open(config_path) as f:
        return json.load(f)


def save_asset_list(config_path, asset_list):
    """Save updated asset list"""
    with open(config_path, 'w') as f:
        json.dump(asset_list, f, indent=2)


def run_blender_script(script_path, asset_id, section):
    """Run Blender script in headless mode"""
    cmd = [
        "blender",
        "-b",  # Background mode
        "-P", str(script_path),  # Python script
        "--",  # Separator for script args
        "--id", asset_id,
        "--section", section
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

        if result.stderr:
            print("Warnings/Errors:", result.stderr)

        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Blender script failed with exit code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

    except FileNotFoundError:
        print("✗ Error: Blender not found in PATH")
        print("Please ensure Blender is installed and added to your PATH")
        print("\nOn macOS:")
        print("  export PATH=\"$PATH:/Applications/Blender.app/Contents/MacOS\"")
        print("\nOr specify full path to blender binary")
        return False


def generate_asset(asset, generator_script):
    """Generate a single asset"""
    asset_id = asset['id']
    section = asset['section']
    status = asset.get('status', 'planned')

    print(f"\n{'='*70}")
    print(f"Asset: {asset_id}")
    print(f"Section: {section}")
    print(f"Status: {status}")
    print(f"Description: {asset.get('description', 'N/A')}")
    print(f"{'='*70}")

    if status != 'planned':
        print(f"⊘ Skipping (status is '{status}', not 'planned')")
        return False

    # Run Blender generation script
    success = run_blender_script(generator_script, asset_id, section)

    if success:
        asset['status'] = 'complete'
        asset['completed_at'] = datetime.now().isoformat()
        print(f"\n✓ Asset {asset_id} generated successfully")
    else:
        asset['status'] = 'failed'
        asset['failed_at'] = datetime.now().isoformat()
        print(f"\n✗ Asset {asset_id} generation failed")

    return success


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Automate asset generation from asset-list.json'
    )
    parser.add_argument(
        '--config',
        default='assets/meta/asset-list.json',
        help='Path to asset-list.json'
    )
    parser.add_argument(
        '--generator',
        help='Path to Blender generator script'
    )
    parser.add_argument(
        '--id',
        help='Generate only specific asset ID'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate assets even if status is not "planned"'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without actually generating'
    )

    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent.parent
    config_path = project_root / args.config

    if not config_path.exists():
        print(f"✗ Error: Config file not found: {config_path}")
        sys.exit(1)

    # Find generator script
    if args.generator:
        generator_script = Path(args.generator)
    else:
        generator_script = script_dir / "generate_asset_template.py"

    if not generator_script.exists():
        print(f"✗ Error: Generator script not found: {generator_script}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print("Asset Automation")
    print(f"{'='*70}")
    print(f"Config: {config_path}")
    print(f"Generator: {generator_script}")
    print(f"Dry run: {args.dry_run}")
    print(f"{'='*70}\n")

    # Load asset list
    asset_list = load_asset_list(config_path)
    assets = asset_list.get('assets', [])

    if not assets:
        print("No assets found in config")
        return

    print(f"Found {len(assets)} asset(s) in config\n")

    # Filter assets
    assets_to_generate = []

    for asset in assets:
        asset_id = asset['id']
        status = asset.get('status', 'planned')

        # Filter by ID if specified
        if args.id and asset_id != args.id:
            continue

        # Filter by status
        if args.force or status == 'planned':
            assets_to_generate.append(asset)
        else:
            print(f"⊘ Skipping {asset_id} (status: {status})")

    if not assets_to_generate:
        print("\nNo assets to generate")
        return

    print(f"\n{len(assets_to_generate)} asset(s) will be generated:\n")
    for asset in assets_to_generate:
        print(f"  - {asset['id']} ({asset['section']})")

    if args.dry_run:
        print("\n⊘ Dry run mode - no assets were generated")
        return

    # Generate assets
    print("\n" + "="*70)
    print("Starting generation...")
    print("="*70)

    success_count = 0
    fail_count = 0

    for asset in assets_to_generate:
        success = generate_asset(asset, generator_script)

        if success:
            success_count += 1
        else:
            fail_count += 1

    # Update asset list
    if not args.dry_run:
        asset_list['updated'] = datetime.now().isoformat()
        save_asset_list(config_path, asset_list)
        print(f"\n✓ Updated asset list: {config_path}")

    # Summary
    print(f"\n{'='*70}")
    print("Generation Summary")
    print(f"{'='*70}")
    print(f"Total: {len(assets_to_generate)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"{'='*70}\n")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
