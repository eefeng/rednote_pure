#!/usr/bin/env python3
"""Generate a fashion portrait using OpenAI's GPT Image 2 API."""

import base64
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "assets" / "fashion_portrait.png"
PROMPT = (
    "A sophisticated editorial fashion photograph of an adult woman in her late "
    "twenties on a rooftop terrace at golden hour. She wears a long black satin "
    "evening gown and understated gold jewelry, with softly styled dark hair. "
    "She is smiling with a confident, relaxed pose. Cinematic warm light, natural "
    "skin texture, a softly blurred city skyline, and the polished aesthetic of a "
    "luxury fashion magazine. Full-length vertical portrait."
)


def api_key() -> str:
    """Read the key from the environment or the local, untracked .env file."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key

    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == "OPENAI_API_KEY":
                return value.strip().strip('"\'')
    return ""


def main() -> int:
    key = api_key()
    if not key:
        print("Set OPENAI_API_KEY in your environment or .env file.", file=sys.stderr)
        return 1

    body = json.dumps(
        {
            "model": "gpt-image-2",
            "prompt": PROMPT,
            "size": "1024x1536",
            "quality": "high",
            "output_format": "png",
            "n": 1,
        }
    ).encode("utf-8")
    request = Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=300) as response:
            result = json.load(response)
        image = base64.b64decode(result["data"][0]["b64_json"], validate=True)
        if not image.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("The API did not return a PNG image")
    except HTTPError as error:
        print(f"Image generation failed: HTTP {error.code}.", file=sys.stderr)
        return 1
    except (URLError, TimeoutError, OSError, ValueError, KeyError, IndexError) as error:
        print(f"Image generation failed: {error}", file=sys.stderr)
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(image)
    print(f"Saved {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
