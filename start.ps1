# Smart Notes Summarizer - Startup Script
# This script starts both backend and frontend servers

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Starting Smart Notes Summarizer..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend" -PathType Container) -or -not (Test-Path "frontend" -PathType Container)) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
        return $connection
    }
    catch {
        return $false
    }
}

# Check if ports are available
if (Test-Port -Port 5000) {
    Write-Host "Warning: Port 5000 is already in use. Backend might already be running." -ForegroundColor Yellow
}

if (Test-Port -Port 3000) {
    Write-Host "Warning: Port 3000 is already in use. Frontend might already be running." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; Write-Host 'Backend starting on http://localhost:5000' -ForegroundColor Green; python app.py" -WindowStyle Normal

Write-Host "Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; Write-Host 'Frontend starting on http://localhost:3000' -ForegroundColor Green; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Smart Notes Summarizer Started!      " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Opening browser in 10 seconds..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to cancel" -ForegroundColor Gray
Write-Host ""

Start-Sleep -Seconds 10

Write-Host "Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Both servers are running in separate windows." -ForegroundColor Green
Write-Host "To stop the servers, close the PowerShell windows or press Ctrl+C in each." -ForegroundColor Gray
Write-Host ""

