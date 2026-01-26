# embeddings/vector_store.py
import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple, Optional

class VectorStore:
    """
    FAISS-based vector store for fast similarity search
    Stores job/resume embeddings and enables quick retrieval
    """
    
    def __init__(self, embedding_dim: int = 384):
        """
        Initialize vector store
        
        Args:
            embedding_dim: Dimension of embeddings (384 for MiniLM)
        """
        self.embedding_dim = embedding_dim
        
        # FAISS index for fast similarity search
        self.index = faiss.IndexFlatIP(embedding_dim)  # Inner Product = Cosine for normalized vectors
        
        # Metadata storage
        self.ids = []  # List of IDs
        self.metadata = {}  # ID -> metadata dict
        
        print(f"✅ Vector store initialized | Dimension: {embedding_dim}")
    
    def add(self, embedding: np.ndarray, id: str, metadata: dict = None):
        """
        Add single embedding to store
        
        Args:
            embedding: Embedding vector
            id: Unique identifier
            metadata: Optional metadata (e.g., file path, parsed object)
        """
        # Normalize embedding for cosine similarity
        embedding = embedding / np.linalg.norm(embedding)
        
        # Add to FAISS index
        self.index.add(np.array([embedding], dtype=np.float32))
        
        # Store ID and metadata
        self.ids.append(id)
        if metadata:
            self.metadata[id] = metadata
    
    def add_batch(self, embeddings: np.ndarray, ids: List[str], metadata_list: List[dict] = None):
        """
        Add multiple embeddings to store
        
        Args:
            embeddings: Matrix of embeddings (n × embedding_dim)
            ids: List of unique identifiers
            metadata_list: Optional list of metadata dicts
        """
        # Normalize embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / norms
        
        # Add to FAISS index
        self.index.add(embeddings.astype(np.float32))
        
        # Store IDs and metadata
        self.ids.extend(ids)
        if metadata_list:
            for id, meta in zip(ids, metadata_list):
                self.metadata[id] = meta
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """
        Search for k most similar embeddings
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            
        Returns:
            List of (id, similarity_score) tuples
        """
        # Normalize query
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search
        scores, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32), 
            k
        )
        
        # Return results
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.ids):  # Valid index
                results.append((self.ids[idx], float(score)))
        
        return results
    
    def get_metadata(self, id: str) -> Optional[dict]:
        """Get metadata for an ID"""
        return self.metadata.get(id)
    
    def save(self, directory: str, name: str = "vector_store"):
        """
        Save vector store to disk
        
        Args:
            directory: Directory to save to
            name: Base name for files
        """
        os.makedirs(directory, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, f"{directory}/{name}.index")
        
        # Save metadata
        with open(f"{directory}/{name}_metadata.pkl", 'wb') as f:
            pickle.dump({
                'ids': self.ids,
                'metadata': self.metadata,
                'embedding_dim': self.embedding_dim
            }, f)
        
        print(f"✅ Vector store saved to {directory}/{name}")
    
    @classmethod
    def load(cls, directory: str, name: str = "vector_store"):
        """
        Load vector store from disk
        
        Args:
            directory: Directory to load from
            name: Base name for files
            
        Returns:
            VectorStore instance
        """
        # Load metadata
        with open(f"{directory}/{name}_metadata.pkl", 'rb') as f:
            data = pickle.load(f)
        
        # Create instance
        store = cls(embedding_dim=data['embedding_dim'])
        
        # Load FAISS index
        store.index = faiss.read_index(f"{directory}/{name}.index")
        
        # Restore metadata
        store.ids = data['ids']
        store.metadata = data['metadata']
        
        print(f"✅ Vector store loaded from {directory}/{name}")
        print(f"   Contains {len(store.ids)} vectors")
        
        return store
    
    def __len__(self):
        """Number of vectors in store"""
        return len(self.ids)