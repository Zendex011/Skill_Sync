import React, { useState } from 'react';
import { Search, Filter, User } from 'lucide-react';
import { mockCandidates } from '../utils/mockData';
import CandidateCard from './CandidateCard';
import './CandidateSearch.css';

const CandidateSearch = () => {
    const [searchTerm, setSearchTerm] = useState('');

    return (
        <div className="candidate-search-section">
            <div className="section-header">
                <h1>Find Candidates</h1>
                <p>AI-ranked candidates based on your active job postings.</p>

                <div className="search-bar-wrapper">
                    <div className="search-input glass">
                        <Search size={20} className="search-icon" />
                        <input
                            type="text"
                            placeholder="Search by skills, title, or name..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>
            </div>

            <div className="candidates-layout">
                <aside className="filters-sidebar glass">
                    <h3>Filters</h3>
                    <div className="filter-group">
                        <label>Skills</label>
                        <input type="text" placeholder="e.g. React" className="glass" />
                    </div>
                    <div className="filter-group">
                        <label>Experience</label>
                        <select className="glass">
                            <option>Any Experience</option>
                            <option>1-3 years</option>
                            <option>3-5 years</option>
                            <option>5+ years</option>
                        </select>
                    </div>
                </aside>

                <div className="candidates-grid">
                    {mockCandidates.map(candidate => (
                        <CandidateCard key={candidate.id} candidate={candidate} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default CandidateSearch;
