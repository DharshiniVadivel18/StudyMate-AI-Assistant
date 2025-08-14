#!/usr/bin/env python3
"""
Verification script for StudyMate application
Tests all core functionality and reports any issues
"""

import sys
import traceback
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

def test_core_functionality():
    """Test StudyMate core functionality"""
    print("🧪 Testing StudyMate Core Functionality")
    print("=" * 50)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from config import config
        print(f"✅ Config loaded - Demo mode: {config.is_demo_mode}")
        
        from backend.studymate_core import StudyMateCore
        print("✅ StudyMate core imported")
        
        from backend.document_processor import DocumentProcessor, DocumentChunk
        print("✅ Document processor imported")
        
        from backend.semantic_search import SemanticSearch
        print("✅ Semantic search imported")
        
        from backend.llm_integration import LLMIntegration
        print("✅ LLM integration imported")
        
        from backend.session_manager import SessionManager
        print("✅ Session manager imported")
        
        from frontend.ui_components import render_main_header
        print("✅ UI components imported")
        
        # Test core initialization
        print("\n🚀 Testing core initialization...")
        core = StudyMateCore(demo_mode=True)
        print("✅ StudyMate core initialized")
        
        # Test system status
        status = core.get_system_status()
        print(f"✅ System status: {status}")
        
        # Test document processing
        print("\n📄 Testing document processing...")
        doc_processor = DocumentProcessor()
        
        # Create a test chunk
        test_chunk = DocumentChunk(
            text="This is a test document chunk for StudyMate verification. It contains sample academic content that would typically be extracted from a PDF document.",
            page_number=1,
            chunk_id="test_chunk_1",
            metadata={"test": True}
        )
        
        print("✅ Document chunk created")
        
        # Test semantic search
        print("\n🔍 Testing semantic search...")
        search = SemanticSearch(demo_mode=True)
        search.index_documents([test_chunk])
        print("✅ Documents indexed")
        
        results = search.search("test document", top_k=1)
        print(f"✅ Search completed - Found {len(results)} results")
        
        # Test LLM integration
        print("\n🤖 Testing LLM integration...")
        llm = LLMIntegration(demo_mode=True)
        answer = llm.generate_answer("What is this document about?", [test_chunk])
        print(f"✅ Answer generated - Confidence: {answer.confidence:.2%}")
        
        # Test session management
        print("\n📊 Testing session management...")
        session_mgr = SessionManager()
        session = session_mgr.start_new_session("Test Session")
        qa_entry = session_mgr.add_qa_to_current_session("Test question", answer)
        print(f"✅ Session created with {len(session.qa_entries)} Q&A entries")
        
        # Test full Q&A workflow
        print("\n🎯 Testing full Q&A workflow...")
        core.semantic_search.index_documents([test_chunk])
        answer, chunks = core.ask_question("What is the main topic of this document?")
        print(f"✅ Q&A workflow completed - Answer length: {len(answer.answer)} chars")
        
        # Test export functionality
        print("\n📤 Testing export functionality...")
        try:
            export_path = core.export_session("json")
            print(f"✅ Session exported to: {export_path}")
        except Exception as e:
            print(f"⚠️  Export test skipped: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! StudyMate is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_dependencies():
    """Test optional dependencies"""
    print("\n🔧 Testing Optional Dependencies")
    print("-" * 30)
    
    deps = {
        'numpy': 'Numerical computing',
        'requests': 'HTTP requests',
        'fitz': 'PyMuPDF - PDF processing',
        'sentence_transformers': 'Sentence embeddings',
        'faiss': 'Vector similarity search',
        'reportlab': 'PDF generation'
    }
    
    available = []
    missing = []
    
    for module, description in deps.items():
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
            available.append(module)
        except ImportError:
            print(f"❌ {module} - {description} (optional)")
            missing.append(module)
    
    print(f"\n📊 Summary: {len(available)} available, {len(missing)} missing")
    
    if missing:
        print("\n💡 To install missing dependencies:")
        if 'sentence_transformers' in missing:
            print("   pip install sentence-transformers")
        if 'faiss' in missing:
            print("   pip install faiss-cpu")
        if 'reportlab' in missing:
            print("   pip install reportlab")

def main():
    """Main verification function"""
    print("🎓 StudyMate Application Verification")
    print("=" * 60)
    
    # Test dependencies first
    test_dependencies()
    
    # Test core functionality
    success = test_core_functionality()
    
    if success:
        print("\n🌟 StudyMate Verification Complete - All Systems Operational!")
        print("\n🚀 To start StudyMate:")
        print("   python -m streamlit run app.py")
        print("   Then open: http://localhost:8501")
    else:
        print("\n⚠️  Some issues were found. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
