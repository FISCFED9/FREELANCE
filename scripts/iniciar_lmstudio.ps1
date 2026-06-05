# Iniciar LMStudio Server
Write-Host "Iniciando LMStudio Server..." -ForegroundColor Cyan

$proceso = Get-Process -Name "LM Studio" -ErrorAction SilentlyContinue
if ($proceso) {
    Write-Host "LMStudio ya esta corriendo" -ForegroundColor Green
    exit 0
}

$lmstudioPath = "$env:USERPROFILE\.lmstudio\bin\lms.exe"
if (Test-Path $lmstudioPath) {
    Start-Process $lmstudioPath -ArgumentList "server", "start"
    Write-Host "Servidor iniciado en http://localhost:1234" -ForegroundColor Green
    Write-Host "Modelos: Qwen 3.5 9B | Llama3-TAIDE 8B | Gemma 3 4B | Nemotron 3 Nano 4B" -ForegroundColor Yellow
} else {
    Write-Host "LMStudio no encontrado en $lmstudioPath" -ForegroundColor Red
    exit 1
}

Write-Host "Esperando servidor..." -ForegroundColor Yellow
$intentos = 0
do {
    Start-Sleep -Seconds 2
    $intentos++
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -Method Get -TimeoutSec 2
        Write-Host "Servidor listo! Modelos: $($response.data.Count)" -ForegroundColor Green
        break
    } catch {
        if ($intentos -gt 15) {
            Write-Host "Timeout esperando servidor" -ForegroundColor Red
            exit 1
        }
    }
} while ($true)
