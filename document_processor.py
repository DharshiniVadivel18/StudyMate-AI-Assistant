"""
Document processing module for StudyMate
Handles PDF parsing and text extraction using PyMuPDF
"""

import tempfile
import os
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DocumentChunk:
    """Represents a chunk of text from a document"""
    text: str
    page_number: int
    chunk_id: str = ""
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class DocumentProcessor:
    """Handles document processing and text extraction"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_pdf(self, file_path: str) -> List[DocumentChunk]:
        """
        Process a PDF file and extract text chunks
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of DocumentChunk objects
        """
        try:
            # Try to import PyMuPDF for PDF processing
            import fitz  # PyMuPDF
            
            chunks = []
            doc = fitz.open(file_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    # Split text into chunks
                    page_chunks = self._split_text_into_chunks(text, page_num + 1)
                    chunks.extend(page_chunks)
            
            doc.close()
            return chunks
            
        except ImportError:
            # Fallback: Create demo chunks if PyMuPDF is not available
            return self._create_demo_chunks(file_path)
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return self._create_demo_chunks(file_path)
    
    def _split_text_into_chunks(self, text: str, page_number: int) -> List[DocumentChunk]:
        """Split text into overlapping chunks"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            if chunk_text.strip():
                chunk = DocumentChunk(
                    text=chunk_text,
                    page_number=page_number,
                    chunk_id=f"page_{page_number}_chunk_{len(chunks)}",
                    metadata={"word_count": len(chunk_words)}
                )
                chunks.append(chunk)
        
        return chunks
    
    def _create_demo_chunks(self, file_path: str) -> List[DocumentChunk]:
        """Create demo chunks when PDF processing is not available"""
        filename = Path(file_path).name
        
        demo_chunks = [
            DocumentChunk(
                text=f"This is a demo chunk from {filename}. In a real implementation, this would contain the actual text extracted from the PDF document. The document processing system would parse the PDF and extract meaningful text content for analysis. This chunk represents the first section of the document with key concepts and introductory material.",
                page_number=1,
                chunk_id="demo_chunk_1",
                metadata={"demo": True, "filename": filename, "section": "introduction"}
            ),
            DocumentChunk(
                text=f"This is the second demo chunk from {filename}. The StudyMate system would normally process multiple pages and create overlapping text chunks to ensure comprehensive coverage of the document content for question answering. This section would contain the main body of content with detailed explanations, methodologies, and core concepts.",
                page_number=1,
                chunk_id="demo_chunk_2",
                metadata={"demo": True, "filename": filename, "section": "main_content"}
            ),
            DocumentChunk(
                text=f"Final demo chunk from {filename}. In production, the system would extract actual content, maintain proper formatting, and create searchable chunks that can be used for semantic search and question answering tasks. This section represents conclusions, findings, and summary information that would be valuable for academic analysis.",
                page_number=2,
                chunk_id="demo_chunk_3",
                metadata={"demo": True, "filename": filename, "section": "conclusion"}
            )
        ]
        
        return demo_chunks
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """
        Save uploaded file to temporary location
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Path to saved file
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")
    
    def get_document_info(self, file_path: str) -> dict:
        """Get basic information about the document"""
        try:
            import fitz
            doc = fitz.open(file_path)
            info = {
                "page_count": len(doc),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", "")
            }
            doc.close()
            return info
        except:
            return {
                "page_count": 1,
                "title": Path(file_path).stem,
                "author": "Unknown",
                "subject": "Demo Document"
            }
    
    def extract_text_from_page(self, file_path: str, page_number: int) -> str:
        """Extract text from a specific page"""
        try:
            import fitz
            doc = fitz.open(file_path)
            if 0 <= page_number < len(doc):
                page = doc.load_page(page_number)
                text = page.get_text()
                doc.close()
                return text
            doc.close()
            return ""
        except:
            return f"Demo text from page {page_number + 1}"
    
    def get_total_pages(self, file_path: str) -> int:
        """Get total number of pages in the document"""
        try:
            import fitz
            doc = fitz.open(file_path)
            page_count = len(doc)
            doc.close()
            return page_count
        except:
            return 1
