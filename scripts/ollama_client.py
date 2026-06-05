"""
Wrapper para interactuar con Ollama localmente.
Compatible con OpenAI SDK syntax para fácil integración.
"""
import requests
import json
from typing import Optional, List, Dict, Any


class OllamaClient:
    """Cliente para usar modelos locales con Ollama."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral:latest"):
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api"

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Enviar prompt a Ollama compatible con OpenAI SDK.

        Args:
            messages: Lista de mensajes [{"role": "user", "content": "..."}]
            **kwargs: stream, temperature, top_p, etc.

        Returns:
            Respuesta en formato compatible con OpenAI
        """
        endpoint = f"{self.api_url}/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": kwargs.get("stream", False),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
        }

        try:
            if kwargs.get("stream"):
                return self._stream_chat(endpoint, payload)
            else:
                response = requests.post(endpoint, json=payload, timeout=300)
                response.raise_for_status()
                data = response.json()

                # Convertir a formato OpenAI compatible
                return {
                    "id": "ollama-" + str(hash(str(messages))),
                    "object": "chat.completion",
                    "created": 0,
                    "model": self.model,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": data.get("message", {}).get("content", "")
                        },
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0
                    }
                }
        except Exception as e:
            raise Exception(f"Error en Ollama: {e}")

    def _stream_chat(self, endpoint: str, payload: dict):
        """Streaming responses desde Ollama."""
        response = requests.post(endpoint, json=payload, stream=True, timeout=300)
        for line in response.iter_lines():
            if line:
                yield json.loads(line)

    def list_models(self) -> List[str]:
        """Listar modelos disponibles."""
        try:
            response = requests.get(f"{self.api_url}/tags")
            response.raise_for_status()
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception as e:
            raise Exception(f"Error listando modelos: {e}")

    def pull_model(self, model_name: str) -> None:
        """Descargar un modelo."""
        endpoint = f"{self.api_url}/pull"
        payload = {"name": model_name}

        try:
            response = requests.post(endpoint, json=payload, stream=True, timeout=3600)
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    print(f"📦 {data.get('status', 'Descargando...')}")
        except Exception as e:
            raise Exception(f"Error descargando modelo: {e}")


# Alias compatible con OpenAI
def create_client(model: str = "mistral:latest") -> OllamaClient:
    """Factory function para crear cliente Ollama."""
    return OllamaClient(model=model)


if __name__ == "__main__":
    # Ejemplo de uso
    client = OllamaClient(model="mistral:latest")

    # Listar modelos
    print("📦 Modelos disponibles:")
    for model in client.list_models():
        print(f"  • {model}")

    # Chat simple
    print("\n🤖 Chat con Mistral:")
    response = client.chat([
        {"role": "user", "content": "¿Cuál es 2+2?"}
    ])
    print(response["choices"][0]["message"]["content"])
