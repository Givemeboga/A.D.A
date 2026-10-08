# hub/

Runs on the ThinkPad, always on. Arrives in Phase 2.

- wake word (openWakeWord) and voice activity (Silero VAD)
- voice loop (Pipecat) with turn detection (Smart Turn)
- text-to-speech (Kokoro, English)
- tool host (FastMCP), memory (SQLite + Chroma), scheduler (APScheduler)
- HUD server (FastAPI + WebSocket) that drives `hud/orb.html`
