"""Build the browser-only Technocore client for a static Vercel deployment."""

from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "humans.html"
OUTPUT = ROOT / "public" / "index.html"
VERCEL_CONFIG = ROOT / "vercel.json"


def _sha256_source(value: str) -> str:
    digest = hashlib.sha256(value.encode()).digest()
    return "'sha256-" + base64.b64encode(digest).decode() + "'"


def _inline_source(html: str, tag: str) -> str:
    match = re.search(rf"<{tag} nonce=\"__NONCE__\">(.*?)</{tag}>", html, re.DOTALL)
    if match is None:
        raise SystemExit(f"missing inline {tag} block in {SOURCE}")
    return match.group(1)


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")
    config = json.loads(VERCEL_CONFIG.read_text(encoding="utf-8"))
    csp = next(
        header["value"]
        for rule in config["headers"]
        for header in rule["headers"]
        if header["key"].lower() == "content-security-policy"
    )
    required = {
        _sha256_source(_inline_source(html, "style")),
        _sha256_source(_inline_source(html, "script")),
    }
    missing = {item for item in required if item not in csp}
    if missing:
        hashes = " ".join(sorted(missing))
        raise SystemExit(f"vercel.json CSP is stale; add: {hashes}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = html.replace(' nonce="__NONCE__"', "")
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"built {OUTPUT}")


if __name__ == "__main__":
    main()
