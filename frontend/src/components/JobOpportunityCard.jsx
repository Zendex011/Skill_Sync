import React from 'react';
import { ExternalLink, Briefcase, MapPin } from 'lucide-react';
import './JobOpportunitiesList.css';

const JobOpportunityCard = ({ opportunity }) => {
    const { platform, platform_key, query, url, priority, location } = opportunity;

    return (
        <div className="job-opp-card glass" data-platform={platform_key}>
            <div className="card-header">
                <span className="platform-badge">{platform}</span>
                {priority && (
                    <div className={`priority-indicator priority-${priority.toLowerCase()}`}>
                        <span>{priority} Match</span>
                    </div>
                )}
            </div>

            <h4 className="query-text">{query}</h4>
            <div className="location-text">
                <MapPin size={12} style={{ display: 'inline', marginRight: '4px' }} />
                {location}
            </div>

            <a href={url} target="_blank" rel="noopener noreferrer" className="view-btn">
                <span>View Jobs</span>
                <ExternalLink size={14} />
            </a>
        </div>
    );
};

export default JobOpportunityCard;
