#!/bin/bash
# Regenerate Cinema-Quality 3D Asset
# Usage: ./regenerate_asset.sh [asset-id] [section]
# Example: ./regenerate_asset.sh station-home home

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ASSET_ID="${1:-station-home}"
SECTION="${2:-home}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Cinema-Quality 3D Asset Regeneration Script             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Asset ID:${NC} $ASSET_ID"
echo -e "${YELLOW}Section:${NC} $SECTION"
echo ""

# Check if Blender is installed
if ! command -v blender &> /dev/null; then
    echo -e "${RED}ERROR: Blender not found in PATH${NC}"
    echo "Please install Blender or add it to your PATH"
    echo "macOS: export PATH=\"/Applications/Blender.app/Contents/MacOS:\$PATH\""
    exit 1
fi

echo -e "${GREEN}✓ Found Blender:${NC} $(blender --version | head -1)"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BLENDER_SCRIPT="$SCRIPT_DIR/tools/blender-scripts/generate_cinematic_station.py"
OUTPUT_GLB="$SCRIPT_DIR/assets/models/${ASSET_ID}.glb"
OUTPUT_META="$SCRIPT_DIR/assets/meta/${ASSET_ID}.json"

# Check if Blender script exists
if [ ! -f "$BLENDER_SCRIPT" ]; then
    echo -e "${RED}ERROR: Blender script not found at:${NC}"
    echo "$BLENDER_SCRIPT"
    exit 1
fi

echo -e "${BLUE}[1/3]${NC} Running Blender generation..."
echo -e "${YELLOW}      This will take 10-30 seconds...${NC}"
echo ""

# Run Blender in background mode
blender -b -P "$BLENDER_SCRIPT" -- --id "$ASSET_ID" --section "$SECTION"

echo ""
echo -e "${BLUE}[2/3]${NC} Verifying output files..."

# Check if GLB was created
if [ ! -f "$OUTPUT_GLB" ]; then
    echo -e "${RED}ERROR: GLB file not generated at:${NC}"
    echo "$OUTPUT_GLB"
    exit 1
fi

# Check if metadata was created
if [ ! -f "$OUTPUT_META" ]; then
    echo -e "${RED}ERROR: Metadata file not generated at:${NC}"
    echo "$OUTPUT_META"
    exit 1
fi

# Get file sizes
GLB_SIZE=$(du -h "$OUTPUT_GLB" | cut -f1)
META_SIZE=$(du -h "$OUTPUT_META" | cut -f1)

echo -e "${GREEN}✓ GLB:${NC} $OUTPUT_GLB (${GLB_SIZE})"
echo -e "${GREEN}✓ Metadata:${NC} $OUTPUT_META (${META_SIZE})"
echo ""

echo -e "${BLUE}[3/3]${NC} Asset regeneration complete!"
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✓ Cinema-Quality Asset Ready                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Start dev server: ${BLUE}cd web && npm run dev${NC}"
echo -e "  2. Open browser: ${BLUE}http://localhost:3000${NC}"
echo -e "  3. Check console for: ${BLUE}[RenderDebug] Full Diagnostic${NC}"
echo ""
echo -e "${YELLOW}Expected console output:${NC}"
echo -e "  - ${GREEN}✓ Loaded X materials (Y emissive)${NC} ${YELLOW}← Should see emissive count > 0${NC}"
echo -e "  - ${GREEN}✓ Total Intensity: 1.35${NC} ${YELLOW}← Should be < 1.5${NC}"
echo -e "  - ${GREEN}✓ All materials verified${NC} ${YELLOW}← Should be ZERO issues${NC}"
echo ""
