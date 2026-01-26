import React from 'react';
import { Linkedin, Github, Heart } from 'lucide-react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer glass">
            <div className="footer-content">
                <div className="footer-info">
                    <p>© 2026 SkillSync. Built with <Heart size={14} className="heart-icon" /> by Ansh Goel</p>
                </div>
                <div className="footer-links">
                    <a href="https://www.linkedin.com/in/ansh-goel-536713282/" target="_blank" rel="noopener noreferrer" className="social-link">
                        <Linkedin size={20} />
                        <span>LinkedIn</span>
                    </a>
                    <a href="https://github.com/Zendex011" target="_blank" rel="noopener noreferrer" className="social-link">
                        <Github size={20} />
                        <span>GitHub</span>
                    </a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
