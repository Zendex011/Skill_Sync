import React, { useState, useEffect } from 'react';
import { useUser } from '../contexts/UserContext';
import JobOpportunityCard from './JobOpportunityCard';
import { Loader2, Search } from 'lucide-react';
import './JobOpportunitiesList.css';

const JobOpportunitiesList = () => {
    const { resumeData } = useUser();
    const [links, setLinks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLinks = async () => {
            if (!resumeData) return;

            setLoading(true);
            try {
                const response = await fetch('http://localhost:8000/api/job-search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ resume_data: resumeData })
                });

                if (!response.ok) throw new Error('Failed to fetch job links');

                const data = await response.json();
                setLinks(data.links);
            } catch (err) {
                console.error("Job Search Error:", err);
                setError("Could not load job search links.");
            } finally {
                setLoading(false);
            }
        };

        fetchLinks();
    }, [resumeData]);

    if (!resumeData) return null;

    return (
        <div className="job-opportunities-container">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                <Search size={24} className="text-primary" />
                <h2>Direct Job Search Links</h2>
            </div>

            {loading ? (
                <div className="opportunities-grid">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="job-opp-card glass" style={{ height: '160px', opacity: 0.5 }}>
                            <Loader2 className="spinner" style={{ margin: 'auto' }} />
                        </div>
                    ))}
                </div>
            ) : error ? (
                <div className="error-message">{error}</div>
            ) : (
                <div className="opportunities-grid">
                    {links.map((link, i) => (
                        <JobOpportunityCard key={i} opportunity={link} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default JobOpportunitiesList;
