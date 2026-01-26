import React, { useState } from 'react';
import { X, Bot, CheckCircle, AlertCircle, ChevronDown, ChevronUp, BookOpen, ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import './MatchDetailsModal.css';

const MatchDetailsModal = ({ job, onClose }) => {
    const { setSelectedJob } = useUser();
    const [expandedSection, setExpandedSection] = useState('skills');
    const navigate = useNavigate();

    const handleGenerateRoadmap = () => {
        setSelectedJob(job);
        navigate('/dashboard/learning');
        onClose();
    };

    const toggleSection = (section) => {
        setExpandedSection(expandedSection === section ? null : section);
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content glass">
                <button className="close-btn" onClick={onClose}><X size={24} /></button>

                <div className="modal-header">
                    <div className="overall-score-large">
                        <span className="score-num">{job.matchScore}%</span>
                        <span className="score-label">Overall Match</span>
                    </div>
                    <div className="job-title-header">
                        <h2>{job.title}</h2>
                        <p>{job.company} • {job.location}</p>
                    </div>
                </div>

                <div className="modal-body">
                    <div className="split-view">
                        <div className="details-column">
                            <div className="ai-explanation-card glass">
                                <div className="card-header">
                                    <Bot size={20} className="robot-icon" />
                                    <h4>Why this match?</h4>
                                </div>
                                <p>Based on your profile, you have high alignment with this role. Click below to see a detailed AI explanation and your personalized learning path for missing skills.</p>
                                <button className="btn btn-primary btn-sm" onClick={handleGenerateRoadmap}>
                                    Generate Learning Roadmap
                                </button>
                            </div>

                            <div className="score-breakdown">
                                <div className={`accordion-item ${expandedSection === 'skills' ? 'open' : ''}`}>
                                    <button className="accordion-toggle" onClick={() => toggleSection('skills')}>
                                        <span>Skill Match</span>
                                        {expandedSection === 'skills' ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                                    </button>
                                    {expandedSection === 'skills' && (
                                        <div className="accordion-content">
                                            <div className="skills-comparison">
                                                <div className="skill-list matched">
                                                    <h5>Matched Skills</h5>
                                                    <div className="tags-container">
                                                        {job.skills.map(s => <span key={s} className="tag matched"><CheckCircle size={12} /> {s}</span>)}
                                                    </div>
                                                </div>
                                                <div className="skill-list missing">
                                                    <h5>Missing Skills</h5>
                                                    <div className="tags-container">
                                                        {job.missingSkills.map(s => (
                                                            <div key={s} className="missing-tag-wrapper">
                                                                <span className="tag missing"><AlertCircle size={12} /> {s}</span>
                                                                <button className="learn-minimal" onClick={handleGenerateRoadmap}><BookOpen size={10} /> Learn</button>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>

                                <div className={`accordion-item ${expandedSection === 'similarity' ? 'open' : ''}`}>
                                    <button className="accordion-toggle" onClick={() => toggleSection('similarity')}>
                                        <span>Semantic Similarity</span>
                                        {expandedSection === 'similarity' ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                                    </button>
                                    {expandedSection === 'similarity' && (
                                        <div className="accordion-content">
                                            <p>Your profile shares <strong>{job.semanticScore}%</strong> semantic similarity with the responsibilities outlined in this JD.</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        <div className="jd-column glass">
                            <h4>Job Description</h4>
                            <p>{job.description}</p>
                            <div className="jd-full-text">
                                <p>Requirements:
                                    - 5+ years of experience with React/Next.js
                                    - Strong understanding of design principles
                                    - Experience with AI integration is a plus</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MatchDetailsModal;
