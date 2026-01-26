import React, { useState, useEffect } from 'react';
import { Search, Filter, MapPin, DollarSign, Briefcase, Loader2, AlertCircle } from 'lucide-react';
import { useUser } from '../contexts/UserContext';
import JobCard from './JobCard';
import './JobMatching.css';

const JobMatching = () => {
    const { resumeData, matches, setMatches, loading, setLoading } = useUser();
    const [searchTerm, setSearchTerm] = useState('');
    const [location, setLocation] = useState('in');
    const [error, setError] = useState(null);
    const [sortBy, setSortBy] = useState('matchScore'); // matchScore, semanticScore, recent
    const [filterText, setFilterText] = useState(''); // For filtering results

    const findMatches = async () => {
        if (!resumeData) {
            setError("Please upload a resume first.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/match-jobs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    resume_data: resumeData
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch job matches');
            }

            const data = await response.json();
            setMatches(data.jobs);
        } catch (err) {
            console.error('Matching error:', err);
            setError('Failed to find job matches. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const searchJobs = async () => {
        if (!searchTerm.trim()) {
            setError("Please enter a job title to search");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/search-jobs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: searchTerm,
                    location: location,
                    remote_only: false,
                    date_posted: 'week',
                    page: 1,
                    resume_data: resumeData // Optional: for immediate matching
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to search jobs');
            }

            const data = await response.json();
            setMatches(data.jobs);
        } catch (err) {
            console.error('Search error:', err);
            setError('Failed to search jobs. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="job-matching-section">
            <div className="matching-header">
                <h1>Job Search & Matching</h1>
                <div className="search-bar-wrapper">
                    <div className="search-input glass">
                        <Search size={20} className="search-icon" />
                        <input
                            type="text"
                            placeholder="Enter job title (e.g., Python Developer)"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && searchJobs()}
                        />
                    </div>
                    <div className="search-input glass" style={{ width: '200px' }}>
                        <MapPin size={20} className="search-icon" />
                        <select
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            className="location-select"
                        >
                            <option value="in">India</option>
                            <option value="us">United States</option>
                            <option value="uk">United Kingdom</option>
                            <option value="ca">Canada</option>
                        </select>
                    </div>
                    <button
                        className="btn btn-primary"
                        onClick={searchJobs}
                        disabled={loading}
                    >
                        {loading ? <Loader2 className="spinner" size={20} /> : "Search Jobs"}
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={findMatches}
                        disabled={loading || !resumeData}
                    >
                        {loading ? <Loader2 className="spinner" size={20} /> : "Match Existing"}
                    </button>
                </div>

                {/* Sorting and Filtering Controls */}
                {matches && matches.length > 0 && (
                    <div className="controls-bar" style={{ display: 'flex', gap: '1rem', marginTop: '1rem', alignItems: 'center' }}>
                        <div className="search-input glass" style={{ flex: 1 }}>
                            <Filter size={16} className="search-icon" />
                            <input
                                type="text"
                                placeholder="Filter by title, company, or skills..."
                                value={filterText}
                                onChange={(e) => setFilterText(e.target.value)}
                            />
                        </div>
                        <div className="search-input glass" style={{ width: '200px' }}>
                            <select
                                value={sortBy}
                                onChange={(e) => setSortBy(e.target.value)}
                                className="location-select"
                            >
                                <option value="matchScore">Sort by Match %</option>
                                <option value="semanticScore">Sort by Semantic Score</option>
                                <option value="recent">Most Recent</option>
                            </select>
                        </div>
                    </div>
                )}
            </div>

            {error && (
                <div className="error-banner glass" style={{ marginBottom: '2rem' }}>
                    <AlertCircle className="error-icon" size={24} />
                    <span>{error}</span>
                </div>
            )}

            {!resumeData && !error && (
                <div className="info-banner glass" style={{ marginBottom: '2rem' }}>
                    <span>You haven't uploaded a resume yet. Go to Dashboard to upload one.</span>
                </div>
            )}



            <div className="matching-layout">
                <aside className="filters-sidebar glass">
                    <h3>Filters</h3>
                    <div className="filter-group">
                        <label>Location</label>
                        <input type="text" placeholder="City or Remote" className="glass" />
                    </div>
                    <div className="filter-group">
                        <label>Experience Level</label>
                        <select className="glass">
                            <option>All Levels</option>
                            <option>Entry Level</option>
                            <option>Intermediate</option>
                            <option>Senior</option>
                        </select>
                    </div>
                    <div className="filter-group">
                        <label>Salary Range</label>
                        <div className="range-inputs">
                            <input type="number" placeholder="Min" className="glass" />
                            <input type="number" placeholder="Max" className="glass" />
                        </div>
                    </div>
                </aside>

                <div className="jobs-grid">
                    {loading ? (
                        <div className="loading-state">
                            <Loader2 className="spinner" size={48} />
                            <p>Finding your perfect matches...</p>
                        </div>
                    ) : matches && matches.length > 0 ? (
                        (() => {
                            // Apply filtering
                            let filteredJobs = matches;
                            if (filterText.trim()) {
                                const searchLower = filterText.toLowerCase();
                                filteredJobs = matches.filter(job =>
                                    job.title?.toLowerCase().includes(searchLower) ||
                                    job.company?.toLowerCase().includes(searchLower) ||
                                    job.skills?.some(skill => skill.toLowerCase().includes(searchLower)) ||
                                    job.missingSkills?.some(skill => skill.toLowerCase().includes(searchLower))
                                );
                            }

                            // Apply sorting
                            const sortedJobs = [...filteredJobs].sort((a, b) => {
                                if (sortBy === 'matchScore') {
                                    return (b.matchScore || 0) - (a.matchScore || 0);
                                } else if (sortBy === 'semanticScore') {
                                    return (b.semanticScore || 0) - (a.semanticScore || 0);
                                } else if (sortBy === 'recent') {
                                    // Assuming newer jobs have higher IDs or we could add timestamp
                                    return 0; // Keep original order for now
                                }
                                return 0;
                            });

                            return sortedJobs.length > 0 ? (
                                sortedJobs.map(job => (
                                    <JobCard key={job.id} job={job} />
                                ))
                            ) : (
                                <div className="no-results">
                                    <p>No jobs match your filter criteria.</p>
                                </div>
                            );
                        })()
                    ) : (
                        <div className="empty-state">
                            <Search size={64} className="empty-icon" />
                            <h3>No jobs found</h3>
                            <p>Try searching for a job title or upload your resume to see matches</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default JobMatching;
