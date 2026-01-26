import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileText, Target, BookOpen, User, Menu, X } from 'lucide-react';
import ResumeUpload from '../components/ResumeUpload';
import JobMatching from '../components/JobMatching';
import LearningRoadmap from './LearningRoadmap';
import './CandidateDashboard.css';

const CandidateDashboard = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const location = useLocation();

    const navItems = [
        { icon: <LayoutDashboard size={20} />, label: "Dashboard", path: "/dashboard" },
        { icon: <Target size={20} />, label: "My Matches", path: "/dashboard/matches" },
        { icon: <BookOpen size={20} />, label: "Learning Path", path: "/dashboard/learning" },
        { icon: <User size={20} />, label: "Profile", path: "/dashboard/profile" },
    ];

    return (
        <div className="dashboard-container">
            <aside className={`sidebar glass ${isSidebarOpen ? 'open' : 'closed'}`}>
                <button className="sidebar-toggle" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                    {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
                </button>

                <nav className="sidebar-nav">
                    {navItems.map((item) => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
                        >
                            {item.icon}
                            {isSidebarOpen && <span>{item.label}</span>}
                        </Link>
                    ))}
                </nav>
            </aside>

            <main className="dashboard-content">
                <Routes>
                    <Route path="/" element={<ResumeUpload />} />
                    <Route path="/matches" element={<JobMatching />} />
                    <Route path="/learning" element={<LearningRoadmap />} />
                    <Route path="/profile" element={<div>Profile Section (Coming Soon)</div>} />
                </Routes>
            </main>
        </div>
    );
};

export default CandidateDashboard;
