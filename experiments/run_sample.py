"""Day-4 sample run: 10 concepts through the pipeline, one batch.

Writes experiments/04_sample.md with per-concept results and aggregate
metrics: first-try success, retry success, fail.

Reusable: change CONCEPTS or pass a model arg via the existing pipeline CLI
to repeat against E2B / 26B once we get to the model benchmark.
"""

from __future__ import annotations

import sys
import time
import traceback
from pathlib import Path

from src.pipeline import SESSIONS_DIR, ask

CONCEPTS: list[tuple[str, str]] = [
    (
        "derivative_x2",
        "Visualise that the derivative of x squared is 2x, by showing a "
        "tangent line whose slope updates at a moving point on the parabola "
        "y = x squared.",
    ),
    (
        "riemann_sum",
        "Show how a Riemann sum approximates the integral of x squared from "
        "0 to 2 by drawing 8 rectangles under the curve.",
    ),
    (
        "limit_secant",
        "Visualise the limit definition of the derivative: a secant line "
        "between two points on a parabola y = x squared becomes the tangent "
        "line as the second point approaches the first.",
    ),
    (
        "triangle_angles",
        "Show that the three angles of a triangle sum to 180 degrees by "
        "drawing a triangle, copying each of its three angles, and "
        "rearranging the copies along a single straight line.",
    ),
    (
        "unit_circle_pythagoras",
        "Animate the Pythagorean identity sin squared theta plus cos squared "
        "theta equals one on a unit circle. Show the right triangle inscribed "
        "in the circle and update the values of sin theta and cos theta as "
        "theta moves around the circle.",
    ),
    (
        "dot_product",
        "Visualise the geometric meaning of the dot product of two 2D vectors "
        "by drawing both vectors from the origin, projecting one onto the "
        "other, and showing that the projection length equals the dot product "
        "divided by the second vector's magnitude.",
    ),
    (
        "compare_powers",
        "Plot f(x) = x squared in blue and g(x) = x cubed in red on the same "
        "axes from x = -2 to x = 2, with labels, so the difference between "
        "quadratic and cubic growth is visible.",
    ),
    (
        "handshake_problem",
        "Visualise the handshake problem for 5 people: arrange 5 dots in a "
        "circle and draw every pairwise handshake as a connecting line, then "
        "display the total count of 10 handshakes as a label.",
    ),
    (
        "cobweb_diagram",
        "Draw the cobweb diagram for the iterative function f(x) = 0.5 x + 1 "
        "starting from x_0 = 0, showing the first 5 iterations converging to "
        "the fixed point at x = 2. Plot the line y = f(x) and the line y = x "
        "and animate the cobweb steps between them.",
    ),
    (
        "saddle_3d",
        "Show a 3D plot of the saddle surface z = x squared minus y squared, "
        "with the camera rotating around the surface so the saddle shape is "
        "clearly visible from multiple angles.",
    ),
]

DEFAULT_SUMMARY_PATH = Path("experiments/04_sample.md")


def count_attempts(session_dir: Path) -> int:
    return len(list(session_dir.glob("attempt_*_scene.py")))


def latest_session() -> Path:
    return max(SESSIONS_DIR.iterdir(), key=lambda p: p.stat().st_mtime)


def run() -> list[dict]:
    results: list[dict] = []
    for cid, concept in CONCEPTS:
        print(f"\n=== {cid} ===", flush=True)
        t0 = time.perf_counter()
        result: dict = {"id": cid, "concept": concept}
        try:
            mp4 = ask(concept)
            result["status"] = "success"
            result["mp4"] = str(mp4)
        except RuntimeError as exc:
            result["status"] = "fail"
            result["error"] = str(exc)[:400]
        except Exception as exc:
            result["status"] = "exception"
            result["error"] = f"{type(exc).__name__}: {exc}"[:400]
            traceback.print_exc()

        result["elapsed_s"] = round(time.perf_counter() - t0, 1)
        try:
            session = latest_session()
            result["session"] = session.name
            result["attempts"] = count_attempts(session)
        except (ValueError, FileNotFoundError):
            result["session"] = ""
            result["attempts"] = 0

        print(
            f"  -> {result['status']} in {result['elapsed_s']}s "
            f"(attempts={result['attempts']})",
            flush=True,
        )
        results.append(result)

    return results


def write_summary(results: list[dict], summary_path: Path = DEFAULT_SUMMARY_PATH) -> None:
    n = len(results)
    success_results = [r for r in results if r["status"] == "success"]
    success = len(success_results)
    first_try = sum(1 for r in success_results if r["attempts"] == 1)
    retry_success = success - first_try
    fail = n - success
    total_time = round(sum(r["elapsed_s"] for r in results), 1)

    lines: list[str] = []
    lines.append("# 04 — Day-4 sample of 10 concepts through the pipeline\n\n")
    lines.append("**Date:** 2026-04-27\n")
    lines.append("**Model:** `gemma4:e4b-it-q8_0`\n\n")
    lines.append("## Summary\n\n")
    lines.append(f"- Total concepts: {n}\n")
    lines.append(f"- Success first try: {first_try}/{n} ({first_try * 100 // n}%)\n")
    lines.append(f"- Success after retry: {retry_success}/{n}\n")
    lines.append(f"- Total success: {success}/{n} ({success * 100 // n}%)\n")
    lines.append(f"- Failed (gave up): {fail}/{n}\n")
    lines.append(f"- Wall time: {total_time}s ({total_time / 60:.1f} min)\n\n")

    lines.append("## Per-concept results\n\n")
    lines.append("| ID | Status | Attempts | Time (s) | Error head |\n")
    lines.append("|----|--------|----------|----------|------------|\n")
    for r in results:
        err = ""
        if r["status"] != "success":
            err = (r.get("error", "") or "").splitlines()[-1][:80]
        lines.append(
            f"| {r['id']} | {r['status']} | {r['attempts']} | "
            f"{r['elapsed_s']} | {err} |\n"
        )

    lines.append("\n## Concepts\n")
    for r in results:
        lines.append(f"\n### {r['id']}\n\n")
        lines.append(f"> {r['concept']}\n\n")
        lines.append(f"Session: `videos/sessions/{r.get('session', '')}/`\n\n")
        lines.append(f"Status: **{r['status']}** (attempts: {r['attempts']}, "
                     f"{r['elapsed_s']}s)\n\n")
        if r["status"] == "success":
            lines.append(f"`{r.get('mp4', '')}`\n")
        elif r.get("error"):
            lines.append(f"```\n{r['error']}\n```\n")

    summary_path.write_text("".join(lines))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_SUMMARY_PATH
    results = run()
    write_summary(results, out)
    print(f"\n=== summary written to {out} ===", flush=True)
    sys.exit(0)
