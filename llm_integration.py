"""
LLM Integration module for StudyMate
Handles AI model interactions and response generation using IBM Granite models
"""

from typing import List, Optional
from dataclasses import dataclass
import random
import time
import os
import requests
import json
from .document_processor import DocumentChunk

@dataclass
class GeneratedAnswer:
    """Represents an AI-generated answer"""
    answer: str
    confidence: float
    source_chunks: List[DocumentChunk]
    model_used: str = "granite-3b-code-instruct"
    processing_time: float = 0.0
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class LLMIntegration:
    """Handles integration with IBM Granite language models"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.model_name = "granite-3b-code-instruct"
        
        # IBM Watsonx/Granite API configuration
        self.api_key = os.getenv("IBM_API_KEY")
        self.project_id = os.getenv("IBM_PROJECT_ID")
        self.base_url = os.getenv("IBM_BASE_URL", "https://us-south.ml.cloud.ibm.com")
        
        # Check if we have proper credentials for production mode
        if not self.demo_mode and not all([self.api_key, self.project_id]):
            print("Warning: IBM API credentials not found. Falling back to demo mode.")
            self.demo_mode = True
    
    def generate_answer(self, question: str, context_chunks: List[DocumentChunk]) -> GeneratedAnswer:
        """
        Generate an answer based on the question and context chunks
        
        Args:
            question: User's question
            context_chunks: Relevant document chunks for context
            
        Returns:
            GeneratedAnswer object
        """
        start_time = time.time()
        
        if self.demo_mode:
            answer = self._generate_demo_answer(question, context_chunks)
        else:
            answer = self._generate_granite_answer(question, context_chunks)
        
        processing_time = time.time() - start_time
        
        return GeneratedAnswer(
            answer=answer,
            confidence=self._calculate_confidence(question, context_chunks),
            source_chunks=context_chunks,
            model_used=self.model_name,
            processing_time=processing_time,
            metadata={
                "question_length": len(question),
                "context_chunks_count": len(context_chunks),
                "total_context_length": sum(len(chunk.text) for chunk in context_chunks)
            }
        )
    
    def _generate_granite_answer(self, question: str, context_chunks: List[DocumentChunk]) -> str:
        """Generate answer using IBM Granite model"""
        try:
            # Prepare context from chunks
            context = self._prepare_context(context_chunks)
            
            # Create prompt for Granite model
            prompt = self._create_granite_prompt(question, context)
            
            # Call IBM Watsonx API
            response = self._call_granite_api(prompt)
            
            if response:
                return response
            else:
                # Fallback to demo if API fails
                return self._generate_demo_answer(question, context_chunks)
                
        except Exception as e:
            print(f"Error calling Granite API: {e}")
            return self._generate_demo_answer(question, context_chunks)
    
    def _call_granite_api(self, prompt: str) -> Optional[str]:
        """Call IBM Watsonx Granite API"""
        try:
            # Get access token
            token = self._get_access_token()
            if not token:
                return None
            
            # Prepare API request
            url = f"{self.base_url}/ml/v1/text/generation?version=2023-05-29"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            data = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "repetition_penalty": 1.1
                },
                "model_id": "ibm/granite-3b-code-instruct",
                "project_id": self.project_id
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("results", [{}])[0].get("generated_text", "").strip()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in Granite API call: {e}")
            return None
    
    def _get_access_token(self) -> Optional[str]:
        """Get IBM Cloud access token"""
        try:
            url = "https://iam.cloud.ibm.com/identity/token"
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "grant_type": "urn:iam:params:oauth:grant-type:apikey",
                "apikey": self.api_key
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"Token Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def _create_granite_prompt(self, question: str, context: str) -> str:
        """Create a well-structured prompt for Granite model"""
        prompt = f"""You are StudyMate, an AI academic assistant. Answer the student's question based ONLY on the provided context from their uploaded documents.

Context from uploaded documents:
{context}

Student's Question: {question}

Instructions:
1. Answer based ONLY on the provided context
2. If the context doesn't contain relevant information, say so clearly
3. Provide specific references to the source material when possible
4. Be concise but comprehensive
5. Use academic language appropriate for students

Answer:"""
        
        return prompt
    
    def _prepare_context(self, context_chunks: List[DocumentChunk]) -> str:
        """Prepare context string from document chunks"""
        if not context_chunks:
            return "No relevant context found in uploaded documents."
        
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(f"[Source {i} - Page {chunk.page_number}]: {chunk.text}")
        
        return "\n\n".join(context_parts)
    
    def _generate_demo_answer(self, question: str, context_chunks: List[DocumentChunk]) -> str:
        """Generate a demo answer for testing purposes"""
        
        # Demo responses based on question type
        demo_responses = {
            "what": f"Based on the uploaded documents, here's what I found regarding '{question}': The documents contain relevant information that addresses your query. This comprehensive response analyzes the content from {len(context_chunks)} relevant sections across your PDF materials.",
            
            "how": f"Here's how to approach '{question}' based on the document analysis: The process involves several key steps that are outlined in your uploaded materials. This detailed explanation is derived from {len(context_chunks)} relevant sections in your documents.",
            
            "why": f"The reason for '{question}' can be explained through the following analysis: Based on {len(context_chunks)} relevant sections from your documents, the underlying principles show that this occurs due to specific factors detailed in your study materials.",
            
            "when": f"Regarding the timing aspect of '{question}': The documents provide temporal information across {len(context_chunks)} sections that help answer when specific events or processes occur in the context of your study materials.",
            
            "where": f"The location or context for '{question}' is addressed in your documents: Based on {len(context_chunks)} relevant sections, spatial and contextual information helps identify where specific activities or phenomena take place.",
            
            "who": f"The people or entities involved in '{question}' are identified across {len(context_chunks)} sections of your documents: The materials contain information about key individuals, organizations, or stakeholders relevant to your query."
        }
        
        # Determine response type based on question
        question_lower = question.lower()
        response_type = "what"  # default
        
        for key in demo_responses.keys():
            if question_lower.startswith(key):
                response_type = key
                break
        
        base_response = demo_responses[response_type]
        
        # Add source information if chunks are available
        if context_chunks:
            pages = sorted(set(chunk.page_number for chunk in context_chunks))
            page_info = f"\n\n**Sources Referenced:** Pages {', '.join(map(str, pages))} from your uploaded documents."
            base_response += page_info
        
        # Add demo disclaimer
        base_response += "\n\n*Note: This is a demonstration response showing StudyMate's capabilities. In production mode with IBM Granite models, this would be generated by analyzing the actual content of your uploaded PDF documents.*"
        
        return base_response
    
    def _calculate_confidence(self, question: str, context_chunks: List[DocumentChunk]) -> float:
        """Calculate confidence score for the answer"""
        if self.demo_mode:
            # Demo confidence calculation
            base_confidence = 0.75
            
            # Adjust based on question length (longer questions might be more specific)
            if len(question) > 50:
                base_confidence += 0.1
            
            # Adjust based on available context
            if len(context_chunks) > 2:
                base_confidence += 0.1
            
            # Add some randomness for demo purposes
            base_confidence += random.uniform(-0.1, 0.1)
            
            return min(max(base_confidence, 0.0), 1.0)
        else:
            # Real confidence calculation would be based on model outputs
            return 0.8
    
    def generate_follow_up_questions(self, question: str, answer: str, context_chunks: List[DocumentChunk]) -> List[str]:
        """Generate follow-up questions based on the current Q&A"""
        if self.demo_mode:
            return self._generate_demo_follow_ups(question, answer)
        else:
            return self._generate_granite_follow_ups(question, answer, context_chunks)
    
    def _generate_demo_follow_ups(self, question: str, answer: str) -> List[str]:
        """Generate demo follow-up questions"""
        follow_ups = [
            f"Can you provide more specific details about the main points in '{question}'?",
            f"What are the practical applications of the concepts discussed?",
            f"Are there any related topics I should explore further?",
            f"Can you explain any technical terms mentioned in the response?",
            f"What are the key takeaways from this information?"
        ]
        
        # Return 2-3 random follow-ups
        return random.sample(follow_ups, min(3, len(follow_ups)))
    
    def _generate_granite_follow_ups(self, question: str, answer: str, context_chunks: List[DocumentChunk]) -> List[str]:
        """Generate follow-up questions using Granite model"""
        try:
            prompt = f"""Based on this Q&A, generate 3 relevant follow-up questions a student might ask:

Question: {question}
Answer: {answer}

Generate 3 follow-up questions:"""
            
            response = self._call_granite_api(prompt)
            if response:
                # Parse the response to extract questions
                lines = response.split('\n')
                questions = [line.strip() for line in lines if line.strip() and ('?' in line)]
                return questions[:3]
            else:
                return self._generate_demo_follow_ups(question, answer)
        except:
            return self._generate_demo_follow_ups(question, answer)
    
    def summarize_document(self, chunks: List[DocumentChunk]) -> str:
        """Generate a summary of the document"""
        if self.demo_mode:
            pages = len(set(chunk.page_number for chunk in chunks))
            return f"This document contains {len(chunks)} sections across {pages} pages. The content covers various academic topics that can be explored through specific questions. In production mode, IBM Granite models would provide a comprehensive summary of the actual document content."
        else:
            # Use Granite model for real summarization
            context = self._prepare_context(chunks[:10])  # Use first 10 chunks for summary
            prompt = f"""Summarize the following academic document content:

{context}

Provide a concise summary highlighting the main topics and key points:"""
            
            response = self._call_granite_api(prompt)
            return response if response else "Unable to generate summary at this time."
