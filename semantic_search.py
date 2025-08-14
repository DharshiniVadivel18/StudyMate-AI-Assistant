"""
Semantic search module for StudyMate
Handles document indexing and similarity search using SentenceTransformers + FAISS
"""

from typing import List, Tuple
import random
import numpy as np
from .document_processor import DocumentChunk

class SemanticSearch:
    """Handles semantic search functionality using SentenceTransformers and FAISS"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.document_chunks: List[DocumentChunk] = []
        self.embeddings = None
        self.index = None
        self.model = None
        
        if not self.demo_mode:
            self._initialize_models()
    
    def _initialize_models(self):
        """Initialize SentenceTransformers and FAISS"""
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            
            # Load the embedding model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("SentenceTransformer model loaded successfully")
            
        except ImportError as e:
            print(f"Warning: Required libraries not installed ({e}). Falling back to demo mode.")
            self.demo_mode = True
        except Exception as e:
            print(f"Error initializing models: {e}. Falling back to demo mode.")
            self.demo_mode = True
    
    def index_documents(self, chunks: List[DocumentChunk]) -> None:
        """
        Index document chunks for semantic search
        
        Args:
            chunks: List of document chunks to index
        """
        self.document_chunks = chunks
        
        if self.demo_mode:
            # In demo mode, just store the chunks
            print(f"Demo mode: Indexed {len(chunks)} document chunks")
        else:
            self._create_faiss_index(chunks)
    
    def _create_faiss_index(self, chunks: List[DocumentChunk]) -> None:
        """Create FAISS index from document chunks"""
        try:
            import faiss
            
            if not chunks:
                return
            
            # Extract text from chunks
            texts = [chunk.text for chunk in chunks]
            
            # Generate embeddings
            print(f"Generating embeddings for {len(texts)} chunks...")
            embeddings = self.model.encode(texts, show_progress_bar=True)
            self.embeddings = embeddings
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add embeddings to index
            self.index.add(embeddings.astype('float32'))
            
            print(f"FAISS index created with {self.index.ntotal} vectors")
            
        except Exception as e:
            print(f"Error creating FAISS index: {e}")
            self.demo_mode = True
    
    def search(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """
        Search for relevant document chunks
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant document chunks
        """
        if self.demo_mode:
            return self._demo_search(query, top_k)
        else:
            return self._semantic_search(query, top_k)
    
    def _semantic_search(self, query: str, top_k: int) -> List[DocumentChunk]:
        """Real semantic search using FAISS"""
        try:
            import faiss
            
            if not self.index or not self.document_chunks:
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search in FAISS index
            scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
            
            # Return corresponding chunks
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.document_chunks):
                    chunk = self.document_chunks[idx]
                    # Add similarity score to metadata
                    chunk.metadata = chunk.metadata or {}
                    chunk.metadata['similarity_score'] = float(score)
                    chunk.metadata['search_rank'] = i + 1
                    results.append(chunk)
            
            return results
            
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return self._demo_search(query, top_k)
    
    def _demo_search(self, query: str, top_k: int) -> List[DocumentChunk]:
        """Demo search that returns chunks with simulated relevance"""
        if not self.document_chunks:
            return []
        
        # Simple keyword matching for demo
        query_words = set(query.lower().split())
        scored_chunks = []
        
        for chunk in self.document_chunks:
            chunk_words = set(chunk.text.lower().split())
            # Simple overlap score
            overlap = len(query_words.intersection(chunk_words))
            scored_chunks.append((chunk, overlap))
        
        # Sort by score and return top_k
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for i, (chunk, score) in enumerate(scored_chunks[:top_k]):
            # Add demo metadata
            chunk.metadata = chunk.metadata or {}
            chunk.metadata['demo_score'] = score
            chunk.metadata['search_rank'] = i + 1
            results.append(chunk)
        
        return results
    
    def get_similar_chunks(self, chunk: DocumentChunk, top_k: int = 3) -> List[DocumentChunk]:
        """Find chunks similar to the given chunk"""
        if self.demo_mode:
            # Return random similar chunks for demo
            other_chunks = [c for c in self.document_chunks if c.chunk_id != chunk.chunk_id]
            return random.sample(other_chunks, min(len(other_chunks), top_k))
        else:
            # Use the chunk's text as query
            return self.search(chunk.text, top_k + 1)[1:]  # Exclude the chunk itself
    
    def get_chunk_by_id(self, chunk_id: str) -> DocumentChunk:
        """Get a specific chunk by its ID"""
        for chunk in self.document_chunks:
            if chunk.chunk_id == chunk_id:
                return chunk
        return None
    
    def get_chunks_by_page(self, page_number: int) -> List[DocumentChunk]:
        """Get all chunks from a specific page"""
        return [chunk for chunk in self.document_chunks if chunk.page_number == page_number]
    
    def get_search_statistics(self) -> dict:
        """Get statistics about the indexed documents"""
        if not self.document_chunks:
            return {
                "total_chunks": 0,
                "total_pages": 0,
                "average_chunk_length": 0,
                "total_text_length": 0,
                "index_type": "none"
            }
        
        total_text_length = sum(len(chunk.text) for chunk in self.document_chunks)
        unique_pages = len(set(chunk.page_number for chunk in self.document_chunks))
        
        return {
            "total_chunks": len(self.document_chunks),
            "total_pages": unique_pages,
            "average_chunk_length": total_text_length // len(self.document_chunks),
            "total_text_length": total_text_length,
            "index_type": "FAISS" if not self.demo_mode and self.index else "demo",
            "embedding_dimension": self.embeddings.shape[1] if self.embeddings is not None else 0
        }
    
    def search_with_filters(self, query: str, page_filter: List[int] = None, top_k: int = 5) -> List[DocumentChunk]:
        """
        Search with additional filters
        
        Args:
            query: Search query
            page_filter: List of page numbers to filter by
            top_k: Number of results to return
            
        Returns:
            Filtered search results
        """
        # Get initial search results
        results = self.search(query, top_k * 2)  # Get more results for filtering
        
        # Apply page filter if specified
        if page_filter:
            results = [chunk for chunk in results if chunk.page_number in page_filter]
        
        return results[:top_k]
    
    def get_document_coverage(self, query: str, top_k: int = 5) -> dict:
        """
        Analyze how well the search results cover the query
        
        Args:
            query: Search query
            top_k: Number of results to analyze
            
        Returns:
            Coverage statistics
        """
        results = self.search(query, top_k)
        
        if not results:
            return {"coverage": 0.0, "pages_covered": 0, "chunks_found": 0}
        
        pages_covered = len(set(chunk.page_number for chunk in results))
        
        # Simple coverage metric based on results found
        coverage = min(len(results) / top_k, 1.0)
        
        return {
            "coverage": coverage,
            "pages_covered": pages_covered,
            "chunks_found": len(results),
            "average_chunk_length": sum(len(chunk.text) for chunk in results) // len(results)
        }
    
    def export_index_info(self) -> dict:
        """Export information about the current index"""
        info = {
            "demo_mode": self.demo_mode,
            "total_chunks": len(self.document_chunks),
            "index_created": self.index is not None,
            "model_loaded": self.model is not None
        }
        
        if not self.demo_mode and self.index:
            info.update({
                "index_size": self.index.ntotal,
                "embedding_dimension": self.index.d,
                "index_type": "FAISS IndexFlatIP"
            })
        
        return info
    
    def clear_index(self) -> None:
        """Clear the current index and chunks"""
        self.document_chunks.clear()
        self.embeddings = None
        self.index = None
        print("Search index cleared")
