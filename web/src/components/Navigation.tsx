/**
 * Navigation Component
 * Header navigation with section links
 */

import { useState, useEffect } from 'react';
import { sceneConfig } from '../sceneConfig';
import '../styles/Navigation.css';

interface NavigationProps {
  activeSection?: string;
  onNavigate?: (sectionId: string) => void;
}

export function Navigation({ activeSection, onNavigate }: NavigationProps) {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleClick = (sectionId: string, route: string) => {
    if (onNavigate) {
      onNavigate(sectionId);
    }

    // Smooth scroll to section
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className={`navigation ${isScrolled ? 'scrolled' : ''}`}>
      <div className="nav-container">
        <div className="nav-logo">
          <h2>Cinematic Journey</h2>
        </div>

        <ul className="nav-links">
          {sceneConfig.sections.map((section) => (
            <li key={section.id}>
              <a
                href={section.route}
                className={activeSection === section.id ? 'active' : ''}
                onClick={(e) => {
                  e.preventDefault();
                  handleClick(section.id, section.route);
                }}
              >
                {section.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
