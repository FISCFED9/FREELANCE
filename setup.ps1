# ================================================================
# SETUP AUTOMÁTICO — Sistema de Memoria con Agentes IA
# FISCFED9/FREELANCE
# ================================================================
# Uso: Click derecho sobre este archivo → "Run with PowerShell"
# O desde PowerShell: .\setup.ps1
# ================================================================

$HOST.UI.RawUI.ForegroundColor = "Cyan"
Write-Host ""
Write-Host "========================================================"
Write-Host "  SETUP: Sistema de Memoria con 5 Agentes IA"
Write-Host "  FISCFED9/FREELANCE"
Write-Host "========================================================"
$HOST.UI.RawUI.ForegroundColor = "White"
Write-Host ""

# ─── 1. Verificar Python ──────────────────────────────────────────
Write-Host "[1/5] Verificando Python..." -ForegroundColor Yellow

$pythonCmd = $null
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "  ERROR: Python no encontrado." -ForegroundColor Red
    Write-Host "  Descarga Python en: https://www.python.org/downloads/"
    Write-Host "  Asegurate de marcar 'Add to PATH' durante la instalacion"
    Read-Host "Presiona Enter para salir"
    exit 1
}

$version = & $pythonCmd --version 2>&1
Write-Host "  OK: $version" -ForegroundColor Green

# ─── 2. Crear entorno virtual ─────────────────────────────────────
Write-Host ""
Write-Host "[2/5] Creando entorno virtual (.venv)..." -ForegroundColor Yellow

if (Test-Path ".venv") {
    Write-Host "  Ya existe .venv, usando el existente" -ForegroundColor Cyan
} else {
    & $pythonCmd -m venv .venv
    Write-Host "  OK: Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
$activateScript = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "  OK: Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "  AVISO: No se pudo activar el entorno virtual automaticamente" -ForegroundColor Yellow
    Write-Host "  Ejecuta manualmente: .\.venv\Scripts\Activate.ps1"
}

# ─── 3. Instalar dependencias ─────────────────────────────────────
Write-Host ""
Write-Host "[3/5] Instalando dependencias (anthropic SDK)..." -ForegroundColor Yellow

& $pythonCmd -m pip install --quiet --upgrade pip
& $pythonCmd -m pip install --quiet -r requirements.txt

Write-Host "  OK: Dependencias instaladas" -ForegroundColor Green

# ─── 4. Configurar variables de entorno ───────────────────────────
Write-Host ""
Write-Host "[4/5] Configurando API key..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "  OK: Archivo .env ya existe" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "  *** ACCION REQUERIDA ***" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Se creo el archivo .env — DEBES editar tu API key antes de continuar."
    Write-Host ""
    Write-Host "  Abre el archivo .env con el Bloc de notas y reemplaza:"
    Write-Host "    ANTHROPIC_API_KEY=tu_clave_openrouter_aqui"
    Write-Host "  con tu clave real de OpenRouter."
    Write-Host ""
    Write-Host "  Opciones para obtener clave:"
    Write-Host "    OpenRouter (recomendado): https://openrouter.ai/keys"
    Write-Host "    Anthropic directo:        https://console.anthropic.com"
    Write-Host "    OLLAMA local:             ver instrucciones en .env"
    Write-Host ""

    $openNotepad = Read-Host "  Abrir .env en el Bloc de notas ahora? (s/n)"
    if ($openNotepad -eq "s" -or $openNotepad -eq "S" -or $openNotepad -eq "si") {
        Start-Process "notepad.exe" ".env" -Wait
    }
}

# Cargar variables del .env
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.+)$") {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
    Write-Host "  OK: Variables de entorno cargadas" -ForegroundColor Green
}

# ─── 5. Verificar configuracion ───────────────────────────────────
Write-Host ""
Write-Host "[5/5] Verificando configuracion..." -ForegroundColor Yellow

$apiKey = [System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "Process")
if (-not $apiKey -or $apiKey -eq "tu_clave_openrouter_aqui") {
    Write-Host "  AVISO: ANTHROPIC_API_KEY no configurada" -ForegroundColor Red
    Write-Host "  Edita el archivo .env con tu clave real antes de correr los agentes"
} else {
    Write-Host "  OK: ANTHROPIC_API_KEY configurada" -ForegroundColor Green
}

$baseUrl = [System.Environment]::GetEnvironmentVariable("ANTHROPIC_BASE_URL", "Process")
if ($baseUrl) {
    Write-Host "  OK: ANTHROPIC_BASE_URL = $baseUrl" -ForegroundColor Green
}

# ─── RESULTADO FINAL ─────────────────────────────────────────────
Write-Host ""
Write-Host "========================================================"  -ForegroundColor Cyan
Write-Host "  SETUP COMPLETADO"  -ForegroundColor Cyan
Write-Host "========================================================"  -ForegroundColor Cyan
Write-Host ""
Write-Host "Comandos disponibles:" -ForegroundColor White
Write-Host ""
Write-Host "  Demo completo (ver el sistema en accion):" -ForegroundColor Yellow
Write-Host "    python demo_sistema_completo.py"
Write-Host ""
Write-Host "  Guardar una conversacion:" -ForegroundColor Yellow
Write-Host "    bash agentes\guardar_conversacion.sh  (necesita Git Bash)"
Write-Host ""
Write-Host "  Ver proyectos pendientes:" -ForegroundColor Yellow
Write-Host "    python agentes\agente_proyectos.py --revisar"
Write-Host ""
Write-Host "  Recordatorios activos:" -ForegroundColor Yellow
Write-Host "    python agentes\agente_proyectos.py --recordatorio"
Write-Host ""
Write-Host "  Ideas de monetizacion rapidas:" -ForegroundColor Yellow
Write-Host "    python agentes\agente_investigador.py --rapido"
Write-Host ""
Write-Host "  Research sobre un nicho:" -ForegroundColor Yellow
Write-Host "    python agentes\agente_investigador.py --nicho 'apps de salud'"
Write-Host ""
Write-Host "  Buscar en historial de conversaciones:" -ForegroundColor Yellow
Write-Host "    python agentes\agente_buscador.py 'android room database'"
Write-Host ""

Read-Host "Presiona Enter para cerrar"
