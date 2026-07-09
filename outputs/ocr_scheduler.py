# -*- coding: utf-8 -*-
import os, sys, time, gc
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
SCR_DIR = str(BASE / "data" / "books")
OUT_DIR = str(BASE / "data" / "books" / "pdf_ocr")
os.makedirs(OUT_DIR, exist_ok=True)
done = set()
for f in os.listdir(OUT_DIR):
    if not f.endswith("_paddleocr.md"): continue
    done.add(f[:-len("_paddleocr.md")])
pdfs = [(f, os.path.getsize(os.path.join(SCR_DIR, f)))
        for f in os.listdir(SCR_DIR) if f.lower().endswith(".pdf")
        and f[:-4] not in done]
pdfs.sort(key=lambda x: x[1])
total = len(pdfs)
print(f"ready: {total} pdfs", flush=True)
if total == 0: sys.exit()
import numpy as np
if not hasattr(np, "sctypes"):
    np.sctypes = {"float": [np.float16, np.float32, np.float64],
                   "int": [np.int8, np.int16, np.int32, np.int64],
                   "uint": [np.uint8, np.uint16, np.uint32, np.uint64],
                   "complex": [np.complex64, np.complex128]}
import imgaug
import pypdfium2 as pdfium
from paddleocr import PaddleOCR
from PIL import Image
print("loading PaddleOCR...", flush=True)
ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False, use_gpu=False)
proc, errs = 0, 0
for idx, (fn, sz) in enumerate(pdfs):
    fp = os.path.join(SCR_DIR, fn)
    base = fn.replace(".pdf", "").replace(".PDF", "")
    out_p = os.path.join(OUT_DIR, base + "_paddleocr.md")
    if os.path.exists(out_p) and os.path.getsize(out_p) > 50: continue
    print(f"[{idx+1}/{total}] {fn}", end=" ", flush=True)
    t0 = time.time()
    try: pdf = pdfium.PdfDocument(fp)
    except Exception as e: print(f"CORRUPT ({e})", flush=True); errs += 1; continue
    pages = len(pdf)
    lines = ["# " + base, "source: " + fn, "pages: " + str(pages)]
    ok = False
    for i in range(pages):
        try:
            pg = pdf[i]; rect = pg.get_bbox()
            w, h = int(rect[2]-rect[0]), int(rect[3]-rect[1])
            sc = min(200/72, 2000/max(w,1), 2000/max(h,1))
            pil = pg.render(scale=sc).to_pil()
            if pil.width > 2000 or pil.height > 2000:
                r = min(2000/pil.width, 2000/pil.height, 1.0)
                if r < 1: pil = pil.resize((int(pil.width*r), int(pil.height*r)), Image.Resampling.LANCZOS)
            img = np.array(pil); del pil; gc.collect()
            res = ocr.ocr(img, cls=True)
            txt = "".join([ld[1][0] for ld in (res[0] if res and res[0] else [])])
            del img, res; gc.collect()
            if txt.strip(): lines.extend(["", "## page " + str(i+1), "", txt]); ok = True
        except Exception: pass
    pdf.close()
    if ok:
        with open(out_p, "w", encoding="utf-8") as f: f.write("\n".join(lines))
        print(f"OK ({time.time()-t0:.0f}s)", flush=True); proc += 1
    else:
        print(f"EMPTY ({time.time()-t0:.0f}s)", flush=True); proc += 1
    if (proc+errs) % 3 == 0:
        dn = len([f for f in os.listdir(OUT_DIR) if f.endswith("_paddleocr.md")])
        print(f"  total: {dn} errs: {errs}", flush=True)
print(f"\nDone! OK:{proc} Err:{errs}", flush=True)
