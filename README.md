# 🎓 StudyMate - AI-Powered Academic Assistant

StudyMate is an advanced AI-powered academic assistant that transforms static study materials into an interactive, conversational knowledge base. Built with IBM Granite models, FAISS semantic search, and modern web technologies.

## ✨ Key Features

### 🎯 **Grounded AI Responses**
- All answers are strictly based on your uploaded PDF documents
- No hallucination - responses are grounded in your actual study materials
- Source references provided for verification

### 🤖 **IBM Granite Integration**
- Powered by IBM Watsonx Granite-3B-Code-Instruct model
- Advanced natural language understanding
- High-quality, contextual responses

### 🔍 **Advanced Semantic Search**
- FAISS-powered vector search for precise document retrieval
- SentenceTransformers embeddings for semantic understanding
- Multi-document reasoning and cross-referencing

### 📚 **Multi-PDF Support**
- Upload and analyze multiple PDF documents simultaneously
- Cross-document information synthesis
- Comprehensive knowledge base creation

### 📊 **Session Management**
- Track your study progress with detailed analytics
- Export Q&A history in multiple formats (PDF, CSV, JSON)
- Downloadable revision logs for later study

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- IBM Cloud account (for production mode)
- 4GB+ RAM recommended

### Installation

1. **Clone or download the project**
   ```bash
   cd StudyMate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your IBM credentials (optional for demo mode)
   ```

5. **Run StudyMate**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:8501`
   - Start uploading PDFs and asking questions!

## 🔧 Configuration

### Demo Mode (Default)
- No API keys required
- Simulated AI responses for testing
- Full UI functionality
- Perfect for development and testing

### Production Mode
Set up IBM Watsonx credentials in `.env`:
```env
IBM_API_KEY=your_api_key
IBM_PROJECT_ID=your_project_id
DEMO_MODE=False
```

## 📖 Usage Guide

### 1. **Upload Documents**
- Use the sidebar to upload PDF files
- Multiple files supported
- Files are processed and indexed automatically

### 2. **Ask Questions**
- Type natural language questions about your documents
- Examples:
  - "What are the main themes in this research?"
  - "Explain the methodology used in chapter 3"
  - "Compare the findings from different studies"

### 3. **Review Answers**
- Get AI-powered responses with confidence scores
- View source references from your documents
- See which pages and sections were used

### 4. **Export Results**
- Download your Q&A session for revision
- Available formats: PDF, CSV, JSON
- Perfect for creating study guides

## 🏗️ Architecture

```
StudyMate/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── backend/              # Core AI and processing logic
│   ├── studymate_core.py    # Main orchestration
│   ├── document_processor.py # PDF text extraction
│   ├── semantic_search.py    # FAISS vector search
│   ├── llm_integration.py    # IBM Granite integration
│   └── session_manager.py    # Session and export handling
├── frontend/             # UI components
│   └── ui_components.py     # Streamlit UI components
├── requirements.txt      # Python dependencies
└── .env.example         # Environment template
```

## 🔬 Technical Details

### **Document Processing**
- PyMuPDF for PDF text extraction
- Intelligent text chunking (500 words + 100 overlap)
- Metadata preservation and page tracking

### **Semantic Search**
- SentenceTransformers (all-MiniLM-L6-v2) for embeddings
- FAISS IndexFlatIP for cosine similarity search
- Efficient vector indexing and retrieval

### **AI Integration**
- IBM Watsonx Granite-3B-Code-Instruct model
- RESTful API integration with proper authentication
- Confidence scoring and response validation

### **Frontend**
- Modern Streamlit interface with custom CSS
- Responsive design with professional styling
- Real-time progress tracking and feedback

## 🎯 Use Cases

### **Students**
- Exam preparation and revision
- Research paper analysis
- Textbook comprehension
- Assignment research

### **Researchers**
- Literature review assistance
- Paper analysis and comparison
- Research methodology understanding
- Citation and reference tracking

### **Educators**
- Course material preparation
- Student question answering
- Content analysis and summarization
- Educational resource development

## 🔒 Privacy & Security

- **Local Processing**: Documents processed locally
- **Secure API**: IBM Cloud security standards
- **No Data Storage**: Documents not permanently stored
- **Offline Capable**: Demo mode works without internet

## 📊 Performance

- **Processing Speed**: ~2-5 seconds per PDF page
- **Memory Usage**: ~100MB base + 50MB per document
- **Concurrent Users**: Supports multiple sessions
- **Scalability**: Easily deployable to cloud platforms

## 🛠️ Development

### **Adding New Features**
1. Backend logic in `backend/` modules
2. UI components in `frontend/ui_components.py`
3. Main app integration in `app.py`

### **Customization**
- Modify `config.py` for application settings
- Update CSS in `ui_components.py` for styling
- Extend LLM integration for other models

## 📈 Roadmap

### **Phase 1: Core MVP** ✅
- PDF upload and processing
- IBM Granite integration
- Basic Q&A functionality
- Export capabilities

### **Phase 2: Enhancements** 🚧
- Multi-language support
- Advanced analytics dashboard
- Collaborative features
- Mobile optimization

### **Phase 3: Enterprise** 📋
- LMS integration
- User management
- Advanced security features
- Custom model training

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check this README and code comments
- **Issues**: Report bugs and feature requests via GitHub issues
- **Demo**: Try the demo mode for immediate testing

## 🙏 Acknowledgments

- **IBM Watsonx** for powerful AI models
- **Streamlit** for the amazing web framework
- **FAISS** for efficient similarity search
- **SentenceTransformers** for semantic embeddings

---

**Transform your study materials into interactive knowledge with StudyMate!** 🎓✨
