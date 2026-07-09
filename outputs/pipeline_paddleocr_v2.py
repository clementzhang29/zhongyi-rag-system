# -*- coding: utf-8 -*-
import numpy as np
np.sctypes = {"float": [np.float16, np.float32, np.float64], "int": [np.int8, np.int16, np.int32, np.int64], "uint": [np.uint8, np.uint16, np.uint32, np.uint64], "complex": [np.complex64, np.complex128]}
import imgaug
import os, sys, time, gc, json, traceback
from paddleocr import PaddleOCR
from PIL import Image
import pypdfium2 as pdfium

SRC = "C:\\Users\\Administrator\\Documents\\Codex\\2026-07-02\\harness-c-users-administrator-codex-skills\\outputs\\中医国学提取"
OUT = "C:\\Users\\Administrator\\Documents\\Codex\\2026-07-02\\harness-c-users-administrator-codex-skills\\中医RAG系统\\data\\books\\pdf_ocr"
os.makedirs(OUT, exist_ok=True)

all_pdfs = [(os.path.join(root,f), os.path.getsize(os.path.join(root,f))) for root,dirs,files in os.walk(SRC) for f in files if f.lower().endswith(".pdf")]
all_pdfs.sort(key=lambda x: x[1])
total = len(all_pdfs)
print("Total PDFs:", total, flush=True)

print("Loading PaddleOCR...", flush=True)
start = time.time()
ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False, use_gpu=False)
print("Model loaded in {:.1f}s".format(time.time()-start), flush=True)

processed = 0; errors = 0; skipped = 0
for idx, (fp, sz) in enumerate(all_pdfs):
    fname = os.path.basename(fp)
    base = fname.replace(".pdf", "")
    out_path = os.path.join(OUT, base + "_paddleocr.md")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        skipped += 1
        if skipped % 20 == 0:
            print("  [{}/{}] {} (cached)".format(idx+1, total, fname), flush=True)
        continue
    
    print("  [{}/{}] {} ({:.1f}MB)...".format(idx+1, total, fname, sz/1024/1024), end="", flush=True)
    t0 = time.time()
    
    try:
        pdf = pdfium.PdfDocument(fp)
    except Exception as pdf_e:
        print(" FAIL (PDF load error: {})".format(str(pdf_e)[:60]), flush=True)
        errors += 1
        continue
    
    pages = len(pdf)
    text_lines = ["# " + base, "源文件: " + fname, "总页数: " + str(pages)]
    any_content = False
    
    for i in range(pages):
        try:
            page = pdf[i]
            rect = page.get_bbox()
            w, h = int(rect[2]-rect[0]), int(rect[3]-rect[1])
            scale = 200.0/72.0
            if w * scale > 2000 or h * scale > 2000:
                scale = min(2000.0/w, 2000.0/h)
            bitmap = page.render(scale=scale)
            pil_img = bitmap.to_pil()
            if pil_img.width > 2000 or pil_img.height > 2000:
                ratio = min(2000.0/pil_img.width, 2000.0/pil_img.height)
                pil_img = pil_img.resize((int(pil_img.width*ratio), int(pil_img.height*ratio)), Image.LANCZOS)
            img_array = np.array(pil_img)
            del bitmap, pil_img
            gc.collect()
            
            for retry in range(2):
                try:
                    result = ocr.ocr(img_array, cls=True)
                    break
                except Exception as ocr_e:
                    if retry == 0 and "Unable to allocate" in str(ocr_e):
                        pil_small = Image.fromarray(img_array).resize((img_array.shape[1]//2, img_array.shape[0]//2), Image.LANCZOS)
                        img_array = np.array(pil_small)
                    else:
                        raise
            
            page_texts = []
            if result and result[0]:
                for ld in result[0]:
                    text, conf = ld[1]
                    page_texts.append(text)
            page_text = "".join(page_texts)
            if page_text.strip():
                text_lines.append("")
                text_lines.append("## 第{}页".format(i+1))
                text_lines.append("")
                text_lines.append(page_text)
                any_content = True
            del img_array, result
            gc.collect()
        except Exception as pe:
            text_lines.append("")
            text_lines.append("## 第{}页 (OCR失败)".format(i+1))
    
    pdf.close()
    if any_content:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(text_lines))
        elapsed = time.time() - t0
        print(" OK ({}p, {:.0f}s)".format(pages, elapsed), flush=True)
    else:
        print(" EMPTY", flush=True)
    processed += 1
    
    if processed % 3 == 0:
        chars_processed = sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if f.endswith("_paddleocr.md")) / 1024 / 1024
        print("  >> Processed: {} Errors: {} TotalChars: {:.1f}MB Progress: {}/{}".format(processed, errors, chars_processed, idx+1, total), flush=True)
    
    time.sleep(0.05)

print()
print("=== Done! Processed: {} Errors: {} Skipped: {} ===".format(processed, errors, skipped), flush=True)
