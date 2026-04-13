# CLAUDE.md — Cerebro Vivo del Proyecto FREELANCE
> Repositorio: https://github.com/FISCFED9/FREELANCE (PRIVADO)
> Última actualización: 2026-04-13

---

## 🤖 PROTOCOLO DE INICIO — LEE ESTO PRIMERO

**Al comenzar CUALQUIER sesión nueva, haz esto automáticamente:**

1. **Saluda con contexto:** Di en qué estabas la última vez y hace cuánto
2. **Pregunta:** *"¿Continuamos con [último tema] o empezamos algo nuevo?"*
3. **Revisa proyectos pendientes:** Si hay proyectos con recordatorio activo y han pasado los días indicados, menciónalos
4. **Búsqueda proactiva:** Si el usuario menciona un tema, busca en `indices/indice_conversaciones.json` si hay conversaciones relacionadas y ofrécelas
5. **Guarda siempre:** Al final de cada sesión o cada 10 mensajes importantes, ejecuta el guardado automático

**Si el usuario dice "guarda" o "no pierdas esto":** Registra inmediatamente en GitHub.
**Si detectas código importante:** Guárdalo aunque no te lo pidan.

---

## 🧠 Contexto del Proyecto

Este proyecto nació de la necesidad de **no perder conversaciones importantes** entre el usuario (FISCFED9) y Claude. Cada sesión de Claude empieza desde cero, por lo que acordamos usar GitHub como memoria persistente.

### El problema original
- Claude no recuerda conversaciones anteriores entre sesiones
- El usuario tocó un botón equivocado y perdió una sesión importante
- Se necesita un sistema automático de respaldo

### La solución acordada
Dos agentes de IA especializados que trabajan juntos:
1. **Agente Analizador** → Lee las conversaciones y extrae solo lo importante (filtra basura)
2. **Agente Organizador** → Guarda lo importante en GitHub, organizado por fecha/relevancia/código

---

## 👤 Información del Usuario

- **GitHub:** FISCFED9
- **Repo:** FISCFED9/FREELANCE
- **Rama principal:** MASTER1
- **Preferencia:** Todo privado hasta que él decida abrirlo a la comunidad
- **Idioma:** Español

---

## 🤖 Los Dos Agentes

### Agente 1: "Analizador" (ANALYZER)
**Función:** Recibe texto de conversación y decide qué guardar
**Criterios de filtrado:**
- ✅ GUARDAR: Código generado, decisiones importantes, configuraciones, aprendizajes clave
- ✅ GUARDAR: Errores resueltos y sus soluciones
- ✅ GUARDAR: Ideas y planes acordados
- ❌ DESCARTAR: Saludos, confirmaciones simples ("ok", "sí", "entendido")
- ❌ DESCARTAR: Preguntas de aclaración repetitivas
- ❌ DESCARTAR: Contenido duplicado

### Agente 2: "Organizador" (ORGANIZER)
**Función:** Recibe lo que filtró el Agente 1 y lo guarda en GitHub
**Estructura de carpetas:**
```
FREELANCE/
├── CLAUDE.md              ← Este archivo (memoria principal)
├── conversaciones/
│   ├── 2026-04/           ← Por mes
│   │   ├── 2026-04-13_sesion_agentes.md
│   │   └── ...
├── codigo/                ← Código generado o importante
│   ├── agentes/
│   └── ...
├── decisiones/            ← Decisiones importantes tomadas
└── aprendizajes/          ← Cosas aprendidas/resueltas
```

---

## 📋 Historial de Decisiones Importantes

### 2026-04-13
- ✅ Decidimos usar GitHub como memoria persistente
- ✅ Sistema de dos agentes para filtrar y organizar
- ✅ Todo privado hasta nuevo aviso
- ✅ El repo ya existe: FISCFED9/FREELANCE
- ✅ Configurado con OpenRouter API (ver settings.json)
- ✅ Hay dos ramas: MASTER1 y 1-salud

---

## ⚙️ Configuración Técnica

### API
- **Provider:** OpenRouter (vía ANTHROPIC_BASE_URL)
- **Modelo:** claude-opus-4-6
- **Settings:** ~/.claude/settings.json

### Git
- **Remote:** https://github.com/FISCFED9/FREELANCE.git
- **Auth:** Token de acceso configurado
- **Rama activa:** MASTER1

---

## 📝 Notas para Futuras Sesiones

Cuando empieces una nueva sesión, lee este archivo primero. Te dirá:
1. En qué estábamos trabajando
2. Qué decisiones se han tomado
3. Qué código existe
4. Cuál es el siguiente paso

**El usuario prefiere:**
- Comunicación en español
- Que seas directo y no repitas cosas innecesarias
- Que guardes automáticamente cualquier cosa importante
- Que el código sea funcional antes de explicarlo

---

## 🔄 Estado Actual del Proyecto

**Fecha:** 2026-04-13
**Estado:** Fase 1 completada ✅ | Fase 2 y 3 en construcción 🔄
**Última sesión:** 2026-04-13 — Sistema de memoria + arquitectura de 5 agentes
**Siguiente paso:** Agente 4 (Project Manager) + Agente 5 (Market Researcher) + Cron

---

## 📊 Tracker de Proyectos

| Proyecto | Estado | Última actividad | Recordatorio |
|----------|--------|-----------------|--------------|
| Sistema Memoria FREELANCE | 🔄 En progreso | 2026-04-13 | — |
| **Proyecto Salud** | ⏸️ **PENDIENTE** | Desconocida | **Cada 3 días** |

> ⚠️ **RECORDATORIO ACTIVO:** El proyecto de salud (rama `1-salud`) está pendiente de completar. Cada 3 días recuerda al usuario retomarlo y pregunta qué bloquea el avance.

---

## 📁 Archivos del Sistema

```
agentes/
├── agente_analizador.py     ← Agente 1: filtra conversaciones
├── agente_organizador.py    ← Agente 2: guarda en GitHub
├── agente_buscador.py       ← Agente 3: busca conversaciones relacionadas
├── agente_proyectos.py      ← Agente 4: gestión de proyectos (por crear)
├── agente_investigador.py   ← Agente 5: market research (por crear)
└── guardar_conversacion.sh  ← Orquestador principal
indices/
└── indice_conversaciones.json  ← Índice semántico de todo
conversaciones/              ← Historial por mes
decisiones/                  ← Decisiones importantes
proyectos/                   ← Estado de proyectos
```
