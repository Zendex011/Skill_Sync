# embeddings/matcher_enhanced.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from embeddings.matcher import ResumeJobMatcher
from rag.weighted_scorer import WeightedScorer
from rag.rag_explainer import RAGExplainer
from rag.roadmap_generator import LearningRoadmapGenerator
from jd_parser.jd_parser import HybridJDParser
from resume_parser.resume_parser import ResumeParser

class MatcherEnhanced:
    """
    Production-level integration of all matching and RAG components.
    Provides a single entry point for parsing, matching, and explanation.
    """
    
    def __init__(self):
        self.matcher = ResumeJobMatcher()
        self.scorer = WeightedScorer()
        self.explainer = RAGExplainer()
        self.roadmap_gen = LearningRoadmapGenerator()
        
        self.jd_parser = HybridJDParser()
        self.resume_parser = ResumeParser(normalize_skills=True)
        
    def match_resume_to_job_text(self, resume_obj, job_text: str) -> Dict:
        """
        Full pipeline: Parse Job -> Semantic Match -> Weighted Score -> RAG Explanation -> Roadmap.
        """
        # 1. Parse Job
        job = self.jd_parser.parse(job_text)
        
        # 2. Get Semantic Score
        # We use the existing matcher logic for consistency with the vector store
        # Here we do a 1-to-1 match for simplicity in this specific method
        job_embedding = self.matcher.embedding_model.encode_job(job)
        resume_embedding = self.matcher.embedding_model.encode_resume(resume_obj)
        semantic_score = self.matcher.embedding_model.compute_similarity(job_embedding, resume_embedding)
        
        # 3. Calculate Weighted Score
        scoring_result = self.scorer.calculate_weighted_score(resume_obj, job, semantic_score)
        
        # 4. Generate RAG Explanation
        matched_skills = scoring_result['breakdown']['skill_match']['details']['matched']
        missing_skills = scoring_result['breakdown']['skill_match']['details']['missing']
        
        explanation = self.explainer.explain_match(
            resume_obj, job,
            scoring_result['total_score'],
            matched_skills,
            missing_skills
        )
        
        # 5. Why Not Fit (if score < 0.8)
        why_not_fit = None
        if scoring_result['total_score'] < 0.8:
            why_not_fit = self.explainer.explain_why_not_fit(resume_obj, job, scoring_result)
            
        # 6. Learning Roadmap
        roadmap = None
        if missing_skills:
            roadmap = self.roadmap_gen.generate_roadmap(
                missing_skills, 
                job.job_title, 
                resume_obj.technical_skills
            )
            
        return {
            'job': job,
            'resume': resume_obj,
            'scoring_result': scoring_result,
            'explanation': explanation,
            'why_not_fit': why_not_fit,
            'roadmap': roadmap
        }

    def display_rich_result(self, result: Dict):
        """Prints a beautified version of the result."""
        job = result['job']
        scoring = result['scoring_result']
        
        print("\n" + "🚀" + " " + "="*58)
        print(f"ENHANCED MATCH RESULT: {job.job_title}")
        print("="*60)
        
        print(self.scorer.format_score_breakdown(scoring))
        
        print("\n💬 AI Insight:")
        print("-" * 60)
        print(result['explanation'])
        
        if result['why_not_fit']:
            print("\n💡 Area for Improvement:")
            print("-" * 60)
            print(result['why_not_fit'])
            
        if result['roadmap']:
            print("\n" + self.roadmap_gen.format_roadmap(result['roadmap']))
        
        print("\n" + "="*60 + "\n")
