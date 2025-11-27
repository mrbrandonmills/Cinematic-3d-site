/**
 * Three.js Scene Manager
 * Handles 3D scene initialization, asset loading, and rendering
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { sceneConfig } from './sceneConfig';
import { PostProcessingManager } from './postProcessing';
import { RenderDebugger } from './utils/renderDebug';

export interface AssetMetadata {
  id: string;
  category: string;
  file: string;
  scale: [number, number, number];
  position: [number, number, number];
  rotation: [number, number, number];
  section: string;
  visibility?: {
    default?: boolean;
    fadeIn?: boolean;
    fadeOut?: boolean;
  };
  animation?: {
    type: string;
    params?: Record<string, any>;
  };
}

export class ThreeScene {
  public scene: THREE.Scene;
  public camera: THREE.PerspectiveCamera;
  public renderer: THREE.WebGLRenderer;
  private loader: GLTFLoader;
  private dracoLoader: DRACOLoader;
  private assets: Map<string, THREE.Object3D> = new Map();
  private clock: THREE.Clock;
  private postProcessing: PostProcessingManager | null = null;

  constructor(canvas: HTMLCanvasElement) {
    console.log('[ThreeScene] Constructing scene...');

    // Initialize scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x1a1a2e);
    console.log('[ThreeScene] Scene created');

    // Initialize camera
    const { fov, near, far, initialPosition } = sceneConfig.camera;
    this.camera = new THREE.PerspectiveCamera(
      fov,
      window.innerWidth / window.innerHeight,
      near,
      far
    );
    this.camera.position.set(...initialPosition);
    this.camera.lookAt(0, 0, 0);  // Look at origin where model will be
    console.log('[ThreeScene] Camera positioned at:', initialPosition);
    console.log('[ThreeScene] Camera looking at: (0, 0, 0)');

    // Initialize renderer with cinematic settings
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: false,  // SMAA will handle this
      alpha: false,
      powerPreference: 'high-performance',
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Cinematic rendering settings
    this.renderer.shadowMap.enabled = false; // Using baked lighting
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 0.9; // Balanced for cinema-quality (was 1.0)

    console.log('[ThreeScene] Tone mapping: ACESFilmic (cinematic, exposure: 0.9)');

    // Initialize loaders
    // Note: Draco decoder disabled for now (decoder files not in public/draco/)
    // Uncomment below to enable Draco compression support
    // this.dracoLoader = new DRACOLoader();
    // this.dracoLoader.setDecoderPath('/draco/');

    this.loader = new GLTFLoader();
    // this.loader.setDRACOLoader(this.dracoLoader);

    // Clock for animations
    this.clock = new THREE.Clock();

    // Setup lighting
    this.setupLighting();

    // Initialize cinematic post-processing
    try {
      this.postProcessing = new PostProcessingManager(this.renderer, this.scene, this.camera);
      console.log('[ThreeScene] ✓ Post-processing enabled');
    } catch (error) {
      console.warn('[ThreeScene] Post-processing failed, using standard rendering:', error);
    }

    // Handle resize
    window.addEventListener('resize', this.handleResize.bind(this));
  }

  private setupLighting(): void {
    const { ambient, directional } = sceneConfig.lighting;

    // Ambient light (soft fill)
    const ambientLight = new THREE.AmbientLight(ambient.color, ambient.intensity);
    this.scene.add(ambientLight);

    // Directional light (main key light)
    if (directional) {
      const dirLight = new THREE.DirectionalLight(
        directional.color,
        directional.intensity
      );
      dirLight.position.set(...directional.position);
      this.scene.add(dirLight);
    }

    // Optional: Add subtle hemisphere light for more natural look
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.15); // Reduced from 0.3
    this.scene.add(hemiLight);
    console.log('[ThreeScene] ✓ Lighting: Ambient(0.4) + Directional(0.8) + Hemisphere(0.15) = Balanced');
  }

  public async loadAsset(
    metadata: AssetMetadata,
    onProgress?: (progress: number) => void
  ): Promise<THREE.Object3D> {
    return new Promise((resolve, reject) => {
      const assetPath = `/assets/${metadata.file}`;
      console.log(`[ThreeScene] Loading asset from: ${assetPath}`);

      this.loader.load(
        assetPath,
        (gltf) => {
          console.log(`[ThreeScene] Successfully loaded: ${metadata.id}`, gltf);
          const model = gltf.scene;
          model.name = metadata.id;

          // Apply transformations from metadata
          model.position.set(...metadata.position);
          model.scale.set(...metadata.scale);
          model.rotation.set(...metadata.rotation);

          // Set initial visibility
          if (metadata.visibility?.default !== undefined) {
            model.visible = metadata.visibility.default;
          }

          // Traverse and optimize (keep Blender materials intact!)
          let materialCount = 0;
          let emissiveCount = 0;
          model.traverse((child) => {
            if ((child as THREE.Mesh).isMesh) {
              const mesh = child as THREE.Mesh;

              // CRITICAL: Enable smooth shading for subdivision surfaces
              mesh.geometry.computeVertexNormals();

              // Disable shadows (using baked lighting)
              mesh.castShadow = false;
              mesh.receiveShadow = false;

              // Keep original materials - they're already optimized from Blender
              if (mesh.material) {
                const mat = mesh.material as THREE.MeshStandardMaterial;
                mat.needsUpdate = true;
                materialCount++;

                // Log material properties for debugging
                if (mat.emissive && mat.emissive.getHex() !== 0x000000) {
                  emissiveCount++;
                  console.log(`[ThreeScene] Emissive material found: ${mat.name}, strength: ${mat.emissiveIntensity}`);
                }
              }
            }
          });

          console.log(`[ThreeScene] ✓ Loaded ${materialCount} materials (${emissiveCount} emissive)`);

          // Run diagnostic on first asset load
          if (this.assets.size === 0) {
            console.log('[ThreeScene] Running cinema-quality diagnostic on first asset...');
            RenderDebugger.analyzeModel(model);
            RenderDebugger.fullDiagnostic(this.renderer, this.scene, this.camera);
          }

          // Store reference
          this.assets.set(metadata.id, model);

          // Add to scene
          this.scene.add(model);
          console.log('[ThreeScene] Model added to scene at position:', model.position);
          console.log('[ThreeScene] Model children count:', model.children.length);
          console.log('[ThreeScene] Model visible:', model.visible);
          console.log('[ThreeScene] Scene total objects:', this.scene.children.length);

          resolve(model);
        },
        (progress) => {
          if (onProgress) {
            const percentComplete = (progress.loaded / progress.total) * 100;
            onProgress(percentComplete);
          }
        },
        (error) => {
          console.error(`[ThreeScene] FAILED to load asset ${metadata.id}:`, error);
          console.error('[ThreeScene] Error details:', {
            path: `/assets/${metadata.file}`,
            metadata,
            error
          });
          reject(error);
        }
      );
    });
  }

  public async loadAllAssets(
    metadataList: AssetMetadata[],
    onProgress?: (assetId: string, progress: number) => void
  ): Promise<void> {
    const loadPromises = metadataList.map((metadata) =>
      this.loadAsset(metadata, (progress) => {
        if (onProgress) {
          onProgress(metadata.id, progress);
        }
      })
    );

    await Promise.all(loadPromises);
  }

  public getAsset(id: string): THREE.Object3D | undefined {
    return this.assets.get(id);
  }

  public setAssetVisibility(id: string, visible: boolean): void {
    const asset = this.assets.get(id);
    if (asset) {
      asset.visible = visible;
    }
  }

  public render(): void {
    if (this.postProcessing) {
      this.postProcessing.render();
    } else {
      this.renderer.render(this.scene, this.camera);
    }
  }

  public animate(callback?: (delta: number) => void): void {
    const animate = () => {
      requestAnimationFrame(animate);

      const delta = this.clock.getDelta();

      // User callback for custom animations
      if (callback) {
        callback(delta);
      }

      this.render();
    };

    animate();
  }

  private handleResize(): void {
    // Update camera aspect ratio
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();

    // Update renderer size
    this.renderer.setSize(window.innerWidth, window.innerHeight);

    // Update post-processing
    if (this.postProcessing) {
      this.postProcessing.setSize(window.innerWidth, window.innerHeight);
    }
  }

  public dispose(): void {
    // Clean up resources
    this.renderer.dispose();
    if (this.dracoLoader) {
      this.dracoLoader.dispose();
    }

    // Dispose post-processing
    if (this.postProcessing) {
      this.postProcessing.dispose();
    }

    // Remove resize listener
    window.removeEventListener('resize', this.handleResize.bind(this));

    // Dispose assets
    this.assets.forEach((asset) => {
      asset.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          mesh.geometry?.dispose();

          if (Array.isArray(mesh.material)) {
            mesh.material.forEach((mat) => mat.dispose());
          } else {
            mesh.material?.dispose();
          }
        }
      });
    });

    this.assets.clear();
  }
}

export default ThreeScene;
