#!/usr/bin/env python3
"""Renderiza todos los .sch de galeria/sch/ a PNG y emite un reporte pass/fail.

Uso:
    python render.py            # render paralelo de todo + RENDER_REPORT.md
    python render.py --dpi 100  # cambia resolución de las miniaturas
    python render.py --jobs 6   # nivel de paralelismo

Verifica además que el fork reproduce cada ejemplo de lcapy (los que fallan
quedan listados en el reporte, no se ocultan). Regenera las miniaturas .png.
"""
import os, sys, subprocess, json, argparse, concurrent.futures as cf
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SCH = os.path.join(HERE, "sch")
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
N2T = os.path.join(REPO, ".venv", "bin", "n2t")


def render_one(args):
    path, dpi, timeout = args
    png = path[:-4] + ".png"
    try:
        r = subprocess.run([N2T, "render", path, "-o", png, "--dpi", str(dpi)],
                           capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0 and os.path.exists(png):
            return (path, "ok", os.path.getsize(png), "")
        tail = (r.stderr or r.stdout or "").strip().splitlines()
        reason = tail[-1][:160] if tail else f"exit {r.returncode}"
        return (path, "fail", 0, reason)
    except subprocess.TimeoutExpired:
        return (path, "timeout", 0, f">{timeout}s")
    except Exception as e:  # noqa
        return (path, "error", 0, str(e)[:160])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=100)
    ap.add_argument("--jobs", type=int, default=min(8, (os.cpu_count() or 4)))
    ap.add_argument("--timeout", type=int, default=90)
    args = ap.parse_args()

    files = []
    for root, _, fs in os.walk(SCH):
        for f in sorted(fs):
            if f.endswith(".sch"):
                files.append(os.path.join(root, f))
    files.sort()
    print(f"Renderizando {len(files)} .sch  (dpi={args.dpi}, jobs={args.jobs})", flush=True)

    results = []
    with cf.ProcessPoolExecutor(max_workers=args.jobs) as ex:
        for i, res in enumerate(ex.map(render_one,
                                       [(p, args.dpi, args.timeout) for p in files]), 1):
            results.append(res)
            if i % 25 == 0 or i == len(files):
                done = Counter(r[1] for r in results)
                print(f"  {i}/{len(files)}  ok={done['ok']} fail={done['fail']} "
                      f"timeout={done['timeout']} error={done['error']}", flush=True)

    status = Counter(r[1] for r in results)
    total_png = sum(r[2] for r in results)
    fails = [r for r in results if r[1] != "ok"]

    # Reporte markdown
    lines = ["# Reporte de render — galería netlist2tikz", ""]
    lines.append(f"- Total: **{len(results)}** · ✅ ok **{status['ok']}** · "
                 f"❌ fail **{status['fail']}** · ⏱ timeout **{status['timeout']}** · "
                 f"⚠ error **{status['error']}**")
    lines.append(f"- Peso total de miniaturas PNG: **{total_png/1e6:.1f} MB** (dpi {args.dpi})")
    lines.append("")
    if fails:
        lines.append("## No reproducidos (revisar / marcar ⚠️ en el índice)")
        lines.append("")
        lines.append("| archivo | estado | motivo |")
        lines.append("|---|---|---|")
        for p, st, _, reason in sorted(fails):
            rel = os.path.relpath(p, HERE)
            lines.append(f"| `{rel}` | {st} | {reason.replace('|','/')} |")
        lines.append("")
    open(os.path.join(HERE, "RENDER_REPORT.md"), "w").write("\n".join(lines))

    # Guardar status por archivo (para construir índices con marca de soporte)
    rstat = {os.path.relpath(p, HERE): st for p, st, _, _ in results}
    json.dump(rstat, open(os.path.join(HERE, "render_status.json"), "w"), indent=1)

    print(f"\nLISTO. ok={status['ok']}/{len(results)}  "
          f"PNG={total_png/1e6:.1f}MB  → RENDER_REPORT.md")


if __name__ == "__main__":
    main()
