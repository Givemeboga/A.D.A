# A.D.A — Agentic Dialogue Assistant

Ada is a local-first, voice-first personal assistant that runs on two laptops at home. You say a wake phrase, talk normally, and Ada answers out loud. She can use a small set of tools (timers, reminders, notes, web search), and nothing that changes anything runs without your spoken or on-screen "yes".

No cloud model, no subscription, no audio leaves the house.

> **Status:** Phase 0, setup. The voice loop does not exist yet. See the [roadmap](#roadmap).

## How it works

```
                     ┌──────────────────────── ThinkPad E15 · Hub (always on) ───────────────────────┐
  you ── mic ──────▶ │  wake word + VAD  ─▶  voice loop (Pipecat)  ─▶  voice (Kokoro)  ─▶  speaker   │ ──▶ you
                     │                          │        ▲                                            │
                     │       tools + memory ◀───┤        │            HUD server ─▶ 3D orb (browser)  │
                     └──────────────────────────┼────────┼──────────────────────┬────────────────────┘
                                   audio → text │        │ prompt → reply       │ alerts · remote
                     ┌──────────────────────────▼────────┴──────┐        ┌──────▼──────────┐
                     │  Legion Pro 5 · GPU node                 │        │  Android phone  │
                     │  faster-whisper  ·  Ollama + qwen3:8b    │        │  ntfy · HUD app │
                     └──────────────────────────────────────────┘        └─────────────────┘
```

| Part | Runs on | Choice (v1) |
| --- | --- | --- |
| Wake word | Hub | openWakeWord, custom phrase |
| Voice activity + turn taking | Hub | Silero VAD, Smart Turn |
| Voice loop | Hub | Pipecat |
| Speech-to-text | GPU node | faster-whisper `distil-large-v3`, English |
| Language model | GPU node | Ollama, `qwen3:8b` (4-bit, 8 GB VRAM) |
| Text-to-speech | Hub | Kokoro, one English voice |
| Tools | Hub | FastMCP over stdio, strict allowlist |
| Memory | Hub | SQLite + Chroma |
| Scheduler | Hub | APScheduler 3.x, SQLite job store |
| HUD | Hub → browser | FastAPI + WebSocket + Three.js orb |
| Phone alerts | Hub → phone | self-hosted ntfy over Tailscale |

More detail: [docs/architecture.md](docs/architecture.md) · every choice and why: [docs/decisions.md](docs/decisions.md).

## The orb

Ada's face is a 3D particle orb with six states — asleep, listening, thinking, speaking, confirming, error — each defined by which way information moves through it. Open [`hud/orb.html`](hud/orb.html) in a browser to see it; keys `1`–`6` switch state.

## Security model

Ada is built by someone on an offensive-security track, so the rules live in code, not in the prompt:

1. **Allowlist only.** Ada can call the tools on the list and nothing else. No shell, no payments, no sending messages in v1.
2. **Confirmation in code.** Any tool that changes something waits for an explicit yes.
3. **Untrusted content is data.** Web pages and notes never become instructions to the planner.
4. **Fixed targets.** Alarms go only to the owner's phone, set in local config, never chosen by the model.
5. **Append-only audit log** of every tool call.
6. **Nothing exposed to the internet.** Services listen on the LAN or Tailscale only.

Full rules and threat model: [docs/security.md](docs/security.md). Found a problem? See [SECURITY.md](SECURITY.md).

## Repository guardrails

This repo is public from the first commit, so secrets and personal data are kept out mechanically:

- Personal values (phone number, IPs, ntfy topic, keys) live in `config/config.local.toml`, which git ignores. The committed [`config/config.example.toml`](config/config.example.toml) holds placeholders only.
- A **gitleaks** pre-commit hook blocks any commit that contains a secret, including a phone number or a Tailscale key ([.gitleaks.toml](.gitleaks.toml)).
- The same scan runs in GitHub Actions on every push and pull request.
- GitHub secret scanning with push protection is turned on.
- `.gitignore` excludes models, recordings, databases, logs and `.env` files.

## Getting started (Phase 0)

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/), Git, and Ollama on the GPU node.

```bash
git clone https://github.com/Givemeboga/A.D.A.git
cd A.D.A

# 1. Turn on the guardrails before your first commit
uv tool install pre-commit
pre-commit install

# 2. Create your private config
cp config/config.example.toml config/config.local.toml   # Windows: copy config\config.example.toml config\config.local.toml
#    then edit config.local.toml: set gpu_node.host to the Legion's IP

# 3. On the GPU node
ollama pull qwen3:8b

# 4. Phase 0 exit test, run from the Hub
python tests/smoke/check_ollama.py
```

## Roadmap

| Phase | Goal | Exit test |
| --- | --- | --- |
| 0 | Setup | The Hub reaches Ollama on the GPU node |
| 1 | Each part works alone | Five smoke tests pass with timings |
| 2 | First voice loop | Median reply under 2.5 s from end of speech |
| 3 | HUD goes live | The orb follows a whole conversation in sync |
| 4 | Tools + safety core | No change tool runs without a yes |
| 5 | Memory | Recalls a fact days later, forgets on request |
| 6 | Custom wake word + polish | 20/20 wakes, at most 1 false wake a day |
| 7 | Phone | A silent phone rings at the set time |
| 8 | Hardening + v1 release | A week of daily use, no injected tool call |

## Repository layout

```
hub/          voice loop, tools, memory, HUD server (ThinkPad)
gpu-node/     speech-to-text service (Legion); Ollama runs alongside
hud/          the 3D orb and, later, the dashboard
tools/        FastMCP tool servers
config/       config.example.toml (committed) · config.local.toml (ignored)
docs/         architecture, decisions, security
tests/smoke/  one script per component, each prints PASS and its timing
```

## License

[MIT](LICENSE)
