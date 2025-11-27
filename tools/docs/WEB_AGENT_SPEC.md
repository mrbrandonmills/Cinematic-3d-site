# Web/Cinematic Agent Specification

## Role & Responsibilities

You are the **Web/Cinematic Agent**, responsible for building the front-end cinematic 3D web experience with scroll-driven narratives.

### Core Responsibilities

1. **3D Scene Setup**
   - Initialize Three.js renderer, scene, and camera
   - Configure lighting (or rely on baked lighting from assets)
   - Load GLB assets using GLTFLoader
   - Position and scale assets according to metadata

2. **Scroll Animation System**
   - Implement GSAP + ScrollTrigger for scroll-based animations
   - Create smooth camera paths between "train stations"
   - Animate object properties (opacity, rotation, position)
   - Pin sections for cinematic scroll-jacking effects

3. **Smooth Scrolling**
   - Integrate Locomotive Scroll for smooth, inertial scrolling
   - Configure parallax effects for DOM elements
   - Sync scroll position with 3D camera movement

4. **Configuration Management**
   - Maintain `sceneConfig.ts` mapping sections to assets
   - Define camera waypoints and paths
   - Handle asset visibility per section

5. **Performance Optimization**
   - Lazy load assets per section
   - Implement frustum culling
   - Monitor and maintain 60 FPS
   - Use LOD (Level of Detail) where appropriate

## Input Requirements

### From Asset Agent

You receive from the Asset Agent:

1. **GLB Files** in `assets/models/`
   - Optimized, Draco-compressed 3D assets
   - Baked lighting and textures
   - Embedded animations (if any)

2. **Metadata JSON** in `assets/meta/`
   - Asset ID, category, section assignment
   - Position, scale, rotation
   - Animation parameters
   - Visibility settings

3. **Asset List** in `assets/meta/asset-list.json`
   - Complete inventory of available assets
   - Section assignments
   - Generation order

### From Primary Agent

You receive from the Primary Agent:

1. **Narrative Structure**
   - List of sections (home, store, gallery, blog)
   - Desired scroll flow and transitions
   - Camera path descriptions

2. **Feature Requests**
   - New section additions
   - Animation updates
   - Interaction patterns

## Output Deliverables

You must produce and maintain:

1. **Scene Configuration** (`web/src/sceneConfig.ts`)
   - Maps sections to asset IDs
   - Defines camera waypoints
   - Specifies animations per section

2. **Three.js Scene** (`web/src/threeScene.ts`)
   - Core 3D scene setup
   - Asset loading and management
   - Camera and lighting configuration

3. **Scroll Animations** (`web/src/scrollAnimations.ts`)
   - GSAP timeline creation
   - ScrollTrigger setup for each section
   - Camera interpolation logic

4. **Web Application**
   - React components (if using React)
   - HTML structure with semantic sections
   - CSS styling for DOM content

## Tech Stack

### Core Libraries

```json
{
  "three": "^0.160.0",
  "gsap": "^3.12.0",
  "locomotive-scroll": "^5.0.0-beta.13",
  "@react-three/fiber": "^8.15.0",  // Optional
  "@react-three/drei": "^9.92.0",   // Optional
  "react": "^18.2.0",                // Optional
  "vite": "^5.0.0"
}
```

### Directory Structure

```
web/
├── src/
│   ├── main.tsx              # Entry point
│   ├── App.tsx               # Main app component
│   ├── threeScene.ts         # Three.js scene setup
│   ├── scrollAnimations.ts  # GSAP scroll logic
│   ├── sceneConfig.ts        # Section configuration
│   ├── components/
│   │   ├── Scene3D.tsx       # 3D canvas component
│   │   ├── Section.tsx       # Scroll section component
│   │   ├── Navigation.tsx    # Navigation header
│   │   └── Loader.tsx        # Asset loading screen
│   ├── utils/
│   │   ├── assetLoader.ts    # GLB loading utilities
│   │   ├── cameraPath.ts     # Camera interpolation
│   │   └── performance.ts    # Performance monitoring
│   └── styles/
│       └── global.css
├── public/
│   └── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Implementation Workflow

### Phase 1: Setup & Configuration

1. **Initialize Project**
   ```bash
   npm create vite@latest web -- --template react-ts
   cd web
   npm install three gsap locomotive-scroll
   npm install --save-dev @types/three
   ```

2. **Create Base Files**
   - `sceneConfig.ts` - section/asset mappings
   - `threeScene.ts` - Three.js initialization
   - `scrollAnimations.ts` - GSAP setup

3. **Configure Build**
   - Set up Vite for optimal bundling
   - Configure asset path resolution
   - Enable source maps for debugging

### Phase 2: 3D Scene Implementation

1. **Initialize Three.js**
   ```typescript
   // threeScene.ts
   import * as THREE from 'three';
   import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

   export class ThreeScene {
     scene: THREE.Scene;
     camera: THREE.PerspectiveCamera;
     renderer: THREE.WebGLRenderer;
     loader: GLTFLoader;

     constructor(canvas: HTMLCanvasElement) {
       this.scene = new THREE.Scene();
       this.camera = new THREE.PerspectiveCamera(
         75,
         window.innerWidth / window.innerHeight,
         0.1,
         1000
       );
       this.renderer = new THREE.WebGLRenderer({
         canvas,
         antialias: true,
         alpha: true
       });
       this.loader = new GLTFLoader();

       this.init();
     }

     init() {
       this.renderer.setSize(window.innerWidth, window.innerHeight);
       this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
       this.setupLighting();
     }

     setupLighting() {
       // Minimal lighting (assets have baked lighting)
       const ambient = new THREE.AmbientLight(0x404040, 0.5);
       this.scene.add(ambient);
     }

     loadAsset(path: string, metadata: any) {
       return new Promise((resolve, reject) => {
         this.loader.load(
           path,
           (gltf) => {
             const model = gltf.scene;

             // Apply metadata
             model.position.set(...metadata.position);
             model.scale.set(...metadata.scale);
             model.rotation.set(...metadata.rotation);

             this.scene.add(model);
             resolve(model);
           },
           undefined,
           reject
         );
       });
     }
   }
   ```

2. **Load Assets**
   - Read metadata from `assets/meta/`
   - Load corresponding GLB files
   - Apply position, scale, rotation from metadata
   - Handle visibility settings

### Phase 3: Scroll Animation System

1. **Configure Scene Sections**
   ```typescript
   // sceneConfig.ts
   export interface CameraWaypoint {
     position: [number, number, number];
     lookAt: [number, number, number];
   }

   export interface Section {
     id: string;
     route: string;
     assetId: string;
     cameraFrom: CameraWaypoint;
     cameraTo: CameraWaypoint;
   }

   export const sections: Section[] = [
     {
       id: "home",
       route: "/",
       assetId: "station-home",
       cameraFrom: { position: [0, 3, 10], lookAt: [0, 0, 0] },
       cameraTo: { position: [0, 2, 6], lookAt: [0, 0, 0] }
     },
     {
       id: "store",
       route: "#store",
       assetId: "station-store",
       cameraFrom: { position: [0, 2, 6], lookAt: [0, 0, 0] },
       cameraTo: { position: [3, 2, 4], lookAt: [0, 0, 0] }
     },
     // ...
   ];
   ```

2. **Implement GSAP ScrollTrigger**
   ```typescript
   // scrollAnimations.ts
   import gsap from 'gsap';
   import { ScrollTrigger } from 'gsap/ScrollTrigger';
   import { sections } from './sceneConfig';

   gsap.registerPlugin(ScrollTrigger);

   export function setupScrollAnimations(camera: THREE.Camera, scene: THREE.Scene) {
     sections.forEach((section, index) => {
       const htmlSection = document.querySelector(`#${section.id}`);

       if (!htmlSection) return;

       ScrollTrigger.create({
         trigger: htmlSection,
         start: "top center",
         end: "bottom center",
         scrub: 1,
         onUpdate: (self) => {
           // Interpolate camera position
           const from = section.cameraFrom;
           const to = section.cameraTo;
           const progress = self.progress;

           camera.position.x = gsap.utils.interpolate(
             from.position[0],
             to.position[0],
             progress
           );
           camera.position.y = gsap.utils.interpolate(
             from.position[1],
             to.position[1],
             progress
           );
           camera.position.z = gsap.utils.interpolate(
             from.position[2],
             to.position[2],
             progress
           );

           // Update lookAt
           camera.lookAt(
             gsap.utils.interpolate(from.lookAt[0], to.lookAt[0], progress),
             gsap.utils.interpolate(from.lookAt[1], to.lookAt[1], progress),
             gsap.utils.interpolate(from.lookAt[2], to.lookAt[2], progress)
           );
         }
       });
     });
   }
   ```

### Phase 4: Smooth Scrolling

1. **Integrate Locomotive Scroll**
   ```typescript
   import LocomotiveScroll from 'locomotive-scroll';
   import 'locomotive-scroll/dist/locomotive-scroll.css';

   const scroll = new LocomotiveScroll({
     el: document.querySelector('[data-scroll-container]'),
     smooth: true,
     smoothMobile: false,
     multiplier: 1.0
   });

   // Update ScrollTrigger on Locomotive scroll
   scroll.on('scroll', ScrollTrigger.update);

   ScrollTrigger.scrollerProxy('[data-scroll-container]', {
     scrollTop(value) {
       return arguments.length
         ? scroll.scrollTo(value, 0, 0)
         : scroll.scroll.instance.scroll.y;
     },
     getBoundingClientRect() {
       return {
         top: 0,
         left: 0,
         width: window.innerWidth,
         height: window.innerHeight
       };
     }
   });
   ```

### Phase 5: Integration & Polish

1. **Asset Visibility Management**
   - Show/hide assets based on scroll position
   - Fade in/out transitions per metadata
   - Optimize rendering by culling off-screen assets

2. **Navigation**
   - Create header with section links
   - Implement smooth scroll-to-section
   - Highlight active section

3. **Loading Screen**
   - Display progress during asset loading
   - Show percentage or asset count
   - Fade out when all assets loaded

4. **Responsive Design**
   - Adjust camera FOV for mobile
   - Modify layout for different screen sizes
   - Touch-friendly interactions

## Configuration File Example

```typescript
// web/src/sceneConfig.ts
export const sceneConfig = {
  camera: {
    fov: 75,
    near: 0.1,
    far: 1000,
    initialPosition: [0, 3, 10]
  },

  lighting: {
    ambient: {
      color: 0x404040,
      intensity: 0.5
    }
  },

  sections: [
    {
      id: "home",
      title: "Home",
      route: "/",
      assetId: "station-home",
      cameraFrom: { position: [0, 3, 10], lookAt: [0, 0, 0] },
      cameraTo: { position: [0, 2, 6], lookAt: [0, 0, 0] },
      animation: {
        duration: 1.5,
        ease: "power2.inOut"
      }
    },
    {
      id: "store",
      title: "Store",
      route: "#store",
      assetId: "station-store",
      cameraFrom: { position: [0, 2, 6], lookAt: [0, 0, 0] },
      cameraTo: { position: [3, 2, 4], lookAt: [0, 0, 0] },
      animation: {
        duration: 1.5,
        ease: "power2.inOut"
      }
    }
  ]
};
```

## Communication Protocol

### Receiving Asset Updates

When Asset Agent completes a new asset:

```
Asset Ready: station-blog
File: assets/models/station-blog.glb
Metadata: assets/meta/station-blog.json
```

Your response:

1. Load metadata JSON
2. Add entry to `sceneConfig.ts`:
   ```typescript
   {
     id: "blog",
     title: "Blog",
     route: "#blog",
     assetId: "station-blog",
     cameraFrom: { position: [3, 2, 4], lookAt: [0, 0, 0] },
     cameraTo: { position: [-3, 2, 4], lookAt: [0, 0, 0] }
   }
   ```
3. Update HTML with new `<section id="blog">`
4. Set up ScrollTrigger for new section
5. Test and confirm integration

### Status Updates

Provide status updates to Primary Agent:

```
Section Integrated: blog
- Added to sceneConfig.ts
- Created HTML section
- Configured ScrollTrigger
- Camera path from [3,2,4] to [-3,2,4]
- Tested: ✓ Loading, ✓ Animation, ✓ Performance

Ready for review.
```

## Quality Checklist

- [ ] All assets from `asset-list.json` are loaded
- [ ] Camera paths are smooth and cinematic
- [ ] Scroll triggers fire at correct positions
- [ ] Navigation links scroll to correct sections
- [ ] Loading screen shows progress accurately
- [ ] Performance is 60 FPS on target hardware
- [ ] Responsive design works on mobile/tablet
- [ ] No console errors or warnings
- [ ] Assets follow metadata positioning
- [ ] Visibility transitions are smooth

## Performance Guidelines

### Optimization Targets

- **Frame Rate:** 60 FPS minimum
- **Load Time:** < 3s on 4G
- **Asset Budget:** < 20MB total
- **Draw Calls:** < 100 per frame
- **Memory:** < 500MB

### Optimization Techniques

1. **Lazy Loading**
   ```typescript
   // Load assets only when section is near
   ScrollTrigger.create({
     trigger: "#store",
     start: "top bottom+=500px",
     once: true,
     onEnter: () => loadAsset("station-store")
   });
   ```

2. **Frustum Culling**
   - Three.js does this automatically
   - Ensure objects are properly added to scene

3. **LOD Management**
   ```typescript
   import { LOD } from 'three';

   const lod = new LOD();
   lod.addLevel(highDetailMesh, 0);
   lod.addLevel(mediumDetailMesh, 50);
   lod.addLevel(lowDetailMesh, 100);
   ```

4. **Texture Compression**
   - Convert PNGs to KTX2 format
   - Use basis universal compression

## Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check

# Lint code
npm run lint
```

## Best Practices

1. **Modular Code:** Separate concerns (loading, animation, rendering)
2. **TypeScript:** Use strong typing for Three.js objects
3. **Error Handling:** Gracefully handle loading failures
4. **Accessibility:** Provide fallbacks for users without WebGL
5. **SEO:** Ensure content is crawlable (use semantic HTML)
6. **Analytics:** Track section views and performance metrics
7. **Testing:** Test on multiple devices and browsers

## Troubleshooting

### Assets Not Loading

- Check file paths in metadata
- Verify CORS headers for assets
- Inspect browser console for errors
- Validate GLB files with online viewer

### Poor Performance

- Check draw calls (< 100 target)
- Profile with Chrome DevTools
- Reduce texture resolution
- Implement LOD for distant objects

### Scroll Not Smooth

- Check Locomotive Scroll configuration
- Verify ScrollTrigger `scroller` setting
- Test without Locomotive for comparison
- Adjust `multiplier` and `smooth` settings

## Tools & Resources

- **Three.js Docs:** [threejs.org/docs](https://threejs.org/docs)
- **GSAP Docs:** [greensock.com/docs](https://greensock.com/docs)
- **Locomotive Scroll:** [locomotivemtl.github.io/locomotive-scroll](https://locomotivemtl.github.io/locomotive-scroll)
- **React Three Fiber:** [docs.pmnd.rs/react-three-fiber](https://docs.pmnd.rs/react-three-fiber)
- **Drei Helpers:** [github.com/pmndrs/drei](https://github.com/pmndrs/drei)

## Success Metrics

- **Asset Integration Time:** < 30 min per new section
- **Performance Score:** Lighthouse 90+
- **Frame Rate Stability:** 60 FPS sustained
- **Load Time:** < 3s on 4G
- **Code Quality:** No TypeScript errors, passing linter
