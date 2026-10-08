# Architecture

Ada v1 runs on two laptops on the same home network, plus an Android phone for alerts.

| Machine | Role | Runs |
| --- | --- | --- |
| ThinkPad E15 | **Hub**, always on | wake word, VAD, voice loop, Kokoro TTS, tools, memory, scheduler, HUD server |
| Legion Pro 5 (Ryzen 9 9955HX, 32 GB, RTX 5070 Laptop 8 GB) | **GPU node** | faster-whisper speech-to-text, Ollama + `qwen3:8b` |
| Android phone | **Client** | ntfy alerts and alarms, the HUD installed as a web app |

## One spoken turn

1. **Wake.** openWakeWord on the Hub hears the wake phrase. The orb goes from asleep to listening.
2. **Listen.** Silero VAD and Smart Turn decide when you have finished speaking.
3. **Transcribe.** The Hub sends the audio to the GPU node; faster-whisper returns English text.
4. **Think.** The Hub sends the text, a short system prompt and recent context to Ollama. The orb shows thinking.
5. **Act (optional).** If the model asks for a tool, the Hub checks the allowlist and the schema. A tool that changes something waits for your yes (orb: confirming). Every call is audited.
6. **Speak.** Kokoro turns the reply into audio on the Hub. The orb shows speaking.
7. **Follow up.** For 8 seconds Ada listens without the wake phrase; then she goes back to sleep. "Ada, stand down" ends it at once.

Target: under 2.5 s from the end of your sentence to the first word of the reply.

## Network

| Service | Host | Port | Reached by |
| --- | --- | --- | --- |
| Ollama | GPU node | 11434 | Hub only |
| Speech-to-text | GPU node | 8001 | Hub only |
| HUD (FastAPI + WebSocket) | Hub | 8080 | browser on LAN, phone over Tailscale |
| ntfy | Hub | 8090 | phone over Tailscale |

Nothing is port-forwarded on the router. Remote access is Tailscale only.

## VRAM budget (GPU node, 8 GB)

| Use | Approx. |
| --- | --- |
| Windows desktop and apps | 1.4 GB |
| `qwen3:8b` 4-bit, 4K context | 5–5.5 GB |
| faster-whisper `distil-large-v3` int8 | about 1 GB |

This is tight. If it does not fit, speech-to-text moves to the Ryzen CPU (16 cores). Measured numbers go in `decisions.md`.
