"""
AGENTE 3: BUSCADOR SEMÁNTICO
==============================
Busca en todas las conversaciones guardadas las que son
relevantes al tema actual. Se activa automáticamente cuando
detecta que el tema de conversación coincide con algo del pasado.

Uso:
    python agente_buscador.py "tema o pregunta a buscar"
    python agente_buscador.py --inicio  # Modo inicio de sesión
"""

import anthropic
import sys
import json
from datetime import datetime
from pathlib import Path

REPO_PATH = Path(__file__).resolve().parents[1]
INDICE_PATH = REPO_PATH / "indices" / "indice_conversaciones.json"

client = anthropic.Anthropic()

SYSTEM_BUSQUEDA = """Eres el Agente Buscador del sistema de memoria de FISCFED9.

Tu función es analizar un tema o pregunta y determinar qué
conversaciones pasadas son relevantes para el contexto actual.

Recibirás:
1. El tema/pregunta actual
2. El índice de conversaciones disponibles

Debes devolver un JSON con:
{
  "conversaciones_relevantes": [
    {
      "id": "conv_001",
      "relevancia": 0.9,  // 0 a 1
      "razon": "Por qué es relevante",
      "archivo": "ruta/al/archivo.md"
    }
  ],
  "hay_resultados": true/false,
  "resumen": "Resumen de qué encontraste"
}

Solo incluye conversaciones con relevancia > 0.5.
Máximo 3 resultados. Ordena por relevancia descendente.
"""

SYSTEM_INICIO = """Eres el asistente de inicio de sesión de FISCFED9.

Al inicio de cada sesión, tu rol es:
1. Leer el estado actual del sistema (proyectos, última sesión)
2. Preparar un saludo de contexto inteligente
3. Ofrecer opciones claras al usuario

Devuelve un JSON con:
{
  "saludo": "Mensaje de bienvenida con contexto",
  "ultima_sesion": {
    "fecha": "...",
    "tema": "...",
    "pendientes": ["..."]
  },
  "proyectos_pendientes": [
    {
      "nombre": "...",
      "dias_sin_actividad": 0,
      "necesita_recordatorio": true/false,
      "mensaje_recordatorio": "..."
    }
  ],
  "opciones": [
    "Continuar con: [tema última sesión]",
    "Revisar proyecto salud",
    "Empezar algo nuevo"
  ]
}
"""


def cargar_indice() -> dict:
    """Carga el índice de conversaciones."""
    if not INDICE_PATH.exists():
        return {"conversaciones": [], "proyectos": [], "temas_indexados": {}}
    with INDICE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def cargar_archivo_conversacion(ruta_relativa: str) -> str:
    """Lee el contenido de una conversación guardada."""
    ruta_completa = Path(REPO_PATH) / ruta_relativa
    if ruta_completa.exists():
        with open(ruta_completa, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def buscar_conversaciones_relacionadas(tema: str) -> dict:
    """
    Busca conversaciones relevantes al tema dado.
    """
    indice = cargar_indice()

    if not indice["conversaciones"]:
        return {"hay_resultados": False, "resumen": "No hay conversaciones guardadas aún"}

    # Búsqueda rápida por keywords primero
    tema_lower = tema.lower()
    conversaciones_candidatas = []

    for conv in indice["conversaciones"]:
        score_keywords = 0
        for tema_idx in conv.get("temas", []):
            if tema_idx in tema_lower or tema_lower in tema_idx:
                score_keywords += 1
        for tech in conv.get("tecnologias", []):
            if tech in tema_lower:
                score_keywords += 1

        if score_keywords > 0:
            conversaciones_candidatas.append({**conv, "score_inicial": score_keywords})

    if not conversaciones_candidatas:
        # Si no hay coincidencias por keyword, usar Claude para búsqueda semántica
        conversaciones_candidatas = indice["conversaciones"][:5]  # Máximo 5 para analizar

    # Usar Claude para búsqueda semántica profunda
    indice_resumido = json.dumps({
        "conversaciones": [
            {
                "id": c["id"],
                "titulo": c["titulo"],
                "resumen": c["resumen"],
                "temas": c["temas"],
                "archivo": c["archivo"]
            }
            for c in conversaciones_candidatas
        ]
    }, ensure_ascii=False)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_BUSQUEDA,
        messages=[{
            "role": "user",
            "content": f"""Busca conversaciones relevantes para este tema:
"{tema}"

Índice disponible:
{indice_resumido}

Devuelve SOLO el JSON."""
        }]
    )

    texto = ""
    for block in response.content:
        if block.type == "text":
            texto = block.text
            break

    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0].strip()
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0].strip()

    return json.loads(texto)


def modo_inicio_sesion() -> dict:
    """
    Genera el contexto de inicio de sesión.
    Carga proyectos, última sesión y prepara el saludo.
    """
    indice = cargar_indice()
    hoy = datetime.now()

    # Calcular días sin actividad para cada proyecto
    proyectos_status = []
    for proj in indice.get("proyectos", []):
        dias_sin_actividad = 0
        if proj.get("ultima_actividad") and proj["ultima_actividad"] != "desconocida":
            try:
                ultima = datetime.strptime(proj["ultima_actividad"], "%Y-%m-%d")
                dias_sin_actividad = (hoy - ultima).days
            except:
                dias_sin_actividad = 99

        recordatorio_dias = proj.get("recordatorio_cada_dias")
        necesita_recordatorio = (
            recordatorio_dias is not None and
            dias_sin_actividad >= recordatorio_dias and
            proj.get("estado") in ["pendiente", "en_progreso"]
        )

        proyectos_status.append({
            "nombre": proj["nombre"],
            "estado": proj["estado"],
            "dias_sin_actividad": dias_sin_actividad,
            "necesita_recordatorio": necesita_recordatorio,
            "mensaje_recordatorio": proj.get("recordatorio_mensaje", "")
        })

    # Última conversación
    ultima_conv = None
    if indice["conversaciones"]:
        ultima_conv = sorted(
            indice["conversaciones"],
            key=lambda x: x["fecha"],
            reverse=True
        )[0]

    # Generar saludo inteligente con Claude
    context_data = json.dumps({
        "fecha_hoy": hoy.strftime("%Y-%m-%d"),
        "proyectos": proyectos_status,
        "ultima_conversacion": ultima_conv
    }, ensure_ascii=False)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_INICIO,
        messages=[{
            "role": "user",
            "content": f"""Genera el contexto de inicio de sesión basado en:
{context_data}

Devuelve SOLO el JSON."""
        }]
    )

    texto = ""
    for block in response.content:
        if block.type == "text":
            texto = block.text
            break

    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0].strip()
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0].strip()

    return json.loads(texto)


def actualizar_indice(nueva_conversacion: dict):
    """
    Agrega una nueva conversación al índice.
    """
    indice = cargar_indice()

    # Generar ID único
    nuevo_id = f"conv_{len(indice['conversaciones']) + 1:03d}"
    nueva_conversacion["id"] = nuevo_id

    indice["conversaciones"].append(nueva_conversacion)
    indice["ultima_actualizacion"] = datetime.now().strftime("%Y-%m-%d")

    # Actualizar índice de temas
    for tema in nueva_conversacion.get("temas", []):
        if tema not in indice["temas_indexados"]:
            indice["temas_indexados"][tema] = []
        if nuevo_id not in indice["temas_indexados"][tema]:
            indice["temas_indexados"][tema].append(nuevo_id)

    INDICE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INDICE_PATH.open("w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)

    return nuevo_id


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--inicio":
            # Modo inicio de sesión
            resultado = modo_inicio_sesion()
        elif sys.argv[1] == "--actualizar":
            # Actualizar índice con datos de stdin
            datos = json.loads(sys.stdin.read())
            nuevo_id = actualizar_indice(datos)
            resultado = {"exito": True, "id_asignado": nuevo_id}
        else:
            # Búsqueda normal
            tema = " ".join(sys.argv[1:])
            resultado = buscar_conversaciones_relacionadas(tema)
    else:
        tema = sys.stdin.read().strip()
        resultado = buscar_conversaciones_relacionadas(tema)

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
