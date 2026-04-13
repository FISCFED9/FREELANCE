"""
AGENTE 1: ANALIZADOR DE CONVERSACIONES
========================================
Recibe texto de una conversación y extrae solo lo importante.
Filtra basura (saludos, confirmaciones simples, repeticiones).

Uso:
    python agente_analizador.py "texto de la conversación"
    o
    echo "conversación" | python agente_analizador.py
"""

import anthropic
import sys
import json
from datetime import datetime

# Cliente con la configuración de OpenRouter vía settings.json
client = anthropic.Anthropic()

SYSTEM_PROMPT = """Eres el Agente Analizador del proyecto FREELANCE de FISCFED9.

Tu única función es analizar conversaciones entre el usuario y Claude,
y extraer SOLO lo que vale la pena guardar.

REGLAS DE FILTRADO:

✅ SIEMPRE GUARDAR:
- Código generado (cualquier lenguaje)
- Soluciones a errores/bugs encontrados
- Decisiones importantes tomadas
- Configuraciones y ajustes acordados
- Ideas y planes de desarrollo
- Aprendizajes técnicos clave
- URLs, nombres de archivos, rutas importantes

❌ NUNCA GUARDAR:
- Saludos ("hola", "gracias", "ok", "entendido")
- Confirmaciones simples (sí/no sin contexto)
- Preguntas de aclaración ya resueltas
- Contenido duplicado o repetitivo
- Conversación casual sin valor técnico

FORMATO DE SALIDA:
Devuelve un JSON con esta estructura exacta:
{
  "fecha": "YYYY-MM-DD",
  "tiene_contenido_valioso": true/false,
  "resumen_breve": "1-2 frases de qué trata",
  "categorias": ["codigo", "decision", "solucion", "aprendizaje", "configuracion"],
  "contenido_filtrado": "El contenido importante formateado en Markdown",
  "codigo_extraido": ["bloque1", "bloque2"],  // solo si hay código
  "palabras_clave": ["tag1", "tag2", "tag3"]
}

Si no hay nada valioso, devuelve:
{
  "tiene_contenido_valioso": false,
  "razon": "explicación breve"
}
"""

def analizar_conversacion(texto_conversacion: str) -> dict:
    """
    Analiza una conversación y extrae lo importante.

    Args:
        texto_conversacion: El texto de la conversación a analizar

    Returns:
        dict con el análisis
    """
    print("🔍 Agente Analizador procesando conversación...", file=sys.stderr)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""Analiza esta conversación y extrae solo lo valioso:

---INICIO CONVERSACIÓN---
{texto_conversacion}
---FIN CONVERSACIÓN---

Devuelve SOLO el JSON, sin texto adicional."""
            }
        ]
    )

    # Extraer el texto de la respuesta
    texto_respuesta = ""
    for block in response.content:
        if block.type == "text":
            texto_respuesta = block.text
            break

    # Intentar parsear como JSON
    try:
        # Limpiar posible markdown code block
        if "```json" in texto_respuesta:
            texto_respuesta = texto_respuesta.split("```json")[1].split("```")[0].strip()
        elif "```" in texto_respuesta:
            texto_respuesta = texto_respuesta.split("```")[1].split("```")[0].strip()

        resultado = json.loads(texto_respuesta)
        resultado["fecha"] = resultado.get("fecha", datetime.now().strftime("%Y-%m-%d"))
        return resultado
    except json.JSONDecodeError:
        # Si no es JSON válido, devolver el texto como contenido
        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "tiene_contenido_valioso": True,
            "resumen_breve": "Contenido analizado (formato manual)",
            "categorias": ["general"],
            "contenido_filtrado": texto_respuesta,
            "codigo_extraido": [],
            "palabras_clave": []
        }


def main():
    # Leer la conversación desde stdin o argumento
    if len(sys.argv) > 1:
        conversacion = " ".join(sys.argv[1:])
    else:
        print("📖 Leyendo conversación desde stdin...", file=sys.stderr)
        conversacion = sys.stdin.read()

    if not conversacion.strip():
        print("❌ Error: No se proporcionó conversación para analizar", file=sys.stderr)
        sys.exit(1)

    # Analizar
    resultado = analizar_conversacion(conversacion)

    # Mostrar resultado
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

    if resultado.get("tiene_contenido_valioso", False):
        print(f"\n✅ Contenido valioso encontrado: {resultado.get('resumen_breve', '')}", file=sys.stderr)
    else:
        print(f"\n⏭️  Sin contenido valioso: {resultado.get('razon', '')}", file=sys.stderr)


if __name__ == "__main__":
    main()
