/**
 * Cliente Ollama para JavaScript/Node.js
 * Compatible con fetch y Axios
 */

class OllamaClient {
  constructor(baseUrl = "http://localhost:11434", model = "mistral:latest") {
    this.baseUrl = baseUrl;
    this.model = model;
    this.apiUrl = `${baseUrl}/api`;
  }

  /**
   * Enviar chat a Ollama
   * @param {Array<{role: string, content: string}>} messages
   * @param {Object} options - temperatura, top_p, etc
   * @returns {Promise<Object>} Respuesta compatible con OpenAI
   */
  async chat(messages, options = {}) {
    const endpoint = `${this.apiUrl}/chat`;

    const payload = {
      model: this.model,
      messages,
      stream: options.stream || false,
      temperature: options.temperature || 0.7,
      top_p: options.top_p || 0.9,
    };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Ollama error: ${response.statusText}`);
      }

      const data = await response.json();

      // Formato compatible con OpenAI
      return {
        id: `ollama-${Date.now()}`,
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: this.model,
        choices: [
          {
            index: 0,
            message: {
              role: "assistant",
              content: data.message?.content || "",
            },
            finish_reason: "stop",
          },
        ],
        usage: {
          prompt_tokens: 0,
          completion_tokens: 0,
          total_tokens: 0,
        },
      };
    } catch (error) {
      throw new Error(`Error en Ollama: ${error.message}`);
    }
  }

  /**
   * Streaming chat
   * @param {Array<{role: string, content: string}>} messages
   * @param {Function} onData - Callback para cada chunk
   */
  async chatStream(messages, onData) {
    const endpoint = `${this.apiUrl}/chat`;

    const payload = {
      model: this.model,
      messages,
      stream: true,
    };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Ollama error: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((l) => l.trim());

        for (const line of lines) {
          try {
            const data = JSON.parse(line);
            onData(data);
          } catch (e) {
            // Ignorar líneas inválidas
          }
        }
      }
    } catch (error) {
      throw new Error(`Error en Ollama stream: ${error.message}`);
    }
  }

  /**
   * Listar modelos disponibles
   * @returns {Promise<Array<string>>}
   */
  async listModels() {
    try {
      const response = await fetch(`${this.apiUrl}/tags`);
      if (!response.ok) throw new Error("Error listando modelos");

      const data = await response.json();
      return data.models?.map((m) => m.name) || [];
    } catch (error) {
      throw new Error(`Error en listModels: ${error.message}`);
    }
  }

  /**
   * Descargar modelo
   * @param {string} modelName
   */
  async pullModel(modelName) {
    const endpoint = `${this.apiUrl}/pull`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: modelName }),
      });

      if (!response.ok) throw new Error("Error descargando modelo");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((l) => l.trim());

        for (const line of lines) {
          try {
            const data = JSON.parse(line);
            console.log(`📦 ${data.status || "Descargando..."}`);
          } catch (e) {
            // Ignorar
          }
        }
      }
    } catch (error) {
      throw new Error(`Error en pullModel: ${error.message}`);
    }
  }
}

// Exportar
module.exports = { OllamaClient };

// Ejemplo de uso
if (require.main === module) {
  (async () => {
    const client = new OllamaClient("http://localhost:11434", "mistral:latest");

    // Listar modelos
    console.log("📦 Modelos disponibles:");
    const models = await client.listModels();
    models.forEach((m) => console.log(`  • ${m}`));

    // Chat
    console.log("\n🤖 Chat:");
    const response = await client.chat([
      { role: "user", content: "¿Cuál es 2+2?" },
    ]);
    console.log(response.choices[0].message.content);
  })();
}
