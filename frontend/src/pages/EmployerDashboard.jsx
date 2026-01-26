import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { PlusCircle, Users, BarChart3, Briefcase, Menu, X } from 'lucide-react';
import PostJobForm from '../components/PostJobForm';
import CandidateSearch from '../components/CandidateSearch';
import './EmployerDashboard.css';

const EmployerDashboard = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const location = useLocation();

    const navItems = [
        { icon: <PlusCircle size={20} />, label: "Post New Job", path: "/employer" },
        { icon: <Users size={20} />, label: "Find Candidates", path: "/employer/candidates" },
        { icon: <Briefcase size={20} />, label: "My Jobs", path: "/employer/jobs" },
        { icon: <BarChart3 size={20} />, label: "Analytics", path: "/employer/analytics" },
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
                    <Route path="/" element={<PostJobForm />} />
                    <Route path="/candidates" element={<CandidateSearch />} />
                    <Route path="/jobs" element={<div>My Jobs (Coming Soon)</div>} />
                    <Route path="/analytics" element={<div>Analytics (Coming Soon)</div>} />
                </Routes>
            </main>
        </div>
    );
};

export default EmployerDashboard;
