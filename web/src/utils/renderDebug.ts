/**
 * Rendering Debug Utilities
 * Tools for diagnosing material and geometry issues
 */

import * as THREE from 'three';

export class RenderDebugger {
  /**
   * Analyze a loaded model and log detailed material/geometry info
   */
  static analyzeModel(model: THREE.Object3D): void {
    console.group(`[RenderDebug] Analyzing Model: ${model.name}`);

    let meshCount = 0;
    let vertexCount = 0;
    let triangleCount = 0;
    const materials = new Map<string, THREE.Material>();
    const geometryTypes = new Map<string, number>();

    model.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        meshCount++;

        // Geometry stats
        const geom = mesh.geometry;
        if (geom.attributes.position) {
          const verts = geom.attributes.position.count;
          vertexCount += verts;

          if (geom.index) {
            triangleCount += geom.index.count / 3;
          } else {
            triangleCount += verts / 3;
          }
        }

        // Track geometry types
        const geomType = geom.type;
        geometryTypes.set(geomType, (geometryTypes.get(geomType) || 0) + 1);

        // Collect unique materials
        if (mesh.material) {
          if (Array.isArray(mesh.material)) {
            mesh.material.forEach(mat => {
              materials.set(mat.uuid, mat);
            });
          } else {
            materials.set(mesh.material.uuid, mesh.material);
          }
        }
      }
    });

    console.log(`📊 Mesh Count: ${meshCount}`);
    console.log(`📐 Vertices: ${vertexCount.toLocaleString()}`);
    console.log(`🔺 Triangles: ${Math.round(triangleCount).toLocaleString()}`);
    console.log(`🎨 Unique Materials: ${materials.size}`);

    console.group('Geometry Types:');
    geometryTypes.forEach((count, type) => {
      console.log(`  ${type}: ${count}`);
    });
    console.groupEnd();

    console.group('Material Details:');
    materials.forEach((mat, uuid) => {
      if (mat.type === 'MeshStandardMaterial') {
        const stdMat = mat as THREE.MeshStandardMaterial;
        console.log(`  ${mat.name || 'Unnamed'} (${mat.type}):`);
        console.log(`    - Color: #${stdMat.color.getHexString()}`);
        console.log(`    - Roughness: ${stdMat.roughness}`);
        console.log(`    - Metalness: ${stdMat.metalness}`);

        if (stdMat.emissive.getHex() !== 0x000000) {
          console.log(`    - Emissive: #${stdMat.emissive.getHexString()} (intensity: ${stdMat.emissiveIntensity})`);
        }

        if (stdMat.map) console.log(`    - Has Albedo Map: ${stdMat.map.image?.width}x${stdMat.map.image?.height}`);
        if (stdMat.normalMap) console.log(`    - Has Normal Map`);
        if (stdMat.roughnessMap) console.log(`    - Has Roughness Map`);
        if (stdMat.metalnessMap) console.log(`    - Has Metalness Map`);
      } else {
        console.log(`  ${mat.name || 'Unnamed'} (${mat.type})`);
      }
    });
    console.groupEnd();

    console.groupEnd();
  }

  /**
   * Log current renderer settings
   */
  static logRendererSettings(renderer: THREE.WebGLRenderer): void {
    console.group('[RenderDebug] Renderer Settings');
    console.log(`Output Color Space: ${renderer.outputColorSpace}`);
    console.log(`Tone Mapping: ${this.getToneMappingName(renderer.toneMapping)}`);
    console.log(`Tone Mapping Exposure: ${renderer.toneMappingExposure}`);
    console.log(`Pixel Ratio: ${renderer.getPixelRatio()}`);
    console.log(`Shadow Map Enabled: ${renderer.shadowMap.enabled}`);

    const size = renderer.getSize(new THREE.Vector2());
    console.log(`Render Size: ${size.x} x ${size.y}`);
    console.groupEnd();
  }

  /**
   * Check if materials are properly loaded
   */
  static verifyMaterials(scene: THREE.Scene): boolean {
    let hasIssues = false;
    const issues: string[] = [];

    scene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;

        if (!mesh.material) {
          issues.push(`Mesh "${mesh.name}" has no material`);
          hasIssues = true;
        } else if (Array.isArray(mesh.material)) {
          mesh.material.forEach((mat, index) => {
            if (mat.type === 'MeshBasicMaterial') {
              issues.push(`Mesh "${mesh.name}" material[${index}] is basic (should be PBR)`);
              hasIssues = true;
            }
          });
        } else {
          if (mesh.material.type === 'MeshBasicMaterial') {
            issues.push(`Mesh "${mesh.name}" has basic material (should be PBR)`);
            hasIssues = true;
          }
        }

        // Check if geometry has normals
        if (!mesh.geometry.attributes.normal) {
          issues.push(`Mesh "${mesh.name}" missing vertex normals (will look faceted)`);
          hasIssues = true;
        }
      }
    });

    if (hasIssues) {
      console.group('[RenderDebug] ⚠️ Material Issues Detected');
      issues.forEach(issue => console.warn(`  - ${issue}`));
      console.groupEnd();
    } else {
      console.log('[RenderDebug] ✓ All materials verified');
    }

    return !hasIssues;
  }

  /**
   * Log scene lighting setup
   */
  static analyzeLighting(scene: THREE.Scene): void {
    console.group('[RenderDebug] Scene Lighting Analysis');

    let ambientCount = 0;
    let directionalCount = 0;
    let pointCount = 0;
    let spotCount = 0;
    let hemiCount = 0;
    let totalIntensity = 0;

    scene.traverse((child) => {
      if (child.type === 'AmbientLight') {
        const light = child as THREE.AmbientLight;
        ambientCount++;
        totalIntensity += light.intensity;
        console.log(`  🌐 Ambient: intensity ${light.intensity}, color #${light.color.getHexString()}`);
      } else if (child.type === 'DirectionalLight') {
        const light = child as THREE.DirectionalLight;
        directionalCount++;
        totalIntensity += light.intensity;
        console.log(`  ☀️ Directional: intensity ${light.intensity}, color #${light.color.getHexString()}`);
      } else if (child.type === 'PointLight') {
        const light = child as THREE.PointLight;
        pointCount++;
        totalIntensity += light.intensity;
        console.log(`  💡 Point: intensity ${light.intensity}, distance ${light.distance}`);
      } else if (child.type === 'SpotLight') {
        const light = child as THREE.SpotLight;
        spotCount++;
        totalIntensity += light.intensity;
        console.log(`  🔦 Spot: intensity ${light.intensity}, angle ${light.angle}`);
      } else if (child.type === 'HemisphereLight') {
        const light = child as THREE.HemisphereLight;
        hemiCount++;
        totalIntensity += light.intensity;
        console.log(`  🌍 Hemisphere: intensity ${light.intensity}, sky #${light.color.getHexString()}, ground #${light.groundColor.getHexString()}`);
      }
    });

    console.log(`\n📊 Summary:`);
    console.log(`  - Total Lights: ${ambientCount + directionalCount + pointCount + spotCount + hemiCount}`);
    console.log(`  - Total Intensity: ${totalIntensity.toFixed(2)}`);
    console.log(`  - Recommended Max: 1.5`);

    if (totalIntensity > 1.5) {
      console.warn(`  ⚠️ Scene is ${((totalIntensity / 1.5 - 1) * 100).toFixed(0)}% too bright!`);
    }

    console.groupEnd();
  }

  private static getToneMappingName(toneMapping: number): string {
    const mappings: Record<number, string> = {
      0: 'None',
      1: 'Linear',
      2: 'Reinhard',
      3: 'Cineon',
      4: 'ACESFilmic',
      5: 'Custom',
    };
    return mappings[toneMapping] || 'Unknown';
  }

  /**
   * Run full diagnostic report
   */
  static fullDiagnostic(renderer: THREE.WebGLRenderer, scene: THREE.Scene, camera: THREE.Camera): void {
    console.group('[RenderDebug] 🎬 FULL CINEMA-QUALITY DIAGNOSTIC');

    this.logRendererSettings(renderer);
    this.analyzeLighting(scene);
    this.verifyMaterials(scene);

    // Camera info
    if (camera.type === 'PerspectiveCamera') {
      const cam = camera as THREE.PerspectiveCamera;
      console.log(`\n📷 Camera:`);
      console.log(`  - FOV: ${cam.fov}°`);
      console.log(`  - Aspect: ${cam.aspect.toFixed(2)}`);
      console.log(`  - Near/Far: ${cam.near} / ${cam.far}`);
      console.log(`  - Position: (${cam.position.x.toFixed(1)}, ${cam.position.y.toFixed(1)}, ${cam.position.z.toFixed(1)})`);
    }

    console.groupEnd();
  }
}

export default RenderDebugger;
