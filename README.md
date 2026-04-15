# 🧠 Smart Notes Summarizer

An AI-powered web application that transforms your notes into concise summaries and generates Q&A pairs using state-of-the-art transformer models.

## 👥 Team Information

**Team Name:** Smart Notes Squad  
**Members:**
- Shiksha Raturi (Lead)
- Harshita Sharma
- Garima Pal

## ✨ Features

- 📝 **Text Input or File Upload** - Enter notes directly or upload PDF/DOCX files
- 🤖 **AI-Powered Summarization** - Using BART and T5 transformer models
- ❓ **Automatic Q&A Generation** - Generate question-answer pairs from your notes
- 📊 **Customizable Summaries** - Choose length (short/medium/detailed) and format (paragraph/points)
- 📜 **History Tracking** - Save and access all your previous summaries
- 👤 **User Authentication** - Secure login and registration system
- 💾 **Export Options** - Download summaries as PDF or TXT files
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **Flask** - Python web framework
- **SQLite** - Database
- **Transformers (Hugging Face)** - AI models
- **PyTorch** - Deep learning framework
- **PyPDF2** - PDF processing
- **docx2txt** - DOCX processing

## 📋 Prerequisites

- **Node.js** 16+ and npm
- **Python** 3.8+
- **pip** (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-notes-summarizer.git
cd smart-notes-summarizer
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the Flask server
python app.py
```

The backend server will start on `http://localhost:5000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from root)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## 📁 Project Structure

```
smart-notes-summarizer/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── init_db.py            # Database initialization
│   ├── requirements.txt       # Python dependencies
│   ├── .env                  # Environment variables
│   └── smart_notes.db        # SQLite database (generated)
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── apiService.js     # API client
│   │   ├── index.css         # Global styles
│   │   └── main.jsx          # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables (.env)

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_PATH=smart_notes.db
HOST=0.0.0.0
PORT=5000
```

### Frontend Environment Variables (.env)

```env
VITE_API_URL=http://localhost:5000/api
```

## 📊 Database Schema

### Users Table
| Column      | Type      | Description                |
|-------------|-----------|----------------------------|
| user_id     | INTEGER   | Primary key (auto)         |
| name        | TEXT      | User's full name           |
| email       | TEXT      | Unique email address       |
| password    | TEXT      | Hashed password            |
| created_at  | TIMESTAMP | Account creation date      |

### Summaries Table
| Column      | Type      | Description                |
|-------------|-----------|----------------------------|
| summary_id  | INTEGER   | Primary key (auto)         |
| user_id     | INTEGER   | Foreign key to users       |
| input_type  | TEXT      | 'text', 'pdf', or 'docx'   |
| content     | TEXT      | Original content preview   |
| summary     | TEXT      | Generated summary          |
| qa_pairs    | TEXT      | JSON array of Q&A pairs    |
| created_at  | TIMESTAMP | Summary creation date      |

## 🎯 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### File Processing
- `POST /api/upload` - Upload and extract text from PDF/DOCX

### Summary Generation
- `POST /api/generate` - Generate summary and Q&A pairs

### History & Downloads
- `GET /api/history/<user_id>` - Get user's summary history
- `GET /api/download/<summary_id>?format=txt|pdf` - Download summary

## 🤖 AI Models Used

1. **facebook/bart-large-cnn** - For text summarization
2. **t5-base** - For Q&A pair generation

## 🚀 Deployment

### Deploy Backend (Render/Heroku)

1. Create a `Procfile`:
```
web: gunicorn app:app
```

2. Deploy to your platform of choice
3. Set environment variables

### Deploy Frontend (Vercel/Netlify)

1. Build the project:
```bash
npm run build
```

2. Deploy the `dist` folder to your platform

## 🎨 UI Improvements & Future Features

### Suggested Enhancements
- 🎴 **Flashcard Generation** - Convert Q&A pairs into interactive flashcards
- 🎤 **Speech-to-Text** - Upload notes via voice recording
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 📊 **Analytics Dashboard** - Track summary usage and statistics
- 🔗 **Share Summaries** - Generate shareable links
- 🌐 **Multi-language Support** - Summarize notes in different languages
- 📱 **Progressive Web App** - Install as mobile app
- 🔔 **Email Notifications** - Get summaries delivered to your inbox

## 🐛 Troubleshooting

### Common Issues

**Backend not starting:**
- Ensure Python 3.8+ is installed
- Activate virtual environment
- Install all requirements

**Frontend not connecting to backend:**
- Check if backend is running on port 5000
- Verify CORS settings in Flask app
- Check API URL in frontend config

**Model loading errors:**
- First run may take time to download models
- Ensure stable internet connection
- Check disk space (models are ~1-2GB)

## 📝 Usage Guide

1. **Register/Login** - Create an account or continue as guest
2. **Choose Input Method** - Type text or upload a document
3. **Customize Settings** - Select summary length and format
4. **Generate Summary** - Click generate and wait for AI processing
5. **Review Results** - View summary and Q&A pairs
6. **Download or Save** - Export summary or save to history

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For questions or support, please contact:
- Email: smartnotessquad@example.com
- GitHub: [Your GitHub Profile]

## 🙏 Acknowledgments

- Hugging Face for transformer models
- Flask and React communities
- All contributors and testers

---

**Made with ❤️ by Smart Notes Squad**