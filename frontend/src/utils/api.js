// frontend/src/utils/api.js
const API_BASE = '/api'; // Uses proxy

export const api = {
    // Parse resume
    async parseResume(file) {
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch(`${API_BASE}/parse-resume`, {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error('Parse failed');
        return res.json();
    },

    // Match jobs
    async matchJobs(resumeData, jobIds = null) {
        const res = await fetch(`${API_BASE}/match-jobs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_data: resumeData,
                job_ids: jobIds
            })
        });

        if (!res.ok) throw new Error('Matching failed');
        return res.json();
    },

    // Generate roadmap
    async generateRoadmap(resumeData, selectedJob) {
        const res = await fetch(`${API_BASE}/generate-roadmap`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_data: resumeData,
                selected_job: selectedJob
            })
        });

        if (!res.ok) throw new Error('Roadmap generation failed');
        return res.json();
    }
};