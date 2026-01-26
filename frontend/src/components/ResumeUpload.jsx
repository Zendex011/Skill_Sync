import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, CheckCircle, Loader2, AlertCircle } from 'lucide-react';
import { useUser } from '../contexts/UserContext';
import './ResumeUpload.css';
import ProjectsDisplay from './ProjectsDisplay';

const ResumeUpload = () => {
    const { setResumeData, resumeData: parsedData } = useUser();
    const [isParsing, setIsParsing] = useState(false);
    const [error, setError] = useState(null);

    const onDrop = useCallback(async acceptedFiles => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];
        setIsParsing(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/parse-resume', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to parse resume');
            }

            const data = await response.json();
            setResumeData(data);
        } catch (err) {
            console.error('Parsing error:', err);
            setError('Failed to parse resume. Please try again.');
        } finally {
            setIsParsing(false);
        }
    }, [setResumeData]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
        },
        multiple: false
    });

    return (
        <div className="resume-section">
            <div className="section-header">
                <h1>Upload Resume</h1>
                <p>Upload your resume to get instant AI-powered job matches.</p>
            </div>

            {!parsedData ? (
                <div {...getRootProps()} className={`dropzone glass ${isDragActive ? 'active' : ''} ${isParsing ? 'parsing' : ''}`}>
                    <input {...getInputProps()} />
                    {isParsing ? (
                        <div className="parsing-state">
                            <Loader2 className="spinner" size={48} />
                            <p>Analyzing your resume with AI...</p>
                        </div>
                    ) : (
                        <div className="upload-state">
                            <div className="upload-icon">
                                <Upload size={32} />
                            </div>
                            <p>Drag & drop your resume here, or <span>click to browse</span></p>
                            <span>Supports PDF, DOCX (Max 5MB)</span>
                        </div>
                    )}
                </div>
            ) : (
                <div className="parsed-results">
                    <div className="success-banner glass">
                        <CheckCircle className="success-icon" size={24} />
                        <span>Resume parsed successfully!</span>
                        <button className="btn btn-secondary btn-sm" onClick={() => setResumeData(null)}>Upload New</button>
                    </div>

                    {error && (
                        <div className="error-banner glass">
                            <AlertCircle className="error-icon" size={24} />
                            <span>{error}</span>
                        </div>
                    )}

                    <div className="results-grid">
                        <div className="result-card glass">
                            <h3>Skills</h3>
                            <div className="tags-container">
                                {parsedData.technical_skills?.map(skill => (
                                    <span key={skill} className="tag">{skill}</span>
                                ))}
                                {parsedData.technical_skills?.length === 0 && <span>No skills detected</span>}
                            </div>
                        </div>

                        <div className="result-card glass">
                            <h3>Experience</h3>
                            {parsedData.experience?.map((exp, i) => (
                                <div key={i} className="exp-item">
                                    <strong>{exp.role}</strong>
                                    <span>{exp.company} • {exp.duration}</span>
                                </div>
                            ))}
                            {parsedData.experience?.length === 0 && <span>No experience detected</span>}
                        </div>

                        <div className="result-card glass">
                            <h3>Education</h3>
                            {parsedData.education?.map((edu, i) => (
                                <div key={i} className="exp-item">
                                    <strong>{edu.degree}</strong>
                                    <span>{edu.institution} • {edu.duration}</span>
                                </div>
                            ))}
                            {parsedData.education?.length === 0 && <span>No education detected</span>}
                        </div>

                        <div className="result-card glass" style={{ gridColumn: '1 / -1' }}>
                            <h3>Projects</h3>
                            <ProjectsDisplay projects={parsedData.projects} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResumeUpload;
