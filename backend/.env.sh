# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_PATH=smart_notes.db

# Model Configuration (offline)
SUMMARIZATION_MODEL=offline
QA_MODEL=offline
MAX_CHUNK_SIZE=1024

# Server Configuration
HOST=0.0.0.0
PORT=5000

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=pdf,docx,doc,txt
