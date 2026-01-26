# rag/weighted_scorer.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
import math
from collections import defaultdict

class WeightedScorer:
    """
    Advanced scoring with multiple factors:
    1. Skill overlap (exact match)
    2. Experience match
    3. Title similarity
    4. Skill depth (core vs nice-to-have)
    """
    
    def __init__(self):
        # Scoring weights (must sum to 1.0)
        self.weights = {
            'skill_match': 0.40,      # 40% - Most important
            'semantic_similarity': 0.25,  # 25% - Context understanding
            'experience': 0.20,       # 20% - Experience level
            'title_similarity': 0.10,  # 10% - Job title match
            'skill_depth': 0.05       # 5% - Core vs optional skills
        }
    
    
    
    def calculate_skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """Calculate skill overlap with detailed metrics"""
        from skill_ontology import SkillOntology  # Lazy import
        
        # 1. Normalize ALL skills to canonical forms using Ontology FIRST
        # This handles aliases: "react.js" -> "React", "react" -> "React"
        resume_canonical = set(SkillOntology.normalize_skill(s) for s in resume_skills)
        job_canonical = set(SkillOntology.normalize_skill(s) for s in job_skills)
        
        # Remove empty strings if any
        resume_canonical.discard("")
        job_canonical.discard("")

        # 1.5 INFER PARENT SKILLS (The "Child Implies Parent" Logic)
        # If resume has "PyTorch" (Child), it implicitly has "Machine Learning" (Parent)
        inferred_skills = set()
        for skill in resume_canonical:
            # Check every parent in hierarchy
            for parent, children in SkillOntology.SKILL_HIERARCHY.items():
                # If the resume skill is a known child of this parent
                if skill in children:
                    # And the JOB requires this parent
                    if parent in job_canonical:
                        inferred_skills.add(parent)
        
        # Add inferred skills to resume set so they match
        resume_canonical.update(inferred_skills)

        
        # 2. Perform set operations on CANONICAL forms
        # We also lower() them just in case normalization missed some edge casing, 
        # but SkillOntology.normalize_skill should handle casing.
        # Let's trust the canonical forms are keyed correctly (Title Case usually).
        
        matched = resume_canonical & job_canonical
        missing = job_canonical - resume_canonical
        extra = resume_canonical - job_canonical
        
        # Calculate scores
        match_percentage = len(matched) / len(job_canonical) if job_canonical else 0
        bonus = min(0.1, len(extra) * 0.01)
        final_score = min(1.0, match_percentage + bonus)
            
        return {
            'score': final_score,
            'matched': sorted(list(matched)),
            'missing': sorted(list(missing)),
            'extra': sorted(list(extra)),
            'match_percentage': match_percentage,
            'num_matched': len(matched),
            'num_required': len(job_canonical)
        }
    
    def calculate_experience_score(self, resume_years: float, job_requirement: str) -> Dict:
        """Calculate experience match score"""
        job_min, job_max = self._parse_experience_requirement(job_requirement)
        
        if job_min is None:
            score = 1.0 if resume_years is not None else 0.5
            status = "Acceptable"
        elif resume_years is None:
            score = 0.5
            status = "Unknown"
        elif resume_years < job_min:
            gap = job_min - resume_years
            score = max(0.3, 1.0 - (gap * 0.15))
            status = f"Under-qualified by {gap:.1f} years"
        elif job_max and resume_years > job_max:
            excess = resume_years - job_max
            score = max(0.8, 1.0 - (excess * 0.05))
            status = f"Over-qualified by {excess:.1f} years"
        else:
            score = 1.0
            status = "Perfect match"
        
        return {
            'score': score,
            'resume_years': resume_years,
            'required_min': job_min,
            'required_max': job_max,
            'status': status
        }
    
    def _parse_experience_requirement(self, req_text: str) -> tuple:
        """Parse experience requirement text"""
        import re
        req_lower = req_text.lower().strip()
        if any(term in req_lower for term in ['entry', 'fresher', '0 year']):
            return (0, 2)
        if '+' in req_lower or 'more' in req_lower:
            match = re.search(r'(\d+)', req_lower)
            if match: return (int(match.group(1)), None)
        match = re.search(r'(\d+)\s*-\s*(\d+)', req_lower)
        if match: return (int(match.group(1)), int(match.group(2)))
        match = re.search(r'(\d+)', req_lower)
        if match:
            years = int(match.group(1))
            return (years, years + 2)
        return (None, None)
    
    def calculate_title_similarity(self, resume_roles: List[str], job_title: str) -> Dict:
        """Calculate job title similarity"""
        from embeddings.embedding_model import get_embedding_model
        model = get_embedding_model()
        if not resume_roles:
            return {'score': 0.5, 'best_match': None}
        
        job_embedding = model.encode_text(job_title.lower())
        best_score = 0
        best_role = None
        
        for role in resume_roles:
            role_embedding = model.encode_text(role.lower())
            sim = model.compute_similarity(job_embedding, role_embedding)
            if sim > best_score:
                best_score = sim
                best_role = role
        return {'score': best_score, 'best_match': best_role}
    
    def calculate_skill_depth_score(self, resume, job) -> Dict:
        """Evaluate skill depth"""
        skill_depth = defaultdict(int)
        resume_skills_lower = set(s.lower() for s in resume.technical_skills)
        for skill in resume_skills_lower:
            skill_depth[skill] += 1
            for exp in resume.experience:
                if skill in [t.lower() for t in exp.technologies]:
                    skill_depth[skill] += 2
            for proj in resume.projects:
                if skill in [t.lower() for t in proj.technologies]:
                    skill_depth[skill] += 1
        
        job_skills_lower = [s.lower() for s in job.technical_skills]
        if not job_skills_lower: return {'score': 0.5, 'depth_map': {}}
        total_depth = sum(skill_depth.get(skill, 0) for skill in job_skills_lower)
        max_possible = len(job_skills_lower) * 4
        return {'score': min(1.0, total_depth / max_possible) if max_possible > 0 else 0}
    
    def calculate_weighted_score(self, resume, job, semantic_score: float) -> Dict:
        """Final weighted score combining all factors"""
        skill_metrics = self.calculate_skill_match_score(resume.technical_skills, job.technical_skills)
        experience_metrics = self.calculate_experience_score(resume.total_experience_years, job.experience_required)
        resume_roles = [exp.role for exp in resume.experience]
        title_metrics = self.calculate_title_similarity(resume_roles, job.job_title)
        depth_metrics = self.calculate_skill_depth_score(resume, job)
        
        total_score = (
            self.weights['skill_match'] * skill_metrics['score'] +
            self.weights['semantic_similarity'] * semantic_score +
            self.weights['experience'] * experience_metrics['score'] +
            self.weights['title_similarity'] * title_metrics['score'] +
            self.weights['skill_depth'] * depth_metrics['score']
        )
        
        return {
            'total_score': total_score,
            'breakdown': {
                'skill_match': {'score': skill_metrics['score'], 'weight': self.weights['skill_match'], 'details': skill_metrics},
                'semantic_similarity': {'score': semantic_score, 'weight': self.weights['semantic_similarity']},
                'experience': {'score': experience_metrics['score'], 'weight': self.weights['experience'], 'details': experience_metrics},
                'title_similarity': {'score': title_metrics['score'], 'weight': self.weights['title_similarity'], 'details': title_metrics},
                'skill_depth': {'score': depth_metrics['score'], 'weight': self.weights['skill_depth']}
            }
        }

    def format_simple_output(self, scoring_result: Dict) -> str:
        """Clean output for users"""
        lines = []
        overall = scoring_result['total_score'] * 100
        semantic = scoring_result['breakdown']['semantic_similarity']['score'] * 100
        skill_score = scoring_result['breakdown']['skill_match']['score'] * 100
        sm_details = scoring_result['breakdown']['skill_match']['details']
        
        lines.append(f"🎯 Overall Match: {overall:.1f}%")
        lines.append(f"   \u2022 Semantic Similarity: {semantic:.1f}%")
        lines.append(f"   \u2022 Skill Match: {skill_score:.1f}%")
        lines.append(f"   \u2022 Skills Matched: {sm_details['num_matched']}/{sm_details['num_required']}")
        
        if sm_details['matched']:
            lines.append(f"\n✅ Matched Skills ({len(sm_details['matched'])}):")
            for skill in sorted(sm_details['matched']):
                lines.append(f"   \u2022 {skill.title()}")
        
        if sm_details['missing']:
            lines.append(f"\n❌ Missing Skills ({len(sm_details['missing'])}):")
            for skill in sorted(sm_details['missing']):
                lines.append(f"   \u2022 {skill.title()}")
        return "\n".join(lines)