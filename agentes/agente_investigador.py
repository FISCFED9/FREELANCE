"""
AGENTE 5: MARKET RESEARCHER
=============================
Hace deep research sobre oportunidades de monetización
y sugiere 3 nuevos proyectos personalizados basados en:
- Tendencias actuales del mercado
- Habilidades del usuario (extraídas de conversaciones pasadas)
- Demanda real vs oferta disponible
- Potencial de monetización con IA

Uso:
    python agente_investigador.py               # Research completo
    python agente_investigador.py --rapido      # 3 ideas rápidas
    python agente_investigador.py --nicho "X"   # Research sobre nicho específico
"""

import anthropic
import sys
import json
import os
from datetime import datetime
from pathlib import Path

REPO_PATH = "/workspace/project"
INDICE_PATH = f"{REPO_PATH}/indices/indice_conversaciones.json"
RESEARCH_PATH = f"{REPO_PATH}/investigacion"

client = anthropic.Anthropic()

SYSTEM_MARKET_RESEARCH = """Eres el Agente Market Researcher de FISCFED9, un experto en monetización digital.

Tu trabajo es identificar oportunidades de negocio reales con:
- Alta demanda actual
- Baja competencia (o competencia débil)
- Capacidad para implementar IA como ventaja competitiva
- Monetización en menos de 60 días

CONTEXTO DEL USUARIO (FISCFED9):
- Sabe programar (Python, Android/móvil según conversaciones)
- Trabaja con Claude/IA — eso es una ventaja ENORME
- Busca proyectos que se puedan monetizar
- Tiene un proyecto de salud pendiente (oportunidad: IA + salud)

CRITERIOS DE EVALUACIÓN para cada idea:
1. Demanda: ¿Hay gente buscando esto ahora mismo?
2. Competencia: ¿Es fácil diferenciarse?
3. Ticket promedio: ¿Cuánto se puede cobrar?
4. Tiempo a primer ingreso: ¿Cuántos días para cobrar el primero?
5. Rol de la IA: ¿Cómo multiplica el valor?

ÁREAS DE MAYOR OPORTUNIDAD AHORA MISMO (2026):
- Automatización con IA para PyMES (toman decisiones lentas, pagan bien)
- Agentes IA personalizados para industrias específicas
- Contenido y SEO con IA (pero enfocado en conversión, no volumen)
- Apps de salud + IA (regulación baja en servicios de bienestar)
- Consultoría de implementación de IA (el que sabe hacer = el que cobra)
- UGC + IA para marcas que no saben crear contenido

Devuelve un JSON estructurado con análisis profundo.
"""

SYSTEM_IDEAS_RAPIDAS = """Eres un consultor de negocios digitales experto.

Genera exactamente 3 ideas de proyectos monetizables para alguien que:
- Sabe programar y trabajar con IA
- Quiere monetizar pronto (menos de 60 días)
- Prefiere proyectos que crezcan solos o con poco mantenimiento

Para cada idea incluye:
- Nombre comercial atractivo
- Qué problema resuelve (1 línea)
- Cómo se monetiza (precio sugerido)
- Cómo usa la IA como ventaja
- Tiempo estimado para primer cliente

Sé específico y realista. No des ideas genéricas.

Devuelve JSON:
{
  "ideas": [
    {
      "nombre": "...",
      "tagline": "...",
      "problema_que_resuelve": "...",
      "modelo_monetizacion": "...",
      "precio_sugerido": "...",
      "rol_ia": "...",
      "dias_primer_cliente": 0,
      "esfuerzo": "bajo/medio/alto",
      "potencial_mensual": "...",
      "primer_paso_concreto": "..."
    }
  ],
  "recomendacion_principal": "nombre de la idea más prometedora",
  "razon": "por qué esa es la mejor opción ahora mismo"
}
"""


def research_completo(perfil_usuario: dict = None) -> dict:
    """
    Hace un deep research completo y genera oportunidades personalizadas.
    Usa web_search para tendencias actuales + análisis de Claude.
    """
    print("🔍 Iniciando Market Research...", file=sys.stderr)

    # Cargar historial para personalizar
    habilidades_detectadas = []
    proyectos_pasados = []

    if os.path.exists(INDICE_PATH):
        with open(INDICE_PATH, "r") as f:
            indice = json.load(f)
        for conv in indice.get("conversaciones", []):
            habilidades_detectadas.extend(conv.get("tecnologias", []))
            proyectos_pasados.extend(conv.get("proyectos_relacionados", []))

    habilidades_detectadas = list(set(habilidades_detectadas))

    # Búsqueda web + análisis con Claude
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        tools=[
            {"type": "web_search_20260209", "name": "web_search"},
        ],
        system=SYSTEM_MARKET_RESEARCH,
        messages=[{
            "role": "user",
            "content": f"""Haz un deep research de oportunidades de monetización para este perfil:

HABILIDADES DETECTADAS: {habilidades_detectadas}
PROYECTOS PASADOS: {list(set(proyectos_pasados))}
FECHA ACTUAL: {datetime.now().strftime("%Y-%m-%d")}

Busca en internet las tendencias más actuales de:
1. "servicios IA para empresas 2026 demanda"
2. "ideas negocio digital monetizar rápido 2026"
3. "nichos poco competidos sitio web ganar dinero"

Luego genera las 3 MEJORES oportunidades personalizadas para este usuario.

Devuelve un JSON con:
{{
  "fecha_research": "{datetime.now().strftime('%Y-%m-%d')}",
  "tendencias_encontradas": ["tendencia1", "tendencia2", "tendencia3"],
  "oportunidades": [
    {{
      "rank": 1,
      "nombre": "...",
      "tagline": "...",
      "problema_que_resuelve": "...",
      "mercado_objetivo": "...",
      "modelo_monetizacion": "...",
      "precio_sugerido": "...",
      "rol_ia": "...",
      "dias_primer_cliente": 0,
      "potencial_mensual_usd": "...",
      "competencia_actual": "baja/media/alta",
      "primer_paso_hoy": "...",
      "recursos_necesarios": "..."
    }}
  ],
  "recomendacion_principal": "...",
  "por_que_ahora": "..."
}}"""
        }]
    )

    texto = ""
    for block in response.content:
        if block.type == "text":
            texto = block.text

    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0].strip()
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0].strip()

    try:
        resultado = json.loads(texto)
    except:
        resultado = {"research_raw": texto, "fecha": datetime.now().strftime("%Y-%m-%d")}

    # Guardar el research
    guardar_research(resultado)
    return resultado


def ideas_rapidas() -> dict:
    """Genera 3 ideas rápidas sin búsqueda web."""
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=SYSTEM_IDEAS_RAPIDAS,
        messages=[{
            "role": "user",
            "content": f"""El usuario sabe: Python, Android, Claude/IA, GitHub.
Tiene proyecto de salud pendiente que puede terminar.
Fecha: {datetime.now().strftime("%Y-%m-%d")}

Genera las 3 mejores ideas monetizables para él AHORA MISMO.
Devuelve SOLO el JSON."""
        }]
    )

    texto = ""
    for block in response.content:
        if block.type == "text":
            texto = block.text

    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0].strip()
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0].strip()

    return json.loads(texto)


def research_nicho(nicho: str) -> dict:
    """Research específico sobre un nicho dado."""
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3096,
        thinking={"type": "adaptive"},
        tools=[
            {"type": "web_search_20260209", "name": "web_search"},
        ],
        system=SYSTEM_MARKET_RESEARCH,
        messages=[{
            "role": "user",
            "content": f"""Analiza este nicho específico para monetización con IA:

NICHO: {nicho}

Busca:
1. Demanda actual
2. Competencia existente
3. Cómo usar IA como ventaja competitiva
4. Precio de mercado

Devuelve JSON con análisis completo del nicho y 2-3 formas de monetizarlo."""
        }]
    )

    texto = ""
    for block in response.content:
        if block.type == "text":
            texto = block.text

    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0].strip()
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(texto)
    except:
        return {"nicho": nicho, "analisis": texto}


def guardar_research(research: dict):
    """Guarda el research en la carpeta de investigación."""
    Path(RESEARCH_PATH).mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d")
    archivo = f"{RESEARCH_PATH}/{fecha}_market_research.json"
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(research, f, ensure_ascii=False, indent=2)
    print(f"💾 Research guardado: {archivo}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        resultado = research_completo()
    elif sys.argv[1] == "--rapido":
        resultado = ideas_rapidas()
    elif sys.argv[1] == "--nicho" and len(sys.argv) > 2:
        nicho = " ".join(sys.argv[2:])
        resultado = research_nicho(nicho)
    else:
        resultado = research_completo()

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
