"""
AGENTE 2: ORGANIZADOR Y GUARDADOR EN GITHUB
=============================================
Recibe el análisis del Agente 1 y lo guarda en GitHub
de forma organizada por fecha, tipo y relevancia.

Uso:
    python agente_organizador.py  # Lee JSON del Agente 1 desde stdin
    echo '{"tiene_contenido_valioso": true, ...}' | python agente_organizador.py
"""

import anthropic
import sys
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Configuración del repo
REPO_PATH = "/workspace/project"
RAMAS = {
    "conversaciones": "MASTER1",
    "codigo": "MASTER1",
    "decisiones": "MASTER1",
    "aprendizajes": "MASTER1",
}

client = anthropic.Anthropic()

SYSTEM_PROMPT = """Eres el Agente Organizador del proyecto FREELANCE de FISCFED9.

Tu función es recibir contenido ya filtrado y decidir EXACTAMENTE cómo organizarlo en GitHub.

Dado un JSON con contenido analizado, debes decidir:
1. En qué carpeta guardarlo
2. Qué nombre de archivo usar (formato: YYYY-MM-DD_descripcion_breve.md)
3. Cómo formatear el contenido en Markdown

ESTRUCTURA DE CARPETAS:
- conversaciones/YYYY-MM/  → Resúmenes de conversaciones
- codigo/                  → Código importante generado
- decisiones/              → Decisiones de proyecto
- aprendizajes/            → Soluciones a errores, aprendizajes técnicos

REGLAS DE NOMENCLATURA:
- Fecha siempre primero: YYYY-MM-DD
- Guiones bajos entre palabras
- Máximo 50 caracteres en el nombre
- Extensión .md siempre

FORMATO DEL ARCHIVO MARKDOWN:
Devuelve un JSON con:
{
  "ruta_archivo": "conversaciones/2026-04/2026-04-13_nombre.md",
  "contenido_markdown": "# Título\\n\\nContenido...",
  "actualizar_claude_md": true/false,
  "adicion_claude_md": "texto para agregar al historial del CLAUDE.md si aplica"
}
"""


def decidir_organizacion(analisis: dict) -> dict:
    """
    Usa Claude para decidir cómo organizar el contenido.
    """
    print("📂 Agente Organizador decidiendo estructura...", file=sys.stderr)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""Decide cómo organizar este contenido en GitHub:

{json.dumps(analisis, ensure_ascii=False, indent=2)}

Devuelve SOLO el JSON con la decisión, sin texto adicional."""
            }
        ]
    )

    texto_respuesta = ""
    for block in response.content:
        if block.type == "text":
            texto_respuesta = block.text
            break

    # Limpiar y parsear JSON
    if "```json" in texto_respuesta:
        texto_respuesta = texto_respuesta.split("```json")[1].split("```")[0].strip()
    elif "```" in texto_respuesta:
        texto_respuesta = texto_respuesta.split("```")[1].split("```")[0].strip()

    return json.loads(texto_respuesta)


def guardar_archivo(ruta_relativa: str, contenido: str) -> bool:
    """
    Guarda el archivo en el repo local.
    """
    ruta_completa = Path(REPO_PATH) / ruta_relativa
    ruta_completa.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_completa, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"💾 Archivo guardado: {ruta_relativa}", file=sys.stderr)
    return True


def actualizar_claude_md(adicion: str) -> bool:
    """
    Agrega información al CLAUDE.md.
    """
    claude_md_path = Path(REPO_PATH) / "CLAUDE.md"
    if not claude_md_path.exists():
        return False

    with open(claude_md_path, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Agregar al historial de decisiones
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nueva_entrada = f"\n### {fecha_hoy} (auto-guardado)\n{adicion}\n"

    # Insertar antes de la sección de configuración técnica
    if "## ⚙️ Configuración Técnica" in contenido:
        contenido = contenido.replace(
            "## ⚙️ Configuración Técnica",
            f"{nueva_entrada}\n## ⚙️ Configuración Técnica"
        )
    else:
        contenido += nueva_entrada

    with open(claude_md_path, "w", encoding="utf-8") as f:
        f.write(contenido)

    print("📝 CLAUDE.md actualizado", file=sys.stderr)
    return True


def commit_y_push(archivos: list, mensaje: str) -> bool:
    """
    Hace git add, commit y push.
    """
    try:
        # git add
        for archivo in archivos:
            subprocess.run(
                ["git", "add", archivo],
                cwd=REPO_PATH,
                check=True,
                capture_output=True
            )

        # git commit
        subprocess.run(
            ["git", "commit", "-m", mensaje],
            cwd=REPO_PATH,
            check=True,
            capture_output=True
        )

        # git push
        result = subprocess.run(
            ["git", "push", "origin", "MASTER1"],
            cwd=REPO_PATH,
            check=True,
            capture_output=True,
            text=True
        )

        print(f"🚀 Push exitoso a GitHub", file=sys.stderr)
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error en git: {e.stderr}", file=sys.stderr)
        return False


def organizar_y_guardar(analisis: dict) -> dict:
    """
    Flujo completo: decidir organización → guardar → commit → push
    """
    if not analisis.get("tiene_contenido_valioso", False):
        return {"exito": False, "razon": "No hay contenido valioso que guardar"}

    # 1. Decidir organización
    decision = decidir_organizacion(analisis)

    archivos_guardados = []

    # 2. Guardar el archivo principal
    ruta = decision.get("ruta_archivo", "")
    contenido = decision.get("contenido_markdown", "")

    if ruta and contenido:
        guardar_archivo(ruta, contenido)
        archivos_guardados.append(ruta)

    # 3. Actualizar CLAUDE.md si es necesario
    if decision.get("actualizar_claude_md") and decision.get("adicion_claude_md"):
        actualizar_claude_md(decision["adicion_claude_md"])
        archivos_guardados.append("CLAUDE.md")

    # 4. Commit y push
    fecha = analisis.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    resumen = analisis.get("resumen_breve", "Actualización automática")
    mensaje_commit = f"[Auto] {fecha}: {resumen[:60]}"

    exito = commit_y_push(archivos_guardados, mensaje_commit)

    return {
        "exito": exito,
        "archivos_guardados": archivos_guardados,
        "mensaje_commit": mensaje_commit,
        "ruta_github": f"https://github.com/FISCFED9/FREELANCE/blob/MASTER1/{ruta}"
    }


def main():
    # Leer análisis del Agente 1 desde stdin
    print("📥 Agente Organizador leyendo análisis...", file=sys.stderr)
    entrada = sys.stdin.read()

    if not entrada.strip():
        print("❌ Error: No se recibió análisis del Agente 1", file=sys.stderr)
        sys.exit(1)

    try:
        analisis = json.loads(entrada)
    except json.JSONDecodeError as e:
        print(f"❌ Error parseando JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Organizar y guardar
    resultado = organizar_y_guardar(analisis)

    # Mostrar resultado
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

    if resultado.get("exito"):
        print(f"\n✅ Guardado exitosamente en GitHub!", file=sys.stderr)
        for archivo in resultado.get("archivos_guardados", []):
            print(f"   📄 {archivo}", file=sys.stderr)
    else:
        print(f"\n⏭️  {resultado.get('razon', 'Error desconocido')}", file=sys.stderr)


if __name__ == "__main__":
    main()
