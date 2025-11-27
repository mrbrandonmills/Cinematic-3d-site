# Cinematic 3D Site Architecture

## Overview

This project implements a dual-agent system for creating cinematic 3D web experiences with scroll-driven narratives. The architecture separates 3D asset creation from web implementation while maintaining a clear contract between the two.

## Agent Roles

### Primary Orchestrator Agent
**Responsibilities:**
- Scaffold the codebase and maintain project structure
- Define and coordinate the Asset Agent and Web/Cinematic Agent
- Manage the shared asset contract and communication protocols
- Handle user requests and delegate to specialized agents

### Asset Agent
**Responsibilities:**
- Create and optimize 3D assets using Blender + Python
- Generate GLB files exported to `assets/models/`
- Create metadata JSON files in `assets/meta/` following the asset schema
- Maintain style consistency across all 3D assets
- Automate asset generation, baking, and export pipelines

**Tools:**
- Blender (headless mode via Python scripts)
- Python scripts for automation
- GLB/GLTF export pipeline

### Web/Cinematic Agent
**Responsibilities:**
- Build the front-end cinematic experience
- Load and position 3D assets from `assets/models/`
- Create scroll-driven camera paths and animations
- Implement smooth scrolling and parallax effects
- Map "train station" sections to assets and camera waypoints

**Tools:**
- Three.js for 3D rendering
- GSAP + ScrollTrigger for scroll animations
- Locomotive Scroll for smooth scrolling
- React + React Three Fiber (optional)

## Project Structure

```
cinematic-3d-site/
├── assets/
│   ├── models/          # GLB/GLTF files from Asset Agent
│   ├── textures/        # KTX2/PNG/HDRI textures
│   └── meta/            # JSON manifests and metadata
│       ├── asset-schema.json
│       ├── style-guide.json
│       ├── asset-list.json
│       └── [asset-id].json
├── web/
│   ├── src/
│   │   ├── components/   # React components (if using React)
│   │   ├── scenes/       # Three.js scene setup
│   │   ├── utils/        # Utility functions
│   │   ├── main.tsx      # Entry point
│   │   ├── threeScene.ts # Core Three.js setup
│   │   ├── scrollAnimations.ts  # GSAP scroll logic
│   │   └── sceneConfig.ts       # Section/asset mappings
│   ├── public/           # Static assets
│   └── package.json
└── tools/
    ├── blender-scripts/
    │   ├── generate_asset_template.py
    │   ├── bake_and_export.py
    │   └── asset_automation.py
    └── docs/
        ├── ARCHITECTURE.md
        ├── ASSET_PIPELINE.md
        └── WEB_DEVELOPMENT.md
```

## Shared Contract

### Asset Metadata Schema
All assets must provide metadata following `assets/meta/asset-schema.json`. This ensures:
- Consistent positioning, scaling, and rotation
- Animation parameters are properly defined
- Section assignment for scroll narrative
- Unique IDs for asset management

### Communication Protocol
1. User describes a new "train station" section
2. Primary Agent sends description to Asset Agent
3. Asset Agent:
   - Creates 3D asset in Blender
   - Exports optimized GLB to `assets/models/`
   - Generates metadata JSON to `assets/meta/`
   - Updates `asset-list.json`
4. Primary Agent notifies Web Agent
5. Web Agent:
   - Adds entry to `sceneConfig.ts`
   - Wires scroll trigger and camera path
   - Updates the site to include new section

## Tech Stack & Costs

### 100% Free/Open Source
- **3D Creation:** Blender + Python (headless) - $0
- **3D Web Rendering:** Three.js - $0
- **Scroll Animations:** GSAP core + ScrollTrigger - $0 (free for personal/client sites)
- **Smooth Scrolling:** Locomotive Scroll - $0
- **Framework:** React + React Three Fiber (optional) - $0
- **Build Tool:** Vite - $0

### Optional Paid Enhancements
- GSAP Club ($99+/year) - for ScrollSmoother and premium plugins
- Spline Pro ($8-39/month) - if you want Spline instead of Blender
- Commercial 3D software licenses (Maya, C4D) - not needed

## Development Workflow

### Adding a New Section
1. Describe the new station (e.g., "Cyberpunk neon train station for Blog")
2. Primary Agent delegates to Asset Agent: "Create station-blog.glb"
3. Asset Agent outputs:
   - `assets/models/station-blog.glb`
   - `assets/meta/station-blog.json`
   - Updated `assets/meta/asset-list.json`
4. Web Agent updates:
   - `web/src/sceneConfig.ts` with new section
   - Camera path for the new station
   - Scroll triggers and animations

### Iterating on Existing Assets
1. Request change (e.g., "Make station-store more minimalist")
2. Asset Agent:
   - Regenerates or modifies Blender file
   - Re-exports GLB (overwrites existing)
   - Updates metadata if positioning/scale changes
3. Web automatically picks up changes on next reload

## Running the System

### Asset Generation (Mac mini)
```bash
# Run headless Blender export for a single asset
blender -b assets.blend -P tools/blender-scripts/bake_and_export.py

# Generate all assets from templates
python tools/blender-scripts/asset_automation.py --config assets/meta/asset-list.json
```

### Web Development
```bash
cd web
npm install
npm run dev  # Start development server
npm run build  # Production build
```

## Best Practices

1. **Asset Optimization:** Keep GLB files under 5MB each, use draco compression
2. **Consistent Scale:** Define a world scale (e.g., 1 unit = 1 meter) and stick to it
3. **Baked Lighting:** Pre-bake lighting in Blender for better performance
4. **Texture Atlasing:** Combine textures where possible to reduce draw calls
5. **LOD (Level of Detail):** Create simplified versions for distant viewing
6. **Version Control:** Commit both `.blend` source files and exported GLBs
7. **Metadata First:** Update asset metadata before building web features

## Performance Targets

- **Initial Load:** < 3s on 4G
- **60 FPS:** Maintain during scroll animations
- **Total Asset Size:** < 20MB uncompressed, < 10MB compressed
- **Lighthouse Score:** 90+ on Performance

## Future Enhancements

- [ ] Dynamic asset streaming (load sections on demand)
- [ ] WebGPU renderer for better performance
- [ ] Real-time lighting with shadow maps
- [ ] Physics integration for interactive elements
- [ ] Audio spatial positioning tied to camera
- [ ] VR/AR mode support
