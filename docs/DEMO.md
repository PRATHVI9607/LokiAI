# Recording the Loki demo GIF

A short demo is the single highest-ROI addition to the README. Aim for **15–30s**
that shows the loop: wake word → a command → Loki acts and replies.

## Suggested script
1. Say **"Hey Loki"** → the orb wakes, the composer appears.
2. **"What's on my screen?"** → vision reads it and answers.
3. **"Open Notepad and type my address, then save it as address.txt"** → multi-step automation runs.
4. **"Remember that my flight is at 6 a.m."** → *"Noted."*
5. Hover a reply → click 👍, then open **Insights** to show the learning loop.

Keep it calm and unhurried — the UI is meant to feel premium, not frantic.

## Capture (Windows)
- **[ScreenToGif](https://www.screentogif.com/)** (free): record the Loki window region,
  trim dead air, **File → Save as → GIF**.
- Target **< 8 MB** so it renders inline on GitHub. If it's larger:
  - drop to ~12–15 fps,
  - reduce the capture region to just the chat dock + orb,
  - shorten to the two best commands.

## Wire it up
1. Save the file as `docs/demo.gif`.
2. In `README.md`, replace the *"Demo GIF coming soon"* line (and the HTML comment
   above it) with:
   ```markdown
   ![Loki demo](docs/demo.gif)
   ```
3. Commit `docs/demo.gif` — it's an asset, not build output, so it belongs in git.

> Tip: a 1080p capture downscaled to ~900px wide looks crisp on GitHub without bloating the file.
