# -*- coding: utf-8 -*-
import numpy as np
np.sctypes = {"float": [np.float16, np.float32, np.float64], "int": [np.int8, np.int16, np.int32, np.int64], "uint": [np.uint8, np.uint16, np.uint32, np.uint64], "complex": [np.complex64, np.complex128]}
import imgaug
import os, sys, time, gc, json
from paddleocr import PaddleOCR
from PIL import Image
import pypdfium2 as pdfium

SRC = "C:\\Users\\Administrator\\Documents\\Codex\\2026-07-02\\harness-c-users-administrator-codex-skills\\outputs\\中医国学提取"
OUT = "C:\\Users\\Administrator\\Documents\\Codex\\2026-07-02\\harness-c-users-administrator-codex-skills\\中医RAG系统\\data\\books\\pdf_ocr"
LOG = os.path.join(os.path.dirname(OUT), "ocr_progress.json")
os.makedirs(OUT, exist_ok=True)

done_set = set()
if os.path.exists(LOG):
    try:
        with open(LOG) as f: done_set = set(json.load(f))
    except: pass

all_pdfs = []
for root, dirs, files in os.walk(SRC):
    for f in files:
        if f.lower().endswith(".pdf"):
            all_pdfs.append((os.path.join(root,f), os.path.getsize(os.path.join(root,f))))
all_pdfs.sort(key=lambda x: x[1])
total = len(all_pdfs)

available = [(fp,sz) for fp,sz in all_pdfs if os.path.basename(fp) not in done_set and not os.path.exists(os.path.join(OUT, os.path.basename(fp).replace(".pdf","")+"_paddleocr.md"))]
print("Total:", total, "Available to process:", len(available), flush=True)
if len(available) == 0:
    print("All done!", flush=True)
    sys.exit(0)

print("Loading PaddleOCR...", flush=True)
start = time.time()
ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False, use_gpu=False)
print("Model loaded in {:.1f}s".format(time.time()-start), flush=True)

processed = 0; errors = 0
for idx, (fp, sz) in enumerate(available):
    fname = os.path.basename(fp)
    base = fname.replace(".pdf","")
    out_path = os.path.join(OUT, base+"_paddleocr.md")
    
    print(f"  [{idx+1}/{len(available)}] {fname} ({sz/1024/1024:.1f}MB)...", end="", flush=True)
    t0 = time.time()
    
    # Try PDF load
    try:
        pdf = pdfium.PdfDocument(fp)
    except:
        print(" FAIL (corrupt PDF)", flush=True)
        errors += 1
        done_set.add(fname)
        continue
    
    pages = len(pdf)
    text_lines = [f"# {base}", f"源文件: {fname}", f"总页数: {pages}"]
    any_content = False
    
    for i in range(pages):
        try:
            page = pdf[i]
            rect = page.get_bbox()
            w, h = int(rect[2]-rect[0]), int(rect[3]-rect[1])
            scale = min(200.0/72.0, 2000.0/w if w>0 else 200, 2000.0/h if h>0 else 200)
            bitmap = page.render(scale=scale)
            pil_img = bitmap.to_pil()
            ratio = min(2000.0/pil_img.width, 2000.0/pil_img.height, 1.0)
            if ratio < 1.0:
                pil_img = pil_img.resize((int(pil_img.width*ratio), int(pil_img.height*ratio)), Image.LANCZOS)
            img_array = np.array(pil_img)
            del bitmap, pil_img; gc.collect()
            
            for retry in range(2):
                try:
                    result = ocr.ocr(img_array, cls=True)
                    break
                except:
                    if retry == 0:
                        pil_small = Image.fromarray(img_array).resize((img_array.shape[1]//2, img_array.shape[0]//2), Image.LANCZOS)
                        img_array = np.array(pil_small)
                    else:
                        raise
            
            page_text = "".join([ld[1][0] for ld in (result[0] if result and result[0] else [])])
            if page_text.strip():
                text_lines.extend(["", f"## 第{i+1}页", "", page_text])
                any_content = True
            del img_array, result; gc.collect()
        except:
            pass
    
    pdf.close()
    
    if any_content:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(text_lines))
        print(f" OK ({pages}p, {time.time()-t0:.0f}s)", flush=True)
    else:
        print(" EMPTY", flush=True)
    
    processed += 1
    done_set.add(fname)
    with open(LOG, "w") as f: json.dump(list(done_set), f, ensure_ascii=False)
    
    if processed % 3 == 0:
        total_chars = sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if f.endswith("_paddleocr.md"))/1024/1024
        print(f"  >> Done:{processed} Err:{errors} Total:{total_chars:.0f}MB", flush=True)

print(f"\n=== Done! Processed:{processed} Errors:{errors} ===", flush=True)
