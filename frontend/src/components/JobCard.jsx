import React, { useState } from 'react';
import { MapPin, Briefcase, Landmark, ChevronRight } from 'lucide-react';
import MatchDetailsModal from './MatchDetailsModal';
import './JobCard.css';

const JobCard = ({ job }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const getScoreColor = (score) => {
        if (score >= 90) return 'var(--success)';
        if (score >= 75) return 'var(--primary)';
        if (score >= 60) return 'var(--warning)';
        return 'var(--error)';
    };

    return (
        <>
            <div className="job-card glass">
                <div className="job-card-header">
                    <div className="company-logo">
                        {job.company.charAt(0)}
                    </div>
                    <div className="match-badge" style={{ '--score-color': getScoreColor(job.matchScore) }}>
                        <svg viewBox="0 0 36 36" className="circular-chart">
                            <path className="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                            <path className="circle" strokeDasharray={`${job.matchScore}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                            <text x="18" y="20.35" className="percentage">{job.matchScore}%</text>
                        </svg>
                    </div>
                </div>

                <div className="job-info">
                    <h3>{job.title}</h3>
                    <p className="company-name">{job.company}</p>

                    <div className="job-meta">
                        <div className="meta-item">
                            <MapPin size={14} />
                            <span>{job.location}</span>
                        </div>
                        <div className="meta-item">
                            <Landmark size={14} />
                            <span>{job.salary}</span>
                        </div>
                        <div className="meta-item">
                            <Briefcase size={14} />
                            <span>{job.type}</span>
                        </div>
                    </div>
                </div>

                <button className="btn btn-secondary view-btn" onClick={() => setIsModalOpen(true)}>
                    View Details <ChevronRight size={16} />
                </button>
            </div>

            {isModalOpen && (
                <MatchDetailsModal
                    job={job}
                    onClose={() => setIsModalOpen(false)}
                />
            )}
        </>
    );
};

export default JobCard;
