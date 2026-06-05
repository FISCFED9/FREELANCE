#!/usr/bin/env python3
"""
Router Híbrido: Decide automáticamente entre LMStudio (local) y Claude (remoto)
Optimiza costos usando local para tareas simples y remoto para complejas.
"""

import os
import requests
from anthropic import Anthropic
from typing import Literal, Optional

class HybridRouter:
    def __init__(self):
        self.lmstudio_url = "http://localhost:1234/v1"
        self.lmstudio_available = self._check_lmstudio()

    def _check_lmstudio(self) -> bool:
        """Verifica si LMStudio está corriendo"""
        try:
            response = requests.get(f"{self.lmstudio_url}/models", timeout=2)
            return response.status_code == 200
        except:
            return False

    def classify_complexity(
        self,
        prompt: str,
        context_length: int = 0,
        requires_multimodal: bool = False
    ) -> Literal["simple", "complex"]:
        """
        Clasifica la complejidad de la tarea

        SIMPLE → LMStudio local (gratis, rápido)
        COMPLEX → Claude remoto (potente, costoso)
        """
        # Forzar remoto si:
        if requires_multimodal:
            return "complex"  # LMStudio no tiene visión

        if context_length > 4000:
            return "complex"  # Contexto largo necesita Claude

        # Keywords que indican complejidad
        complex_keywords = [
            "arquitectura", "diseño de sistema", "debugging complejo",
            "optimización", "seguridad", "escalabilidad",
            "refactoring profundo", "análisis completo"
        ]

        simple_keywords = [
            "sintaxis", "documentar", "traducir", "formatear",
            "pequeño cambio", "quick fix", "simple refactor"
        ]

        prompt_lower = prompt.lower()

        # Si contiene keywords complejas
        if any(kw in prompt_lower for kw in complex_keywords):
            return "complex"

        # Si contiene keywords simples y prompt es corto
        if any(kw in prompt_lower for kw in simple_keywords) and len(prompt) < 500:
            return "simple"

        # Por defecto: si es corto → simple, si es largo → complex
        return "simple" if len(prompt) < 300 else "complex"

    def get_client(
        self,
        complexity: Literal["simple", "complex"] = "simple",
        force_remote: bool = False
    ) -> tuple[Anthropic, str]:
        """
        Retorna el cliente apropiado y el modelo a usar

        Returns:
            (client, model_name)
        """
        # Forzar remoto o LMStudio no disponible
        if force_remote or not self.lmstudio_available:
            print("🌐 Usando Claude remoto (OpenRouter)")
            return (Anthropic(), "claude-opus-4-6")

        # Usar local si es simple
        if complexity == "simple":
            print("💻 Usando LMStudio local (Qwen 3.5 9B)")
            client = Anthropic(
                base_url=self.lmstudio_url,
                api_key="not-needed"  # LMStudio no necesita API key
            )
            # Obtener primer modelo disponible en LMStudio
            try:
                response = requests.get(f"{self.lmstudio_url}/models", timeout=2)
                models = response.json().get("data", [])
                model_name = models[0]["id"] if models else "qwen-3.5-9b"
                return (client, model_name)
            except:
                print("⚠️ Error al obtener modelos de LMStudio, usando remoto")
                return (Anthropic(), "claude-opus-4-6")

        # Usar remoto si es complejo
        print("🌐 Usando Claude remoto (tarea compleja)")
        return (Anthropic(), "claude-opus-4-6")

    def chat(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 2048,
        auto_classify: bool = True,
        force_remote: bool = False
    ) -> str:
        """
        Envía un prompt al modelo apropiado

        Args:
            prompt: El prompt del usuario
            system: Prompt de sistema opcional
            max_tokens: Tokens máximos de respuesta
            auto_classify: Si True, clasifica automáticamente complejidad
            force_remote: Si True, fuerza uso de Claude remoto

        Returns:
            La respuesta del modelo
        """
        # Clasificar complejidad
        if auto_classify:
            complexity = self.classify_complexity(prompt)
            print(f"📊 Complejidad detectada: {complexity}")
        else:
            complexity = "complex" if force_remote else "simple"

        # Obtener cliente y modelo
        client, model_name = self.get_client(complexity, force_remote)

        # Preparar mensajes
        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "model": model_name,
            "max_tokens": max_tokens,
            "messages": messages
        }

        if system:
            kwargs["system"] = system

        # Enviar request
        try:
            response = client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            print(f"❌ Error: {e}")
            # Fallback a remoto si falla local
            if not force_remote and complexity == "simple":
                print("⚠️ Fallback a Claude remoto")
                return self.chat(prompt, system, max_tokens, auto_classify=False, force_remote=True)
            raise


# === EJEMPLO DE USO ===
if __name__ == "__main__":
    router = HybridRouter()

    # Prueba simple (debería usar local)
    print("\n=== PRUEBA 1: Tarea Simple ===")
    response = router.chat(
        "Explica qué hace este código: def suma(a, b): return a + b"
    )
    print(f"Respuesta: {response[:100]}...\n")

    # Prueba compleja (debería usar remoto)
    print("\n=== PRUEBA 2: Tarea Compleja ===")
    response = router.chat(
        "Diseña una arquitectura de microservicios escalable para un e-commerce con 1M de usuarios"
    )
    print(f"Respuesta: {response[:100]}...\n")

    # Forzar remoto
    print("\n=== PRUEBA 3: Forzar Remoto ===")
    response = router.chat(
        "Hola mundo",
        force_remote=True
    )
    print(f"Respuesta: {response[:100]}...\n")
