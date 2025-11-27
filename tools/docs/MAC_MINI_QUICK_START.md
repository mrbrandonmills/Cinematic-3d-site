# Mac mini Quick Start Guide

This guide shows you exactly how to run the asset generation pipeline on your Mac mini.

## One-Time Setup

### 1. Install Blender (if not already installed)

Download from: https://www.blender.org/download/

Or install with Homebrew:
```bash
brew install --cask blender
```

### 2. Add Blender to PATH

Edit your shell configuration:

```bash
# Open your shell config
nano ~/.zshrc  # or ~/.bash_profile if using bash

# Add this line:
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"

# Save (Ctrl+X, then Y, then Enter)

# Reload shell
source ~/.zshrc
```

### 3. Verify Installation

```bash
# Check Blender version
blender --version

# Should show something like:
# Blender 3.6.5
# Build: 2023-10-10
```

## Daily Usage - Asset Generation

### Generate One Asset

**Home Station:**
```bash
cd "/Volumes/Super Mastery/cinematic-3d-site"

blender -b -P tools/blender-scripts/generate_asset_template.py -- \
  --id station-home \
  --section home
```

**Store Station:**
```bash
blender -b -P tools/blender-scripts/generate_asset_template.py -- \
  --id station-store \
  --section store
```

**Gallery Station:**
```bash
blender -b -P tools/blender-scripts/generate_asset_template.py -- \
  --id station-gallery \
  --section gallery
```

**Blog Station:**
```bash
blender -b -P tools/blender-scripts/generate_asset_template.py -- \
  --id station-blog \
  --section blog
```

### Generate All Assets at Once

```bash
cd "/Volumes/Super Mastery/cinematic-3d-site"

python tools/blender-scripts/asset_automation.py
```

**Expected output:**
```
======================================================================
Asset Automation
======================================================================
Config: /Volumes/Super Mastery/cinematic-3d-site/assets/meta/asset-list.json
Generator: tools/blender-scripts/generate_asset_template.py
Dry run: False
======================================================================

Found 4 asset(s) in config

4 asset(s) will be generated:
  - station-home (home)
  - station-store (store)
  - station-gallery (gallery)
  - station-blog (blog)

======================================================================
Starting generation...
======================================================================

[... Blender output ...]

✓ Asset station-home generated successfully
✓ Asset station-store generated successfully
✓ Asset station-gallery generated successfully
✓ Asset station-blog generated successfully

======================================================================
Generation Summary
======================================================================
Total: 4
Success: 4
Failed: 0
======================================================================
```

### Preview Before Generating

```bash
python tools/blender-scripts/asset_automation.py --dry-run
```

This shows what would be generated without actually running Blender.

## Working with Existing Blender Files

### If You Have a .blend File

**Export and bake:**
```bash
blender -b "/path/to/your/file.blend" -P tools/blender-scripts/bake_and_export.py
```

**Quick export (skip baking):**
```bash
blender -b "/path/to/your/file.blend" -P tools/blender-scripts/bake_and_export.py -- --no-bake
```

### Batch Process Multiple Files

```bash
# Export all .blend files in a directory
for file in /path/to/blends/*.blend; do
  blender -b "$file" -P tools/blender-scripts/bake_and_export.py
done
```

## Validating Assets

### Check Asset Metadata

```bash
python tools/blender-scripts/validate_metadata.py assets/meta/station-home.json
```

**Expected output:**
```
======================================================================
Validating: station-home.json
======================================================================

✓ Schema validation: Passed
✓ GLB file exists: Passed
✓ File size matches: Passed
✓ Required fields: All present

======================================================================
Metadata Summary
======================================================================
ID: station-home
Category: hero_stop
Section: home
File: models/station-home.glb
Polycount: 45,321
File size: 2.4 MB
Version: 1.0.0
======================================================================

✓ All validation checks passed!
```

### Check All Assets

```bash
for file in assets/meta/station-*.json; do
  echo "Checking $file..."
  python tools/blender-scripts/validate_metadata.py "$file"
  echo ""
done
```

## Viewing Generated Assets

### Option 1: Online Viewer

1. Go to https://gltf-viewer.donmccurdy.com
2. Drag and drop your GLB file
3. Inspect the asset, check polycount, materials, etc.

### Option 2: Open in Blender

```bash
blender assets/models/station-home.glb
```

## Modifying the Style Guide

The style guide controls the look and feel of all generated assets.

**Edit:**
```bash
# Open in your favorite editor
code assets/meta/style-guide.json
# or
nano assets/meta/style-guide.json
```

**Key settings:**
- `color_palette` - Main colors used
- `materials` - PBR material properties
- `lighting` - Lighting setup for baking
- `geometry.target_polycount` - Polygon budgets
- `textures.resolution` - Texture sizes

**After editing, regenerate assets:**
```bash
# Mark assets as "planned" in asset-list.json, then:
python tools/blender-scripts/asset_automation.py --force
```

## Performance Monitoring

### Check Asset File Sizes

```bash
ls -lh assets/models/
```

Target: < 3MB per hero asset (compressed)

### Check Polycount

```bash
python tools/blender-scripts/validate_metadata.py assets/meta/station-home.json | grep Polycount
```

Target: < 50,000 triangles per hero asset

### Optimize Oversized Assets

If an asset is too large:

1. **Reduce texture resolution** in `style-guide.json`
2. **Simplify geometry** in Blender (Decimate modifier)
3. **Re-export** with higher Draco compression

## Troubleshooting

### "blender: command not found"

**Fix:**
```bash
# Check if Blender is installed
ls /Applications/Blender.app

# If it exists, add to PATH
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"

# Make it permanent
echo 'export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "Python module not found"

**Fix:** Use Blender's built-in Python
```bash
# Find Blender's Python
BLENDER_PYTHON="/Applications/Blender.app/Contents/Resources/3.6/python/bin/python3.10"

# Install module
$BLENDER_PYTHON -m pip install <module-name>
```

### "Export failed" or Blender Crashes

**Fix:**
1. Run Blender in foreground to see errors:
   ```bash
   blender tools/blender-scripts/generate_asset_template.py
   ```
2. Check Blender console for error messages
3. Simplify the scene (reduce polycount)
4. Update Blender to latest version

### Assets Look Black/Wrong in Browser

**Fix:**
1. Ensure textures are baked: Don't use `--no-bake`
2. Check material settings in Blender
3. Verify lighting setup in `style-guide.json`
4. Test GLB in online viewer first

## Advanced: Custom Scripts

### Create a Custom Generator

Copy the template:
```bash
cp tools/blender-scripts/generate_asset_template.py tools/blender-scripts/custom_generator.py
```

Edit `custom_generator.py` to create your own parametric assets.

Run it:
```bash
blender -b -P tools/blender-scripts/custom_generator.py -- --id my-asset --section home
```

### Batch Operations

**Regenerate all assets in one command:**
```bash
cd "/Volumes/Super Mastery/cinematic-3d-site"
python tools/blender-scripts/asset_automation.py --force
```

**Validate all assets:**
```bash
for file in assets/meta/station-*.json; do
  python tools/blender-scripts/validate_metadata.py "$file" || exit 1
done
```

## Keyboard Shortcuts Summary

```bash
# Navigate to project
cd "/Volumes/Super Mastery/cinematic-3d-site"

# Generate one asset
blender -b -P tools/blender-scripts/generate_asset_template.py -- --id ASSET_ID --section SECTION

# Generate all planned assets
python tools/blender-scripts/asset_automation.py

# Validate asset
python tools/blender-scripts/validate_metadata.py assets/meta/ASSET_ID.json

# Export existing .blend file
blender -b FILE.blend -P tools/blender-scripts/bake_and_export.py
```

## Next Steps

Once assets are generated:

1. **Validate** all assets
2. **Test** in GLB viewer
3. **Integrate** into web (see main README)
4. **Deploy** and enjoy!

## Resources

- Main README: `README.md`
- Architecture: `tools/docs/ARCHITECTURE.md`
- Asset Agent Spec: `tools/docs/ASSET_AGENT_SPEC.md`
- Web Agent Spec: `tools/docs/WEB_AGENT_SPEC.md`

---

**Questions?** Check the main README or the detailed specs in `tools/docs/`.
