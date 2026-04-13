"""
DEMO COMPLETO — Sistema de Memoria con 5 Agentes
=================================================
Muestra el flujo completo del sistema con un ejemplo realista.

Escenario: El usuario tuvo una sesión sobre una app Android de salud,
luego abre una nueva sesión y el sistema reconstruye el contexto,
muestra el recordatorio del proyecto salud y sugiere ideas de monetización.

Uso:
    python demo_sistema_completo.py
"""

import json
import sys
import os
from datetime import datetime

# Colores para terminal
VERDE = "\033[92m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

def separador(titulo: str, color: str = AZUL):
    print(f"\n{color}{NEGRITA}{'='*60}{RESET}")
    print(f"{color}{NEGRITA}  {titulo}{RESET}")
    print(f"{color}{NEGRITA}{'='*60}{RESET}\n")

def paso(numero: int, texto: str):
    print(f"{AMARILLO}{NEGRITA}[PASO {numero}]{RESET} {texto}")

def output(agente: str, datos: dict, color: str = VERDE):
    print(f"\n{color}{NEGRITA}▶ OUTPUT de {agente}:{RESET}")
    print(json.dumps(datos, ensure_ascii=False, indent=2))

def pausa():
    input(f"\n{CYAN}[ Presiona ENTER para continuar... ]{RESET}\n")


# ============================================================
# CONVERSACIÓN DE EJEMPLO (input del sistema)
# ============================================================

CONVERSACION_EJEMPLO = """
Usuario: Hola, necesito ayuda con mi app Android de seguimiento de salud.
Claude: Claro, ¿qué problema tienes?
Usuario: Quiero guardar los datos de pasos del usuario usando Room Database. No sé cómo estructurar la entidad.
Claude: Aquí tienes la estructura con Room:

@Entity(tableName = "pasos_diarios")
data class PasosDiarios(
    @PrimaryKey val fecha: String,
    @ColumnInfo(name = "cantidad_pasos") val cantidadPasos: Int,
    @ColumnInfo(name = "distancia_km") val distanciaKm: Float,
    @ColumnInfo(name = "calorias") val calorias: Int
)

@Dao
interface PasosDao {
    @Query("SELECT * FROM pasos_diarios ORDER BY fecha DESC")
    fun obtenerTodos(): LiveData<List<PasosDiarios>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertar(pasos: PasosDiarios)
}

Usuario: Perfecto. ¿Y cómo integro esto con Google Fit API?
Claude: Para Google Fit necesitas configurar el cliente así...
[explicación técnica de Google Fit API]
Usuario: Ok, el error que me da es "PERMISSION_DENIED" al leer pasos.
Claude: Ese error es por los permisos en el manifest. Agrega esto:
<uses-permission android:name="android.permission.ACTIVITY_RECOGNITION"/>
Y en el código solicita el permiso en runtime antes de llamar a la API.
Usuario: Funcionó! Gracias.
Claude: De nada. ¿Quieres agregar gráficas ahora?
Usuario: Sí pero eso lo vemos otro día.
"""


def demo_agente1_analizador():
    """Simula lo que hace el Agente 1: Analizador"""
    separador("AGENTE 1: ANALIZADOR", AZUL)

    paso(1, "Recibiendo conversación cruda...")
    print(f"{AMARILLO}Input: conversación de {len(CONVERSACION_EJEMPLO)} caracteres{RESET}")
    print(f"{AMARILLO}Tema detectado: Android + Room Database + Google Fit{RESET}")

    paso(2, "Filtrando contenido (descartando saludos, confirmaciones simples)...")
    print(f"  {ROJO}✗ DESCARTADO:{RESET} 'Hola, necesito ayuda...'")
    print(f"  {ROJO}✗ DESCARTADO:{RESET} 'Claro, ¿qué problema tienes?'")
    print(f"  {ROJO}✗ DESCARTADO:{RESET} 'Funcionó! Gracias.' / 'De nada.'")
    print(f"  {ROJO}✗ DESCARTADO:{RESET} 'Sí pero eso lo vemos otro día.'")
    print(f"  {VERDE}✓ GUARDADO:{RESET}   Entidad Room Database (código)")
    print(f"  {VERDE}✓ GUARDADO:{RESET}   DAO con LiveData (código)")
    print(f"  {VERDE}✓ GUARDADO:{RESET}   Solución error PERMISSION_DENIED (fix)")
    print(f"  {VERDE}✓ GUARDADO:{RESET}   Permiso ACTIVITY_RECOGNITION (configuración)")

    resultado = {
        "tiene_contenido_valioso": True,
        "resumen_breve": "App Android de salud: Room Database para pasos + Google Fit API. Fix de PERMISSION_DENIED resuelto.",
        "categorias": ["codigo", "error_resuelto", "configuracion"],
        "palabras_clave": ["android", "room-database", "google-fit", "kotlin", "permission-denied", "salud", "pasos"],
        "contenido_filtrado": "## Room Database - Entidad PasosDiarios\nEstructura de Room DB para tracking de pasos...\n\n## Fix: PERMISSION_DENIED en Google Fit\nAgregar permiso ACTIVITY_RECOGNITION en manifest...",
        "codigo_extraido": [
            {
                "lenguaje": "kotlin",
                "descripcion": "Entidad Room Database para pasos diarios",
                "codigo": "@Entity(tableName = 'pasos_diarios')\ndata class PasosDiarios(...)"
            },
            {
                "lenguaje": "kotlin",
                "descripcion": "DAO con LiveData para consultas",
                "codigo": "@Dao\ninterface PasosDao { ... }"
            },
            {
                "lenguaje": "xml",
                "descripcion": "Permiso Android para Google Fit",
                "codigo": "<uses-permission android:name='android.permission.ACTIVITY_RECOGNITION'/>"
            }
        ]
    }

    output("Agente 1 (Analizador)", resultado, VERDE)
    return resultado


def demo_agente2_organizador(analisis: dict):
    """Simula lo que hace el Agente 2: Organizador"""
    separador("AGENTE 2: ORGANIZADOR", MAGENTA)

    paso(3, "Recibiendo análisis del Agente 1...")
    paso(4, "Decidiendo estructura de archivos...")

    fecha = datetime.now().strftime("%Y-%m-%d")
    mes = datetime.now().strftime("%Y-%m")

    print(f"""
{MAGENTA}📁 Estructura decidida:{RESET}

  FREELANCE/
  ├── conversaciones/
  │   └── {mes}/
  │       └── {fecha}_android_salud_room_database.md  ← Conversación principal
  ├── codigo/
  │   └── android/
  │       └── room_database_pasos.kt                  ← Código extraído
  └── decisiones/
      └── {fecha}_fix_google_fit_permission.md        ← Fix documentado
""")

    paso(5, "Generando archivos y haciendo commit a GitHub...")
    print(f"  {VERDE}✓{RESET} git add conversaciones/{mes}/{fecha}_android_salud_room_database.md")
    print(f"  {VERDE}✓{RESET} git add codigo/android/room_database_pasos.kt")
    print(f"  {VERDE}✓{RESET} git commit -m 'feat: app Android salud - Room DB + Google Fit fix'")
    print(f"  {VERDE}✓{RESET} git push origin MASTER1")

    resultado = {
        "exito": True,
        "archivos_creados": [
            f"conversaciones/{mes}/{fecha}_android_salud_room_database.md",
            f"codigo/android/room_database_pasos.kt",
            f"decisiones/{fecha}_fix_google_fit_permission.md"
        ],
        "commit_hash": "a3f7b2c",
        "mensaje_commit": f"feat: app Android salud - Room DB + Google Fit fix [{fecha}]",
        "rama": "MASTER1"
    }

    output("Agente 2 (Organizador)", resultado, MAGENTA)
    return resultado


def demo_agente3_buscador():
    """Simula lo que hace el Agente 3: Buscador en una nueva sesión"""
    separador("AGENTE 3: BUSCADOR SEMÁNTICO", CYAN)

    paso(6, "Nueva sesión iniciada — cargando contexto automáticamente...")
    print(f"\n{CYAN}El usuario escribe: 'Quiero retomar la app de salud'{RESET}\n")

    paso(7, "Buscando conversaciones relacionadas...")
    print(f"  → Keywords detectadas: 'salud', 'app'")
    print(f"  → Buscando en índice: temas_indexados['salud'], temas_indexados['android']")
    print(f"  → Encontradas 2 conversaciones candidatas")
    print(f"  → Usando Claude para ranking semántico...")

    resultado_busqueda = {
        "hay_resultados": True,
        "conversaciones_relevantes": [
            {
                "id": "conv_002",
                "relevancia": 0.97,
                "razon": "Conversación directa sobre app Android de salud con Room Database y Google Fit",
                "archivo": "conversaciones/2026-04/2026-04-13_android_salud_room_database.md",
                "resumen": "Room DB para tracking de pasos, fix PERMISSION_DENIED en Google Fit"
            },
            {
                "id": "conv_001",
                "relevancia": 0.61,
                "razon": "Menciona 'proyecto salud' como proyecto pendiente del usuario",
                "archivo": "conversaciones/2026-04/2026-04-13_sistema_memoria_agentes.md",
                "resumen": "Arquitectura del sistema de memoria — menciona proyecto salud en rama 1-salud"
            }
        ],
        "resumen": "Encontré 2 sesiones relevantes. La más importante: implementación de Room DB para app de salud Android con solución a error de Google Fit."
    }

    output("Agente 3 (Buscador)", resultado_busqueda, CYAN)

    print(f"\n{NEGRITA}{CYAN}💡 Contexto que Claude recibirá automáticamente:{RESET}")
    print(f"""
  ┌─────────────────────────────────────────────────────┐
  │  📌 CONVERSACIÓN RELACIONADA ENCONTRADA             │
  │                                                     │
  │  Sesión del 2026-04-13 — App Android Salud          │
  │  • Implementaste Room Database para pasos diarios   │
  │  • Resolviste error PERMISSION_DENIED en Google Fit │
  │  • Quedó pendiente: agregar gráficas                │
  │                                                     │
  │  Relevancia: 97% | Ver: conversaciones/2026-04/...  │
  └─────────────────────────────────────────────────────┘
""")
    return resultado_busqueda


def demo_agente4_proyectos():
    """Simula lo que hace el Agente 4: Project Manager"""
    separador("AGENTE 4: PROJECT MANAGER", AMARILLO)

    paso(8, "Verificando proyectos con recordatorio pendiente...")
    print(f"  → Proyecto Salud: última actividad 'desconocida' → {ROJO}99 días sin actividad{RESET}")
    print(f"  → Recordatorio configurado: cada 3 días")
    print(f"  → 99 >= 3 → {ROJO}¡RECORDATORIO DISPARADO!{RESET}")

    resultado_recordatorio = {
        "tiene_pendientes": True,
        "recordatorios": [
            {
                "proyecto": "Proyecto Salud",
                "mensaje": "⚡ Oye, el proyecto de salud lleva tiempo parado. Tienes una rama '1-salud' en GitHub con trabajo hecho que está esperando. No es un proyecto nuevo — ya tiene base.",
                "accion_sugerida": "Abre la rama 1-salud y dame un git log para ver en qué punto quedó. Con eso retomamos en 10 minutos.",
                "pregunta": "¿Qué te está bloqueando específicamente? ¿Es técnico, tiempo, o perdiste el hilo de lo que faltaba?"
            }
        ]
    }

    output("Agente 4 (Project Manager)", resultado_recordatorio, AMARILLO)

    paso(9, "Análisis profundo del proyecto salud...")

    resultado_analisis = {
        "proyecto": "Proyecto Salud",
        "evaluacion": "Proyecto en rama 1-salud con base técnica establecida. La implementación de Room DB y Google Fit ya fue resuelta en sesión reciente. Falta: UI de gráficas y posiblemente monetización.",
        "riesgos": [
            "Sin actividad definida → riesgo de perder contexto completamente",
            "Si es app de salud distribución en Play Store requiere política de privacidad",
            "Google Fit API requiere OAuth — puede complicar el onboarding de usuarios"
        ],
        "proximos_pasos": [
            {
                "paso": 1,
                "descripcion": "Hacer git checkout 1-salud y revisar estado actual del código",
                "tiempo_estimado": "15 minutos"
            },
            {
                "paso": 2,
                "descripcion": "Agregar gráficas con MPAndroidChart o Compose Charts para visualizar pasos",
                "tiempo_estimado": "3 horas"
            },
            {
                "paso": 3,
                "descripcion": "Definir modelo de monetización: premium, freemium o B2B para gimnasios",
                "tiempo_estimado": "1 hora"
            }
        ],
        "tiempo_total_estimado": "2-3 días",
        "prioridad_recomendada": "alta"
    }

    output("Agente 4 — Análisis Proyecto", resultado_analisis, AMARILLO)
    return resultado_recordatorio


def demo_agente5_investigador():
    """Simula lo que hace el Agente 5: Market Researcher"""
    separador("AGENTE 5: MARKET RESEARCHER", VERDE)

    paso(10, "Ejecutando deep research con búsqueda web real...")
    print(f"  → Buscando: 'servicios IA para empresas 2026 demanda'")
    print(f"  → Buscando: 'apps salud monetización 2026'")
    print(f"  → Buscando: 'nichos poco competidos IA negocio'")
    print(f"  → Analizando con Claude + habilidades del usuario detectadas...")
    print(f"     Habilidades: Python, Android, Claude/IA, GitHub")

    resultado_research = {
        "fecha_research": "2026-04-13",
        "tendencias_encontradas": [
            "Automatización de procesos con IA para PyMES latinoamericanas — demanda 340% vs 2024",
            "Apps de wellness/salud con IA personalizada — mercado $4.5B proyectado 2027",
            "Agentes IA para WhatsApp Business — adoptado por 67% de comercios en LATAM"
        ],
        "oportunidades": [
            {
                "rank": 1,
                "nombre": "SaludBot Pro",
                "tagline": "Tu app de salud Android + agente IA que interpreta tus datos",
                "problema_que_resuelve": "Las apps de salud son aburridas y no personalizan. Un agente IA que analiza tus pasos/sueño y da recomendaciones reales es lo que falta.",
                "mercado_objetivo": "Usuarios 25-45 que ya usan apps de salud pero quieren más que números",
                "modelo_monetizacion": "Freemium: básico gratis, Premium $4.99/mes con IA ilimitada",
                "precio_sugerido": "$4.99/mes",
                "rol_ia": "Agente que analiza patrones históricos y genera recomendaciones personalizadas con Claude. El diferencial frente a Google Fit o Samsung Health.",
                "dias_primer_cliente": 21,
                "potencial_mensual_usd": "$500-$2,000 a 100-400 usuarios premium",
                "competencia_actual": "media",
                "primer_paso_hoy": "Terminar la rama 1-salud que ya tienes — tienes el 60% hecho. Agregar el agente IA encima es 1-2 días extra.",
                "recursos_necesarios": "Lo que ya tienes: Android, Room DB, Google Fit. Solo agregar Claude API calls."
            },
            {
                "rank": 2,
                "nombre": "AutomatiPyme",
                "tagline": "Agente IA que automatiza el WhatsApp y pedidos de tu negocio",
                "problema_que_resuelve": "Las PyMES pierden clientes porque no responden WhatsApp a tiempo. Un agente IA que responde, cotiza y agenda — sin contratar a nadie.",
                "mercado_objetivo": "Dueños de tiendas, restaurantes y servicios locales en LATAM",
                "modelo_monetizacion": "SaaS mensual: $49-149 USD/mes por negocio",
                "precio_sugerido": "$79/mes por cliente",
                "rol_ia": "Agente Claude que aprende el catálogo del negocio, responde WhatsApp Business API, genera cotizaciones y agenda citas automáticamente.",
                "dias_primer_cliente": 14,
                "potencial_mensual_usd": "$790-$3,950 con 10-50 clientes",
                "competencia_actual": "baja",
                "primer_paso_hoy": "Crear un bot básico para UN restaurante conocido como demo. Mostrar en video y ofrecer gratis el primer mes a 3 negocios locales.",
                "recursos_necesarios": "WhatsApp Business API (gratuito para empezar), Claude API, Python (ya lo tienes)"
            },
            {
                "rank": 3,
                "nombre": "CodeReview IA",
                "tagline": "Revisión de código Android/Python con IA experta — para equipos que crecen rápido",
                "problema_que_resuelve": "Startups técnicas en LATAM no tienen senior developers para revisar PRs. Un servicio de code review con IA especializada en Android/Python llena ese gap.",
                "mercado_objetivo": "Equipos de desarrollo de 2-10 personas en startups o agencias",
                "modelo_monetizacion": "Por PR revisado: $5-15 USD, o suscripción $99/mes ilimitado",
                "precio_sugerido": "$99/mes por equipo",
                "rol_ia": "Claude analiza PR de GitHub, detecta bugs, problemas de rendimiento, sugerencias de arquitectura. Tu curación y experiencia Android le da credibilidad.",
                "dias_primer_cliente": 7,
                "potencial_mensual_usd": "$1,000-$5,000 con 10-50 equipos",
                "competencia_actual": "baja",
                "primer_paso_hoy": "Integrar Claude con GitHub webhooks (2-3 horas de desarrollo). Ofrecer review gratis a 3 proyectos open source visibles para ganar tracción.",
                "recursos_necesarios": "GitHub API, Claude API, Python. Todo lo tienes."
            }
        ],
        "recomendacion_principal": "SaludBot Pro",
        "por_que_ahora": "Ya tienes el 60% construido en la rama 1-salud. Terminarlo con el agente IA encima es 2-3 días de trabajo sobre código que ya existe. Es la ruta más rápida a tu primer $1 — y además resuelve el proyecto pendiente que llevas meses postponiendo."
    }

    output("Agente 5 (Investigador)", resultado_research, VERDE)
    return resultado_research


def demo_flujo_completo():
    """Muestra el flujo completo del sistema"""

    print(f"""
{NEGRITA}{CYAN}
╔══════════════════════════════════════════════════════════════╗
║     DEMO: SISTEMA DE MEMORIA CON 5 AGENTES                  ║
║     FISCFED9/FREELANCE — Flujo completo                     ║
╚══════════════════════════════════════════════════════════════╝
{RESET}""")

    print(f"""{AMARILLO}ESCENARIO:{RESET}
  1. El usuario tuvo una sesión sobre una app Android de salud
  2. Se guarda automáticamente en GitHub
  3. El usuario abre una nueva sesión al día siguiente
  4. El sistema reconstruye el contexto inteligentemente
  5. Muestra recordatorio del proyecto pendiente
  6. Sugiere ideas de monetización personalizadas

{CYAN}Los 5 agentes en acción:{RESET}
  🔵 Agente 1: Analizador  → Filtra la conversación, extrae lo valioso
  🟣 Agente 2: Organizador → Guarda en GitHub con estructura inteligente
  🟦 Agente 3: Buscador    → Encuentra conversaciones relacionadas
  🟡 Agente 4: Proyectos   → Recordatorios y análisis de proyectos
  🟢 Agente 5: Investigador→ Deep research + 3 ideas monetizables
""")

    pausa()

    # ─── SESIÓN 1: Guardar ────────────────────────────────────
    separador("📼 SESIÓN 1 — GUARDANDO CONVERSACIÓN", ROJO)
    print(f"{AMARILLO}Trigger:{RESET} El usuario termina la sesión sobre Android")
    print(f"{AMARILLO}Comando:{RESET} echo '<conversacion>' | ./guardar_conversacion.sh\n")

    analisis = demo_agente1_analizador()
    pausa()

    organizacion = demo_agente2_organizador(analisis)
    pausa()

    # ─── SESIÓN 2: Nueva sesión ───────────────────────────────
    separador("🌅 SESIÓN 2 — NUEVA SESIÓN (día siguiente)", ROJO)
    print(f"{AMARILLO}Trigger:{RESET} El usuario abre Claude y escribe sobre la app de salud")
    print(f"{AMARILLO}Comando automático:{RESET} python agente_buscador.py --inicio\n")

    busqueda = demo_agente3_buscador()
    pausa()

    recordatorio = demo_agente4_proyectos()
    pausa()

    research = demo_agente5_investigador()
    pausa()

    # ─── RESUMEN FINAL ───────────────────────────────────────
    separador("✅ RESUMEN: LO QUE VE EL USUARIO AL INICIO DE SESIÓN", VERDE)

    print(f"""{NEGRITA}Mensaje automático al abrir Claude:{RESET}

{VERDE}┌──────────────────────────────────────────────────────────────┐{RESET}
{VERDE}│{RESET}  {NEGRITA}👋 ¡Hola FISCFED9! Contexto de tu última sesión:{RESET}          {VERDE}│{RESET}
{VERDE}│{RESET}                                                              {VERDE}│{RESET}
{VERDE}│{RESET}  📱 {NEGRITA}App Android Salud{RESET} — Ayer resolviste:                     {VERDE}│{RESET}
{VERDE}│{RESET}     • Room Database para tracking de pasos ✅                 {VERDE}│{RESET}
{VERDE}│{RESET}     • PERMISSION_DENIED en Google Fit → Solucionado ✅        {VERDE}│{RESET}
{VERDE}│{RESET}     • Pendiente: gráficas de datos                            {VERDE}│{RESET}
{VERDE}│{RESET}                                                              {VERDE}│{RESET}
{VERDE}│{RESET}  ⚡ {NEGRITA}RECORDATORIO — Proyecto Salud:{RESET}                         {VERDE}│{RESET}
{VERDE}│{RESET}     "Llevas tiempo sin tocar la rama 1-salud.                 {VERDE}│{RESET}
{VERDE}│{RESET}      Tienes el 60% hecho. ¿Qué te está bloqueando?"           {VERDE}│{RESET}
{VERDE}│{RESET}                                                              {VERDE}│{RESET}
{VERDE}│{RESET}  💡 {NEGRITA}Mejor oportunidad de monetización ahora:{RESET}               {VERDE}│{RESET}
{VERDE}│{RESET}     SaludBot Pro — Termina tu app + agrega IA                 {VERDE}│{RESET}
{VERDE}│{RESET}     → Potencial: $500-$2,000/mes | Tiempo: 21 días           {VERDE}│{RESET}
{VERDE}│{RESET}     → YA TIENES el 60% construido en 1-salud                 {VERDE}│{RESET}
{VERDE}│{RESET}                                                              {VERDE}│{RESET}
{VERDE}│{RESET}  ¿Qué hacemos hoy?                                           {VERDE}│{RESET}
{VERDE}│{RESET}  [1] Retomar app de salud (agregar gráficas)                 {VERDE}│{RESET}
{VERDE}│{RESET}  [2] Ver el plan completo de SaludBot Pro                    {VERDE}│{RESET}
{VERDE}│{RESET}  [3] Empezar con AutomatiPyme (WhatsApp + IA)                {VERDE}│{RESET}
{VERDE}│{RESET}  [4] Algo completamente nuevo                                {VERDE}│{RESET}
{VERDE}└──────────────────────────────────────────────────────────────┘{RESET}
""")

    separador("📊 ARQUITECTURA DEL SISTEMA", AZUL)
    print(f"""
{CYAN}Flujo de datos:{RESET}

  Conversación → {AZUL}[Agente 1]{RESET} → Análisis filtrado
                      ↓
               {MAGENTA}[Agente 2]{RESET} → GitHub (commit automático)
                      ↓
  Nueva sesión → {CYAN}[Agente 3]{RESET} → Contexto relevante surfaceado
                      ↓
               {AMARILLO}[Agente 4]{RESET} → Recordatorios + análisis proyectos
                      ↓
               {VERDE}[Agente 5]{RESET} → Web research + 3 ideas monetizables

{CYAN}Automatización (cron jobs activos):{RESET}
  🕘 Cada 3 días → Agente 4 revisa proyectos pendientes
  📅 Cada lunes  → Agente 5 genera nuevas ideas de mercado

{CYAN}Archivos del sistema:{RESET}
  📂 /workspace/project/
  ├── CLAUDE.md                        ← Memoria principal (leída al inicio)
  ├── agentes/
  │   ├── agente_analizador.py         ← Agente 1
  │   ├── agente_organizador.py        ← Agente 2
  │   ├── agente_buscador.py           ← Agente 3
  │   ├── agente_proyectos.py          ← Agente 4
  │   ├── agente_investigador.py       ← Agente 5
  │   └── guardar_conversacion.sh      ← Orquestador
  ├── conversaciones/                  ← Guardadas en GitHub
  ├── indices/indice_conversaciones.json ← Índice semántico
  └── investigacion/                   ← Research de mercado
""")

    print(f"{NEGRITA}{VERDE}✓ Demo completado. El sistema está operativo y corriendo.{RESET}\n")


if __name__ == "__main__":
    demo_flujo_completo()
