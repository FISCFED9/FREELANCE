# Script para iniciar Ollama en Windows
Write-Host "🚀 Iniciando Ollama..." -ForegroundColor Green

# Ruta del ejecutable
$ollama = "C:\Users\alber\AppData\Local\Programs\Ollama\ollama.exe"

# Verificar si está corriendo
$running = Get-Process -Name ollama -ErrorAction SilentlyContinue

if ($running) {
    Write-Host "✅ Ollama ya está corriendo (PID: $($running.Id))" -ForegroundColor Green
} else {
    Write-Host "⏳ Iniciando servicio..." -ForegroundColor Yellow
    Start-Process $ollama -ArgumentList "serve" -NoNewWindow
    Start-Sleep -Seconds 3
}

# Verificar puerto
$response = $null
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Ollama respondiendo en puerto 11434" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama no responde" -ForegroundColor Red
    exit 1
}

# Listar modelos
Write-Host "`n📦 Modelos disponibles:" -ForegroundColor Cyan
$models = $response.Content | ConvertFrom-Json
$models.models | ForEach-Object {
    Write-Host "  • $($_.name) ($([math]::Round($_.size / 1GB, 2)) GB)" -ForegroundColor White
}

Write-Host "`n✨ Ollama listo para usar en http://localhost:11434" -ForegroundColor Green
