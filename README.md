# Problem Solver 🧠

A comprehensive Streamlit application that combines RAG (Retrieval Augmented Generation), YouTube video discovery, and AI-powered student assistance.

## Features ✨

- **🎥 YouTube Video Finder** - Find the best YouTube videos based on engagement rates (likes, views, engagement percentage)
- **📚 Student Assistant** - AI-powered student help system with document retrieval
- **🔍 RAG System** - Retrieval Augmented Generation for intelligent information retrieval
- **💾 Vector Database** - Chroma-based vector storage for semantic search
- **📝 Embedding Management** - Advanced embedding and vector store operations

## Project Structure 📁

```
Problem_solver/
├── Frontend/
│   ├── Home.py                           # Main Streamlit page
│   └── Pages/
│       ├── Best_Youtube_Video_Finder.py  # YouTube video search
│       └── Student_assistant.py          # Student assistance page
├── Backend/
│   └── backend.py                        # Backend API
├── RAG/
│   ├── data_ingestion.py                 # Data processing pipeline
│   ├── embedding_manager.py              # Embedding generation
│   ├── retriever.py                      # Information retrieval
│   ├── vector_store.py                   # Vector database management
│   └── __init__.py
├── Tools/
│   └── yt_video_finder.py                # YouTube search tool
├── Docs/
│   ├── Basic_concepts/                   # AI/ML concepts documentation
│   └── Basic_tutorials/                  # Git and tutorial guides
├── database/
│   └── chroma.sqlite3                    # Vector database
├── logs/                                 # Application logs
├── Dockerfile                            # Docker configuration
├── entrypoint.sh                         # Startup script
├── requirements.txt                      # Python dependencies
├── pyproject.toml                        # Project configuration
├── logger.py                             # Logging configuration
└── README.md                             # This file
```

## Tech Stack 🛠️

- **Frontend**: Streamlit
- **Backend**: Python, FastAPI (optional)
- **Vector Database**: Chroma
- **Embeddings**: HuggingFace, OpenAI
- **ML/AI**: PyTorch, TensorFlow, scikit-learn
- **Utilities**: Pandas, NumPy
- **Containerization**: Docker

## Installation 🚀

### Prerequisites
- Python 3.8+
- pip or conda
- YouTube API Key (for video finder feature)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Problem_solver
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run Frontend/Home.py
   ```

## Usage 💻

### YouTube Video Finder
1. Navigate to "Best YouTube Video Finder" page
2. Enter your search query (e.g., "machine learning tutorials")
3. Click the Search button
4. View results sorted by engagement rate
5. Click "Watch on YouTube" to visit the video

### Student Assistant
1. Go to "Student Assistant" page
2. Ask a question or request help
3. The system uses RAG to find relevant documents
4. Get AI-powered responses with source attribution

## Configuration ⚙️

### Logging
Logs are stored in the `logs/` directory. Configure logging in `logger.py`.

### Vector Database
The Chroma vector database is stored in `database/chroma.sqlite3`. Manage embeddings through:
- `RAG/embedding_manager.py` - Generate and manage embeddings
- `RAG/vector_store.py` - Vector storage operations

## API Keys Required 🔑

- **YouTube API Key**: Required for video search functionality
  - Get one from [Google Cloud Console](https://console.cloud.google.com/)

## Docker Deployment 🐳

Build and run with Docker:
```bash
docker build -t problem-solver .
docker run -p 8501:8501 problem-solver
```

## Development 👨‍💻

### Project Structure
- Keep frontend code in `Frontend/`
- Add tools in `Tools/`
- Extend RAG pipeline in `RAG/`
- API endpoints in `Backend/`

### Adding New Pages
1. Create a new file in `Frontend/Pages/`
2. Import required modules
3. Add page configuration
4. Access via Streamlit's multi-page app feature

### Logging
Use the configured logger for all output:
```python
from logger import get_logger
logger = get_logger(__name__)
logger.info("Your message here")
```

## Features in Development 🚧

- Enhanced RAG pipeline with multiple embedding models
- Multi-language support
- Advanced caching mechanisms
- Real-time data ingestion
- Analytics dashboard

## Troubleshooting 🔧

### "YouTube API key not found"
- Ensure `.env` file exists with `YOUTUBE_API_KEY` set
- Verify the API key is valid

### Slow response times
- Check vector database size
- Consider adding caching
- Review embedding model selection

### Streamlit connection issues
- Clear Streamlit cache: Click menu → "Clear cache"
- Hard refresh browser (Ctrl+Shift+R)
- Restart Streamlit server

## Contributing 🤝

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License 📄

This project is private and for internal use only.

## Contact & Support 📧

For issues or questions, please open an issue or contact the development team.

---

**Last Updated**: June 2026
