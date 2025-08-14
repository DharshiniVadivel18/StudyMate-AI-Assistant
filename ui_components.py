"""
UI Components for StudyMate Frontend
Streamlit-based user interface components
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
import tempfile
import os
from datetime import datetime
import base64

def load_custom_css():
    """Load custom CSS for enhanced UI styling"""
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Answer styling */
    .answer-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
    }
    
    .question-recap {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    .confidence-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.8s ease;
    }
    
    .confidence-high { background: linear-gradient(90deg, #28a745, #20c997); }
    .confidence-medium { background: linear-gradient(90deg, #ffc107, #fd7e14); }
    .confidence-low { background: linear-gradient(90deg, #dc3545, #e83e8c); }
    
    /* Document status */
    .doc-status {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        0% { opacity: 0; transform: translateX(-30px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    /* Welcome screen */
    .welcome-container {
        text-align: center;
        padding: 3rem 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5a6fd8;
    }
    </style>
    """, unsafe_allow_html=True)

def render_main_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🎓 StudyMate</h1>
        <p>AI-Powered Academic Assistant with IBM Granite Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar() -> Dict:
    """Render the enhanced sidebar with file upload and settings"""
    # Load custom CSS
    load_custom_css()
    
    # Sidebar header
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h2 style="margin: 0;">📚 StudyMate</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">AI Academic Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <h3 style="margin-top: 0; color: #495057;">📄 Document Upload</h3>
        <p style="color: #6c757d; font-size: 0.9rem;">Upload PDF files to analyze with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.sidebar.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF documents to analyze with StudyMate AI"
    )
    
    # Model settings
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <h3 style="margin-top: 0; color: #495057;">🤖 AI Model Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    demo_mode = st.sidebar.checkbox(
        "Demo Mode", 
        value=True, 
        help="Use demo responses (disable for IBM Granite model)"
    )
    
    if not demo_mode:
        st.sidebar.info("🔑 Ensure IBM API credentials are set in environment variables")
    
    # Advanced settings
    with st.sidebar.expander("⚙️ Advanced Settings", expanded=False):
        max_results = st.slider("Max Search Results", 1, 10, 5)
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.1)
        
        show_confidence = st.checkbox("Show Confidence Scores", True)
        show_sources = st.checkbox("Show Source References", True)
        show_metadata = st.checkbox("Show Metadata", False)
        
        export_format = st.selectbox("Export Format", ["csv", "pdf", "json"])
    
    # Quick actions
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <h3 style="margin-top: 0; color: #495057;">⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        clear_session = st.button("🗑️ Clear", use_container_width=True)
    with col2:
        new_session = st.button("🆕 New", use_container_width=True)
    
    return {
        "uploaded_files": uploaded_files,
        "demo_mode": demo_mode,
        "max_results": max_results,
        "confidence_threshold": confidence_threshold,
        "show_confidence": show_confidence,
        "show_sources": show_sources,
        "show_metadata": show_metadata,
        "export_format": export_format,
        "clear_session": clear_session,
        "new_session": new_session
    }

def render_welcome_screen():
    """Render enhanced welcome screen with features overview"""
    st.markdown("""
    <div class="welcome-container fade-in">
        <h1 style="color: #495057; margin-bottom: 1rem;">🎓 Welcome to StudyMate!</h1>
        <p style="font-size: 1.3rem; color: #6c757d; margin-bottom: 2rem;">
            Transform your study materials into an interactive AI-powered knowledge assistant
        </p>

        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
            <h2 style="margin: 0 0 1rem 0;">🚀 Getting Started</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📄</div>
                    <h4 style="margin: 0;">1. Upload PDFs</h4>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Upload your study materials</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">💬</div>
                    <h4 style="margin: 0;">2. Ask Questions</h4>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Query in natural language</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
                    <h4 style="margin: 0;">3. Get AI Answers</h4>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Powered by IBM Granite</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
                    <h4 style="margin: 0;">4. Export Results</h4>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Save for revision</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature highlights
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="color: #495057;">Grounded Answers</h3>
            <p style="color: #6c757d;">All responses are strictly based on your uploaded documents</p>
        </div>

        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
            <h3 style="color: #495057;">Multi-PDF Reasoning</h3>
            <p style="color: #6c757d;">Synthesize information across multiple documents</p>
        </div>

        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #495057;">Semantic Search</h3>
            <p style="color: #6c757d;">Advanced FAISS-powered document retrieval</p>
        </div>

        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
            <h3 style="color: #495057;">Export History</h3>
            <p style="color: #6c757d;">Download Q&A sessions for revision</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_document_status(uploaded_docs: List[str], processing_status: Dict) -> None:
    """Render document processing status with enhanced UI"""
    if not uploaded_docs:
        st.info("📄 No documents uploaded yet. Use the sidebar to upload PDF files.")
        return

    st.markdown("""
    <div class="slide-in">
        <h2 style="color: #495057; margin-bottom: 1.5rem;">📚 Document Status</h2>
    </div>
    """, unsafe_allow_html=True)

    for doc in uploaded_docs:
        status = processing_status.get(doc, "pending")

        if status == "processed":
            icon = "✅"
            color = "#28a745"
            status_text = "Processed"
            progress = 1.0
        elif status == "processing":
            icon = "⏳"
            color = "#ffc107"
            status_text = "Processing..."
            progress = 0.5
        elif status == "error":
            icon = "❌"
            color = "#dc3545"
            status_text = "Error"
            progress = 0.0
        else:
            icon = "⏸️"
            color = "#6c757d"
            status_text = "Pending"
            progress = 0.0

        st.markdown(f"""
        <div class="doc-status">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 1rem;">{icon}</span>
                <div>
                    <strong style="color: {color};">{doc}</strong><br>
                    <small style="color: #6c757d;">{status_text}</small>
                </div>
            </div>
            <div style="width: 100px;">
                <div style="background: #e9ecef; border-radius: 10px; height: 8px;">
                    <div style="background: {color}; height: 100%; border-radius: 10px; width: {progress*100}%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_question_input() -> Optional[str]:
    """Render enhanced question input interface"""
    st.markdown("""
    <div class="slide-in">
        <h2 style="color: #495057; margin-bottom: 1rem;">💬 Ask Your Question</h2>
    </div>
    """, unsafe_allow_html=True)

    # Question suggestions
    with st.expander("💡 Question Examples & Tips", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **📊 Analysis Questions:**
            - What are the main themes in this document?
            - Summarize the key findings
            - What conclusions does the author draw?
            - Compare different viewpoints presented
            """)

        with col2:
            st.markdown("""
            **🔍 Specific Questions:**
            - What does the document say about [topic]?
            - How is [concept] defined?
            - What evidence supports [claim]?
            - When did [event] occur?
            """)

        st.markdown("""
        **💡 Tips for Better Results:**
        - Be specific in your questions
        - Reference particular concepts or topics
        - Ask for comparisons between ideas
        - Request examples or evidence
        """)

    question = st.text_area(
        "Enter your question:",
        height=120,
        placeholder="Ask anything about your uploaded documents... For example: 'What are the main concepts discussed in chapter 3?' or 'Explain the methodology used in this research.'",
        help="Type your question in natural language. StudyMate will search through your documents and provide AI-powered answers."
    )

    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        ask_button = st.button(
            "🚀 Ask StudyMate",
            type="primary",
            use_container_width=True,
            help="Get AI-powered answer from your documents"
        )

    if ask_button and question.strip():
        return question.strip()
    elif ask_button and not question.strip():
        st.warning("⚠️ Please enter a question before submitting!")

    return None

def render_answer_display(question: str, answer, source_chunks: List = None, show_confidence: bool = True, show_sources: bool = True, show_metadata: bool = False):
    """Render enhanced answer display with confidence and sources"""
    st.markdown("""
    <div class="slide-in">
        <h2 style="color: #495057; margin-bottom: 1.5rem;">🎯 AI Response</h2>
    </div>
    """, unsafe_allow_html=True)

    # Question recap
    st.markdown(f"""
    <div class="question-recap">
        <strong>Your Question:</strong> {question}
    </div>
    """, unsafe_allow_html=True)

    # Answer content
    if hasattr(answer, 'answer'):
        answer_text = answer.answer
        confidence = getattr(answer, 'confidence', 0.8)
        model_used = getattr(answer, 'model_used', 'StudyMate AI')
        processing_time = getattr(answer, 'processing_time', 0.0)
    else:
        answer_text = str(answer)
        confidence = 0.8
        model_used = 'StudyMate AI'
        processing_time = 0.0

    st.markdown(f"""
    <div class="answer-card">
        <div style="margin-bottom: 1.5rem;">
            <strong style="color: #495057; font-size: 1.1rem;">Answer:</strong>
        </div>
        <div style="line-height: 1.6; color: #495057;">
            {answer_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence and metadata
    if show_confidence:
        confidence_color = "confidence-high" if confidence > 0.8 else "confidence-medium" if confidence > 0.6 else "confidence-low"
        confidence_text_color = "#28a745" if confidence > 0.8 else "#ffc107" if confidence > 0.6 else "#dc3545"

        st.markdown(f"""
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="color: #495057;">Confidence Score:</strong>
                <span style="color: {confidence_text_color}; font-weight: bold; font-size: 1.1rem;">{confidence:.0%}</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill {confidence_color}" style="width: {confidence*100}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Model and processing info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Used", model_used)
    with col2:
        st.metric("Processing Time", f"{processing_time:.2f}s")
    with col3:
        if source_chunks:
            st.metric("Sources Found", len(source_chunks))
        else:
            st.metric("Sources Found", "0")

    # Source references
    if show_sources and source_chunks:
        with st.expander(f"📚 View Source References ({len(source_chunks)} found)", expanded=False):
            for i, chunk in enumerate(source_chunks, 1):
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 3px solid #667eea;">
                    <strong>Source {i} - Page {chunk.page_number}</strong>
                    <p style="margin: 0.5rem 0 0 0; color: #495057;">{chunk.text[:300]}{'...' if len(chunk.text) > 300 else ''}</p>
                </div>
                """, unsafe_allow_html=True)

                if show_metadata and hasattr(chunk, 'metadata') and chunk.metadata:
                    st.json(chunk.metadata)

def render_session_metrics(session, uploaded_docs: List[str]):
    """Render session metrics dashboard"""
    if not uploaded_docs:
        return

    st.markdown("""
    <div class="fade-in">
        <h2 style="color: #495057; margin-bottom: 1.5rem;">📊 Session Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(uploaded_docs)}</div>
            <div class="metric-label">📚 Documents</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        qa_count = len(session.qa_entries) if session and hasattr(session, 'qa_entries') else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{qa_count}</div>
            <div class="metric-label">💬 Questions</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if session and hasattr(session, 'qa_entries') and session.qa_entries:
            avg_confidence = sum(qa.answer.confidence for qa in session.qa_entries) / len(session.qa_entries)
            confidence_pct = f"{avg_confidence:.0%}"
        else:
            confidence_pct = "N/A"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{confidence_pct}</div>
            <div class="metric-label">🎯 Avg Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        session_duration = "Active" if session else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{session_duration}</div>
            <div class="metric-label">⏱️ Session</div>
        </div>
        """, unsafe_allow_html=True)

def render_qa_history(qa_entries: List, limit: int = 5):
    """Render Q&A history with enhanced styling"""
    if not qa_entries:
        return

    st.markdown("""
    <div class="fade-in">
        <h2 style="color: #495057; margin-bottom: 1.5rem;">📝 Recent Q&A History</h2>
    </div>
    """, unsafe_allow_html=True)

    # Show recent entries
    recent_entries = qa_entries[-limit:] if len(qa_entries) > limit else qa_entries

    for i, entry in enumerate(reversed(recent_entries), 1):
        timestamp = entry.timestamp.strftime("%H:%M:%S") if hasattr(entry, 'timestamp') else "Unknown"
        confidence = entry.answer.confidence if hasattr(entry.answer, 'confidence') else 0.8

        confidence_color = "#28a745" if confidence > 0.8 else "#ffc107" if confidence > 0.6 else "#dc3545"

        with st.expander(f"Q{len(qa_entries)-len(recent_entries)+len(recent_entries)-i+1}: {entry.question[:60]}... ({timestamp})", expanded=False):
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <strong>Question:</strong> {entry.question}
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;">
                <strong>Answer:</strong> {entry.answer.answer}
            </div>
            <div style="margin-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #6c757d;">Confidence: <strong style="color: {confidence_color};">{confidence:.0%}</strong></span>
                <span style="color: #6c757d;">{timestamp}</span>
            </div>
            """, unsafe_allow_html=True)

def render_export_options(session_id: str = None) -> Optional[str]:
    """Render export options with enhanced UI"""
    if not session_id:
        return None

    st.markdown("""
    <div class="sidebar-section">
        <h3 style="margin-top: 0; color: #495057;">📊 Export Session</h3>
        <p style="color: #6c757d; font-size: 0.9rem;">Download your Q&A history</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 PDF", use_container_width=True, help="Export as PDF document"):
            return "pdf"

    with col2:
        if st.button("📊 CSV", use_container_width=True, help="Export as CSV spreadsheet"):
            return "csv"

    with col3:
        if st.button("📋 JSON", use_container_width=True, help="Export as JSON data"):
            return "json"

    return None

def render_follow_up_questions(questions: List[str]) -> Optional[str]:
    """Render follow-up questions suggestions"""
    if not questions:
        return None

    st.markdown("""
    <div class="fade-in">
        <h3 style="color: #495057; margin: 2rem 0 1rem 0;">🤔 Suggested Follow-up Questions</h3>
    </div>
    """, unsafe_allow_html=True)

    for i, question in enumerate(questions):
        if st.button(f"❓ {question}", key=f"followup_{i}", use_container_width=True):
            return question

    return None

def render_loading_spinner(message: str = "Processing your request..."):
    """Render enhanced loading animation"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">
            <div style="animation: spin 2s linear infinite; display: inline-block;">🔄</div>
        </div>
        <h3 style="color: #495057; margin-bottom: 1rem;">{message}</h3>
        <p style="color: #6c757d;">StudyMate AI is analyzing your documents...</p>
    </div>

    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_error_message(error: str):
    """Render error message with enhanced styling"""
    st.markdown(f"""
    <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>❌ Error:</strong> {error}
    </div>
    """, unsafe_allow_html=True)

def render_success_message(message: str):
    """Render success message with enhanced styling"""
    st.markdown(f"""
    <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>✅ Success:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def render_info_message(message: str):
    """Render info message with enhanced styling"""
    st.markdown(f"""
    <div style="background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>ℹ️ Info:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; margin-top: 3rem; padding: 2rem;">
        <p style="margin: 0;">
            <strong>StudyMate</strong> - AI-Powered Academic Assistant<br>
            <small>Powered by IBM Granite Models • Built with Streamlit • Enhanced with FAISS</small>
        </p>
        <p style="margin: 1rem 0 0 0; font-size: 0.8rem;">
            Transform your study materials into interactive knowledge with advanced AI
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_download_link(file_path: str, link_text: str) -> str:
    """Create a download link for exported files"""
    try:
        with open(file_path, "rb") as f:
            bytes_data = f.read()

        b64 = base64.b64encode(bytes_data).decode()
        file_name = os.path.basename(file_path)

        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" style="text-decoration: none; background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 5px;">{link_text}</a>'
        return href
    except Exception as e:
        return f"Error creating download link: {e}"

def render_system_status(status_info: Dict):
    """Render system status information"""
    with st.expander("🔧 System Status", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Application Status:**")
            st.write(f"• Demo Mode: {'✅' if status_info.get('demo_mode') else '❌'}")
            st.write(f"• Documents Processed: {status_info.get('documents_processed', 0)}")
            st.write(f"• Active Session: {'✅' if status_info.get('active_session') else '❌'}")

        with col2:
            st.markdown("**AI Model:**")
            st.write(f"• Model: {status_info.get('model_name', 'Unknown')}")
            st.write(f"• Q&A Count: {status_info.get('session_qa_count', 0)}")
            st.write(f"• Temp Files: {status_info.get('temp_files_count', 0)}")

def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file to temporary location"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def cleanup_temp_files(file_paths: List[str]):
    """Clean up temporary files"""
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {e}")

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f}{size_names[i]}"

def validate_pdf_file(uploaded_file) -> Tuple[bool, str]:
    """Validate uploaded PDF file"""
    if not uploaded_file:
        return False, "No file uploaded"

    if not uploaded_file.name.lower().endswith('.pdf'):
        return False, "File must be a PDF"

    if uploaded_file.size > 50 * 1024 * 1024:  # 50MB limit
        return False, f"File too large ({format_file_size(uploaded_file.size)}). Maximum size is 50MB."

    return True, "Valid PDF file"
