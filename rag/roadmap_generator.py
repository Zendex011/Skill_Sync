# rag/roadmap_generator.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict
from collections import defaultdict
import json

class LearningRoadmapGenerator:
    """
    Generate personalized learning roadmap based on skill gaps
    Prioritizes skills: Critical → Important → Nice-to-have
    """
    
    def __init__(self):
        # Skill categories and learning times (in weeks)
        self.skill_learning_time = {
            # Programming languages
            'python': 4,
            'java': 6,
            'javascript': 4,
            'sql': 3,
            'r': 4,
            
            # ML/DL frameworks
            'tensorflow': 3,
            'pytorch': 3,
            'scikit-learn': 2,
            'keras': 2,
            
            # Cloud
            'aws': 4,
            'azure': 4,
            'gcp': 4,
            'google cloud platform': 4,
            
            # DevOps
            'docker': 2,
            'kubernetes': 3,
            'git': 1,
            'jenkins': 2,
            
            # Databases
            'mongodb': 2,
            'postgresql': 2,
            'mysql': 2,
            'redis': 2,
            
            # Web frameworks
            'react': 3,
            'angular': 4,
            'django': 3,
            'flask': 2,
            'fastapi': 2,
            
            # Data tools
            'pandas': 2,
            'numpy': 2,
            'tableau': 3,
            'power bi': 3,
            
            # ML concepts
            'machine learning': 6,
            'deep learning': 8,
            'natural language processing': 6,
            'computer vision': 6,
            'mlops': 4,
        }
        
        # Learning resources
        self.resources = self._load_resources()
    
    def _load_resources(self) -> Dict:
        """Load learning resources (can be from file/database)"""
        return {
            'python': {
                'beginner': ['Python.org Tutorial', 'Codecademy Python'],
                'intermediate': ['Real Python', 'Python Crash Course (Book)'],
                'advanced': ['Fluent Python (Book)', 'Python Cookbook']
            },
            'machine learning': {
                'beginner': ['Coursera: ML by Andrew Ng', 'fast.ai'],
                'intermediate': ['Hands-On ML (Book)', 'Kaggle Learn'],
                'advanced': ['Deep Learning Specialization', 'Research Papers']
            },
            'tensorflow': {
                'beginner': ['TensorFlow.org Tutorials', 'TensorFlow in Practice'],
                'intermediate': ['TensorFlow Developer Certificate', 'Advanced TensorFlow'],
                'advanced': ['Custom Model Development', 'TensorFlow Extended (TFX)']
            },
            'aws': {
                'beginner': ['AWS Cloud Practitioner', 'AWS Free Tier Hands-on'],
                'intermediate': ['AWS Solutions Architect', 'A Cloud Guru'],
                'advanced': ['AWS Professional Certifications', 'Well-Architected Framework']
            },
            'docker': {
                'beginner': ['Docker Getting Started', 'Docker for Beginners'],
                'intermediate': ['Docker Mastery Course', 'Multi-container Apps'],
                'advanced': ['Docker in Production', 'Container Orchestration']
            },
            # Add more as needed...
        }
    
    def categorize_skills(self, missing_skills: List[str], job_title: str) -> Dict:
        """
        Categorize missing skills by priority
        
        Returns:
            {
                'critical': [],     # Must-have for role
                'important': [],    # Should-have
                'nice_to_have': []  # Good-to-have
            }
        """
        # Core skills by job role
        role_core_skills = {
            'data scientist': ['python', 'machine learning', 'sql', 'statistics'],
            'ml engineer': ['python', 'tensorflow', 'pytorch', 'docker', 'mlops'],
            'data analyst': ['sql', 'excel', 'tableau', 'python'],
            'data engineer': ['python', 'sql', 'spark', 'aws', 'airflow'],
            'software engineer': ['python', 'java', 'git', 'sql'],
            'frontend developer': ['javascript', 'react', 'css', 'html'],
            'backend developer': ['python', 'java', 'sql', 'api', 'docker'],
            'devops engineer': ['docker', 'kubernetes', 'aws', 'jenkins', 'terraform'],
        }
        
        # Determine role category
        job_lower = job_title.lower()
        role_category = None
        for role, skills in role_core_skills.items():
            if role in job_lower:
                role_category = skills
                break
        
        if not role_category:
            # Default: treat first 50% as critical
            split_point = len(missing_skills) // 2
            return {
                'critical': missing_skills[:split_point],
                'important': missing_skills[split_point:],
                'nice_to_have': []
            }
        
        # Categorize based on role
        categorized = {
            'critical': [],
            'important': [],
            'nice_to_have': []
        }
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            if skill_lower in role_category:
                categorized['critical'].append(skill)
            elif any(core in skill_lower for core in role_category):
                categorized['important'].append(skill)
            else:
                categorized['nice_to_have'].append(skill)
        
        return categorized
    
    def estimate_learning_time(self, skill: str) -> int:
        """Estimate learning time in weeks"""
        skill_lower = skill.lower()
        return self.skill_learning_time.get(skill_lower, 4)  # Default: 4 weeks
    
    def generate_roadmap(self, missing_skills: List[str], job_title: str, 
                        has_skills: List[str] = None) -> Dict:
        """
        Generate complete learning roadmap
        
        Args:
            missing_skills: Skills to learn
            job_title: Target job title
            has_skills: Current skills (for context)
            
        Returns:
            Structured roadmap with timeline and resources
        """
        # Categorize skills
        categorized = self.categorize_skills(missing_skills, job_title)
        
        # Build roadmap phases
        roadmap = {
            'summary': {
                'total_skills': len(missing_skills),
                'critical': len(categorized['critical']),
                'important': len(categorized['important']),
                'nice_to_have': len(categorized['nice_to_have']),
                'estimated_weeks': 0
            },
            'phases': []
        }
        
        current_week = 0
        
        # Phase 1: Critical skills (Weeks 0-8)
        if categorized['critical']:
            phase1 = self._build_phase(
                "Phase 1: Critical Skills",
                categorized['critical'],
                current_week,
                max_weeks=8,
                description="Must-have skills for the role"
            )
            roadmap['phases'].append(phase1)
            current_week = phase1['end_week']
        
        # Phase 2: Important skills (Weeks 8-16)
        if categorized['important']:
            phase2 = self._build_phase(
                "Phase 2: Important Skills",
                categorized['important'],
                current_week,
                max_weeks=8,
                description="Highly valuable skills"
            )
            roadmap['phases'].append(phase2)
            current_week = phase2['end_week']
        
        # Phase 3: Nice-to-have (Weeks 16+)
        if categorized['nice_to_have']:
            phase3 = self._build_phase(
                "Phase 3: Nice-to-Have Skills",
                categorized['nice_to_have'],
                current_week,
                max_weeks=12,
                description="Additional skills for competitive edge"
            )
            roadmap['phases'].append(phase3)
            current_week = phase3['end_week']
        
        roadmap['summary']['estimated_weeks'] = current_week
        
        return roadmap
    
    def _build_phase(self, phase_name: str, skills: List[str], 
                    start_week: int, max_weeks: int, description: str) -> Dict:
        """Build a learning phase"""
        phase = {
            'name': phase_name,
            'description': description,
            'start_week': start_week,
            'end_week': start_week,
            'skills': []
        }
        
        weeks_used = 0
        
        for skill in skills:
            learning_time = self.estimate_learning_time(skill)
            
            # Don't exceed max_weeks for this phase
            if weeks_used + learning_time > max_weeks and weeks_used > 0:
                break
            
            skill_plan = {
                'name': skill,
                'weeks': learning_time,
                'start_week': start_week + weeks_used,
                'end_week': start_week + weeks_used + learning_time,
                'resources': self._get_resources(skill)
            }
            
            phase['skills'].append(skill_plan)
            weeks_used += learning_time
        
        phase['end_week'] = start_week + weeks_used
        
        return phase
    
    def _get_resources(self, skill: str) -> Dict:
        """Get learning resources for a skill"""
        skill_lower = skill.lower()
        if skill_lower in self.resources:
            return self.resources[skill_lower]
        else:
            return {
                'beginner': [
                    f'https://www.youtube.com/results?search_query={skill.replace(" ", "+")}+tutorial+for+beginners',
                    f'Search: "{skill} tutorial for beginners"'
                ],
                'intermediate': [
                    f'https://www.youtube.com/results?search_query={skill.replace(" ", "+")}+advanced+course',
                    f'Search: "{skill} intermediate course"'
                ],
                'advanced': [
                    f'https://www.youtube.com/results?search_query={skill.replace(" ", "+")}+best+practices',
                    f'Search: "{skill} best practices"'
                ]
            }
    
    def format_roadmap(self, roadmap: Dict) -> str:
        """Format roadmap for display"""
        lines = []
        
        lines.append("📚 PERSONALIZED LEARNING ROADMAP")
        lines.append("=" * 60)
        
        # Summary
        summary = roadmap['summary']
        lines.append(f"\n📊 Summary:")
        lines.append(f"  Total skills to learn: {summary['total_skills']}")
        lines.append(f"  Critical: {summary['critical']} | Important: {summary['important']} | Nice-to-have: {summary['nice_to_have']}")
        lines.append(f"  Estimated time: {summary['estimated_weeks']} weeks (~{summary['estimated_weeks']/4:.1f} months)")
        
        # Phases
        for phase in roadmap['phases']:
            lines.append(f"\n{'='*60}")
            lines.append(f"{phase['name']}")
            lines.append(f"Week {phase['start_week']} - Week {phase['end_week']}")
            lines.append(f"{phase['description']}")
            lines.append('-' * 60)
            
            for skill_plan in phase['skills']:
                lines.append(f"\n  📖 {skill_plan['name']}")
                lines.append(f"     Duration: {skill_plan['weeks']} weeks (Week {skill_plan['start_week']}-{skill_plan['end_week']})")
                
                resources = skill_plan['resources']
                if 'beginner' in resources:
                    lines.append(f"     Beginner: {', '.join(resources['beginner'][:2])}")
        
        return "\n".join(lines)