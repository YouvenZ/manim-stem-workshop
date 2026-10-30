"""
Render every workshop scene and publish it to the website folder (docs/).

For each scene this script:
  1. runs Manim,
  2. copies the MP4 to docs/videos/<slug>.mp4 (remuxed with +faststart so it
     streams in the browser),
  3. grabs a poster image from the last second -> docs/posters/<slug>.jpg,
  4. copies the source code -> docs/code/<slug>.py (shown on the website).

Usage (from the repository root, with the conda env active):
    python scripts/render_all.py              # all scenes, 720p30
    python scripts/render_all.py -q h         # 1080p60
    python scripts/render_all.py --only 05    # scenes whose slug starts with "05"
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def discover_scenes():
    """Every scenes/NN_*.py file and the first Scene class defined in it."""
    found = []
    for path in sorted((ROOT / "scenes").glob("[0-9][0-9]_*.py")):
        match = re.search(r"^class\s+(\w+)\s*\(", path.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            found.append((path.name, match.group(1)))
    return found


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-q", "--quality", default="m", choices=list("lmhk"),
                        help="Manim quality flag: l=480p15, m=720p30, h=1080p60, k=4K")
    parser.add_argument("--only", default="", help="render only scenes whose file name starts with this")
    args = parser.parse_args()

    media = ROOT / "build" / "media"
    out_dirs = {name: ROOT / "docs" / name for name in ("videos", "posters", "code")}
    for d in out_dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    for filename, cls in discover_scenes():
        if not filename.startswith(args.only):
            continue
        slug = Path(filename).stem
        print(f"\n=== {slug} ({cls}) ===")
        run([sys.executable, "-m", "manim", f"-q{args.quality}", "--media_dir", media,
             Path("scenes") / filename, cls])

        candidates = sorted((media / "videos" / slug).glob(f"*/{cls}.mp4"), key=lambda p: p.stat().st_mtime)
        if not candidates:
            sys.exit(f"Could not find the rendered video for {cls}")
        video = candidates[-1]

        dst = out_dirs["videos"] / f"{slug}.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-c", "copy", "-movflags", "+faststart", dst])
        run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-1", "-i", video,
             "-frames:v", "1", "-q:v", "3", out_dirs["posters"] / f"{slug}.jpg"])
        shutil.copy(ROOT / "scenes" / filename, out_dirs["code"] / f"{slug}.py")
        print(f"  -> docs/videos/{slug}.mp4")

    print("\nDone. Preview the site with:  python -m http.server -d docs 8000")


if __name__ == "__main__":
    main()
