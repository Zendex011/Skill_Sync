import React from 'react';
import { User, Briefcase, GraduationCap, ChevronRight } from 'lucide-react';
import './CandidateCard.css';

const CandidateCard = ({ candidate }) => {
    const getScoreColor = (score) => {
        if (score >= 90) return 'var(--success)';
        if (score >= 75) return 'var(--primary)';
        return 'var(--warning)';
    };

    return (
        <div className="candidate-card glass">
            <div className="card-top">
                <div className="candidate-avatar">
                    <User size={24} />
                </div>
                <div className="match-score" style={{ color: getScoreColor(candidate.matchScore) }}>
                    {candidate.matchScore}% Match
                </div>
            </div>

            <div className="candidate-info">
                <h3>{candidate.name}</h3>
                <p className="candidate-title">{candidate.title}</p>

                <div className="candidate-meta">
                    <div className="meta-item">
                        <Briefcase size={14} />
                        <span>{candidate.experience}</span>
                    </div>
                    <div className="meta-item">
                        <GraduationCap size={14} />
                        <span>{candidate.education}</span>
                    </div>
                </div>

                <div className="candidate-skills">
                    {candidate.skills.map(skill => (
                        <span key={skill} className="skill-tag">{skill}</span>
                    ))}
                </div>
            </div>

            <button className="btn btn-secondary view-btn">
                View Profile <ChevronRight size={16} />
            </button>
        </div>
    );
};

export default CandidateCard;
