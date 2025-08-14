#!/usr/bin/env python3
"""
Test script to check StudyMate dependencies and identify any issues
"""

import sys
import traceback

def test_import(module_name, description=""):
    """Test importing a module and report status"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} - {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {description} - ERROR: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - {description} - WARNING: {e}")
        return False

def test_studymate_components():
    """Test StudyMate specific components"""
    print("\n🔍 Testing StudyMate Components:")
    
    # Test config
    try:
        from config import config
        print(f"✅ config - Demo mode: {config.is_demo_mode}")
    except Exception as e:
        print(f"❌ config - ERROR: {e}")
        traceback.print_exc()
    
    # Test backend components
    try:
        from backend.document_processor import DocumentProcessor
        print("✅ backend.document_processor")
    except Exception as e:
        print(f"❌ backend.document_processor - ERROR: {e}")
    
    try:
        from backend.semantic_search import SemanticSearch
        print("✅ backend.semantic_search")
    except Exception as e:
        print(f"❌ backend.semantic_search - ERROR: {e}")
    
    try:
        from backend.llm_integration import LLMIntegration
        print("✅ backend.llm_integration")
    except Exception as e:
        print(f"❌ backend.llm_integration - ERROR: {e}")
    
    try:
        from backend.session_manager import SessionManager
        print("✅ backend.session_manager")
    except Exception as e:
        print(f"❌ backend.session_manager - ERROR: {e}")
    
    try:
        from backend.studymate_core import StudyMateCore
        print("✅ backend.studymate_core")
    except Exception as e:
        print(f"❌ backend.studymate_core - ERROR: {e}")
    
    # Test frontend components
    try:
        from frontend.ui_components import render_main_header
        print("✅ frontend.ui_components")
    except Exception as e:
        print(f"❌ frontend.ui_components - ERROR: {e}")

def main():
    """Main test function"""
    print("🧪 StudyMate Dependency Test")
    print("=" * 50)
    
    print("\n📦 Testing Core Dependencies:")
    
    # Core dependencies
    core_deps = [
        ("streamlit", "Web framework"),
        ("python_dotenv", "Environment variables"),
        ("requests", "HTTP requests"),
        ("numpy", "Numerical computing"),
        ("pandas", "Data manipulation"),
    ]
    
    for module, desc in core_deps:
        test_import(module, desc)
    
    print("\n📄 Testing PDF Processing:")
    pdf_deps = [
        ("fitz", "PyMuPDF - PDF processing"),
    ]
    
    for module, desc in pdf_deps:
        test_import(module, desc)
    
    print("\n🤖 Testing AI/ML Dependencies:")
    ai_deps = [
        ("sentence_transformers", "Sentence embeddings"),
        ("faiss", "Vector similarity search"),
        ("torch", "PyTorch deep learning"),
        ("transformers", "Hugging Face transformers"),
        ("sklearn", "Scikit-learn ML library"),
    ]
    
    for module, desc in ai_deps:
        test_import(module, desc)
    
    print("\n📊 Testing Export Dependencies:")
    export_deps = [
        ("reportlab", "PDF generation"),
    ]
    
    for module, desc in export_deps:
        test_import(module, desc)
    
    # Test StudyMate components
    test_studymate_components()
    
    print("\n🎯 Testing StudyMate Core Functionality:")
    try:
        from backend.studymate_core import StudyMateCore
        core = StudyMateCore(demo_mode=True)
        status = core.get_system_status()
        print(f"✅ StudyMate Core initialized successfully")
        print(f"   - Demo mode: {status.get('demo_mode')}")
        print(f"   - Model: {status.get('model_name')}")
    except Exception as e:
        print(f"❌ StudyMate Core initialization failed: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🏁 Test Complete!")

if __name__ == "__main__":
    main()
