import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sun, Moon, Briefcase } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import './Header.css';

const Header = () => {
    const { theme, toggleTheme } = useTheme();
    const navigate = useNavigate();

    return (
        <header className="header glass">
            <div className="header-content">
                <div className="logo" onClick={() => navigate('/')}>
                    <Briefcase className="logo-icon" />
                    <span className="logo-text">SkillSync</span>
                </div>

                <nav className="nav">
                    <Link to="/" className="nav-link">Home</Link>
                    <Link to="/dashboard" className="nav-link">Dashboard</Link>
                </nav>

                <div className="header-actions">
                    <button onClick={toggleTheme} className="theme-toggle" aria-label="Toggle theme">
                        {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Header;
