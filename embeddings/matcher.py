# embeddings/matcher.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embeddings.embedding_model import get_embedding_model
from embeddings.vector_store import VectorStore
from typing import List, Tuple, Dict
from skill_ontology import SkillOntology
import numpy as np

class ResumeJobMatcher:
    """
    Match resumes to jobs using:
    1. Semantic similarity (embeddings)
    2. Skill overlap (exact matching)
    3. Combined scoring
    """
    
    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.job_store = None
        self.resume_store = None
    
    def build_job_index(self, jobs: List[Tuple[str, any]]):
        """
        Build vector index for jobs
        
        Args:
            jobs: List of (job_id, job_object) tuples
        """
        print(f"🔨 Building job index for {len(jobs)} jobs...")
        
        self.job_store = VectorStore(embedding_dim=self.embedding_model.embedding_dim)
        
        for job_id, job in jobs:
            embedding = self.embedding_model.encode_job(job)
            self.job_store.add(
                embedding, 
                job_id,
                metadata={'job': job}
            )
        
        print(f"✅ Job index built | {len(self.job_store)} jobs indexed")
    
    def build_resume_index(self, resumes: List[Tuple[str, any]]):
        """
        Build vector index for resumes
        
        Args:
            resumes: List of (resume_id, resume_object) tuples
        """
        print(f"🔨 Building resume index for {len(resumes)} resumes...")
        
        self.resume_store = VectorStore(embedding_dim=self.embedding_model.embedding_dim)
        
        for resume_id, resume in resumes:
            embedding = self.embedding_model.encode_resume(resume)
            self.resume_store.add(
                embedding,
                resume_id,
                metadata={'resume': resume}
            )
        
        print(f"✅ Resume index built | {len(self.resume_store)} resumes indexed")
    
    def calculate_skill_overlap(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """
        Calculate skill overlap metrics
        
        Returns:
            Dict with matched, missing, extra skills and scores
        """
        resume_set = set(resume_skills)
        job_set = set(job_skills)
        
        # Skill Hierarchy Logic: Parent requirements can be met by specialized child skills
        matched = set()
        for job_skill in job_set:
            # Get all specialized/equivalent skills for this job requirement
            equivalent_skills = SkillOntology.get_equivalent_skills(job_skill)
            
            # If any of these specialized skills exist in the resume, it's a match
            if any(req_skill in resume_set for req_skill in equivalent_skills):
                matched.add(job_skill)
        
        missing = job_set - matched
        extra = resume_set - matched
        
        # Calculate scores
        skill_match_score = len(matched) / len(job_set) if job_set else 0
        skill_coverage = len(matched) / len(resume_set) if resume_set else 0
        
        return {
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'extra_skills': list(extra),
            'skill_match_score': skill_match_score,
            'skill_coverage': skill_coverage,
            'num_matched': len(matched),
            'num_required': len(job_set)
        }
    
    def match_resume_to_jobs(self, resume, top_k: int = 10) -> List[Dict]:
        """
        Find top K matching jobs for a resume
        
        Args:
            resume: Resume object
            top_k: Number of jobs to return
            
        Returns:
            List of match results with scores
        """
        if self.job_store is None:
            raise ValueError("Job index not built. Call build_job_index() first.")
        
        # Generate resume embedding
        resume_embedding = self.embedding_model.encode_resume(resume)
        
        # Semantic search
        candidates = self.job_store.search(resume_embedding, k=top_k)
        
        # Calculate detailed scores
        results = []
        for job_id, semantic_score in candidates:
            job = self.job_store.get_metadata(job_id)['job']
            
            # Skill overlap
            skill_metrics = self.calculate_skill_overlap(
                resume.technical_skills,
                job.technical_skills
            )
            
            # Combined score (weighted average)
            combined_score = (
                0.6 * semantic_score +  # 60% semantic similarity
                0.4 * skill_metrics['skill_match_score']  # 40% skill match
            )
            
            results.append({
                'job_id': job_id,
                'job': job,
                'semantic_score': semantic_score,
                'skill_match_score': skill_metrics['skill_match_score'],
                'combined_score': combined_score,
                'matched_skills': skill_metrics['matched_skills'],
                'missing_skills': skill_metrics['missing_skills'],
                'num_matched': skill_metrics['num_matched'],
                'num_required': skill_metrics['num_required']
            })
        
        # Sort by combined score
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return results
    
    def match_job_to_resumes(self, job, top_k: int = 10) -> List[Dict]:
        """
        Find top K matching resumes for a job
        
        Args:
            job: JobDescription object
            top_k: Number of resumes to return
            
        Returns:
            List of match results with scores
        """
        if self.resume_store is None:
            raise ValueError("Resume index not built. Call build_resume_index() first.")
        
        # Generate job embedding
        job_embedding = self.embedding_model.encode_job(job)
        
        # Semantic search
        candidates = self.resume_store.search(job_embedding, k=top_k)
        
        # Calculate detailed scores
        results = []
        for resume_id, semantic_score in candidates:
            resume = self.resume_store.get_metadata(resume_id)['resume']
            
            # Skill overlap
            skill_metrics = self.calculate_skill_overlap(
                resume.technical_skills,
                job.technical_skills
            )
            
            # Combined score
            combined_score = (
                0.6 * semantic_score +
                0.4 * skill_metrics['skill_match_score']
            )
            
            results.append({
                'resume_id': resume_id,
                'resume': resume,
                'semantic_score': semantic_score,
                'skill_match_score': skill_metrics['skill_match_score'],
                'combined_score': combined_score,
                'matched_skills': skill_metrics['matched_skills'],
                'missing_skills': skill_metrics['missing_skills'],
                'num_matched': skill_metrics['num_matched'],
                'num_required': skill_metrics['num_required']
            })
        
        # Sort by combined score
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return results
    
    def explain_match(self, result: Dict) -> str:
        """Generate human-readable explanation of match"""
        explanation = []
        
        explanation.append(f"🎯 Overall Match: {result['combined_score']*100:.1f}%")
        explanation.append(f"   • Semantic Similarity: {result['semantic_score']*100:.1f}%")
        explanation.append(f"   • Skill Match: {result['skill_match_score']*100:.1f}%")
        explanation.append(f"   • Skills Matched: {result['num_matched']}/{result['num_required']}")
        
        if result['matched_skills']:
            explanation.append(f"\n✅ Matched Skills ({len(result['matched_skills'])}):")
            for skill in result['matched_skills'][:10]:
                explanation.append(f"   • {skill}")
        
        if result['missing_skills']:
            explanation.append(f"\n❌ Missing Skills ({len(result['missing_skills'])}):")
            for skill in result['missing_skills'][:10]:
                explanation.append(f"   • {skill}")
        
        return "\n".join(explanation)