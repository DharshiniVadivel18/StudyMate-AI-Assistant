"""
StudyMate Core - Main orchestration module
Integrates all backend components for the StudyMate application
"""

import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import tempfile
import time

from .document_processor import DocumentProcessor, DocumentChunk
from .semantic_search import SemanticSearch
from .llm_integration import LLMIntegration, GeneratedAnswer
from .session_manager import SessionManager, StudySession, QAEntry

# Import config with proper path handling
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import config

class StudyMateCore:
    """
    Main orchestration class for StudyMate
    Coordinates all backend components
    """
    
    def __init__(self, demo_mode: bool = None):
        """
        Initialize StudyMate core components
        
        Args:
            demo_mode: Whether to run in demo mode (uses config default if None)
        """
        self.demo_mode = demo_mode if demo_mode is not None else config.is_demo_mode
        
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.semantic_search = SemanticSearch(demo_mode=self.demo_mode)
        self.llm_integration = LLMIntegration(demo_mode=self.demo_mode)
        self.session_manager = SessionManager()
        
        # State tracking
        self.processed_documents: Dict[str, List[DocumentChunk]] = {}
        self.temp_files: List[str] = []
        
        print(f"StudyMate initialized in {'demo' if self.demo_mode else 'production'} mode")
    
    def process_uploaded_files(self, uploaded_files) -> Dict[str, str]:
        """
        Process uploaded PDF files
        
        Args:
            uploaded_files: List of Streamlit uploaded file objects
            
        Returns:
            Dictionary mapping filename to processing status
        """
        processing_status = {}
        
        for uploaded_file in uploaded_files:
            try:
                # Save uploaded file temporarily
                temp_path = self.document_processor.save_uploaded_file(uploaded_file)
                self.temp_files.append(temp_path)
                
                processing_status[uploaded_file.name] = "processing"
                
                # Process the PDF
                chunks = self.document_processor.process_pdf(temp_path)
                
                if chunks:
                    # Store processed chunks
                    self.processed_documents[uploaded_file.name] = chunks
                    
                    # Index chunks for search
                    self.semantic_search.index_documents(chunks)
                    
                    # Update session with uploaded document
                    current_session = self.session_manager.get_current_session()
                    if not current_session:
                        current_session = self.session_manager.start_new_session()
                    
                    if uploaded_file.name not in current_session.uploaded_documents:
                        current_session.uploaded_documents.append(uploaded_file.name)
                    
                    processing_status[uploaded_file.name] = "processed"
                else:
                    processing_status[uploaded_file.name] = "error"
                    
            except Exception as e:
                print(f"Error processing {uploaded_file.name}: {e}")
                processing_status[uploaded_file.name] = "error"
        
        return processing_status
    
    def ask_question(self, question: str, max_chunks: int = 5) -> Tuple[GeneratedAnswer, List[DocumentChunk]]:
        """
        Process a question and generate an answer
        
        Args:
            question: User's question
            max_chunks: Maximum number of context chunks to use
            
        Returns:
            Tuple of (GeneratedAnswer, relevant_chunks)
        """
        if not question.strip():
            raise ValueError("Question cannot be empty")
        
        # Search for relevant chunks
        relevant_chunks = self.semantic_search.search(question, top_k=max_chunks)
        
        if not relevant_chunks:
            # If no chunks found, create a default response
            answer = GeneratedAnswer(
                answer="I don't have any uploaded documents to reference. Please upload PDF documents first to ask questions about them.",
                confidence=0.0,
                source_chunks=[],
                model_used=self.llm_integration.model_name,
                processing_time=0.0
            )
        else:
            # Generate answer using LLM
            answer = self.llm_integration.generate_answer(question, relevant_chunks)
        
        # Add to session history
        source_docs = list(self.processed_documents.keys())
        self.session_manager.add_qa_to_current_session(question, answer, source_docs)
        
        return answer, relevant_chunks
    
    def get_document_summary(self, filename: str) -> str:
        """
        Get a summary of a specific document
        
        Args:
            filename: Name of the document to summarize
            
        Returns:
            Document summary
        """
        if filename not in self.processed_documents:
            return f"Document '{filename}' not found or not processed."
        
        chunks = self.processed_documents[filename]
        return self.llm_integration.summarize_document(chunks)
    
    def get_all_documents_summary(self) -> str:
        """Get a summary of all uploaded documents"""
        if not self.processed_documents:
            return "No documents have been uploaded yet."
        
        all_chunks = []
        for chunks in self.processed_documents.values():
            all_chunks.extend(chunks)
        
        return self.llm_integration.summarize_document(all_chunks)
    
    def get_follow_up_questions(self, question: str, answer: GeneratedAnswer) -> List[str]:
        """
        Generate follow-up questions based on the current Q&A
        
        Args:
            question: Original question
            answer: Generated answer
            
        Returns:
            List of follow-up questions
        """
        relevant_chunks = answer.source_chunks
        return self.llm_integration.generate_follow_up_questions(question, answer.answer, relevant_chunks)
    
    def get_session_history(self, limit: int = 10) -> List[QAEntry]:
        """
        Get recent Q&A history from current session
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of QAEntry objects
        """
        current_session = self.session_manager.get_current_session()
        if not current_session:
            return []
        
        return current_session.get_recent_entries(limit)
    
    def export_session(self, format: str = "csv", output_path: str = None) -> str:
        """
        Export current session to file
        
        Args:
            format: Export format ('csv', 'json', 'pdf')
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        current_session = self.session_manager.get_current_session()
        if not current_session:
            raise ValueError("No active session to export")
        
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"studymate_session_{timestamp}.{format}"
        
        if format == "csv":
            success = self.session_manager.export_session_csv(current_session.session_id, output_path)
        elif format == "pdf":
            success = self.session_manager.export_session_pdf(current_session.session_id, output_path)
        elif format == "json":
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(current_session.to_dict(), f, indent=2, ensure_ascii=False)
            success = True
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        if success:
            return output_path
        else:
            raise RuntimeError(f"Failed to export session in {format} format")
    
    def get_document_stats(self) -> Dict:
        """Get statistics about processed documents"""
        if not self.processed_documents:
            return {
                "total_documents": 0,
                "total_chunks": 0,
                "total_pages": 0,
                "average_chunks_per_document": 0
            }
        
        total_chunks = sum(len(chunks) for chunks in self.processed_documents.values())
        total_pages = sum(len(set(chunk.page_number for chunk in chunks)) 
                         for chunks in self.processed_documents.values())
        
        return {
            "total_documents": len(self.processed_documents),
            "total_chunks": total_chunks,
            "total_pages": total_pages,
            "average_chunks_per_document": total_chunks // len(self.processed_documents) if self.processed_documents else 0
        }
    
    def get_search_stats(self) -> Dict:
        """Get search and indexing statistics"""
        return self.semantic_search.get_search_statistics()
    
    def clear_session(self) -> None:
        """Clear current session and processed documents"""
        # Clear processed documents
        self.processed_documents.clear()
        
        # Clear search index
        self.semantic_search = SemanticSearch(demo_mode=self.demo_mode)
        
        # Start new session
        self.session_manager.start_new_session()
        
        # Clean up temp files
        self.cleanup_temp_files()
    
    def cleanup_temp_files(self) -> None:
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            self.document_processor.cleanup_temp_file(temp_file)
        self.temp_files.clear()
    
    def get_system_status(self) -> Dict:
        """Get overall system status"""
        current_session = self.session_manager.get_current_session()
        
        return {
            "demo_mode": self.demo_mode,
            "documents_processed": len(self.processed_documents),
            "active_session": current_session is not None,
            "session_qa_count": len(current_session.qa_entries) if current_session else 0,
            "temp_files_count": len(self.temp_files),
            "model_name": self.llm_integration.model_name
        }
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.cleanup_temp_files()
        except:
            pass
