import React from 'react';
import { Github, ExternalLink, Code2 } from 'lucide-react';
import './ProjectsDisplay.css'; // We'll create this next

const ProjectsDisplay = ({ projects }) => {
    if (!projects || projects.length === 0) {
        return (
            <div className="empty-projects glass">
                <Code2 size={48} className="empty-icon" />
                <p>No projects detected in resume</p>
            </div>
        );
    }

    return (
        <div className="projects-grid">
            {projects.map((proj, i) => (
                <div key={i} className="project-card glass">
                    <div className="project-header">
                        <h3>{proj.title || "Untitled Project"}</h3>
                        {proj.link && proj.link.startsWith('http') && (
                            <a
                                href={proj.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="project-link-btn"
                                title="View Project"
                            >
                                {proj.link.includes('github') ? <Github size={18} /> : <ExternalLink size={18} />}
                            </a>
                        )}
                    </div>

                    <p className="project-description">
                        {proj.description || "No description provided."}
                    </p>

                    {proj.technologies && proj.technologies.length > 0 && (
                        <div className="project-tech-stack">
                            {proj.technologies.slice(0, 5).map((tech, tIndex) => (
                                <span key={tIndex} className="tech-tag">
                                    {tech}
                                </span>
                            ))}
                            {proj.technologies.length > 5 && (
                                <span className="tech-tag more">+{proj.technologies.length - 5}</span>
                            )}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default ProjectsDisplay;
