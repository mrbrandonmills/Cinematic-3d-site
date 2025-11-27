# Cinematic 3D Site - Award-Winning Standards

**Project Type:** Cinema-Quality 3D Web Experience
**Standards:** Awwwards Site of the Day, FWA, CSS Design Awards Eligible
**Quality Level:** Museum-Grade, Industry-Leading, Revolutionary
**Date:** November 27, 2025

---

## 🏆 PROJECT VISION

Build a **revolutionary 3D web experience** that sets new industry standards and is eligible for:

- **Awwwards** - Site of the Day / Developer Award / Site of the Year
- **FWA** - Favourite Website Awards
- **CSS Design Awards** - Website of the Day
- **Webby Awards** - Best Visual Design
- **The One Show** - Interactive Design

**Benchmark Studios:**
- Active Theory (activetheory.net)
- Resn (resn.co.nz)
- UNIT9 (unit9.com)
- Locomotive (locomotive.ca)
- Aristide Benoist (aristidebenoist.com)

**Benchmark Sites:**
- Bruno Simon's Portfolio (bruno-simon.com)
- Gucci's Virtual 25 (25.gucci.com)
- Oat Foundry (oatfoundry.com)
- Aristide Benoist (aristidebenoist.com)

---

## 🎯 CORE PRINCIPLES

### 1. **Cinema-Quality Rendering**
- Custom GLSL shaders (vertex + fragment)
- Advanced post-processing (grain, chromatic aberration, bloom, vignette)
- Physically-based rendering (PBR) with real-time reflections
- Dynamic lighting with shadow mapping
- Ambient occlusion (SSAO/HBAO)
- Lens flares and light scattering
- Color grading and LUT support

### 2. **Performance Excellence**
- **Lighthouse Score:** 100/100 (Performance, Accessibility, Best Practices, SEO)
- **60 FPS minimum** on mid-range devices (M1 MacBook Air baseline)
- **90 FPS target** on high-end devices
- **Initial Load:** < 2 seconds on 4G
- **Total Budget:** < 10MB compressed assets
- **WebGL Draw Calls:** < 50 per frame
- **Memory Usage:** < 300MB

### 3. **Accessibility First**
- **WCAG AAA** compliance (Level AAA, not just AA)
- Keyboard navigation fully supported
- Screen reader optimized (ARIA labels, semantic HTML)
- Reduced motion support (prefers-reduced-motion)
- High contrast mode support
- Focus indicators and skip links
- Alt text for all visual content
- Captions for audio/video

### 4. **Progressive Enhancement**
- Mobile-first responsive design
- Touch-optimized interactions
- Graceful degradation for older browsers
- WebGL 1.0 fallback for unsupported devices
- Static fallback for no-JS environments
- Service Worker for offline capability

### 5. **Interaction Design**
- Custom cursor with physics (magnetic, elastic)
- Micro-interactions on every element (hover, click, focus)
- Sound design integration (spatial audio, UI sounds)
- Physics-based interactions (drag, throw, collision)
- Gesture support (pinch, swipe, rotate on mobile)
- Haptic feedback on supported devices

---

## 🛠️ TECHNOLOGY STACK - AWARD-WINNING GRADE

### **Core Technologies**

**3D Engine:**
- ✅ **Three.js 0.181.2** - Latest WebGL library
- ✅ **GLSL Shaders** - Custom vertex/fragment shaders
- ✅ **Post-processing** - Custom effects stack
- ✅ **Physics** - Cannon.js or Rapier (WASM)

**Animation & Interaction:**
- ✅ **GSAP 3.13.0** - Professional animation library
- ✅ **Lenis** - Smooth scroll (replaces Locomotive Scroll - more modern)
- ✅ **Theatre.js** - Animation sequencing and timeline editor
- ✅ **Framer Motion** - React animation library

**Frontend Framework:**
- ✅ **React 19.2.0** - Latest with Server Components
- ✅ **Next.js 15** - App Router, Server Actions, streaming
- ✅ **TypeScript 5.7** - Strict mode, full type safety
- ✅ **Tailwind CSS 4.0** - Utility-first CSS

**Build & Performance:**
- ✅ **Vite 6.x** / **Turbopack** - Ultra-fast bundling
- ✅ **SWC** - Rust-based compiler (faster than Babel)
- ✅ **Sharp** - Image optimization
- ✅ **Partytown** - Web Worker for 3rd-party scripts

**Audio:**
- ✅ **Howler.js** - Spatial audio and sound management
- ✅ **Tone.js** - Interactive music and synthesis

**Quality Assurance:**
- ✅ **Playwright** - E2E testing
- ✅ **Vitest** - Unit testing (faster than Jest)
- ✅ **Storybook 8** - Component development
- ✅ **Chromatic** - Visual regression testing

---

## 📐 ARCHITECTURE - REVOLUTIONARY DESIGN

### **Agent Team - Award-Winning Specialists**

```
PRIMARY ORCHESTRATOR (You - Award-Winning Director)
│
├─ 🎨 VISUAL EXCELLENCE DIVISION
│  ├─ shader-artist (Custom GLSL, effects)
│  ├─ lighting-cinematographer (Cinema-grade lighting)
│  ├─ material-scientist (Advanced PBR materials)
│  └─ post-processing-master (Grain, CA, bloom, vignette)
│
├─ 🏗️ TECHNICAL EXCELLENCE DIVISION
│  ├─ webgl-performance-wizard (60-90 FPS optimization)
│  ├─ blender-automation-architect (Procedural generation)
│  ├─ asset-optimization-specialist (< 10MB budget)
│  └─ rendering-pipeline-engineer (Draw call optimization)
│
├─ 🎭 INTERACTION DESIGN DIVISION
│  ├─ animation-choreographer (GSAP timelines)
│  ├─ physics-engineer (Realistic interactions)
│  ├─ sound-designer (Spatial audio, UI sounds)
│  └─ cursor-interaction-specialist (Custom cursor physics)
│
├─ ♿ ACCESSIBILITY & QUALITY DIVISION
│  ├─ accessibility-advocate (WCAG AAA compliance)
│  ├─ performance-auditor (Lighthouse 100 enforcer)
│  ├─ seo-specialist (Core Web Vitals optimization)
│  └─ qa-automation-engineer (Playwright testing)
│
└─ 🚀 DEPLOYMENT & DEVOPS DIVISION
   ├─ build-optimization-engineer (Bundle size < 500KB)
   ├─ cdn-architect (Edge caching, streaming)
   ├─ monitoring-specialist (Real-user monitoring)
   └─ ci-cd-pipeline-engineer (Automated deployment)
```

---

## 🎬 AWARD-WORTHY FEATURES

### **Must-Have Features for Award Submission:**

#### **Visual Excellence**
- [ ] Custom GLSL shaders (at least 3 unique effects)
- [ ] Real-time reflections (screen-space or cube maps)
- [ ] Dynamic shadows (shadow mapping)
- [ ] Volumetric lighting (god rays)
- [ ] Particle systems (GPU-accelerated)
- [ ] Procedural textures (noise, patterns)
- [ ] Color grading with LUTs
- [ ] Film grain and chromatic aberration
- [ ] Depth of field (DOF) effects
- [ ] Motion blur (per-object or camera-based)

#### **Interaction Design**
- [ ] Custom physics-based cursor (magnetic, elastic)
- [ ] Drag-and-throw interactions
- [ ] Object collision detection
- [ ] Gesture support (mobile: pinch, swipe, rotate)
- [ ] Haptic feedback (supported devices)
- [ ] Sound effects for all interactions
- [ ] Micro-animations on hover (every element)
- [ ] Loading progress with animation
- [ ] Page transitions (smooth, cinematic)
- [ ] Easter eggs (hidden interactions)

#### **Performance & Accessibility**
- [ ] Lighthouse 100/100/100/100 score
- [ ] 60 FPS minimum (90 FPS target)
- [ ] < 2s initial load on 4G
- [ ] WCAG AAA compliance
- [ ] Keyboard navigation (every feature)
- [ ] Screen reader optimized
- [ ] Reduced motion support
- [ ] High contrast mode
- [ ] Service Worker (offline capability)
- [ ] Progressive Web App (PWA)

#### **Technical Innovation**
- [ ] WebGL 2.0 with fallback to 1.0
- [ ] Web Workers for heavy computation
- [ ] WASM for physics (Rapier)
- [ ] Streaming assets (progressive loading)
- [ ] Adaptive quality (based on device)
- [ ] GPU instancing for performance
- [ ] Frustum culling optimization
- [ ] LOD system (3+ levels)
- [ ] Texture compression (KTX2, Basis)
- [ ] Brotli/Gzip compression

---

## 📊 PERFORMANCE BUDGETS - STRICT ENFORCEMENT

### **Asset Budgets**
| Asset Type | Max Size | Max Poly Count | Format |
|------------|----------|----------------|--------|
| Hero Model | 2MB compressed | 30,000 triangles | GLB (Draco 7) + KTX2 |
| Environment | 1MB compressed | 15,000 triangles | GLB (Draco 7) + KTX2 |
| Prop | 500KB compressed | 5,000 triangles | GLB (Draco 7) + KTX2 |
| Texture | 500KB compressed | 2048x2048 max | KTX2 (Basis Universal) |
| Audio | 100KB compressed | 30s max | OGG/WebM Opus |

**Total Asset Budget:** < 10MB (compressed)

### **JavaScript Bundle Budgets**
| Bundle | Max Size | Notes |
|--------|----------|-------|
| Initial JS | 300KB (gzipped) | Critical path only |
| Vendor | 200KB (gzipped) | React, Three.js, GSAP |
| Route Chunk | 100KB (gzipped) | Per-route code splitting |
| Total JS | 500KB (gzipped) | All JavaScript combined |

### **Performance Metrics (Lighthouse 100 Target)**
| Metric | Target | Notes |
|--------|--------|-------|
| First Contentful Paint (FCP) | < 1.0s | When content first appears |
| Largest Contentful Paint (LCP) | < 1.5s | Main content loaded |
| Time to Interactive (TTI) | < 2.5s | Fully interactive |
| Total Blocking Time (TBT) | < 100ms | Main thread blocking |
| Cumulative Layout Shift (CLS) | < 0.05 | Visual stability |
| Speed Index | < 1.5s | Visual completion |

---

## 🎨 VISUAL QUALITY STANDARDS

### **Cinema-Grade Rendering Checklist**

**Lighting:**
- [ ] Three-point lighting (key, fill, rim)
- [ ] HDRI environment maps
- [ ] Real-time shadows (PCF or VSM)
- [ ] Ambient occlusion (SSAO or HBAO)
- [ ] Light probes for global illumination
- [ ] Emissive materials with bloom
- [ ] Dynamic time-of-day lighting (optional)

**Materials (PBR):**
- [ ] Metallic-roughness workflow
- [ ] Normal maps for detail
- [ ] Ambient occlusion maps
- [ ] Emissive maps for lights
- [ ] Alpha transparency where needed
- [ ] Clearcoat for multi-layer materials
- [ ] Subsurface scattering (skin, wax)

**Post-Processing Stack:**
```glsl
1. SSAO (Screen-Space Ambient Occlusion)
2. Bloom (Unreal/Kawase algorithm)
3. Chromatic Aberration (lens distortion)
4. Vignette (darkened edges)
5. Film Grain (noise texture)
6. Color Grading (LUT-based)
7. SMAA (Anti-aliasing)
8. Depth of Field (bokeh effect)
9. Motion Blur (velocity-based)
10. Lens Flares (selective)
```

---

## ♿ ACCESSIBILITY STANDARDS - WCAG AAA

### **Mandatory Requirements:**

**Keyboard Navigation:**
- [ ] Tab navigation for all interactive elements
- [ ] Focus indicators (visible, high contrast)
- [ ] Skip links (skip to content, skip to nav)
- [ ] Escape key closes modals/overlays
- [ ] Arrow keys for carousels/galleries
- [ ] Enter/Space for buttons

**Screen Reader Support:**
- [ ] ARIA labels on all interactive elements
- [ ] ARIA live regions for dynamic content
- [ ] Semantic HTML (header, nav, main, footer)
- [ ] Alt text for all images (descriptive)
- [ ] Role attributes where needed
- [ ] ARIA expanded/collapsed states

**Reduced Motion:**
- [ ] Detect `prefers-reduced-motion`
- [ ] Disable scroll animations if preferred
- [ ] Disable parallax effects if preferred
- [ ] Reduce/eliminate 3D camera movement
- [ ] Crossfade transitions instead of slides
- [ ] Respect user preferences

**Visual Accessibility:**
- [ ] Contrast ratio 7:1+ (AAA standard)
- [ ] Text resizable to 200% without breaking
- [ ] No color-only information
- [ ] Focus indicators never hidden
- [ ] Touch targets minimum 44x44px
- [ ] Readable fonts (16px+ body text)

---

## 🚀 DEPLOYMENT STRATEGY - PRODUCTION EXCELLENCE

### **Hosting Architecture**

**Recommended Stack:**
- **CDN:** Cloudflare (edge caching, DDoS protection)
- **Hosting:** Vercel (Next.js optimized, edge functions)
- **Assets:** Cloudflare R2 (S3-compatible, zero egress)
- **Analytics:** Vercel Analytics + Plausible (privacy-first)
- **Monitoring:** Sentry (error tracking) + LogRocket (session replay)

**Optimization Pipeline:**
```
1. Build with Next.js 15 (App Router)
2. Compress assets (Brotli + Gzip)
3. Generate image variants (Sharp)
4. Create service worker (Workbox)
5. Deploy to Vercel Edge Network
6. Cache static assets on Cloudflare CDN
7. Enable streaming for HTML
8. Preload critical resources
9. Lazy load below-fold content
10. Monitor with Real User Monitoring (RUM)
```

---

## 📚 DOCUMENTATION STANDARDS

### **Required Documentation:**

1. **CLAUDE.md** (this file) - Project overview and standards
2. **README.md** - Setup instructions and quick start
3. **ARCHITECTURE.md** - System design and agent roles
4. **API.md** - Component API reference
5. **PERFORMANCE.md** - Performance budgets and optimization
6. **ACCESSIBILITY.md** - WCAG compliance documentation
7. **DEPLOYMENT.md** - Deployment and CI/CD pipeline
8. **CONTRIBUTING.md** - Code standards and PR process

### **Code Documentation:**
- TypeScript types for all functions
- JSDoc comments for complex logic
- Storybook stories for all components
- E2E tests for critical user flows
- Unit tests for utility functions
- Visual regression tests for UI

---

## 🎯 SUCCESS METRICS - AWARD SUBMISSION

### **Technical Excellence**
- [ ] Lighthouse 100/100/100/100 (all categories)
- [ ] 60 FPS sustained (90 FPS target)
- [ ] < 2s load time on 4G
- [ ] < 10MB total assets (compressed)
- [ ] WCAG AAA compliant
- [ ] Zero console errors/warnings
- [ ] 95+ PageSpeed score (mobile + desktop)

### **Visual Excellence**
- [ ] Custom GLSL shaders implemented
- [ ] Cinema-quality lighting
- [ ] Advanced post-processing stack
- [ ] Smooth animations (no jank)
- [ ] Responsive design (mobile-first)
- [ ] Comparable to Awwwards winners

### **Innovation & Creativity**
- [ ] Unique interaction design
- [ ] Physics-based interactions
- [ ] Sound design integration
- [ ] Easter eggs / hidden features
- [ ] Memorable user experience
- [ ] Industry-leading execution

### **Code Quality**
- [ ] TypeScript strict mode (zero `any`)
- [ ] 100% test coverage (critical paths)
- [ ] ESLint + Prettier configured
- [ ] Git hooks (Husky + lint-staged)
- [ ] Automated CI/CD pipeline
- [ ] Zero security vulnerabilities

---

## 🏆 AWARD SUBMISSION CHECKLIST

Before submitting to Awwwards/FWA/CSS Design Awards:

**Technical Audit:**
- [ ] Run Lighthouse CI (100/100/100/100)
- [ ] Test on 5+ devices (iOS, Android, Windows, Mac)
- [ ] Test on 3+ browsers (Chrome, Firefox, Safari)
- [ ] Verify all animations smooth (60 FPS)
- [ ] Check accessibility (keyboard, screen reader)
- [ ] Validate HTML/CSS (W3C validators)
- [ ] Security scan (no vulnerabilities)

**Visual Audit:**
- [ ] Compare to Awwwards winners
- [ ] Verify cinema-quality rendering
- [ ] Check micro-interactions (every element)
- [ ] Test custom cursor (physics, magnetic)
- [ ] Verify sound design integration
- [ ] Check loading animations
- [ ] Test page transitions

**Content Audit:**
- [ ] Case study prepared (design process)
- [ ] Screenshots (desktop + mobile)
- [ ] Video walkthrough (30-60s)
- [ ] Credits (team, tools used)
- [ ] Description (200-300 words)
- [ ] Tags/categories accurate
- [ ] Links working (demo, GitHub, etc.)

---

## 📞 AGENT INVOCATION PROTOCOL

### **When to Delegate:**

**For Visual Excellence:**
```typescript
Task({
  subagent_type: "luxury-visual-designer",
  description: "Create custom GLSL shader",
  prompt: "Design and implement a custom vertex + fragment shader for [effect]"
})
```

**For Performance Optimization:**
```typescript
Task({
  subagent_type: "react-developer",
  description: "Optimize to Lighthouse 100",
  prompt: "Profile and optimize performance to achieve Lighthouse 100/100 score"
})
```

**For Blender Asset Creation:**
```typescript
Task({
  subagent_type: "infrastructure-developer",
  description: "Generate award-winning 3D asset",
  prompt: "Create cinema-quality asset with < 30K polys, PBR materials, optimized for web"
})
```

**For Accessibility:**
```typescript
Task({
  subagent_type: "qa-engineer",
  description: "Implement WCAG AAA compliance",
  prompt: "Audit and implement WCAG AAA accessibility standards"
})
```

---

## 🎬 PHASE 2 NEXT STEPS

**Immediate Actions:**
1. Install latest dependencies (Three.js 0.181.2, GSAP 3.13.0, React 19.2.0, Next.js 15)
2. Configure TypeScript strict mode
3. Setup ESLint + Prettier + Husky
4. Create component library with Storybook
5. Setup Playwright for E2E testing
6. Configure performance monitoring
7. Implement accessibility audit workflow

**Development Workflow:**
1. Design in Blender (cinema-quality assets)
2. Optimize and export (< 2MB, Draco 7, KTX2 textures)
3. Build components in Storybook
4. Write E2E tests in Playwright
5. Profile performance (Lighthouse CI)
6. Audit accessibility (WCAG AAA)
7. Deploy to staging (Vercel preview)
8. Final QA and sign-off
9. Deploy to production
10. Submit to awards

---

## 🌟 INSPIRATION & REFERENCES

**Award-Winning Sites:**
- Bruno Simon's Portfolio - bruno-simon.com
- Gucci Virtual 25 - 25.gucci.com
- Aristide Benoist - aristidebenoist.com
- Oat Foundry - oatfoundry.com
- Active Theory - activetheory.net

**Technical Resources:**
- Three.js Journey (threejs-journey.com)
- WebGL Fundamentals (webglfundamentals.org)
- The Book of Shaders (thebookofshaders.com)
- Awwwards Collections (awwwards.com/collections)

---

**Status:** PHASE 2 - REVOLUTIONARY STANDARDS ESTABLISHED

**Next:** Install dependencies, configure tooling, begin award-worthy implementation

**Benchmark:** Every decision measured against Awwwards Site of the Year standards

🏆 **LET'S BUILD SOMETHING AWARD-WINNING** 🏆
