/**
 * Scene Configuration
 * Maps scroll sections to 3D assets and camera waypoints
 */

export interface CameraWaypoint {
  position: [number, number, number];
  lookAt: [number, number, number];
}

export interface SectionConfig {
  id: string;
  title: string;
  route: string;
  assetId: string;
  cameraFrom: CameraWaypoint;
  cameraTo: CameraWaypoint;
  animation?: {
    duration?: number;
    ease?: string;
  };
}

export interface SceneConfig {
  camera: {
    fov: number;
    near: number;
    far: number;
    initialPosition: [number, number, number];
  };
  lighting: {
    ambient: {
      color: number;
      intensity: number;
    };
    directional?: {
      color: number;
      intensity: number;
      position: [number, number, number];
    };
  };
  sections: SectionConfig[];
}

export const sceneConfig: SceneConfig = {
  camera: {
    fov: 75,
    near: 0.1,
    far: 1000,
    initialPosition: [0, 3, 10],
  },

  lighting: {
    ambient: {
      color: 0x404050,
      intensity: 0.4, // MATCHES STYLE GUIDE (was 0.6 - too bright)
    },
    directional: {
      color: 0xfff5e1,
      intensity: 0.8, // MATCHES STYLE GUIDE (was 1.2 - way too bright)
      position: [5, 10, 7],
    },
  },

  sections: [
    {
      id: 'home',
      title: 'Home',
      route: '/',
      assetId: 'station-home',
      cameraFrom: { position: [0, 3, 10], lookAt: [0, 0, 0] },
      cameraTo: { position: [0, 2, 6], lookAt: [0, 0, 0] },
      animation: {
        duration: 1.5,
        ease: 'power2.inOut',
      },
    },
    {
      id: 'store',
      title: 'Store',
      route: '#store',
      assetId: 'station-store',
      cameraFrom: { position: [0, 2, 6], lookAt: [0, 0, 0] },
      cameraTo: { position: [3, 2, 4], lookAt: [0, 0, 0] },
      animation: {
        duration: 1.5,
        ease: 'power2.inOut',
      },
    },
    {
      id: 'gallery',
      title: 'Gallery',
      route: '#gallery',
      assetId: 'station-gallery',
      cameraFrom: { position: [3, 2, 4], lookAt: [0, 0, 0] },
      cameraTo: { position: [-3, 2, 4], lookAt: [0, 0, 0] },
      animation: {
        duration: 1.5,
        ease: 'power2.inOut',
      },
    },
    {
      id: 'blog',
      title: 'Blog',
      route: '#blog',
      assetId: 'station-blog',
      cameraFrom: { position: [-3, 2, 4], lookAt: [0, 0, 0] },
      cameraTo: { position: [0, 2, -6], lookAt: [0, 0, 0] },
      animation: {
        duration: 1.5,
        ease: 'power2.inOut',
      },
    },
  ],
};

export default sceneConfig;
