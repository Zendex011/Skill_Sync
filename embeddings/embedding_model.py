# embeddings/embedding_model.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import os

class EmbeddingModel:
    """
    Generate embeddings for resumes and job descriptions
    Using sentence-transformers (free, local, no API needed!)
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize embedding model
        
        Args:
            model_name: HuggingFace model name
                - 'all-MiniLM-L6-v2': Fast, good quality (DEFAULT)
                - 'all-mpnet-base-v2': Slower, better quality
                - 'paraphrase-multilingual': For multilingual support
        """
        print(f"📥 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ Model loaded | Dimension: {self.embedding_dim}")
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector (numpy array)
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts (faster than one-by-one)
        """
        embeddings = self.model.encode(
            texts, 
            convert_to_numpy=True,
            show_progress_bar=False
        )
        return embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """LangChain compatibility: embed multiple texts"""
        embeddings = self.encode_batch(texts)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """LangChain compatibility: embed single query"""
        embedding = self.encode_text(text)
        return embedding.tolist()

    def __call__(self, text: Union[str, List[str]]):
        """Allow calling the object directly"""
        if isinstance(text, str):
            return self.embed_query(text)
        else:
            return self.embed_documents(text)
    
    def encode_resume(self, resume) -> np.ndarray:
        """
        Generate embedding for resume
        Combines: skills + experience + projects
        
        Args:
            resume: Resume object from resume_parser
            
        Returns:
            Resume embedding vector
        """
        # Build comprehensive text representation
        parts = []
        
        # Skills (most important)
        if resume.technical_skills:
            parts.append("Skills: " + ", ".join(resume.technical_skills))
        
        # Experience
        for exp in resume.experience:
            parts.append(f"{exp.role} at {exp.company}")
            if exp.technologies:
                parts.append("Technologies: " + ", ".join(exp.technologies))
        
        # Projects
        for proj in resume.projects:
            parts.append(f"Project: {proj.title} - {proj.description}")
            if proj.technologies:
                parts.append("Tech: " + ", ".join(proj.technologies))
        
        # Education
        for edu in resume.education:
            parts.append(f"{edu.degree} from {edu.institution}")
        
        # Summary
        if resume.summary:
            parts.append(resume.summary)
        
        # Combine all parts
        resume_text = " | ".join(parts)
        
        return self.encode_text(resume_text)
    
    def encode_job(self, job) -> np.ndarray:
        """
        Generate embedding for job description
        Combines: skills + title + requirements
        
        Args:
            job: JobDescription object from jd_parser
            
        Returns:
            Job embedding vector
        """
        parts = []
        
        # Job title
        parts.append(f"Job: {job.job_title}")
        
        # Skills (most important)
        if job.technical_skills:
            parts.append("Required Skills: " + ", ".join(job.technical_skills))
        
        # Experience
        parts.append(f"Experience: {job.experience_required}")
        
        # Combine all parts
        job_text = " | ".join(parts)
        
        return self.encode_text(job_text)
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1, embedding2: Embedding vectors
            
        Returns:
            Similarity score (0 to 1, higher = more similar)
        """
        # Cosine similarity
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        return float(similarity)

# Global instance (load once, reuse)
_embedding_model = None

def get_embedding_model(model_name='all-MiniLM-L6-v2'):
    """Get global embedding model instance"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = EmbeddingModel(model_name)
    return _embedding_model