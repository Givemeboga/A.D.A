"""Phase 0 exit test: the Hub can reach Ollama on the GPU node.

Run from the Hub (or the Legion itself):
    python tests/smoke/check_ollama.py

Reads gpu_node.host / ollama_port / model from config/config.local.toml.
Uses only the Python standard library, so it works before any setup.
"""

from __future__ import annotations

import json
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "config.local.toml"
PROMPT = "Answer in one sentence: who was Ada Lovelace?"


def fail(message: str) -> None:
    print(f"FAIL  {message}")
    sys.exit(1)


def load_config() -> dict:
    if not CONFIG.exists():
        fail(f"{CONFIG.relative_to(ROOT)} not found. Copy config/config.example.toml to it and set gpu_node.host.")
    with CONFIG.open("rb") as f:
        cfg = tomllib.load(f)
    node = cfg.get("gpu_node", {})
    if node.get("host", "REPLACE_ME") == "REPLACE_ME":
        fail("Set gpu_node.host in config/config.local.toml to the Legion's IP address.")
    return node


def call(url: str, payload: dict | None = None, timeout: float = 120) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def main() -> None:
    node = load_config()
    base = f"http://{node['host']}:{node.get('ollama_port', 11434)}"
    model = node.get("model", "qwen3:8b")

    try:
        version = call(f"{base}/api/version", timeout=5)["version"]
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        fail(f"Cannot reach Ollama at {base} ({e}). On the Legion, set OLLAMA_HOST=0.0.0.0 and allow port 11434 in the firewall.")
    print(f"ok    Ollama {version} at {base}")

    start = time.perf_counter()
    try:
        out = call(f"{base}/api/generate", {
            "model": model,
            "prompt": PROMPT,
            "stream": False,
            "think": False,
            "options": {"num_ctx": node.get("num_ctx", 4096)},
        })
    except urllib.error.HTTPError as e:
        fail(f"Ollama answered {e.code}: {e.read().decode(errors='replace')[:200]}. Did you run 'ollama pull {model}'?")
    total = time.perf_counter() - start

    tokens = out.get("eval_count", 0)
    gen_s = out.get("eval_duration", 0) / 1e9
    tps = tokens / gen_s if gen_s else 0
    print(f"ok    {model} answered in {total:.2f} s ({tps:.0f} tokens/s)")
    print(f"      \"{out.get('response', '').strip()}\"")

    try:
        for m in call(f"{base}/api/ps", timeout=5).get("models", []):
            vram = m.get("size_vram", 0) / 2**30
            size = m.get("size", 0) / 2**30
            print(f"ok    {m.get('name')} uses {vram:.1f} GB VRAM of {size:.1f} GB total")
    except (urllib.error.URLError, OSError):
        pass

    print("PASS  Phase 0: the Hub reaches Ollama on the GPU node")


if __name__ == "__main__":
    main()
