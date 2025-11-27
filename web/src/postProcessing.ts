/**
 * Post-Processing Manager
 * Adds cinematic effects: bloom, SSAO, tone mapping, anti-aliasing
 */

import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { SSAOPass } from 'three/examples/jsm/postprocessing/SSAOPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { SMAAPass } from 'three/examples/jsm/postprocessing/SMAAPass.js';

export class PostProcessingManager {
  private composer: EffectComposer;
  private bloomPass: UnrealBloomPass;
  private ssaoPass: SSAOPass | null = null;
  private smaaPass: SMAAPass;

  constructor(
    renderer: THREE.WebGLRenderer,
    scene: THREE.Scene,
    camera: THREE.PerspectiveCamera
  ) {
    console.log('[PostProcessing] Initializing cinematic post-processing...');

    // Create composer
    this.composer = new EffectComposer(renderer);
    this.composer.setSize(window.innerWidth, window.innerHeight);

    // 1. Render Pass (base scene)
    const renderPass = new RenderPass(scene, camera);
    this.composer.addPass(renderPass);

    // 2. SSAO Pass (realistic ambient occlusion)
    try {
      this.ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
      this.ssaoPass.kernelRadius = 8;
      this.ssaoPass.minDistance = 0.005;
      this.ssaoPass.maxDistance = 0.1;
      this.ssaoPass.output = 0; // Default output
      this.composer.addPass(this.ssaoPass);
      console.log('[PostProcessing] ✓ SSAO enabled');
    } catch (error) {
      console.warn('[PostProcessing] SSAO failed, continuing without it:', error);
    }

    // 3. Bloom Pass (glowing lights) - BALANCED FOR CINEMA QUALITY
    this.bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      0.4,    // strength (reduced from 0.8 - subtle glow, not nuclear)
      0.6,    // radius (increased from 0.4 - smoother spread)
      0.88    // threshold (slightly raised - only bright lights bloom)
    );
    this.composer.addPass(this.bloomPass);
    console.log('[PostProcessing] ✓ Bloom enabled (cinema-balanced)');

    // 4. SMAA Pass (anti-aliasing)
    this.smaaPass = new SMAAPass(window.innerWidth, window.innerHeight);
    this.composer.addPass(this.smaaPass);
    console.log('[PostProcessing] ✓ SMAA anti-aliasing enabled');

    // 5. Output Pass (final color correction)
    const outputPass = new OutputPass();
    this.composer.addPass(outputPass);

    console.log('[PostProcessing] ✓ Cinematic post-processing initialized');
  }

  /**
   * Render with post-processing
   */
  public render(): void {
    this.composer.render();
  }

  /**
   * Update on window resize
   */
  public setSize(width: number, height: number): void {
    this.composer.setSize(width, height);

    if (this.ssaoPass) {
      this.ssaoPass.setSize(width, height);
    }

    // Update bloom resolution
    this.bloomPass.resolution.set(width, height);

    this.smaaPass.setSize(width, height);
  }

  /**
   * Adjust bloom intensity (for different scenes/moods)
   */
  public setBloomIntensity(strength: number, radius: number = 0.6, threshold: number = 0.3): void {
    this.bloomPass.strength = strength;
    this.bloomPass.radius = radius;
    this.bloomPass.threshold = threshold;
  }

  /**
   * Adjust SSAO settings
   */
  public setSSAO(kernelRadius: number = 8, minDistance: number = 0.005, maxDistance: number = 0.1): void {
    if (this.ssaoPass) {
      this.ssaoPass.kernelRadius = kernelRadius;
      this.ssaoPass.minDistance = minDistance;
      this.ssaoPass.maxDistance = maxDistance;
    }
  }

  /**
   * Clean up resources
   */
  public dispose(): void {
    this.composer.dispose();
  }
}

export default PostProcessingManager;
