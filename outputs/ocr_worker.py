# -*- coding: utf-8 -*-
import numpy as np
np.sctypes = {"float": [np.float16, np.float32, np.float64], "int": [np.int8, np.int16, np.int32, np.int64], "uint": [np.uint8, np.uint16, np.uint32, np.uint64], "complex": [np.complex64, np.complex128]}
import imgaug
import os, sys, gc, time
from paddleocr import PaddleOCR
from PIL import Image
import pypdfium2 as pdfium

fp, out_dir = sys.argv[1], sys.argv[2]
fname = os.path.basename(fp)
base = fname.replace(".pdf","")
out_p = os.path.join(out_dir, base+"_paddleocr.md")
if os.path.exists(out_p) and os.path.getsize(out_p) > 50:
    sys.exit(0)

try:
    pdf = pdfium.PdfDocument(fp)
except:
    print("CORRUPT", flush=True)
    sys.exit(2)

pages = len(pdf)
ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False, use_gpu=False)
lines = ["# "+base, "源文件: "+fname, "总页数: "+str(pages)]
ok = False

for i in range(pages):
    try:
        page = pdf[i]; rect = page.get_bbox()
        w, h = int(rect[2]-rect[0]), int(rect[3]-rect[1])
        scale = min(200/72, 2000/max(w,1), 2000/max(h,1))
        pil = page.render(scale=scale).to_pil()
        if pil.width > 2000 or pil.height > 2000:
            r = min(2000/pil.width, 2000/pil.height, 1.0)
            if r < 1: pil = pil.resize((int(pil.width*r), int(pil.height*r)), Image.LANCZOS)
        img = np.array(pil); del pil; gc.collect()
        result = ocr.ocr(img, cls=True)
        text = "".join([ld[1][0] for ld in (result[0] if result and result[0] else [])])
        del img, result; gc.collect()
        if text.strip():
            lines.extend(["", "## 第"+str(i+1)+"页", "", text])
            ok = True
    except:
        pass

pdf.close()
if ok:
    with open(out_p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("OK", flush=True)
    sys.exit(0)
else:
    print("EMPTY", flush=True)
    sys.exit(3)
