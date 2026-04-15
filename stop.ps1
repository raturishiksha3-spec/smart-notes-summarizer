# Smart Notes Summarizer - Stop Script
# This script stops both backend and frontend servers

Write-Host "Stopping Smart Notes Summarizer servers..." -ForegroundColor Yellow
Write-Host ""

# Find and stop backend Python processes
$backendProcesses = Get-Process | Where-Object {
    $_.ProcessName -eq 'python' -and 
    $_.Path -like "*Smartnotessummarizer\backend\venv*"
}

if ($backendProcesses) {
    Write-Host "Stopping backend servers..." -ForegroundColor Cyan
    $backendProcesses | ForEach-Object {
        Write-Host "  Stopping process $($_.Id)..." -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Backend stopped." -ForegroundColor Green
}
else {
    Write-Host "No backend processes found." -ForegroundColor Gray
}

# Find and stop frontend Node processes
# We'll look for node processes running on port 3000
try {
    $frontendProcess = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | 
        Select-Object -ExpandProperty OwningProcess -First 1
    
    if ($frontendProcess) {
        Write-Host "Stopping frontend server..." -ForegroundColor Cyan
        Stop-Process -Id $frontendProcess -Force -ErrorAction SilentlyContinue
        Write-Host "Frontend stopped." -ForegroundColor Green
    }
    else {
        Write-Host "No frontend process found." -ForegroundColor Gray
    }
}
catch {
    Write-Host "No frontend process found." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Smart Notes Summarizer stopped." -ForegroundColor Green
Write-Host ""

