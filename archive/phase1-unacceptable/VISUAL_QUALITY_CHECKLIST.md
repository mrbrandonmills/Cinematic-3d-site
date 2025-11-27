# Visual Quality Checklist - Cinema-Grade 3D Rendering

Use this checklist to verify your 3D scene meets cinema-quality standards.

---

## 🎬 OVERALL SCENE QUALITY

### ✅ CORRECT (Cinema-Quality)
- Scene has depth and dimension (not flat)
- Can clearly distinguish foreground, midground, background
- Colors are rich but not oversaturated
- Highlights are bright but not blown out (no pure white areas)
- Shadows exist and are visible (ambient occlusion working)
- Scene has atmosphere and mood

### ❌ INCORRECT (Common Issues)
- **Washed Out:** Everything too bright, details lost in white
- **Flat:** No depth, looks like a 2D rendering
- **Oversaturated:** Colors too intense, unrealistic
- **Too Dark:** Can't see details, muddy shadows
- **Blocky:** Geometry looks low-poly, faceted edges

---

## 💡 LIGHTING QUALITY

### ✅ CORRECT
- **Platform:** Can see concrete texture, not pure white
- **Emissive Lights (Signs/Lamps):** Glow subtly, not blinding
- **Soft Shadows:** Visible under benches and around objects
- **Ambient Fill:** All areas lit enough to see, no pitch black zones
- **Key Light (Directional):** Creates dimension, visible light direction
- **Bloom Glow:** Only around bright lights, doesn't spread to entire scene

### ❌ INCORRECT
- **Overexposed:** Platform is pure white, can't see texture
- **Nuclear Bloom:** Everything glowing, halos around all objects
- **No Shadows:** Flat lighting, objects don't feel grounded
- **Too Bright:** Scene looks like it's in a hospital, no mood
- **Too Dark:** Can barely see geometry, all details lost

### 🔍 Browser Console Check
```
[RenderDebug] Total Intensity: 1.35  ← Should be 1.2-1.5
[PostProcessing] Bloom: strength 0.4  ← Should be 0.3-0.5
[ThreeScene] Tone mapping exposure: 0.9  ← Should be 0.8-1.0
```

---

## 🎨 MATERIAL QUALITY

### ✅ CORRECT (PBR Materials)

**Metal (Frame, Trim, Light Posts):**
- [ ] Reflective surface (catches light highlights)
- [ ] Specular reflections visible (bright spots)
- [ ] Color has slight metallic tint
- [ ] Not flat gray (should have shine)

**Wood (Bench Seats/Backs):**
- [ ] Matte finish (low reflectivity)
- [ ] Warm brown/tan color visible
- [ ] Slight roughness texture (not perfectly smooth)
- [ ] Darker than metal (correct roughness)

**Concrete (Platform):**
- [ ] Light gray color
- [ ] Very rough surface (minimal shine)
- [ ] Texture variation visible
- [ ] Not reflective like metal

**Emissive (LED Signs, Light Bulbs):**
- [ ] Glowing from inside (emission visible)
- [ ] Color correct (golden/orange warm light)
- [ ] Bloom around edges (subtle glow)
- [ ] Not just a flat color (actual light emission)

**Glass (Light Housings):**
- [ ] Semi-transparent or reflective
- [ ] Shows environment reflections
- [ ] Emission visible through glass
- [ ] Not opaque solid

### ❌ INCORRECT (Material Issues)

**All Materials Look the Same:**
- Everything is flat gray (PBR not loading)
- No roughness variation (all shiny or all matte)
- No metallic surfaces (nothing reflects)

**Emissive Not Working:**
- Signs/lights are solid color (not glowing)
- No bloom effect around lights
- Lights don't illuminate surroundings

**Textures Missing:**
- All surfaces perfectly smooth
- No color variation
- Looks like clay model

### 🔍 Browser Console Check
```
[ThreeScene] ✓ Loaded 8 materials (4 emissive)  ← Should be > 0 materials, > 0 emissive
[RenderDebug] ✓ All materials verified  ← Should see this, not "Material Issues Detected"
```

---

## 🔷 GEOMETRY QUALITY

### ✅ CORRECT (Smooth Subdivision)

**Platform:**
- [ ] Edges are smoothly beveled (not sharp 90° corners)
- [ ] Top surface is slightly curved (subdivision working)
- [ ] Trim around edge is distinct separate element
- [ ] Can see depth/thickness

**Benches:**
- [ ] Wooden seat has rounded edges (not sharp rectangles)
- [ ] Metal legs are cylindrical (not octagonal/hexagonal)
- [ ] Seat and back have subtle curve (not perfectly flat)
- [ ] Legs connect smoothly to frame

**Light Posts:**
- [ ] Post is cylindrical (not polygonal)
- [ ] Light housing is spherical (smooth dome)
- [ ] No visible facets or flat sides
- [ ] Silhouette is smooth curve

**Signs:**
- [ ] Frame has beveled edges (not sharp)
- [ ] LED panel is inset (depth visible)
- [ ] Corners are rounded (subdivision applied)
- [ ] Frame and panel are distinct materials

### ❌ INCORRECT (Blocky Geometry)

**Platform:**
- Sharp 90° corners (no bevels)
- Perfectly flat (no subdivision)
- Edges look like Minecraft blocks

**Benches:**
- Seat is rectangular box (no rounding)
- Legs are hexagons/octagons (not cylinders)
- Everything has hard edges

**Light Posts:**
- Can count polygon sides (6-sided, 8-sided)
- Not smooth cylinders
- Light housing is geometric (not sphere)

**Overall:**
- Looks low-poly (like PS1 graphics)
- Visible polygon edges
- No smooth curves

### 🔍 Browser Console Check
```
[ThreeScene] 📐 Vertices: 25,000  ← Should be > 10,000 (subdivision applied)
[ThreeScene] 🔺 Triangles: 15,000  ← Should be > 5,000
[RenderDebug] ✓ All materials verified  ← Should NOT say "missing vertex normals"
```

---

## 🌟 POST-PROCESSING EFFECTS

### ✅ CORRECT

**Bloom (Glow Around Lights):**
- [ ] Subtle golden halo around LED signs
- [ ] Soft glow around light bulbs
- [ ] Bloom radius 2-3x light size
- [ ] Doesn't affect non-emissive objects
- [ ] Can still see platform texture clearly

**SSAO (Ambient Occlusion):**
- [ ] Darker areas where objects meet (bench legs on platform)
- [ ] Shadow under bench seats
- [ ] Corners and crevices are darker
- [ ] Adds depth and grounding

**SMAA (Anti-Aliasing):**
- [ ] Smooth edges (no jagged lines)
- [ ] Clean silhouettes against background
- [ ] No stair-stepping on diagonal lines

### ❌ INCORRECT

**Bloom Overload:**
- Everything glows (not just lights)
- Entire scene has white haze
- Can't see platform texture (washed out)
- Bloom bleeds 50%+ across screen

**No SSAO:**
- Objects float (no contact shadows)
- Flat lighting (no depth)
- Everything same brightness

**Aliasing Issues:**
- Jagged edges (stair-stepping)
- Diagonal lines look pixelated
- Flickering edges when camera moves

### 🔍 Browser Console Check
```
[PostProcessing] ✓ Bloom enabled (cinema-balanced)  ← Should see "cinema-balanced"
[PostProcessing] ✓ SSAO enabled  ← Should be present
[PostProcessing] ✓ SMAA anti-aliasing enabled  ← Should be present
```

---

## 📊 PERFORMANCE METRICS

### ✅ TARGET (60 FPS Smooth)
- Frame rate: 60 FPS (constant)
- Frame time: ~16ms
- Load time: < 3 seconds
- No stuttering during camera movement
- Smooth bloom/SSAO (no lag)

### ❌ NEEDS OPTIMIZATION
- Frame rate: < 30 FPS
- Stuttering/hitching
- Slow load times (> 10 seconds)
- Laggy post-processing

### 🔍 Browser Console Check
```
[ThreeScene] 🔺 Triangles: 15,000  ← Should be < 50,000 for hero asset
[ThreeScene] File size: 2.8 MB  ← Should be < 5 MB
```

---

## 🎯 QUICK DIAGNOSTIC STEPS

### Step 1: Check Lighting Intensity
1. Open browser console (F12)
2. Find: `[RenderDebug] Total Intensity:`
3. **CORRECT:** 1.2-1.5
4. **PROBLEM:** > 1.8 (too bright) or < 0.8 (too dark)

### Step 2: Verify Materials Loaded
1. Find: `[ThreeScene] ✓ Loaded X materials (Y emissive)`
2. **CORRECT:** X > 5, Y > 0
3. **PROBLEM:** X = 0 (materials failed to load)

### Step 3: Check Geometry Detail
1. Find: `[ThreeScene] 🔺 Triangles:`
2. **CORRECT:** > 10,000 (subdivision applied)
3. **PROBLEM:** < 5,000 (blocky geometry)

### Step 4: Verify Bloom Settings
1. Find: `[PostProcessing] Bloom enabled`
2. **CORRECT:** "cinema-balanced" in message
3. **PROBLEM:** No message or different text

---

## 🔧 COMMON FIXES

### Scene is Washed Out
```typescript
// In web/src/sceneConfig.ts
ambient: { intensity: 0.3 },      // Reduce from 0.4
directional: { intensity: 0.6 },  // Reduce from 0.8

// In web/src/postProcessing.ts
this.bloomPass.strength = 0.3;  // Reduce from 0.4
this.bloomPass.threshold = 0.9; // Raise from 0.88
```

### Scene is Too Dark
```typescript
// In web/src/sceneConfig.ts
ambient: { intensity: 0.5 },      // Increase from 0.4
directional: { intensity: 1.0 },  // Increase from 0.8

// In web/src/threeScene.ts
this.renderer.toneMappingExposure = 1.1; // Increase from 0.9
```

### Geometry is Blocky
```bash
# Regenerate GLB with updated Blender script
./regenerate_asset.sh station-home home
```

### Materials Not Loading
1. Check GLB in online viewer: https://gltf-viewer.donmccurdy.com/
2. Verify materials exist in Blender file
3. Re-export with `export_materials='EXPORT'`

### Bloom Too Strong
```typescript
// In web/src/postProcessing.ts
this.bloomPass.strength = 0.2;   // Reduce
this.bloomPass.radius = 0.8;     // Increase (smoother)
this.bloomPass.threshold = 0.92; // Raise (fewer objects bloom)
```

---

## ✨ FINAL VERIFICATION

### Your scene is cinema-quality when:
- [ ] All 5 lighting checks pass
- [ ] All 4 material types render correctly
- [ ] All 4 geometry smoothness checks pass
- [ ] All 3 post-processing effects visible
- [ ] Performance is 60 FPS
- [ ] Browser console shows NO errors
- [ ] Scene looks comparable to luxury brand website
- [ ] You would show this to a client with confidence

### If ANY check fails:
1. Review the specific section above
2. Check browser console for diagnostic output
3. Apply the suggested fix
4. Regenerate assets if needed
5. Re-test until all checks pass

---

**Remember:** Cinema-quality is about BALANCE, not extremes. Subtle bloom, balanced lighting, smooth geometry, and proper materials all working together.

**Comparison:**
- ❌ **Too Bright:** Like staring at the sun
- ❌ **Too Dark:** Like a cave
- ✅ **CORRECT:** Like a luxury hotel lobby (well-lit but not blinding)

---

**Visual Designer (Agent 3)**
*Your scene should make people stop scrolling and say "wow."*
