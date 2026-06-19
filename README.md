# Domin8 — League of Rising Stars: AR Gamer Cards

Physical gamer cards that come alive. Scan QR on card back → camera opens → point at card front → the photo area animates with a video while the name plate stays as printed.

## How it works
- `index.html` — single page, handles all 30 players via URL param `?p=playername`
- `targets/targets.mind` — compiled image-tracking data for all card fronts
- `videos/` — one compressed MP4 per player
- `qr/` — auto-generated QR code PNGs (one per player, for printing on card backs)
- `players.json` — the only file you edit to add/remove players

## Card layout (from your Figma)
```
┌──────────────────────┐
│                      │  ← dark border
│  ┌────────────────┐  │
│  │                │  │
│  │   PHOTO AREA   │  │  ← VIDEO plays here (680 × 740)
│  │   (animated)   │  │
│  │                │  │
│  ├────────────────┤  │
│  │  NAME PLATE    │  │  ← stays as printed card
│  └────────────────┘  │
│                      │
└──────────────────────┘
Card: 750 × 1050
```

## Setup (one time)

### 1. Create GitHub repo
- GitHub Desktop → New Repository → name: `cards`, public
- Set the local path to this folder
- Publish to GitHub

### 2. Enable GitHub Pages
- On github.com: repo → Settings → Pages
- Source: `main` branch, `/ (root)` → Save
- Your URL: `https://YOUR-USERNAME.github.io/cards/`

### 3. Set your URL
- Open `players.json`, change `_baseUrl` to your real GitHub Pages URL

## Adding players

### A. Prepare your video
- **Aspect ratio**: render your video to match the photo area on the card (~680:740 ≈ 0.92:1, nearly square portrait)
- **Compress**: MP4 H.264, under 5 MB. Use HandBrake → preset "Vimeo YouTube 720p30" → quality RF 28
- **Name**: lowercase, no spaces: `mamanotjoe.mp4`
- Drop into `/videos/`

### B. Export card fronts
- From Figma, export each player's card front as PNG at 2x or 3x
- These are only used for compiling the target file (step C), not deployed to the site

### C. Compile targets.mind
1. Open https://hiukim.github.io/mind-ar-js-doc/tools/compile
2. Upload ALL card front PNGs at once, **in alphabetical order by player key**
3. Click Start → wait → Download `targets.mind`
4. Put it in `/targets/targets.mind` (replace the old one)

**The upload order = the targetIndex in players.json. Alphabetical order keeps them in sync.**

### D. Edit players.json
List all players in **alphabetical order by key**:
```json
{
  "_baseUrl": "https://yourname.github.io/cards/",
  "players": [
    { "key": "ghostwire",   "name": "GHOSTWIRE",   "video": "ghostwire.mp4" },
    { "key": "kaalbhairav", "name": "KAALBHAIRAV", "video": "kaalbhairav.mp4" },
    { "key": "mamanotjoe",  "name": "MAMANOTJOE",  "video": "mamanotjoe.mp4" }
  ]
}
```

### E. Run the generator
```bash
pip install qrcode[pil]
python3 scripts/generate.py
```
This does two things:
- Rewrites the PLAYERS map inside `index.html`
- Generates QR PNGs in `/qr/` for each player

### F. Push and test
- GitHub Desktop → Commit → Push
- Wait ~1 minute for Pages to rebuild
- Open `https://yourname.github.io/cards/?p=mamanotjoe` on your phone
- Point at the printed card front

### G. Print QR codes on card backs
- QR PNGs are in `/qr/`
- Place each player's QR in the empty space on the card back layout in Figma (below "SCAN TO ACTIVATE")

## Fine-tuning the video position

If the video doesn't align perfectly with the photo area, edit these 3 values at the top of the script in `index.html`:

```javascript
const VIDEO_WIDTH  = 0.648;  // make bigger = wider video
const VIDEO_HEIGHT = 0.705;  // make bigger = taller video
const VIDEO_Y      = 0.148;  // make bigger = shifts video up, smaller = shifts down
```

Change, push, test on phone. Repeat until it looks right.

## Troubleshooting
- **Black screen**: grant camera permission, must be HTTPS (GitHub Pages handles this)
- **Card not detected**: card front needs visual detail (yours is good). Check the MindAR compiler's preview
- **Video stretched/squished**: your video aspect ratio doesn't match the photo area. Re-render at ~680:740
- **Wrong video for wrong card**: targetIndex doesn't match upload order. Re-upload in alphabetical order
- **Slow load**: video > 5 MB. Recompress
- **iOS won't play video**: video must be muted (it is in the code). User may need to tap once
