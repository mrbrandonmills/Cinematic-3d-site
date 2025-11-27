/**
 * Loading Screen Component
 * Displays loading progress while assets are being loaded
 */

import { useEffect, useState } from 'react';
import '../styles/Loader.css';

interface LoaderProps {
  progress: number;
  isComplete: boolean;
  onComplete?: () => void;
}

export function Loader({ progress, isComplete, onComplete }: LoaderProps) {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    if (isComplete) {
      // Start fade out animation
      const timer = setTimeout(() => {
        setFadeOut(true);

        // Call onComplete after fade
        const completeTimer = setTimeout(() => {
          if (onComplete) {
            onComplete();
          }
        }, 800);

        return () => clearTimeout(completeTimer);
      }, 300);

      return () => clearTimeout(timer);
    }
  }, [isComplete, onComplete]);

  const progressPercent = Math.round(progress);

  return (
    <div className={`loader-container ${fadeOut ? 'fade-out' : ''}`}>
      <div className="loader-content">
        <div className="loader-title">
          <h1>Cinematic 3D Experience</h1>
          <p>Preparing your journey...</p>
        </div>

        <div className="loader-progress">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <div className="progress-text">{progressPercent}%</div>
        </div>

        <div className="loader-tip">
          {progressPercent < 30 && <p>Loading 3D assets...</p>}
          {progressPercent >= 30 && progressPercent < 70 && (
            <p>Preparing textures...</p>
          )}
          {progressPercent >= 70 && progressPercent < 100 && (
            <p>Almost ready...</p>
          )}
          {progressPercent === 100 && <p>Welcome aboard!</p>}
        </div>
      </div>
    </div>
  );
}

export default Loader;
