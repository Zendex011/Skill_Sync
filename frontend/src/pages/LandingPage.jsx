import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Zap, Map, Lightbulb, ArrowRight } from 'lucide-react';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    const features = [
        {
            icon: <Zap className="feat-icon" />,
            title: "Smart Matching",
            description: "AI analyzes your unique skills and experience to find the perfect role."
        },
        {
            icon: <Map className="feat-icon" />,
            title: "Learning Roadmap",
            description: "Get personalized upskilling plans tailored to your career goals."
        },
        {
            icon: <Lightbulb className="feat-icon" />,
            title: "Instant Insights",
            description: "Understand your fit with detailed explanations and gap analysis."
        }
    ];

    return (
        <div className="landing-page">
            <section className="hero">
                <div className="hero-content">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                        className="hero-title"
                    >
                        AI-Powered <span className="gradient-text">Resume-to-Job</span> Matching
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="hero-subtitle"
                    >
                        SkillSync bridges the gap between your talent and your dream career with precision AI matching and personalized growth paths.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.4 }}
                        className="hero-ctas"
                    >
                        <button className="btn btn-primary btn-lg" onClick={() => navigate('/dashboard')}>
                            Upload Resume <ArrowRight size={20} />
                        </button>
                        <button className="btn btn-secondary btn-lg" onClick={() => navigate('/dashboard/matches')}>
                            Find Jobs
                        </button>
                    </motion.div>
                </div>
                <div className="hero-bg-gradient"></div>
            </section>

            <section className="features">
                <div className="features-grid">
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="feature-card glass"
                        >
                            <div className="feature-icon-wrapper">
                                {feature.icon}
                            </div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </motion.div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default LandingPage;
