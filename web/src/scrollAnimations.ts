/**
 * Scroll Animations
 * GSAP + ScrollTrigger integration for camera paths and asset animations
 */

import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import * as THREE from 'three';
import { sceneConfig, SectionConfig } from './sceneConfig';

// Register GSAP plugin
gsap.registerPlugin(ScrollTrigger);

export interface ScrollAnimationOptions {
  camera: THREE.Camera;
  scene: THREE.Scene;
  locomotiveScroll?: any;
}

export class ScrollAnimations {
  private camera: THREE.Camera;
  private scene: THREE.Scene;
  private triggers: ScrollTrigger[] = [];

  constructor(options: ScrollAnimationOptions) {
    this.camera = options.camera;
    this.scene = options.scene;

    // Configure ScrollTrigger for Locomotive Scroll if provided
    if (options.locomotiveScroll) {
      this.configureLocomotiveIntegration(options.locomotiveScroll);
    }
  }

  private configureLocomotiveIntegration(locomotiveScroll: any): void {
    // Update ScrollTrigger on Locomotive scroll
    locomotiveScroll.on('scroll', ScrollTrigger.update);

    // Set up ScrollTrigger scroller proxy
    ScrollTrigger.scrollerProxy('[data-scroll-container]', {
      scrollTop(value?: number) {
        if (arguments.length) {
          locomotiveScroll.scrollTo(value, { duration: 0, disableLerp: true });
        }
        return locomotiveScroll.scroll.instance.scroll.y;
      },
      getBoundingClientRect() {
        return {
          top: 0,
          left: 0,
          width: window.innerWidth,
          height: window.innerHeight,
        };
      },
      pinType: document.querySelector('[data-scroll-container]')?.style.transform
        ? 'transform'
        : 'fixed',
    });

    // Refresh ScrollTrigger when Locomotive updates
    locomotiveScroll.on('scroll', () => {
      ScrollTrigger.update();
    });

    ScrollTrigger.addEventListener('refresh', () => locomotiveScroll.update());
    ScrollTrigger.refresh();
  }

  public setupSectionAnimations(): void {
    sceneConfig.sections.forEach((section, index) => {
      this.createSectionTrigger(section, index);
    });
  }

  private createSectionTrigger(section: SectionConfig, index: number): void {
    const htmlSection = document.querySelector(`#${section.id}`);

    if (!htmlSection) {
      console.warn(`Section element not found: #${section.id}`);
      return;
    }

    // Camera animation
    const trigger = ScrollTrigger.create({
      trigger: htmlSection,
      start: 'top center',
      end: 'bottom center',
      scrub: 1, // Smooth scrubbing
      onUpdate: (self) => {
        const progress = self.progress;
        this.interpolateCamera(section, progress);
      },
      onEnter: () => {
        console.log(`Entered section: ${section.id}`);
        this.onSectionEnter(section);
      },
      onLeave: () => {
        console.log(`Left section: ${section.id}`);
        this.onSectionLeave(section);
      },
      onEnterBack: () => {
        this.onSectionEnter(section);
      },
      onLeaveBack: () => {
        this.onSectionLeave(section);
      },
    });

    this.triggers.push(trigger);

    // Optional: Pin section for dramatic effect
    // Uncomment to enable scroll-jacking
    /*
    ScrollTrigger.create({
      trigger: htmlSection,
      start: 'top top',
      end: '+=100%',
      pin: true,
      pinSpacing: true,
    });
    */
  }

  private interpolateCamera(section: SectionConfig, progress: number): void {
    const { cameraFrom, cameraTo } = section;

    // Interpolate position
    this.camera.position.x = gsap.utils.interpolate(
      cameraFrom.position[0],
      cameraTo.position[0],
      progress
    );
    this.camera.position.y = gsap.utils.interpolate(
      cameraFrom.position[1],
      cameraTo.position[1],
      progress
    );
    this.camera.position.z = gsap.utils.interpolate(
      cameraFrom.position[2],
      cameraTo.position[2],
      progress
    );

    // Interpolate lookAt
    const lookAtX = gsap.utils.interpolate(
      cameraFrom.lookAt[0],
      cameraTo.lookAt[0],
      progress
    );
    const lookAtY = gsap.utils.interpolate(
      cameraFrom.lookAt[1],
      cameraTo.lookAt[1],
      progress
    );
    const lookAtZ = gsap.utils.interpolate(
      cameraFrom.lookAt[2],
      cameraTo.lookAt[2],
      progress
    );

    this.camera.lookAt(lookAtX, lookAtY, lookAtZ);
  }

  private onSectionEnter(section: SectionConfig): void {
    // Find corresponding asset in scene
    const asset = this.scene.getObjectByName(section.assetId);

    if (asset && asset.visible === false) {
      // Fade in asset
      gsap.to(asset, {
        visible: true,
        duration: 0.5,
        onStart: () => {
          asset.visible = true;
          if (asset.traverse) {
            asset.traverse((child) => {
              if ((child as THREE.Mesh).isMesh) {
                const mesh = child as THREE.Mesh;
                if (mesh.material) {
                  const mat = mesh.material as THREE.Material;
                  if ('opacity' in mat) {
                    (mat as any).transparent = true;
                    (mat as any).opacity = 0;
                  }
                }
              }
            });
          }
        },
      });

      asset.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          if (mesh.material) {
            const mat = mesh.material as THREE.Material;
            if ('opacity' in mat) {
              gsap.to(mat, {
                opacity: 1,
                duration: 0.5,
              });
            }
          }
        }
      });
    }
  }

  private onSectionLeave(section: SectionConfig): void {
    // Optional: Fade out asset
    const asset = this.scene.getObjectByName(section.assetId);

    if (asset) {
      // Keep visible but could fade out
      // Uncomment to enable fade out
      /*
      asset.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          if (mesh.material) {
            const mat = mesh.material as THREE.Material;
            if ('opacity' in mat) {
              gsap.to(mat, {
                opacity: 0.5,
                duration: 0.3,
              });
            }
          }
        }
      });
      */
    }
  }

  public animateAsset(assetId: string, animation: any): void {
    const asset = this.scene.getObjectByName(assetId);

    if (!asset) {
      console.warn(`Asset not found: ${assetId}`);
      return;
    }

    const { type, params } = animation;

    switch (type) {
      case 'idle':
        this.createIdleAnimation(asset, params);
        break;
      case 'loop':
        this.createLoopAnimation(asset, params);
        break;
      case 'scroll_triggered':
        this.createScrollTriggeredAnimation(asset, params);
        break;
      default:
        console.warn(`Unknown animation type: ${type}`);
    }
  }

  private createIdleAnimation(asset: THREE.Object3D, params: any): void {
    const { duration = 4, ease = 'sine.inOut', loop = true } = params;

    // Example: Subtle floating animation
    gsap.to(asset.position, {
      y: asset.position.y + 0.1,
      duration: duration,
      ease: ease,
      repeat: loop ? -1 : 0,
      yoyo: true,
    });

    // Example: Gentle rotation
    gsap.to(asset.rotation, {
      y: asset.rotation.y + Math.PI * 0.1,
      duration: duration * 2,
      ease: ease,
      repeat: loop ? -1 : 0,
      yoyo: true,
    });
  }

  private createLoopAnimation(asset: THREE.Object3D, params: any): void {
    const { duration = 2, ease = 'linear' } = params;

    gsap.to(asset.rotation, {
      y: '+=' + Math.PI * 2,
      duration: duration,
      ease: ease,
      repeat: -1,
    });
  }

  private createScrollTriggeredAnimation(asset: THREE.Object3D, params: any): void {
    const {
      scrollStart = 'top center',
      scrollEnd = 'bottom center',
      duration = 1,
      ease = 'power2.out',
    } = params;

    // Find the section this asset belongs to
    const section = sceneConfig.sections.find((s) => s.assetId === asset.name);

    if (!section) return;

    const htmlSection = document.querySelector(`#${section.id}`);

    if (!htmlSection) return;

    ScrollTrigger.create({
      trigger: htmlSection,
      start: scrollStart,
      end: scrollEnd,
      onEnter: () => {
        gsap.to(asset.scale, {
          x: asset.scale.x * 1.1,
          y: asset.scale.y * 1.1,
          z: asset.scale.z * 1.1,
          duration: duration,
          ease: ease,
        });
      },
      onLeaveBack: () => {
        gsap.to(asset.scale, {
          x: asset.scale.x / 1.1,
          y: asset.scale.y / 1.1,
          z: asset.scale.z / 1.1,
          duration: duration,
          ease: ease,
        });
      },
    });
  }

  public destroy(): void {
    // Kill all triggers
    this.triggers.forEach((trigger) => trigger.kill());
    this.triggers = [];

    // Kill all tweens
    gsap.killTweensOf('*');
  }
}

export default ScrollAnimations;
