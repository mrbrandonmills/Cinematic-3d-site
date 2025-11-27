# 3D Animation Mastery - All Agent Specifications Summary

**Purpose:** Quick reference for all specialized agent roles
**Date:** November 27, 2025

---

## 🎯 AGENT DELEGATION MAP

```
Task Type → Agent to Use → Delegate Via

Blender Python scripting → blender-automation-master → Task(subagent_type="infrastructure-developer")
Cinema lighting/materials → cinema-quality-renderer → Task(subagent_type="luxury-visual-designer")
Three.js/WebGL optimization → webgl-performance-architect → Task(subagent_type="react-developer")
GSAP scroll animations → scroll-animation-choreographer → Task(subagent_type="react-developer")
Pipeline architecture → 3d-pipeline-architect → Task(subagent_type="cto")
Quality validation → visual-quality-auditor → Task(subagent_type="qa-engineer")
```

---

## 1️⃣ BLENDER AUTOMATION MASTER

**Expertise:** Blender 5.0.0 Python API, procedural generation, batch automation

**When to Use:**
- Generate new train station assets
- Automate texture baking workflows
- Batch export GLB files with Draco compression
- Generate asset metadata JSON files
- Optimize geometry and apply smooth shading

**Key Responsibilities:**
✅ Write Blender Python scripts for parametric asset creation
✅ Bake textures (combined, AO, normal, ORM, emissive)
✅ Export GLB with Draco level 6 compression
✅ Generate validated metadata JSON
✅ Apply smooth shading and recalculate normals

**Success Metrics:**
- Assets generated in < 1 hour per hero stop
- File size < 3MB (Draco compressed)
- Polycount < 50,000 triangles
- Metadata validates 100%

**Documentation:** `tools/docs/agents/BLENDER_AUTOMATION_MASTER.md`

---

## 2️⃣ CINEMA QUALITY RENDERER

**Expertise:** Lighting design, PBR materials, post-processing, visual quality

**When to Use:**
- Fix overexposed/washed out scenes
- Configure lighting (ambient, directional, emissive)
- Setup PBR materials (metal/roughness workflow)
- Balance bloom, SSAO, SMAA post-processing
- Troubleshoot blocky geometry or material issues

**Key Responsibilities:**
✅ Configure Three.js renderer (tone mapping, exposure, color space)
✅ Balance scene lighting (target: 1.2-1.5 total intensity)
✅ Setup post-processing (bloom 0.3-0.5, SSAO, SMAA)
✅ Ensure smooth subdivision surfaces render correctly
✅ Validate PBR materials load properly

**Quality Standards:**
- Balanced exposure (no blown-out highlights)
- Subtle bloom on emissive lights only
- Smooth geometry (vertex normals computed)
- Cinema-grade comparable to luxury brand sites

**Documentation:** `CINEMA_QUALITY_FIXES.md`, `VISUAL_QUALITY_CHECKLIST.md`

---

## 3️⃣ WEBGL PERFORMANCE ARCHITECT

**Expertise:** Three.js 0.181.2, WebGL optimization, 60FPS performance

**When to Use:**
- Optimize scenes for 60 FPS performance
- Reduce draw calls and memory usage
- Implement lazy loading and frustum culling
- Profile and debug performance issues
- Upgrade Three.js to latest version (0.181.2)

**Key Responsibilities:**
✅ Achieve 60 FPS sustained during scroll
✅ Optimize asset loading (progressive, lazy loading)
✅ Reduce draw calls (< 100 per frame)
✅ Configure LOD systems for distant objects
✅ Profile with Chrome DevTools Performance

**Performance Targets:**
- 60 FPS minimum on mid-range devices
- < 3s load time on 4G
- < 20MB total asset budget
- < 100 draw calls per frame
- < 500MB memory usage

**Documentation:** `web/src/threeScene.ts`, `web/src/utils/renderDebug.ts`

---

## 4️⃣ SCROLL ANIMATION CHOREOGRAPHER

**Expertise:** GSAP 3.13.0, ScrollTrigger, Locomotive Scroll, cinematic timing

**When to Use:**
- Design camera paths between train stations
- Implement scroll-driven animations
- Configure section-based scroll triggers
- Choreograph asset visibility/opacity animations
- Upgrade GSAP to latest version (3.13.0)

**Key Responsibilities:**
✅ Design smooth camera interpolation paths
✅ Configure GSAP ScrollTrigger for each section
✅ Integrate Locomotive Scroll for smooth inertia
✅ Choreograph timeline animations
✅ Ensure 60 FPS during scroll

**Animation Standards:**
- Smooth camera transitions (power2.inOut easing)
- No janky/stuttering scroll behavior
- Perfectly timed section triggers
- Cinematic pacing and flow

**Documentation:** `web/src/scrollAnimations.ts`, `web/src/sceneConfig.ts`

---

## 5️⃣ 3D PIPELINE ARCHITECT

**Expertise:** System design, asset pipeline architecture, workflow coordination

**When to Use:**
- Design asset pipeline workflows
- Coordinate Asset Agent ↔ Web Agent communication
- Manage asset metadata schema
- Orchestrate batch generation workflows
- Document system architecture

**Key Responsibilities:**
✅ Maintain asset metadata schema (asset-schema.json)
✅ Coordinate agent communication protocols
✅ Design scalable pipeline architecture
✅ Document workflows and best practices
✅ Ensure system maintainability

**System Quality:**
- Clear separation of concerns
- Modular, maintainable architecture
- Comprehensive documentation
- Scalable for future growth

**Documentation:** `tools/docs/ARCHITECTURE.md`, `tools/docs/AGENT_ARCHITECTURE_3D_MASTERY.md`

---

## 6️⃣ VISUAL QUALITY AUDITOR

**Expertise:** Quality control, cinema-grade validation, standards compliance

**When to Use:**
- Validate cinema-quality standards before production
- Run visual quality checklists
- Identify rendering issues (overexposed, blocky, flat)
- Verify performance metrics (60 FPS, load times)
- Final sign-off for production deployment

**Key Responsibilities:**
✅ Run VISUAL_QUALITY_CHECKLIST.md validation
✅ Check lighting intensity (1.2-1.5 total)
✅ Verify materials load correctly (no issues)
✅ Validate smooth geometry (no blocky edges)
✅ Confirm 60 FPS performance sustained

**Quality Gates:**
- All visual quality checks pass ✅
- Zero material issues detected
- Lighting balanced (not overexposed/underexposed)
- Smooth subdivision surfaces
- 60 FPS sustained
- Zero console errors/warnings

**Documentation:** `VISUAL_QUALITY_CHECKLIST.md`, `web/src/utils/renderDebug.ts`

---

## 🔄 COMPLETE WORKFLOW EXAMPLE

### **Request:** Add new "About" section with train station

```
1. PRIMARY ORCHESTRATOR (You)
   ↓ Delegates to:

2. 3D-PIPELINE-ARCHITECT
   - Designs workflow for new section
   - Defines metadata requirements
   ↓ Coordinates:

3. BLENDER-AUTOMATION-MASTER
   - Generates station-about.glb asset
   - Creates metadata JSON
   - Validates against schema
   ↓ Hands off to:

4. CINEMA-QUALITY-RENDERER
   - Validates lighting and materials
   - Checks for rendering issues
   - Applies fixes if needed
   ↓ Passes to:

5. WEBGL-PERFORMANCE-ARCHITECT
   - Optimizes asset for web
   - Verifies filesize and polycount
   - Tests loading performance
   ↓ Integrates via:

6. SCROLL-ANIMATION-CHOREOGRAPHER
   - Adds section to sceneConfig.ts
   - Designs camera path
   - Wires ScrollTrigger animations
   ↓ Final validation:

7. VISUAL-QUALITY-AUDITOR
   - Runs complete quality checklist
   - Verifies all standards met
   - Signs off for production
   ↓ Returns to:

8. PRIMARY ORCHESTRATOR (You)
   - Delivers cinema-quality section
   - Confirms all metrics met
   - Ready for deployment
```

---

## 🛠️ QUICK DELEGATION EXAMPLES

### Generate New Asset:
```typescript
// Delegate to blender-automation-master
Task({
  subagent_type: "infrastructure-developer",
  description: "Generate station-about asset",
  prompt: `Generate a new train station asset for the "About" section:

  Requirements:
  - Asset ID: station-about
  - Section: about
  - Theme: Professional, corporate blue tones, clean modern architecture
  - Use style guide: assets/meta/style-guide.json

  Deliverables:
  - assets/models/station-about.glb (< 3MB, Draco compressed)
  - assets/meta/station-about.json (validated metadata)
  - Updated assets/meta/asset-list.json`
})
```

### Fix Rendering Issues:
```typescript
// Delegate to cinema-quality-renderer
Task({
  subagent_type: "luxury-visual-designer",
  description: "Fix washed out rendering",
  prompt: `The scene is appearing washed out and overexposed.

  Diagnosis needed:
  - Check lighting intensity (should be 1.2-1.5 total)
  - Verify bloom settings (strength should be 0.3-0.5)
  - Validate tone mapping exposure (0.8-1.0)
  - Ensure materials are loading correctly

  Reference: CINEMA_QUALITY_FIXES.md

  Expected result: Balanced, cinema-quality rendering`
})
```

### Optimize Performance:
```typescript
// Delegate to webgl-performance-architect
Task({
  subagent_type: "react-developer",
  description: "Optimize for 60 FPS",
  prompt: `Scene is running at 30-40 FPS, need to optimize to 60 FPS.

  Profile and optimize:
  - Check draw calls (should be < 100)
  - Verify triangle count (< 100,000 total)
  - Implement lazy loading if needed
  - Optimize texture sizes
  - Test on mid-range device

  Target: Sustained 60 FPS during scroll`
})
```

### Setup Scroll Animations:
```typescript
// Delegate to scroll-animation-choreographer
Task({
  subagent_type: "react-developer",
  description: "Create scroll animations",
  prompt: `Integrate the new station-about asset into the scroll narrative.

  Tasks:
  - Add section to web/src/sceneConfig.ts
  - Design camera path from previous station
  - Configure ScrollTrigger (start/end points)
  - Wire visibility animations
  - Test smooth transitions

  Expected: Cinematic camera movement, 60 FPS during scroll`
})
```

---

## 📊 TECHNOLOGY STACK UPDATES REQUIRED

Current vs Latest (November 27, 2025):

| Package | Current | Latest | Status |
|---------|---------|--------|--------|
| Blender | 5.0.0 | 5.0.0 | ✅ CURRENT |
| Three.js | 0.160.0 | **0.181.2** | 🔄 UPGRADE |
| GSAP | 3.12.5 | **3.13.0** | 🔄 UPGRADE |
| React | 18.2.0 | **19.2.0** | 🔄 UPGRADE |
| TypeScript | 5.3.3 | **5.7+** | 🔄 UPGRADE |
| Vite | 5.0.8 | **6.x** | 🔄 UPGRADE |
| Locomotive Scroll | 5.0.0-beta.13 | 5.0.0-beta.13 | ✅ CURRENT |

**Note:** Technology stack updates should be delegated to `webgl-performance-architect` to ensure compatibility and no breaking changes.

---

## ✅ PRE-PHASE ONE STATUS

**Complete:**
- ✅ Agent architecture designed
- ✅ All 6 specialized agent roles documented
- ✅ Delegation protocols established
- ✅ Workflow coordination defined
- ✅ Technology stack assessed
- ✅ Quality standards documented

**Ready For:**
- Phase 1: Project analysis and assessment
- Technology stack updates
- Prototype review
- Production implementation

---

**Primary Orchestrator:** 3D Animation Design Master (Claude)
**Status:** Pre-Phase One Complete - Ready for Phase 1
