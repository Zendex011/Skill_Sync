import React, { useState } from 'react';
import { Send, FileText, MapPin, DollarSign, Type } from 'lucide-react';
import './PostJobForm.css';

const PostJobForm = () => {
    const [formData, setFormData] = useState({
        title: '',
        company: '',
        location: '',
        salary: '',
        description: '',
        skills: ''
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        alert("Job posted successfully (Mock)");
    };

    return (
        <div className="post-job-section">
            <div className="section-header">
                <h1>Post a New Job</h1>
                <p>Use our AI to find the best matching talent for your role.</p>
            </div>

            <form className="post-job-form glass" onSubmit={handleSubmit}>
                <div className="form-grid">
                    <div className="form-group">
                        <label><Type size={16} /> Job Title</label>
                        <input
                            type="text"
                            placeholder="e.g. Senior Frontend Engineer"
                            className="glass"
                            value={formData.title}
                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label><MapPin size={16} /> Location</label>
                        <input
                            type="text"
                            placeholder="e.g. Remote or San Francisco, CA"
                            className="glass"
                            value={formData.location}
                            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label><DollarSign size={16} /> Salary Range</label>
                        <input
                            type="text"
                            placeholder="e.g. $120k - $160k"
                            className="glass"
                            value={formData.salary}
                            onChange={(e) => setFormData({ ...formData, salary: e.target.value })}
                        />
                    </div>

                    <div className="form-group">
                        <label><Briefcase size={16} /> Required Skills (comma separated)</label>
                        <input
                            type="text"
                            placeholder="e.g. React, TypeScript, Node.js"
                            className="glass"
                            value={formData.skills}
                            onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                        />
                    </div>
                </div>

                <div className="form-group full-width">
                    <label><FileText size={16} /> Job Description</label>
                    <textarea
                        placeholder="Describe the role, responsibilities, and benefits..."
                        className="glass"
                        rows="10"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        required
                    ></textarea>
                </div>

                <button type="submit" className="btn btn-primary btn-lg submit-btn">
                    Post Job & Find Candidates <Send size={20} />
                </button>
            </form>
        </div>
    );
};

export default PostJobForm;
