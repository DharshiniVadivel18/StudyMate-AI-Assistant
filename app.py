"""
StudyMate - AI-Powered Academic Assistant
Main Streamlit Application with IBM Granite Integration
"""

import streamlit as st
import sys
from pathlib import Path
import tempfile
import os
from typing import List, Dict, Optional
import traceback
from datetime import datetime

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

# Import configuration
from config import config

# Import backend modules
try:
    from backend.studymate_core import StudyMateCore
    from backend.llm_integration import GeneratedAnswer
    from backend.session_manager import QAEntry
except ImportError as e:
    st.error(f"Backend import error: {e}")
    st.stop()

# Import frontend components
from frontend.ui_components import (
    load_custom_css, render_main_header, render_sidebar, render_welcome_screen,
    render_document_status, render_question_input, render_answer_display,
    render_session_metrics, render_qa_history, render_export_options,
    render_follow_up_questions, render_loading_spinner, render_error_message,
    render_success_message, render_info_message, render_footer,
    render_system_status, validate_pdf_file, create_download_link
)

# Page configuration
st.set_page_config(
    page_title="StudyMate - AI Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'studymate_core' not in st.session_state:
        try:
            st.session_state.studymate_core = StudyMateCore(demo_mode=config.is_demo_mode)
        except Exception as e:
            st.error(f"Error initializing StudyMate core: {e}")
            st.session_state.studymate_core = None
    
    if 'uploaded_docs' not in st.session_state:
        st.session_state.uploaded_docs = []
    
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = {}
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    
    if 'follow_up_questions' not in st.session_state:
        st.session_state.follow_up_questions = []

def process_uploaded_files(uploaded_files):
    """Process uploaded PDF files"""
    if not uploaded_files or not st.session_state.studymate_core:
        return
    
    # Validate files
    valid_files = []
    for file in uploaded_files:
        is_valid, message = validate_pdf_file(file)
        if is_valid:
            valid_files.append(file)
        else:
            render_error_message(f"File '{file.name}': {message}")
    
    if not valid_files:
        return
    
    # Update uploaded docs list
    new_docs = [f.name for f in valid_files if f.name not in st.session_state.uploaded_docs]
    st.session_state.uploaded_docs.extend(new_docs)
    
    # Process files
    if new_docs:
        with st.spinner("Processing uploaded documents..."):
            try:
                processing_status = st.session_state.studymate_core.process_uploaded_files(valid_files)
                st.session_state.processing_status.update(processing_status)
                
                # Show success message
                processed_count = sum(1 for status in processing_status.values() if status == "processed")
                if processed_count > 0:
                    render_success_message(f"Successfully processed {processed_count} document(s)")
                
            except Exception as e:
                render_error_message(f"Error processing files: {str(e)}")

def handle_question_submission(question: str, settings: Dict):
    """Handle question submission and generate answer"""
    if not question or not st.session_state.studymate_core:
        return
    
    # Clear previous results
    st.session_state.current_question = question
    st.session_state.current_answer = None
    st.session_state.follow_up_questions = []
    
    # Show loading
    with st.spinner("StudyMate AI is analyzing your question..."):
        try:
            # Generate answer
            answer, source_chunks = st.session_state.studymate_core.ask_question(
                question, 
                max_chunks=settings.get('max_results', 5)
            )
            
            # Store results
            st.session_state.current_answer = answer
            
            # Generate follow-up questions
            if answer and hasattr(answer, 'answer'):
                follow_ups = st.session_state.studymate_core.get_follow_up_questions(question, answer)
                st.session_state.follow_up_questions = follow_ups
            
            render_success_message("Answer generated successfully!")
            
        except Exception as e:
            render_error_message(f"Error generating answer: {str(e)}")
            st.error(traceback.format_exc())

def handle_export(export_format: str):
    """Handle session export"""
    if not st.session_state.studymate_core:
        return
    
    try:
        with st.spinner(f"Exporting session as {export_format.upper()}..."):
            file_path = st.session_state.studymate_core.export_session(format=export_format)
            
            # Create download link
            download_link = create_download_link(file_path, f"Download {export_format.upper()}")
            st.markdown(download_link, unsafe_allow_html=True)
            
            render_success_message(f"Session exported successfully as {export_format.upper()}")
            
    except Exception as e:
        render_error_message(f"Export failed: {str(e)}")

def handle_sidebar_actions(sidebar_state: Dict):
    """Handle sidebar actions"""
    if sidebar_state.get('clear_session'):
        if st.session_state.studymate_core:
            st.session_state.studymate_core.clear_session()
        
        # Clear session state
        st.session_state.uploaded_docs = []
        st.session_state.processing_status = {}
        st.session_state.current_question = ""
        st.session_state.current_answer = None
        st.session_state.follow_up_questions = []
        
        render_success_message("Session cleared successfully!")
        st.rerun()
    
    if sidebar_state.get('new_session'):
        if st.session_state.studymate_core:
            st.session_state.studymate_core.session_manager.start_new_session()
        
        render_success_message("New session started!")
        st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Load custom CSS
    load_custom_css()
    
    # Render main header
    render_main_header()
    
    # Create main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Render sidebar and get settings
        sidebar_state = render_sidebar()
        
        # Handle sidebar actions
        handle_sidebar_actions(sidebar_state)
        
        # Process uploaded files
        if sidebar_state.get("uploaded_files"):
            process_uploaded_files(sidebar_state["uploaded_files"])
        
        # Main content area
        if not st.session_state.uploaded_docs:
            # Show welcome screen
            render_welcome_screen()
        else:
            # Show document status
            render_document_status(st.session_state.uploaded_docs, st.session_state.processing_status)
            
            # Show session metrics
            current_session = st.session_state.studymate_core.session_manager.get_current_session() if st.session_state.studymate_core else None
            render_session_metrics(current_session, st.session_state.uploaded_docs)
            
            # Question input
            question = render_question_input()
            
            if question:
                handle_question_submission(question, sidebar_state)
            
            # Display current answer
            if st.session_state.current_answer:
                render_answer_display(
                    st.session_state.current_question,
                    st.session_state.current_answer,
                    st.session_state.current_answer.source_chunks if hasattr(st.session_state.current_answer, 'source_chunks') else [],
                    show_confidence=sidebar_state.get('show_confidence', True),
                    show_sources=sidebar_state.get('show_sources', True),
                    show_metadata=sidebar_state.get('show_metadata', False)
                )
                
                # Follow-up questions
                if st.session_state.follow_up_questions:
                    follow_up = render_follow_up_questions(st.session_state.follow_up_questions)
                    if follow_up:
                        handle_question_submission(follow_up, sidebar_state)
                        st.rerun()
    
    with col2:
        # Right sidebar content
        if st.session_state.uploaded_docs:
            # Q&A History
            if st.session_state.studymate_core:
                qa_history = st.session_state.studymate_core.get_session_history(limit=10)
                if qa_history:
                    render_qa_history(qa_history, limit=5)
            
            # Export options
            current_session = st.session_state.studymate_core.session_manager.get_current_session() if st.session_state.studymate_core else None
            if current_session:
                export_format = render_export_options(current_session.session_id)
                if export_format:
                    handle_export(export_format)
            
            # System status
            if st.session_state.studymate_core:
                status_info = st.session_state.studymate_core.get_system_status()
                render_system_status(status_info)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
