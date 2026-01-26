import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Book, Clock, CheckCircle2, ChevronRight, Trophy, Loader2, Bot, AlertCircle, ExternalLink, Calendar } from 'lucide-react';
import { useUser } from '../contexts/UserContext';
import './LearningRoadmap.css';

const LearningRoadmap = () => {
    const { resumeData, selectedJob } = useUser();
    const [roadmap, setRoadmap] = useState(null);
    const [explanation, setExplanation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [completedSkills, setCompletedSkills] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            if (!resumeData || !selectedJob) return;

            setLoading(true);
            setError(null);

            try {
                // 1. Fetch Roadmap
                const roadmapResponse = await fetch('http://localhost:8000/api/generate-roadmap', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        resume_data: resumeData,
                        selected_job: selectedJob
                    }),
                });

                if (!roadmapResponse.ok) throw new Error('Failed to generate roadmap');
                const roadmapData = await roadmapResponse.json();
                setRoadmap(roadmapData);

                // 2. Fetch Explanation
                const explanationResponse = await fetch('http://localhost:8000/api/explain-match', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        resume_data: resumeData,
                        job: selectedJob,
                        match_score: selectedJob.matchScore
                    }),
                });

                if (!explanationResponse.ok) throw new Error('Failed to generate explanation');
                const explanationData = await explanationResponse.json();
                setExplanation(explanationData.explanation);

            } catch (err) {
                console.error('Roadmap error:', err);
                setError('Failed to load roadmap. Please try again.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [resumeData, selectedJob]);

    const toggleSkill = (skillName) => {
        setCompletedSkills(prev =>
            prev.includes(skillName) ? prev.filter(s => s !== skillName) : [...prev, skillName]
        );
    };

    if (!resumeData || !selectedJob) {
        return (
            <div className="roadmap-page">
                <div className="empty-state glass">
                    <AlertCircle size={48} />
                    <h2>No Job Selected</h2>
                    <p>Please select a job from the "My Matches" page to generate a learning roadmap.</p>
                    <button className="btn btn-primary" onClick={() => navigate('/dashboard/matches')}>
                        View Matches
                    </button>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="roadmap-page">
                <div className="loading-state glass">
                    <Loader2 className="spinner" size={48} />
                    <h2>Generating Your Personalized Roadmap</h2>
                    <p>Our AI is analyzing the skills gap and curating the best resources for you...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="roadmap-page">
                <div className="error-state glass">
                    <AlertCircle size={48} color="var(--error)" />
                    <h2>Something went wrong</h2>
                    <p>{error}</p>
                    <button className="btn btn-primary" onClick={() => window.location.reload()}>
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    const totalSkillsCount = roadmap?.phases?.reduce((acc, phase) => acc + phase.skills.length, 0) || 1;
    const progress = Math.round((completedSkills.length / totalSkillsCount) * 100);

    return (
        <div className="roadmap-page">
            <div className="roadmap-header">
                <div className="header-text">
                    <h1>Learning Path for {selectedJob.title}</h1>
                    <p>A curated journey to bridge your {roadmap?.total_skills || 0} skill gaps in {roadmap?.estimated_weeks || 0} weeks.</p>
                </div>
                <div className="overall-progress-card glass">
                    <div className="progress-info">
                        <Trophy className="trophy-icon" />
                        <div className="text-box">
                            <span className="label">Overall Progress</span>
                            <span className="value">{progress}%</span>
                        </div>
                    </div>
                    <div className="progress-bar-bg">
                        <div className="progress-bar-fill" style={{ width: `${progress}%` }}></div>
                    </div>
                </div>
            </div>

            {explanation && (
                <div className="ai-explanation-section glass" style={{ marginBottom: '2rem', padding: '1.5rem' }}>
                    <div className="explanation-header" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--primary)' }}>
                        <Bot size={24} />
                        <h3 style={{ margin: 0 }}>AI Match Insight</h3>
                    </div>
                    <div className="explanation-content" style={{ lineHeight: '1.6', color: 'rgba(255,255,255,0.8)' }}>
                        {explanation.split('\n').map((line, i) => (
                            <p key={i} style={{ marginBottom: '0.5rem' }}>{line}</p>
                        ))}
                    </div>
                </div>
            )}

            <div className="roadmap-timeline">
                {roadmap?.phases?.map((phase, pIndex) => (
                    <div key={pIndex} className="phase-section">
                        <div className="phase-marker">
                            <div className="dot"></div>
                            {pIndex !== roadmap.phases.length - 1 && <div className="line"></div>}
                        </div>

                        <div className="phase-content">
                            <div className="phase-header">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <h3>{phase.name}</h3>
                                    <span className="phase-weeks" style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.5)' }}>
                                        Week {phase.start_week} - {phase.end_week}
                                    </span>
                                </div>
                                <p>{phase.description}</p>
                            </div>

                            <div className="skill-cards-grid">
                                {phase.skills.map((skill, sIndex) => (
                                    <motion.div
                                        key={sIndex}
                                        layout
                                        className={`skill-card glass ${completedSkills.includes(skill.name) ? 'completed' : ''}`}
                                    >
                                        <div className="skill-main">
                                            <div className="skill-check" onClick={() => toggleSkill(skill.name)}>
                                                {completedSkills.includes(skill.name) ? <CheckCircle2 size={24} className="check-icon" /> : <div className="check-circle"></div>}
                                            </div>
                                            <div className="skill-info">
                                                <h4>{skill.name}</h4>
                                                <div className="skill-meta">
                                                    <Clock size={14} />
                                                    <span>{skill.weeks} weeks</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="skill-resources">
                                            <div className="resource-header">
                                                <Book size={14} />
                                                <span>Resources</span>
                                            </div>
                                            <div className="resource-links">
                                                {Object.entries(skill.resources || {}).map(([level, links]) => (
                                                    Array.isArray(links) && links.map((res, rIndex) => (
                                                        res.startsWith('http') ? (
                                                            <a href={res} target="_blank" rel="noopener noreferrer" key={`${level}-${rIndex}`} className="res-link">
                                                                {res.length > 30 ? res.substring(0, 30) + '...' : res} <ExternalLink size={12} />
                                                            </a>
                                                        ) : (
                                                            <span key={`${level}-${rIndex}`} className="res-link" style={{ cursor: 'default', textDecoration: 'none' }}>
                                                                {res}
                                                            </span>
                                                        )
                                                    ))
                                                ))}
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LearningRoadmap;
