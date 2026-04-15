# Quick Start Guide - Smart Notes Summarizer

This guide will help you quickly get the Smart Notes Summarizer running on your local machine.

## Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- Windows PowerShell (or your terminal)

## Quick Start Instructions

### Option 1: Using Quick Start Script (Easiest!)

**Windows PowerShell:**

1. Open PowerShell in the project directory
2. Run the start script:
   ```powershell
   .\start.ps1
   ```
3. Two new windows will open - one for backend, one for frontend
4. Your browser will automatically open to http://localhost:3000

**To stop the servers:**
```powershell
.\stop.ps1
```

That's it! You can now use the Smart Notes Summarizer.

---

### Option 2: Manual Start (Step by Step)

#### Step 1: Start the Backend Server

Open a PowerShell terminal and run:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

The backend will start on `http://localhost:5000`

#### Step 2: Start the Frontend Server

Open a **NEW** PowerShell terminal and run:

```powershell
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

#### Step 3: Access the Application

Open your web browser and navigate to:
**http://localhost:3000**

---

### Option 3: Manual Setup (Troubleshooting)

If the scripts don't work, follow these detailed steps:

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1

# Install/verify dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

#### Frontend Setup

Open a **NEW** terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Run the dev server
npm run dev
```

---

## Troubleshooting

### Backend Issues

**Problem:** "ModuleNotFoundError: No module named 'docx2txt'"

**Solution:** Activate the virtual environment before running:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

**Problem:** Port 5000 is already in use

**Solution:** Kill the process using port 5000:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Frontend Issues

**Problem:** Port 3000 is already in use

**Solution:** The vite config uses port 3000. You can change it in `frontend/vite.config.js` or kill the process:
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

**Problem:** Frontend can't connect to backend

**Solution:** Make sure the backend is running first! The frontend proxy expects the backend on `http://localhost:5000`

---

## Testing

### Test Backend Health

```powershell
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Backend is running"
}
```

### Test Summarization

Visit `http://localhost:3000` in your browser and:
1. Paste at least 50 characters of text
2. Click "Summarize Notes"
3. Wait for the AI to generate a summary

---

## Features

- ✅ **Text Summarization** - Paste your notes and get instant summaries
- ✅ **File Upload** - Upload PDF, DOCX, or TXT files (coming soon)
- ✅ **AI-Powered** - Uses LSA (Latent Semantic Analysis) for intelligent summarization
- ✅ **Configurable Length** - Choose how many sentences you want in your summary

---

## Project Structure

```
Smartnotessummarizer/
├── backend/           # Flask API server
│   ├── app.py        # Main application
│   ├── requirements.txt
│   └── venv/         # Virtual environment
├── frontend/          # React + Vite app
│   ├── src/
│   │   ├── App.jsx   # Main component
│   │   └── ...
│   └── package.json
└── QUICK_START.md    # This file
```

---

## API Endpoints

- `GET /` - Home page
- `GET /api/health` - Health check
- `POST /api/summarize` - Summarize text
  ```json
  {
    "text": "Your text here...",
    "sentences": 5
  }
  ```

---

## Need Help?

If you encounter any issues:
1. Check that both servers are running
2. Verify Python 3.8+ and Node.js 16+ are installed
3. Make sure port 5000 and 3000 are not in use
4. Check the console output for error messages

---

**Made with ❤️ by Smart Notes Squad**

