# Configuración Híbrida: Claude (Remoto) + LMStudio (Local)

## 📋 Estado Actual

### ✅ Instalado
- **LMStudio:** `C:\Users\alber\.lmstudio\bin\lms.exe`
- **Claude:** Vía VSCode + OpenRouter
- **Modelos locales:** 4 modelos GGUF (Q4_K_M)

### ⚠️ Pendiente
- [x] Instalar LMStudio
- [ ] Iniciar servidor LMStudio
- [ ] Configurar routing inteligente
- [ ] Probar ambos backends

---

## 🔧 Uso Recomendado

### Cuándo usar LMStudio (Local)
✅ **Tareas rápidas y privadas:**
- Análisis de código pequeño
- Refactoring simple
- Preguntas de sintaxis
- Documentación básica
- Traducción de texto
- **Ventajas:** Gratis, privado, sin latencia

**Modelo recomendado:** Qwen 3.5 9B (mejor relación calidad/velocidad)

### Cuándo usar Claude (Remoto)
✅ **Tareas complejas y creativas:**
- Arquitectura de sistemas
- Debugging complejo
- Generación de código largo
- Análisis profundo
- Decisiones de negocio
- **Ventajas:** Mayor capacidad, contexto largo, multimodal

**Modelo actual:** Claude Opus 4.6

---

## 🚀 Inicio Rápido

### 1. Iniciar LMStudio
```powershell
# Opción A: Script automatizado
.\scripts\iniciar_lmstudio.ps1

# Opción B: Manual
lms server start
```

### 2. Verificar que funciona
```bash
curl http://localhost:1234/v1/models
```

### 3. Configurar uso híbrido en código
```python
# Ejemplo: router.py
import os
from anthropic import Anthropic

def get_client(task_complexity="simple"):
    if task_complexity == "simple":
        # Usar LMStudio local
        return Anthropic(
            base_url="http://localhost:1234/v1",
            api_key="not-needed"
        )
    else:
        # Usar Claude remoto (OpenRouter)
        return Anthropic()  # Usa ANTHROPIC_BASE_URL del env

# Uso
client = get_client("simple")
response = client.messages.create(
    model="qwen-3.5-9b",  # o el modelo que cargues en LMStudio
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hola"}]
)
```

---

## 📊 Comparativa de Modelos Locales

| Modelo | RAM | Velocidad | Calidad | Uso recomendado |
|--------|-----|-----------|---------|------------------|
| **Qwen 3.5 9B** | ~6GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | **General (MEJOR)** |
| **Llama3-TAIDE 8B** | ~5GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | Bilingüe ES/EN |
| **Gemma 3 4B** | ~3GB | ⭐⭐⭐⭐ | ⭐⭐⭐ | Tareas simples |
| **Nemotron 3 Nano 4B** | ~3GB | ⭐⭐⭐⭐⭐ | ⭐⭐ | Ultra-rápido |

---

## 💰 Ahorro Estimado

Con uso híbrido (70% local / 30% remoto):
- **Sin híbrido:** ~$150/mes en Claude
- **Con híbrido:** ~$45/mes en Claude
- **Ahorro:** ~$105/mes (70%)

---

## 🔄 Próximos Pasos

1. **Ejecutar:** `.\scripts\iniciar_lmstudio.ps1`
2. **Probar:** `curl http://localhost:1234/v1/models`
3. **Cargar modelo:** Abrir LMStudio GUI → Load Model → Qwen 3.5 9B
4. **Integrar:** Crear `agentes/router_hibrido.py`
5. **Monitorear:** Uso y ahorro

---

**Última actualización:** 2026-06-05
