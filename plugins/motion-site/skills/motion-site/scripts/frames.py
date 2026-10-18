"""Frame sheet for motion websites: captures the page at every scroll step
on desktop and mobile, assembles contact sheets, and reports technical problems.

Usage:
    python frames.py index.html
    python frames.py https://example.com --out frames --step 0.5

Requires Playwright:
    pip install playwright && playwright install chromium

Output (in --out, ./frames by default):
    sheet-desktop.png, sheet-mobile.png  — labeled contact sheets
    report.json                          — console errors, horizontal overflow,
                                           small text, visibility under reduced motion
"""

import argparse
import base64
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright is required: pip install playwright && playwright install chromium")

VIEWPORTS = {
    "desktop": {"viewport": {"width": 1440, "height": 900}},
    "mobile": {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True},
}
MAX_FRAMES = 36
SETTLE_MS = 1100  # time for Lenis and scrub smoothing to settle

PROBE_JS = """
() => {
  const textEls = [...document.querySelectorAll('h1,h2,h3,h4,p,li,a,button,span,figcaption,td,th,label')]
    .filter(el => el.childElementCount === 0 && el.textContent.trim().length > 1);
  const small = textEls.filter(el => {
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && parseFloat(cs.fontSize) < 14;
  }).map(el => ({ text: el.textContent.trim().slice(0, 40), size: getComputedStyle(el).fontSize }));
  return {
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth,
    small: small.slice(0, 15), smallCount: small.length,
  };
}
"""

HIDDEN_JS = """
() => [...document.querySelectorAll('h1,h2,h3,p,a,li,figure,img')].filter(el => {
  let n = el; while (n && n !== document.body) {
    const cs = getComputedStyle(n);
    if (cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return true;
    n = n.parentElement;
  } return false;
}).map(el => el.tagName + ': ' + (el.textContent || el.getAttribute('alt') || '').trim().slice(0, 40)).slice(0, 15)
"""


def resolve_url(target: str) -> str:
    if target.startswith(("http://", "https://", "file://")):
        return target
    path = Path(target).resolve()
    if not path.exists():
        sys.exit(f"File not found: {path}")
    return path.as_uri()


def shoot(browser, url: str, name: str, opts: dict, step: float, out: Path) -> dict:
    ctx = browser.new_context(**opts, device_scale_factor=1)
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(2600)  # intro animation

    vh = opts["viewport"]["height"]
    height = page.evaluate("document.documentElement.scrollHeight")
    stride = max(vh * step, (height - vh) / (MAX_FRAMES - 1))
    positions, y = [], 0.0
    while y < height - vh:
        positions.append(int(y))
        y += stride
    positions.append(max(0, height - vh))

    frames, probe = [], None
    for i, pos in enumerate(positions):
        page.evaluate(f"window.scrollTo(0, {pos})")
        page.wait_for_timeout(SETTLE_MS)
        shot = page.screenshot(type="jpeg", quality=72)
        frames.append({"pos": pos, "pct": round(100 * pos / max(1, height - vh)), "img": base64.b64encode(shot).decode()})
        result = page.evaluate(PROBE_JS)
        if probe is None or result["scrollWidth"] > probe["scrollWidth"]:
            probe = result

    ctx.close()
    build_sheet(browser, frames, name, opts["viewport"], out)
    return {
        "frames": len(frames),
        "page_height": height,
        "console_errors": errors[:20],
        "horizontal_overflow": probe["scrollWidth"] > probe["innerWidth"],
        "scroll_width": probe["scrollWidth"],
        "small_text_count": probe["smallCount"] if name == "mobile" else None,
        "small_text_examples": probe["small"] if name == "mobile" else None,
    }


def build_sheet(browser, frames: list, name: str, vp: dict, out: Path):
    cols = 4 if name == "desktop" else 6
    cell_w = 340 if name == "desktop" else 200
    cells = "".join(
        f'<figure><img src="data:image/jpeg;base64,{f["img"]}"><figcaption>#{i + 1} · {f["pct"]}% · y={f["pos"]}</figcaption></figure>'
        for i, f in enumerate(frames))
    html = f"""<!doctype html><meta charset="utf-8"><style>
      body{{margin:0;padding:24px;background:#111;color:#bbb;font:13px monospace}}
      h1{{font:600 18px sans-serif;color:#fff;margin:0 0 16px}}
      .g{{display:grid;grid-template-columns:repeat({cols},{cell_w}px);gap:14px}}
      figure{{margin:0}} img{{width:100%;display:block;border:1px solid #333;border-radius:6px}}
      figcaption{{margin-top:5px}}</style>
      <h1>{name} · {vp['width']}×{vp['height']} · {len(frames)} frames</h1><div class="g">{cells}</div>"""
    page = browser.new_page(viewport={"width": cols * (cell_w + 14) + 48, "height": 600})
    page.set_content(html, wait_until="load")
    page.screenshot(path=str(out / f"sheet-{name}.png"), full_page=True)
    page.close()


def check_reduced_motion(browser, url: str) -> list:
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(1500)
    hidden = page.evaluate(HIDDEN_JS)
    ctx.close()
    return hidden


def main():
    ap = argparse.ArgumentParser(description="Frame sheet and technical check for motion websites")
    ap.add_argument("target", help="path to index.html or a URL")
    ap.add_argument("--out", default="frames", help="output folder")
    ap.add_argument("--step", type=float, default=0.5, help="scroll step as a fraction of the viewport height")
    args = ap.parse_args()

    url = resolve_url(args.target)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        report = {"url": url}
        for name, opts in VIEWPORTS.items():
            print(f"Shooting {name}...")
            report[name] = shoot(browser, url, name, opts, args.step, out)
        report["reduced_motion_hidden"] = check_reduced_motion(browser, url)
        browser.close()

    problems = []
    for name in VIEWPORTS:
        r = report[name]
        if r["console_errors"]:
            problems.append(f"{name}: console errors — {len(r['console_errors'])}")
        if r["horizontal_overflow"]:
            problems.append(f"{name}: horizontal overflow (width {r['scroll_width']}px)")
    if report["mobile"]["small_text_count"]:
        problems.append(f"mobile: text under 14px — {report['mobile']['small_text_count']} elements")
    if report["reduced_motion_hidden"]:
        problems.append(f"reduced motion: hidden elements — {len(report['reduced_motion_hidden'])}")
    report["problems"] = problems

    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSheets: {out / 'sheet-desktop.png'}, {out / 'sheet-mobile.png'}")
    print(f"Report: {out / 'report.json'}")
    print("Problems:\n  " + "\n  ".join(problems) if problems else "No technical problems found.")


if __name__ == "__main__":
    main()
