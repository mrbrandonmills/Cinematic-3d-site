/**
 * Main App Component
 * Orchestrates the entire 3D scroll experience
 */

import { useEffect, useRef, useState } from 'react';
import { Navigation } from './components/Navigation';
import { Section } from './components/Section';
import { Loader } from './components/Loader';
import { ThreeScene } from './threeScene';
import { ScrollAnimations } from './scrollAnimations';
import { sceneConfig } from './sceneConfig';
import { loadAllAssetMetadata, calculateProgress } from './utils/assetLoader';
import './styles/global.css';

function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<ThreeScene | null>(null);
  const animationsRef = useRef<ScrollAnimations | null>(null);

  const [loading, setLoading] = useState(true);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [activeSection, setActiveSection] = useState('home');

  useEffect(() => {
    let mounted = true;

    const initScene = async () => {
      if (!canvasRef.current) return;

      try {
        console.log('[App] Initializing 3D scene...');

        // Initialize Three.js scene
        const threeScene = new ThreeScene(canvasRef.current);
        sceneRef.current = threeScene;
        console.log('[App] ThreeScene created');

        // Load all asset metadata
        console.log('[App] Loading asset metadata...');
        const allMetadata = await loadAllAssetMetadata();
        console.log('[App] Loaded metadata for', allMetadata.length, 'assets:', allMetadata);

        // Track loading progress
        const loadingMap = new Map<string, number>();
        allMetadata.forEach((meta) => loadingMap.set(meta.id, 0));

        // Load assets with progress tracking
        console.log('[App] Starting to load assets...');
        await threeScene.loadAllAssets(allMetadata, (assetId, progress) => {
          if (!mounted) return;

          console.log(`[App] Loading ${assetId}: ${progress.toFixed(0)}%`);
          loadingMap.set(assetId, progress);
          const totalProgress = calculateProgress(
            loadingMap,
            allMetadata.length
          );
          setLoadingProgress(totalProgress);
        });
        console.log('[App] All assets loaded!');

        // Initialize scroll animations
        const scrollAnims = new ScrollAnimations({
          camera: threeScene.camera,
          scene: threeScene.scene,
        });
        animationsRef.current = scrollAnims;

        // Setup section animations
        scrollAnims.setupSectionAnimations();

        // Apply asset-specific animations from metadata
        allMetadata.forEach((meta) => {
          if (meta.animation) {
            scrollAnims.animateAsset(meta.id, meta.animation);
          }
        });

        // Start render loop
        threeScene.animate();

        // Mark loading complete
        if (mounted) {
          setLoadingProgress(100);
          setTimeout(() => {
            setLoading(false);
          }, 500);
        }
      } catch (error) {
        console.error('Failed to initialize scene:', error);
      }
    };

    initScene();

    // Cleanup
    return () => {
      mounted = false;

      if (animationsRef.current) {
        animationsRef.current.destroy();
      }

      if (sceneRef.current) {
        sceneRef.current.dispose();
      }
    };
  }, []);

  // Track active section based on scroll position
  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY + window.innerHeight / 2;

      for (const section of sceneConfig.sections) {
        const element = document.getElementById(section.id);
        if (element) {
          const rect = element.getBoundingClientRect();
          const elementTop = rect.top + window.scrollY;
          const elementBottom = elementTop + rect.height;

          if (scrollPosition >= elementTop && scrollPosition <= elementBottom) {
            setActiveSection(section.id);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLoaderComplete = () => {
    setLoading(false);
  };

  return (
    <div className="app">
      {loading && (
        <Loader
          progress={loadingProgress}
          isComplete={loadingProgress === 100}
          onComplete={handleLoaderComplete}
        />
      )}

      {/* 3D Canvas */}
      <canvas
        ref={canvasRef}
        className="three-canvas"
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: 0,
        }}
      />

      {/* Navigation */}
      <Navigation activeSection={activeSection} />

      {/* Scroll Container */}
      <div className="scroll-container" data-scroll-container>
        {sceneConfig.sections.map((section) => (
          <Section
            key={section.id}
            id={section.id}
            title={section.title}
            className={`section-${section.id}`}
          >
            {section.id === 'home' && (
              <div>
                <p>
                  Welcome to a cinematic journey through space. Scroll down to
                  explore different train stations, each representing a unique
                  destination.
                </p>
                <p>
                  Experience seamless 3D transitions and immersive storytelling
                  as you navigate through our world.
                </p>
              </div>
            )}

            {section.id === 'store' && (
              <div>
                <p>
                  Discover our collection of unique products and experiences.
                  Each item tells a story and invites you to be part of it.
                </p>
              </div>
            )}

            {section.id === 'gallery' && (
              <div>
                <p>
                  Explore a curated collection of visual stories and creative
                  works. Art meets technology in this immersive space.
                </p>
              </div>
            )}

            {section.id === 'blog' && (
              <div>
                <p>
                  Read our latest thoughts, insights, and stories. Join the
                  conversation and stay connected with our community.
                </p>
              </div>
            )}
          </Section>
        ))}
      </div>
    </div>
  );
}

export default App;
