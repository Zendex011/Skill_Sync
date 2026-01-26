# rag/rag_explainer.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from embeddings.embedding_model import get_embedding_model
from typing import List, Dict
import numpy as np

class RAGExplainer:
    """
    RAG-powered explanation system
    
    Uses:
    1. Vector DB to retrieve relevant resume/job chunks
    2. LLM to generate natural language explanations
    """
    
    def __init__(self):
        # Initialize LLM
        endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="conversational",
            temperature=0.3,  # Slightly higher for more natural explanations
            huggingfacehub_api_token=os.getenv("HF_TOKEN")
        )
        
        self.llm = ChatHuggingFace(llm=endpoint, temperature=0.3)
        
        # Initialize embedding model
        self.embedding_model = get_embedding_model()
        
        # Vector store for resume chunks (for retrieval)
        self.resume_chunks_store = None
    
    def chunk_resume(self, resume) -> List[Dict]:
        """
        Break resume into meaningful chunks for RAG
        """
        chunks = []
        
        # Chunk 1: Skills summary
        if resume.technical_skills:
            chunks.append({
                'content': f"Technical Skills: {', '.join(resume.technical_skills)}",
                'type': 'skills',
                'metadata': {'skills': resume.technical_skills}
            })
        
        # Chunk 2-N: Each work experience
        for i, exp in enumerate(resume.experience):
            content = f"{exp.role} at {exp.company} ({exp.duration})"
            if exp.technologies:
                content += f"\nTechnologies: {', '.join(exp.technologies)}"
            if exp.description:
                content += f"\n{exp.description}"
            
            chunks.append({
                'content': content,
                'type': 'experience',
                'metadata': {'company': exp.company, 'role': exp.role}
            })
        
        # Chunk N+1-M: Each project
        for proj in resume.projects:
            content = f"Project: {proj.title}\n{proj.description}"
            if proj.technologies:
                content += f"\nTechnologies: {', '.join(proj.technologies)}"
            
            chunks.append({
                'content': content,
                'type': 'project',
                'metadata': {'title': proj.title}
            })
        
        # Chunk M+1: Education
        for edu in resume.education:
            chunks.append({
                'content': f"{edu.degree} from {edu.institution} ({edu.duration})",
                'type': 'education',
                'metadata': {'degree': edu.degree}
            })
        
        return chunks
    
    def build_resume_vector_store(self, resume) -> FAISS:
        """Build FAISS vector store from resume chunks"""
        chunks = self.chunk_resume(resume)
        
        if not chunks:
            return None
        
        # Extract texts and metadata
        texts = [chunk['content'] for chunk in chunks]
        metadatas = [{'type': chunk['type'], **chunk.get('metadata', {})} for chunk in chunks]
        
        # Create FAISS vector store
        vectorstore = FAISS.from_texts(
            texts,
            self.embedding_model,  # Use compliant wrapper
            metadatas=metadatas
        )
        
        return vectorstore
    
    def retrieve_relevant_context(self, vectorstore: FAISS, query: str, k: int = 3) -> List[Dict]:
        """Retrieve relevant resume chunks based on query"""
        if vectorstore is None:
            return []
        
        # Similarity search
        results = vectorstore.similarity_search_with_score(query, k=k)
        
        context = []
        for doc, score in results:
            context.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'relevance_score': float(score)
            })
        
        return context
    
    def explain_match(self, resume, job, match_score: float, 
                     matched_skills: List[str], missing_skills: List[str]) -> str:
        """
        Generate natural language explanation of match using RAG
        """
        # Build vector store for this resume
        vectorstore = self.build_resume_vector_store(resume)
        
        # Query 1: Retrieve context about matched skills
        matched_context = self.retrieve_relevant_context(
            vectorstore,
            f"experience with {', '.join(matched_skills[:5])}"
        ) if matched_skills else []
        
        # Build context string
        context_parts = []
        if matched_context:
            context_parts.append("Relevant experience:")
            for ctx in matched_context[:2]:
                context_parts.append(f"- {ctx['content']}")
        
        context_str = "\n".join(context_parts) if context_parts else "No specific experience found."
        
        # Create prompt
        prompt = PromptTemplate(
            input_variables=["match_score", "job_title", "matched_skills","missing_skills", "context"],
            template="""You are a career advisor explaining why a candidate is a good/bad fit for a job.
Job Title: {job_title}
Match Score: {match_score}%
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}

Candidate's Relevant Background:
{context}

Provide a short, 2-3 sentence explanation covering:
- Why they fit (core strengths)
- Key gaps (missing requirements)
- Final verdict

Keep it extremely concise and professional.
Explanation:"""
        )

        formatted_prompt = prompt.format(
            match_score=f"{match_score*100:.1f}",
            job_title=job.job_title,
            matched_skills=", ".join(matched_skills[:8]) if matched_skills else "None",
            missing_skills=", ".join(missing_skills[:8]) if missing_skills else "None",
            context=context_str
        )
        
        try:
            response = self.llm.invoke(formatted_prompt)
            explanation = response.content.strip()
            return explanation
        except Exception as e:
            print(f"⚠️ LLM explanation failed: {e}")
            return self._fallback_explanation(match_score, matched_skills, missing_skills)

    def _fallback_explanation(self, match_score: float, 
                             matched_skills: List[str], 
                             missing_skills: List[str]) -> str:
        """Fallback template-based explanation if LLM fails"""
        if match_score >= 0.7:
            return f"Strong match! You have {len(matched_skills)} out of the key skills required. " \
                   f"You're well-qualified for this role. Consider highlighting your experience with " \
                   f"{', '.join(matched_skills[:3])} in your application. " \
                   f"Learning {', '.join(missing_skills[:2])} would make you an even stronger candidate."
        elif match_score >= 0.5:
            return f"Moderate match. You possess {len(matched_skills)} relevant skills which is a good foundation. " \
                   f"However, you're missing {len(missing_skills)} skills that are important for this role. " \
                   f"Consider applying if you're willing to quickly learn {', '.join(missing_skills[:2])}."
        else:
            return f"This role requires significant skill development. You match only {len(matched_skills)} skills " \
                   f"and are missing {len(missing_skills)} key requirements including {', '.join(missing_skills[:3])}. " \
                   f"Consider roles that better match your current skillset or invest time in upskilling first."

    def explain_why_not_fit(self, resume, job, scoring_result: Dict) -> str:
        """
        Deep dive: Why is this NOT a good fit?
        """
        breakdown = scoring_result['breakdown']
        
        # Find weak points
        weak_factors = []
        for factor, metrics in breakdown.items():
            if metrics['score'] < 0.6:  # Below 60%
                weak_factors.append((factor, metrics))
        
        if not weak_factors:
            return "This is actually a good fit! All major factors score above 60%."
        
        # Get context for weakest factor
        weakest_factor, weakest_metrics = min(weak_factors, key=lambda x: x[1]['score'])
        
        prompt = PromptTemplate(
            input_variables=["job_title", "weak_factor", "score", "details"],
            template="""Explain why a candidate is NOT a good fit for a job based on this weakness:
Job: {job_title}
Weak Area: {weak_factor}
Score: {score}%
Details: {details}

Provide a brief assessment in bullet points (max 3 bullets) of why this is a problem.
Explanation:"""
        )

        details_str = str(weakest_metrics.get('details', 'Low match'))
        
        formatted_prompt = prompt.format(
            job_title=job.job_title,
            weak_factor=weakest_factor.replace('_', ' ').title(),
            score=f"{weakest_metrics['score']*100:.1f}",
            details=details_str
        )
        
        try:
            response = self.llm.invoke(formatted_prompt)
            return response.content.strip()
        except Exception as e:
            return f"The main issue is {weakest_factor.replace('_', ' ')} (scoring only {weakest_metrics['score']*100:.0f}%). This significantly impacts your candidacy."
