"""
Minimal test version of StudyMate to identify issues
"""

import streamlit as st
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

st.set_page_config(
    page_title="StudyMate Test",
    page_icon="🎓",
    layout="wide"
)

def test_imports():
    """Test all imports and report status"""
    import_status = {}
    
    # Test config
    try:
        from config import config
        import_status['config'] = f"✅ OK - Demo mode: {config.is_demo_mode}"
    except Exception as e:
        import_status['config'] = f"❌ ERROR: {e}"
    
    # Test backend components
    try:
        from backend.document_processor import DocumentProcessor
        import_status['document_processor'] = "✅ OK"
    except Exception as e:
        import_status['document_processor'] = f"❌ ERROR: {e}"
    
    try:
        from backend.semantic_search import SemanticSearch
        import_status['semantic_search'] = "✅ OK"
    except Exception as e:
        import_status['semantic_search'] = f"❌ ERROR: {e}"
    
    try:
        from backend.llm_integration import LLMIntegration
        import_status['llm_integration'] = "✅ OK"
    except Exception as e:
        import_status['llm_integration'] = f"❌ ERROR: {e}"
    
    try:
        from backend.session_manager import SessionManager
        import_status['session_manager'] = "✅ OK"
    except Exception as e:
        import_status['session_manager'] = f"❌ ERROR: {e}"
    
    try:
        from backend.studymate_core import StudyMateCore
        import_status['studymate_core'] = "✅ OK"
    except Exception as e:
        import_status['studymate_core'] = f"❌ ERROR: {e}"
    
    try:
        from frontend.ui_components import render_main_header
        import_status['ui_components'] = "✅ OK"
    except Exception as e:
        import_status['ui_components'] = f"❌ ERROR: {e}"
    
    return import_status

def test_dependencies():
    """Test optional dependencies"""
    deps_status = {}
    
    try:
        import numpy
        deps_status['numpy'] = "✅ Available"
    except ImportError:
        deps_status['numpy'] = "❌ Missing"
    
    try:
        import requests
        deps_status['requests'] = "✅ Available"
    except ImportError:
        deps_status['requests'] = "❌ Missing"
    
    try:
        import fitz
        deps_status['PyMuPDF'] = "✅ Available"
    except ImportError:
        deps_status['PyMuPDF'] = "❌ Missing"
    
    try:
        import sentence_transformers
        deps_status['sentence_transformers'] = "✅ Available"
    except ImportError:
        deps_status['sentence_transformers'] = "❌ Missing"
    
    try:
        import faiss
        deps_status['faiss'] = "✅ Available"
    except ImportError:
        deps_status['faiss'] = "❌ Missing"
    
    try:
        import reportlab
        deps_status['reportlab'] = "✅ Available"
    except ImportError:
        deps_status['reportlab'] = "❌ Missing"
    
    return deps_status

def main():
    """Main test function"""
    st.title("🧪 StudyMate Diagnostic Test")
    
    st.header("📦 Import Status")
    import_status = test_imports()
    
    for component, status in import_status.items():
        if "✅" in status:
            st.success(f"{component}: {status}")
        else:
            st.error(f"{component}: {status}")
    
    st.header("🔧 Dependencies Status")
    deps_status = test_dependencies()
    
    for dep, status in deps_status.items():
        if "✅" in status:
            st.success(f"{dep}: {status}")
        else:
            st.warning(f"{dep}: {status}")
    
    st.header("🎯 Core Functionality Test")
    
    # Test StudyMate core if imports are successful
    if "✅" in import_status.get('studymate_core', ''):
        try:
            from backend.studymate_core import StudyMateCore
            core = StudyMateCore(demo_mode=True)
            status = core.get_system_status()
            
            st.success("StudyMate Core initialized successfully!")
            st.json(status)
            
            # Test basic functionality
            if st.button("Test Demo Q&A"):
                with st.spinner("Testing Q&A functionality..."):
                    try:
                        # Create demo chunks
                        from backend.document_processor import DocumentChunk
                        demo_chunks = [
                            DocumentChunk(
                                text="This is a test document chunk for demonstration purposes.",
                                page_number=1,
                                chunk_id="test_chunk_1"
                            )
                        ]
                        
                        # Test search
                        core.semantic_search.index_documents(demo_chunks)
                        
                        # Test Q&A
                        answer, chunks = core.ask_question("What is this document about?")
                        
                        st.success("✅ Q&A functionality working!")
                        st.write("**Answer:**", answer.answer)
                        st.write("**Confidence:**", f"{answer.confidence:.2%}")
                        
                    except Exception as e:
                        st.error(f"❌ Q&A test failed: {e}")
                        st.exception(e)
        
        else:
            st.error("Cannot test core functionality - StudyMate core import failed")
    
    st.header("🌐 Server Status")
    st.success("✅ Streamlit server is running successfully!")
    st.info("If you can see this page, the basic application structure is working.")

if __name__ == "__main__":
    main()
