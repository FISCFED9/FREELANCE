#!/bin/bash
# ============================================
# SCRIPT PRINCIPAL: Guardar Conversación
# ============================================
# Conecta los dos agentes en secuencia:
# Agente 1 (Analizador) → Agente 2 (Organizador)
#
# Uso:
#   echo "conversación aquí" | ./guardar_conversacion.sh
#   ./guardar_conversacion.sh "texto de conversación"
#   cat conversacion.txt | ./guardar_conversacion.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Iniciando sistema de guardado de conversaciones..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Leer la conversación
if [ $# -gt 0 ]; then
    CONVERSACION="$*"
else
    CONVERSACION=$(cat)
fi

if [ -z "$CONVERSACION" ]; then
    echo "❌ Error: No se proporcionó conversación"
    exit 1
fi

echo "📝 Conversación recibida (${#CONVERSACION} caracteres)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# PASO 1: Agente Analizador
echo "🔍 PASO 1: Analizando conversación..."
ANALISIS=$(echo "$CONVERSACION" | python3 "$SCRIPT_DIR/agente_analizador.py")

if [ $? -ne 0 ]; then
    echo "❌ Error en el Agente Analizador"
    exit 1
fi

# Verificar si hay contenido valioso
TIENE_CONTENIDO=$(echo "$ANALISIS" | python3 -c "import json,sys; d=json.load(sys.stdin); print('si' if d.get('tiene_contenido_valioso') else 'no')")

if [ "$TIENE_CONTENIDO" = "no" ]; then
    RAZON=$(echo "$ANALISIS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('razon','Sin contenido valioso'))")
    echo "⏭️  Sin contenido valioso que guardar: $RAZON"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Proceso completado (nada que guardar)"
    exit 0
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# PASO 2: Agente Organizador
echo "📂 PASO 2: Organizando y guardando en GitHub..."
RESULTADO=$(echo "$ANALISIS" | python3 "$SCRIPT_DIR/agente_organizador.py")

if [ $? -ne 0 ]; then
    echo "❌ Error en el Agente Organizador"
    exit 1
fi

# Mostrar resultado final
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
EXITO=$(echo "$RESULTADO" | python3 -c "import json,sys; d=json.load(sys.stdin); print('si' if d.get('exito') else 'no')")

if [ "$EXITO" = "si" ]; then
    URL=$(echo "$RESULTADO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ruta_github',''))")
    echo "✅ ¡GUARDADO EXITOSAMENTE EN GITHUB!"
    echo "🔗 Ver en: $URL"
else
    RAZON=$(echo "$RESULTADO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('razon','Error desconocido'))")
    echo "❌ Error al guardar: $RAZON"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
