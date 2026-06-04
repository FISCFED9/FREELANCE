"""
AGENTE 4: PROJECT MANAGER
==========================
Gestiona el estado de todos los proyectos activos.
- Trackea progreso y estado
- Genera recordatorios para proyectos pendientes
- Pregunta qué bloquea el avance
- Sugiere próximos pasos

Uso:
    python agente_proyectos.py --revisar        # Revisa todos los proyectos
    python agente_proyectos.py --recordatorio   # Genera recordatorios pendientes
    python agente_proyectos.py --actualizar     # Actualiza estado desde stdin
    python agente_proyectos.py --nuevo          # Registra nuevo proyecto desde stdin
"""

import anthropic
import sys
import json
from datetime import datetime
from pathlib import Path

REPO_PATH = Path(__file__).resolve().parents[1]
INDICE_PATH = REPO_PATH / "indices" / "indice_conversaciones.json"
PROYECTOS_PATH = REPO_PATH / "proyectos"

client = anthropic.Anthropic()

SYSTEM_RECORDATORIO = """Eres el Agente Project Manager de FISCFED9.

Tu tono es directo, motivador y sin rodeos. Cuando hay un proyecto pendiente,
debes generar un recordatorio que:
1. Mencione el proyecto por nombre
2. Diga cuánto tiempo lleva pendiente
3. Pregunte específicamente qué está bloqueando
4. Sugiera una acción concreta pequeña para retomarlo

NO seas condescendiente. Sé como un socio de trabajo que te da un empujón.

Devuelve JSON:
{
  "tiene_pendientes": true/false,
  "recordatorios": [
    {
      "proyecto": "nombre",
      "mensaje": "mensaje directo al usuario",
      "accion_sugerida": "algo concreto y pequeño para empezar",
      "pregunta": "¿qué te está bloqueando específicamente?"
    }
  ]
}
"""

SYSTEM_ANALISIS_PROYECTO = """Eres el Agente Project Manager de FISCFED9.

Analiza el estado de un proyecto y genera:
1. Evaluación del estado actual
2. Riesgos detectados
3. Próximos 3 pasos concretos
4. Estimación para completarlo

Devuelve JSON:
{
  "evaluacion": "texto breve",
  "riesgos": ["riesgo1", "riesgo2"],
  "proximos_pasos": [
    {"paso": 1, "descripcion": "...", "tiempo_estimado": "X horas"},
    {"paso": 2, "descripcion": "...", "tiempo_estimado": "X horas"},
    {"paso": 3, "descripcion": "...", "tiempo_estimado": "X horas"}
  ],
  "tiempo_total_estimado": "X días",
  "prioridad_recomendada": "alta/media/baja"
}
"""


def _extraer_json(texto: str) -> dict:
    if "```json" in texto:
        texto = texto.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in texto:
        texto = texto.split("```", 1)[1].split("```", 1)[0].strip()
    return json.loads(texto)


def cargar_indice() -> dict:
    if not INDICE_PATH.exists():
        return {"conversaciones": [], "proyectos": []}
    with INDICE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def guardar_indice(indice: dict):
    INDICE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INDICE_PATH.open("w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)


def revisar_recordatorios() -> dict:
    """
    Revisa qué proyectos necesitan recordatorio hoy.
    """
    indice = cargar_indice()
    hoy = datetime.now()
    proyectos_necesitan_recordatorio = []

    for proj in indice.get("proyectos", []):
        if proj["estado"] not in ["pendiente", "en_progreso"]:
            continue

        recordatorio_dias = proj.get("recordatorio_cada_dias")
        if not recordatorio_dias:
            continue

        ultima_actividad = proj.get("ultima_actividad", "desconocida")
        dias_sin_actividad = 99  # Default si no hay fecha

        if ultima_actividad != "desconocida":
            try:
                ultima = datetime.strptime(ultima_actividad, "%Y-%m-%d")
                dias_sin_actividad = (hoy - ultima).days
            except:
                pass

        if dias_sin_actividad >= recordatorio_dias:
            proyectos_necesitan_recordatorio.append({
                **proj,
                "dias_sin_actividad": dias_sin_actividad
            })

    if not proyectos_necesitan_recordatorio:
        return {"tiene_pendientes": False, "recordatorios": []}

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=SYSTEM_RECORDATORIO,
            messages=[{
                "role": "user",
                "content": f"""Genera recordatorios para estos proyectos pendientes:

{json.dumps(proyectos_necesitan_recordatorio, ensure_ascii=False, indent=2)}

Devuelve SOLO el JSON."""
            }]
        )

        texto = ""
        for block in response.content:
            if block.type == "text":
                texto = block.text
                break
        return _extraer_json(texto)
    except Exception:
        recordatorios = []
        for proj in proyectos_necesitan_recordatorio:
            recordatorios.append({
                "proyecto": proj["nombre"],
                "mensaje": f"{proj['nombre']} lleva {proj['dias_sin_actividad']} días sin actividad.",
                "accion_sugerida": "Dedica 25 minutos hoy a completar una sola tarea pequeña y comitear avance.",
                "pregunta": "¿Qué bloqueo concreto te está frenando ahora mismo?"
            })
        return {"tiene_pendientes": True, "recordatorios": recordatorios}


def analizar_proyecto(nombre_proyecto: str) -> dict:
    """
    Análisis profundo de un proyecto específico.
    """
    indice = cargar_indice()
    proyecto = None

    for proj in indice.get("proyectos", []):
        if nombre_proyecto.lower() in proj["nombre"].lower():
            proyecto = proj
            break

    if not proyecto:
        return {"error": f"Proyecto '{nombre_proyecto}' no encontrado"}

    # Buscar conversaciones relacionadas
    convs_relacionadas = [
        c for c in indice.get("conversaciones", [])
        if nombre_proyecto.lower() in " ".join(c.get("proyectos_relacionados", [])).lower()
    ]

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1536,
            thinking={"type": "adaptive"},
            system=SYSTEM_ANALISIS_PROYECTO,
            messages=[{
                "role": "user",
                "content": f"""Analiza este proyecto:

PROYECTO:
{json.dumps(proyecto, ensure_ascii=False, indent=2)}

CONVERSACIONES RELACIONADAS:
{json.dumps([{"titulo": c["titulo"], "resumen": c["resumen"]} for c in convs_relacionadas], ensure_ascii=False, indent=2)}

Devuelve SOLO el JSON con el análisis."""
            }]
        )

        texto = ""
        for block in response.content:
            if block.type == "text":
                texto = block.text
                break

        resultado = _extraer_json(texto)
    except Exception:
        resultado = {
            "evaluacion": f"Proyecto en estado '{proyecto.get('estado', 'desconocido')}'.",
            "riesgos": ["Falta de continuidad", "Bloqueos no explicitados"],
            "proximos_pasos": [
                {"paso": 1, "descripcion": "Definir el siguiente hito pequeño", "tiempo_estimado": "1 hora"},
                {"paso": 2, "descripcion": "Implementar y comitear ese hito", "tiempo_estimado": "2 horas"},
                {"paso": 3, "descripcion": "Actualizar estado del proyecto", "tiempo_estimado": "30 minutos"}
            ],
            "tiempo_total_estimado": "1-2 días",
            "prioridad_recomendada": proyecto.get("prioridad", "media")
        }

    resultado["proyecto"] = proyecto["nombre"]
    return resultado


def registrar_proyecto(datos_proyecto: dict) -> dict:
    """
    Registra un nuevo proyecto en el índice.
    """
    indice = cargar_indice()

    nuevo_id = f"proj_{len(indice.get('proyectos', [])) + 1:03d}"
    datos_proyecto["id"] = nuevo_id
    datos_proyecto["ultima_actividad"] = datetime.now().strftime("%Y-%m-%d")

    if "proyectos" not in indice:
        indice["proyectos"] = []

    indice["proyectos"].append(datos_proyecto)
    guardar_indice(indice)

    return {"exito": True, "id_asignado": nuevo_id, "proyecto": datos_proyecto["nombre"]}


def actualizar_estado_proyecto(nombre: str, nuevo_estado: str, nota: str = "") -> dict:
    """
    Actualiza el estado de un proyecto existente.
    """
    indice = cargar_indice()
    hoy = datetime.now().strftime("%Y-%m-%d")

    for proj in indice.get("proyectos", []):
        if nombre.lower() in proj["nombre"].lower():
            proj["estado"] = nuevo_estado
            proj["ultima_actividad"] = hoy
            if nota:
                if "notas" not in proj:
                    proj["notas"] = []
                proj["notas"].append({"fecha": hoy, "nota": nota})
            guardar_indice(indice)
            return {"exito": True, "proyecto": proj["nombre"], "nuevo_estado": nuevo_estado}

    return {"error": f"Proyecto '{nombre}' no encontrado"}


def listar_proyectos() -> dict:
    """
    Lista todos los proyectos con su estado actual.
    """
    indice = cargar_indice()
    hoy = datetime.now()
    proyectos_info = []

    for proj in indice.get("proyectos", []):
        dias = 0
        if proj.get("ultima_actividad") and proj["ultima_actividad"] != "desconocida":
            try:
                ultima = datetime.strptime(proj["ultima_actividad"], "%Y-%m-%d")
                dias = (hoy - ultima).days
            except:
                dias = 99

        proyectos_info.append({
            "nombre": proj["nombre"],
            "estado": proj["estado"],
            "dias_sin_actividad": dias,
            "prioridad": proj.get("prioridad", "media"),
            "recordatorio": f"Cada {proj['recordatorio_cada_dias']} días" if proj.get("recordatorio_cada_dias") else "Sin recordatorio"
        })

    return {
        "total": len(proyectos_info),
        "proyectos": sorted(proyectos_info, key=lambda x: x["dias_sin_actividad"], reverse=True)
    }


def main():
    if len(sys.argv) < 2:
        resultado = listar_proyectos()
    elif sys.argv[1] == "--revisar":
        resultado = listar_proyectos()
    elif sys.argv[1] == "--recordatorio":
        resultado = revisar_recordatorios()
    elif sys.argv[1] == "--analizar" and len(sys.argv) > 2:
        nombre = " ".join(sys.argv[2:])
        resultado = analizar_proyecto(nombre)
    elif sys.argv[1] == "--nuevo":
        datos = json.loads(sys.stdin.read())
        resultado = registrar_proyecto(datos)
    elif sys.argv[1] == "--actualizar" and len(sys.argv) > 3:
        nombre = sys.argv[2]
        estado = sys.argv[3]
        nota = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        resultado = actualizar_estado_proyecto(nombre, estado, nota)
    else:
        resultado = {"error": "Argumento no reconocido. Usa --revisar, --recordatorio, --analizar, --nuevo, --actualizar"}

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
