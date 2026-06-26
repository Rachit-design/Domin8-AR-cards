#!/usr/bin/env python3
"""
Reads players.json → rewrites PLAYERS map in index.html → generates QR PNGs.

Usage:  python3 scripts/generate.py
Install: pip install qrcode[pil]
"""
import json, re, sys
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "players.json"
INDEX  = ROOT / "index.html"
QR_DIR = ROOT / "qr"

def load_config():
    with open(CONFIG) as f:
        data = json.load(f)
    base = data.get("_baseUrl", "").rstrip("/") + "/"
    return base, data.get("players", [])

def update_index(players):
    lines = ["  const PLAYERS = {"]
    for i, p in enumerate(players):
        rank = p.get("rank", "")
        rank_field = f', rank: "{rank}"' if rank else ""
        lines.append(
            f'    "{p["key"]}": {{ targetIndex: {i}, video: "./videos/{p["video"]}",'
            f' name: "{p["name"]}"{rank_field} }},'
        )
    lines.append("  };")
    new_block = "\n".join(lines)

    html = INDEX.read_text("utf-8")
    pattern = re.compile(r"  const PLAYERS = \{[\s\S]*?\n  \};")
    if not pattern.search(html):
        print("ERROR: PLAYERS block not found in index.html"); sys.exit(1)
    INDEX.write_text(pattern.sub(new_block, html), "utf-8")
    print(f"  [OK] index.html updated — {len(players)} players")

def generate_qrs(base_url, players):
    try:
        import qrcode
    except ImportError:
        print("ERROR: run  pip install qrcode[pil]"); sys.exit(1)
    QR_DIR.mkdir(exist_ok=True)
    for p in players:
        url = f"{base_url}?p={p['key']}"
        img = qrcode.make(url, box_size=20, border=2)
        img.save(QR_DIR / f"{p['key']}.png")
        print(f"  QR  {p['key']:24s} → {url}")

def check_videos(players):
    vdir = ROOT / "videos"
    missing = [p["video"] for p in players if not (vdir / p["video"]).exists()]
    if missing:
        print(f"\n  [!]  Missing videos in /videos/:")
        for m in missing: print(f"     - {m}")
    else:
        print(f"\n  [OK] All {len(players)} videos found in /videos/")

def check_targets():
    t = ROOT / "targets" / "targets.mind"
    if not t.exists():
        print("  [!]  targets/targets.mind not found — compile it from https://hiukim.github.io/mind-ar-js-doc/tools/compile")
    else:
        size_mb = t.stat().st_size / 1024 / 1024
        print(f"  [OK] targets/targets.mind exists ({size_mb:.1f} MB)")

def main():
    base, players = load_config()
    if "YOUR-GITHUB-USERNAME" in base:
        print("[!]  Set your real GitHub Pages URL in players.json _baseUrl first!\n")

    print("Updating index.html...")
    update_index(players)

    print("\nGenerating QR codes → /qr/")
    generate_qrs(base, players)

    print("\nChecking assets...")
    check_videos(players)
    check_targets()

    print(f"\n[OK] Done. {len(players)} players ready.")

if __name__ == "__main__":
    main()
