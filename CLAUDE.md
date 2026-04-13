# CLAUDE.md — Memoria Persistente del Proyecto FREELANCE
> Repositorio: https://github.com/FISCFED9/FREELANCE (PRIVADO)
> Última actualización: 2026-04-13

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
**Estado:** Configurando el sistema de memoria y los dos agentes
**Siguiente paso:** Implementar los agentes y probar el flujo completo
