# Decision log

One entry per decision: what was chosen, and why. Newest first.

| Date | Decision | Why |
| --- | --- | --- |
| 2026-10-08 | Repository is public from day one, with gitleaks pre-commit, CI scan and push protection | Portfolio value; guardrails make leaks a blocked commit instead of a cleanup |
| 2026-10-08 | Python 3.12 in a uv environment | Python 3.14 is too new for several ML libraries Ada needs |
| 2026-10-07 | v1 is English only | Simplest speech-to-text, best Kokoro voice; French in v1.5 |
| 2026-10-07 | Language model: `qwen3:8b`, 4-bit, via Ollama | Fits the 8 GB RTX 5070 Laptop beside speech-to-text; strong tool calling |
| 2026-10-07 | Speech-to-text: faster-whisper `distil-large-v3` | English-only model, smaller and faster than multilingual ones |
| 2026-10-07 | Phone alerts through self-hosted ntfy | Free, no Google account, rings as an alarm on Android |
| 2026-10-07 | Orb design: revision 3, information movement as the visual grammar | Six states read as six behaviours of one entity |
| 2026-10-07 | Machines named by role: Hub, GPU node, Phone | Plain names over codenames |
| 2026-10-07 | Name: A.D.A, Agentic Dialogue Assistant, spoken "Ada" | Named after Ada Lovelace |
| 2026-10-07 | Stack: openWakeWord, Silero VAD + Smart Turn, Pipecat, Kokoro, FastMCP, SQLite + Chroma, APScheduler, FastAPI + Three.js | Open-source, local, proven in similar assistants |

## Open

- Wake phrase: "Ada, stand by" (recommended), "Hiya Ada" or "Accio Ada"
- ThinkPad OS: Windows or Ubuntu 24.04
- Kokoro voice: `af_heart` or `bf_emma`
