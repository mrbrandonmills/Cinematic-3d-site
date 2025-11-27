/**
 * Section Component
 * Represents a scroll section with content
 */

import { ReactNode } from 'react';
import '../styles/Section.css';

interface SectionProps {
  id: string;
  title: string;
  children?: ReactNode;
  className?: string;
}

export function Section({ id, title, children, className = '' }: SectionProps) {
  return (
    <section
      id={id}
      className={`scroll-section ${className}`}
      data-scroll-section
    >
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">{title}</h2>
        </div>

        {children && <div className="section-body">{children}</div>}
      </div>
    </section>
  );
}

export default Section;
