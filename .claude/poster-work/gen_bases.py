# -*- coding: utf-8 -*-
"""Generate the base illustration for every poster in the batch.

Usage: python gen_bases.py [slug ...]     (no args = all)

Wraps sn-image-base's CLI. The prompt shape is copied from the 1Panel run that
was verified to produce a usable layout: character hard right, left third left
empty for the typography overlay. The model ignores "no text" and always stamps
a sensenova watermark bottom-right -- clean.py and the poster's bottom bar deal
with those, so they are not treated as failures here.
"""
import json
import subprocess
import sys
from pathlib import Path

RUNNER_DIR = Path(r"C:\Users\xinan\.claude\skills\sn-image-base")
WORK = Path(__file__).parent
NEGATIVE = ("text, letters, numbers, words, watermark, logo, dark background, "
            "clutter, photorealistic, vertical")

BODY = (
    "Composition: wide 16:9 landscape layout. "
    "RIGHT SIDE: one original anime-style character, {char}, surrounded by floating "
    "holographic {props}, dynamic but elegant pose, looking slightly toward the viewer, "
    "high-quality anime illustration, clean line art, detailed hair and clothing, "
    "professional developer aesthetic. "
    "LEFT SIDE: keep mostly clean and empty, only a very soft light cool gradient "
    "background with a subtle grid, tiny dots and faint abstract data lines, reserved "
    "for typography overlay, no objects and no character on the left third. "
    "Color palette: primary {primary}, secondary {secondary}, background very light cool "
    "gray, low contrast, soft lighting, light particles, subtle glow around the character. "
    "Style: high-end anime technology magazine, clean infographic poster, professional "
    "technical blog hero image, balanced whitespace, sharp details, cohesive visual system. "
    "Avoid: any text, letters, numbers, watermark, vertical composition, mobile layout, "
    "photorealistic character, overly dark background, visual clutter, low-quality "
    "anatomy, objects covering the left side."
)

POSTERS = {
    "linux": dict(
        theme="Linux command line and shell system administration",
        char="a calm focused young female Linux system engineer with short black hair "
             "and a deep violet streak, wearing a dark technical jacket with rolled sleeves",
        props="terminal windows, a glowing shell prompt, a file system tree, command line "
              "panels and small penguin-shaped tech badges",
        primary="deep charcoal blue and violet", secondary="soft indigo"),
    "mysql": dict(
        theme="MySQL relational database and SQL querying",
        char="a sharp professional young female database engineer with long navy blue hair "
             "and blue highlights, wearing a smart dark blue blazer over a hoodie",
        props="floating data tables, SQL query windows, an ER diagram, index nodes and "
              "glowing database cylinder icons",
        primary="deep database blue and cyan", secondary="soft steel blue"),
    "git": dict(
        theme="Git version control and team collaboration workflow",
        char="an energetic young female software engineer with dark hair and vivid orange "
             "highlights, wearing a casual grey hoodie with a lanyard",
        props="a glowing git branch graph, commit nodes, merge arrows, repository cards "
              "and small branch labels",
        primary="warm orange red and slate", secondary="soft amber"),
    "html": dict(
        theme="HTML markup and web page structure",
        char="a cheerful young female frontend developer with dark brown hair in a short "
             "ponytail, wearing a light orange cardigan over a t-shirt",
        props="a browser window, floating angle-bracket tag chips, a DOM tree diagram and "
              "web page wireframe panels",
        primary="web orange and deep slate", secondary="soft coral"),
    "css": dict(
        theme="CSS styling, selectors and the box model",
        char="a stylish young female UI designer with dark hair fading to blue at the tips, "
             "wearing a light blue shirt with a short jacket",
        props="color swatch palettes, a glowing box model diagram, style rule panels, "
              "selector cards and floating gradient tiles",
        primary="css blue and deep navy", secondary="soft sky blue"),
    "markdown": dict(
        theme="Markdown writing and technical note taking",
        char="a gentle young female technical writer with soft dark hair and thin glasses, "
             "wearing a knitted cream sweater",
        props="a floating markdown editor window, heading hash marks, bullet list cards, "
              "a preview pane and quotation marks",
        primary="slate grey and teal", secondary="soft warm grey"),
    "frontend-run": dict(
        theme="running a frontend project with Node.js, pnpm and Vite",
        char="a lively young female frontend developer with dark hair in two loose braids "
             "and a green streak, wearing a casual dark green hoodie",
        props="a laptop showing a dev server terminal, package manager cards, a Vite "
              "lightning badge and floating dependency nodes",
        primary="node green and deep teal", secondary="soft mint"),
    "hexo": dict(
        theme="building a personal blog with Hexo and the Butterfly theme",
        char="a warm creative young female blogger with long dark hair and a cyan hairpin, "
             "wearing a soft blue cardigan",
        props="a glowing blog homepage, floating post cards, a GitHub repository panel, "
              "butterfly motifs and deployment arrows",
        primary="hexo blue and cyan", secondary="soft lavender"),
    "pingjiao": dict(
        theme="JavaScript browser automation script for a university course evaluation "
              "system",
        char="a bright young female student developer with dark hair in a messy bun and "
             "yellow highlights, wearing an oversized yellow hoodie",
        props="a browser window with an auto-filling form, JavaScript snippet panels, "
              "clicking cursor symbols and checkmark badges",
        primary="javascript yellow and dark charcoal", secondary="soft gold"),
    "deploy": dict(
        theme="deploying and running a full stack frontend and backend project",
        char="a confident young female full stack engineer with dark hair tied back and "
             "teal highlights, wearing a technical vest over a dark shirt",
        props="a server rack, API request and response panels, a deployment pipeline with "
              "connected stages and cloud nodes",
        primary="teal blue and deep navy", secondary="soft aqua"),
}


def main(slugs):
    for slug in slugs:
        spec = POSTERS[slug]
        prompt = (
            f"Create a premium 16:9 horizontal anime-style technology editorial poster "
            f"background for a modern developer technical blog. Theme: {spec['theme']}. "
            + BODY.format(**spec)
        )
        out = WORK / f"{slug}-base.png"
        cmd = [
            sys.executable, "scripts/sn_agent_runner.py", "sn-image-generate",
            "--prompt", prompt,
            "--negative-prompt", NEGATIVE,
            "--aspect-ratio", "16:9",
            "--image-size", "2k",
            "--save-path", str(out),
            "--output-format", "json",
        ]
        print(f"=== {slug} -> {out.name}", flush=True)
        r = subprocess.run(cmd, cwd=RUNNER_DIR, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        tail = (r.stdout or "").strip().splitlines()
        print(f"    rc={r.returncode} {tail[-1] if tail else (r.stderr or '')[-300:]}",
              flush=True)
        if r.returncode != 0:
            print(f"    !! FAILED: {(r.stderr or '')[-500:]}", flush=True)
    print("=== done", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(POSTERS))
