# CVapp

Interactive personal CV site for Oleg Saveliev.

## Files

- `cv-site.html`: the source you edit (styles, markup and script in one file).
- `build.sh`: wraps the source into a full page at `site/index.html`.
- `site/`: the finished site, ready to host (`index.html`, `oleg.jpg`, `Oleg-Saveliev-CV.pdf`, the Pip images `pip-*.jpg`, `hireloop-demo.mp4` and its poster `hireloop-poster.jpg`, `aid-hero.jpg` for the Projects desktop, and the tab icons `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`).
- `vercel.json`: tells Vercel to run `build.sh` and serve the `site/` folder.
- `.claude/launch.json`: local preview server on port 8791.
- `tools/build_geo.py`: turns Natural Earth and OpenStreetMap downloads into the map data embedded in `cv-site.html` (the `kyivGeo` block) for the Locate animation.

## Edit and rebuild

```bash
./build.sh
```

## Preview locally

```bash
python3 -m http.server 8791 --directory site
```

Then open http://localhost:8791.

## Publish

Live on Vercel: https://oleg-saveliev.vercel.app/ . Every push to `main` redeploys; `vercel.json` runs `build.sh` and serves the `site/` folder. The `site/` folder also works on any other static host.

## What's on the page

- **Projects:** a working mini desktop split into workspace tabs.
  - Personal productivity: Timeline Studio, Planning Poker, Nimbus, Delivery Copilot (its outputs use sample data).
  - Education: AI Decoded, a copy of the academy home screen with its real 105-module catalogue. The Token Generation card opens a live mini lesson; the others link to aidecoded.academy.
  - Personal bot: Pip, who naps until clicked and falls back asleep after 45 seconds. He lives only in this tab. The Pip images are cropped from the Pip LinkedIn carousel.
  - Development: AI Factory.
  - Computer vision: CAM-02, Pi Cam Bot and Frame Journey, a drawn simulation of the Raspberry Pi 5 edge camera from github.com/olegsaveliev/cv-project (the 60-second alert cooldown runs 6x faster there). The hero's person box and the subject file both link to it ("Real camera: CAM-02").
  - Recruitment: Hireloop recruitment, a window that plays the product demo video (it pauses when the window is closed or you switch workspace).
- **My professional journey** (right after the projects): runs as a Claude Code style agent session. Choosing a role shows tool calls, MCP calls and parallel subagents loading it, and a context-window bar fills with every load. Near 84% it auto-compacts; `/compact` and `/clear` work by hand. Steps fold away once a role has loaded (click the summary line to reopen them). Tool names are illustrative, but every result in the traces comes from the CV.
- **The work, in numbers:** eight counted outcomes, each with its story and a Source link that opens the matching role in the career agent.
- **HIRE.EXE:** a relaxed 60-second game. Catch and hire Oleg on night-vision camera feeds (press and hold to lock on, tap Pip for a bonus, tap-frenzy in the last seconds), ending with a printed offer letter.
  - A "Still thinking of hiring me?" alert offers it after 30 seconds on the page or when the mouse heads for the browser tabs (once per visit).
  - It also runs from the terminal (`play`), the command palette and a "Play HIRE.EXE" button in the header. After a game that button becomes "Hired me N× · Send the offer →" plus "↻ Play again" (remembered on the device); the first jumps to Contact and copies the email.
- **Thermal vision:** the Konami code (↑ ↑ ↓ ↓ ← → ← → B A, or `thermal` in the terminal) switches the whole site to a heat-map look.
- **Terminal and command menu:** press `` ` `` for the terminal or ⌘K for the command menu.

The Locate animation uses map data © OpenStreetMap contributors (ODbL) and Natural Earth (public domain). Keep the attribution line visible in the overlay.
