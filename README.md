# CVapp

Interactive personal CV site for Oleg Saveliev.

## Files

- `cv-site.html`: the source you edit (styles, markup and script in one file).
- `build.sh`: wraps the source into a full page at `site/index.html`.
- `site/`: the finished site, ready to host (`index.html`, `oleg.jpg`, `Oleg-Saveliev-CV.pdf`, the Pip images `pip-*.jpg` and `aid-hero.jpg` for the Projects desktop).
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

Upload the `site/` folder to any static host, for example Netlify Drop (app.netlify.com/drop), GitHub Pages or Vercel.

The Locate animation uses map data © OpenStreetMap contributors (ODbL) and Natural Earth (public domain). Keep the attribution line visible in the overlay.

The Projects section is a working mini desktop split into workspace tabs: Personal productivity (Timeline Studio, Planning Poker, Nimbus, Delivery Copilot), Education (AI Decoded, a copy of the academy home screen with its real 105-module catalogue; the Token Generation card opens a live mini lesson and the others link to aidecoded.academy), Personal bot (Pip), Development (AI Factory) and Computer vision (CAM-02, Pi Cam Bot and Frame Journey, a drawn simulation of the Raspberry Pi 5 edge camera from github.com/olegsaveliev/cv-project; the 60-second alert cooldown runs 6x faster there). The hero's person box and the subject file both link to it ("Real camera: CAM-02"). Each app window runs a small self-contained demo, and the Delivery Copilot outputs use sample data. The Pip mascot lives only in the Personal bot tab; he naps until clicked, then falls back asleep after 45 seconds without interaction. The Pip images are cropped from the Pip LinkedIn carousel.

The career section (My professional journey, right after the projects) runs as a Claude Code style agent session: choosing a role shows tool calls, MCP calls and parallel subagents loading it, and a context-window bar fills with every load. Near 84% it auto-compacts; `/compact` and `/clear` work by hand. The agent console replaces the old years bar and folds its steps away once a role has loaded (click the summary line to reopen them). Tool names are illustrative, but every result in the traces comes from the CV.

The Impact section (The work, in numbers) merges the old number tiles and flagged events: eight counted outcomes, each with its story and a Source link that opens the matching role in the career agent.

HIRE.EXE is a relaxed 60-second game: catch and hire Oleg on night-vision camera feeds (press and hold to lock on, tap Pip for a bonus, tap-frenzy in the last seconds), ending with a printed offer letter. A "Still thinking of hiring me?" alert offers it after 30 seconds on the page or when the mouse heads for the browser tabs (once per visit); it also runs from the terminal (`play`), the command palette and a "Play HIRE.EXE" button in the header. After a game that button becomes "Hired me N× · Send the offer →" plus a "↻ Play again" button (remembered on the device); the first jumps to Contact and copies the email. The Konami code (↑ ↑ ↓ ↓ ← → ← → B A, or `thermal` in the terminal) switches the whole site to thermal vision.
