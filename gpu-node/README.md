# gpu-node/

Runs on the Legion (RTX 5070 Laptop, 8 GB). Arrives in Phase 1–2.

- speech-to-text service: faster-whisper `distil-large-v3`, English, exposed over HTTP on the LAN
- Ollama with `qwen3:8b` runs alongside (installed separately)

Ollama must listen on the LAN for the Hub to reach it: set the environment variable `OLLAMA_HOST=0.0.0.0`,
restart Ollama, and allow TCP 11434 from the Hub only in Windows Firewall.
