import numpy as np
np.sctypes = {'float': [np.float16, np.float32, np.float64], 'int': [np.int8, np.int16, np.int32, np.int64], 'uint': [np.uint8, np.uint16, np.uint32, np.uint64], 'complex': [np.complex64, np.complex128]}
import imgaug

import os, sys, time, json
from paddleocr import PaddleOCR
import pypdfium2 as pdfium

SRC = r'C:\Users\Administrator\Documents\Codex\2026-07-02\harness-c-users-administrator-codex-skills\outputs\中医国学提取'
OUT = r'C:\Users\Administrator\Documents\Codex\2026-07-02\harness-c-users-administrator-codex-skills\中医RAG系统\data\books\pdf_ocr'
os.makedirs(OUT, exist_ok=True)

# Collect all PDFs sorted by size
all_pdfs = []
for root, dirs, files in os.walk(SRC):
    for f in files:
        if f.lower().endswith('.pdf'):
            fp = os.path.join(root, f)
            all_pdfs.append((fp, os.path.getsize(fp)))
all_pdfs.sort(key=lambda x: x[1])
total = len(all_pdfs)
print(f'Total PDFs: {total}')

# Init PaddleOCR once
print('Loading PaddleOCR...')
start = time.time()
ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False, use_gpu=False)
print(f'Model loaded in {time.time()-start:.1f}s')

# Process PDFs
processed = 0
errors = 0
for idx, (fp, sz) in enumerate(all_pdfs):
    fname = os.path.basename(fp)
    base = fname.replace('.pdf', '')
    out_path = os.path.join(OUT, f'{base}_paddleocr.md')
    if os.path.exists(out_path):
        if (idx+1) % 20 == 0:
            print(f'  [{idx+1}/{total}] {fname} (cached)')
        continue
    
    sz_mb = sz / 1024 / 1024
    print(f'  [{idx+1}/{total}] {fname} ({sz_mb:.1f}MB)...', end=' ', flush=True)
    t0 = time.time()
    
    try:
        pdf = pdfium.PdfDocument(fp)
        pages = len(pdf)
        lines = [f'# {base}\n', f'源文件: {fname}\n', f'总页数: {pages}\n']
        
        for i in range(pages):
            page = pdf[i]
            bitmap = page.render(scale=2)
            pil_img = bitmap.to_pil()
            img_array = np.array(pil_img)
            
            result = ocr.ocr(img_array, cls=True)
            page_texts = []
            if result and result[0]:
                for line_data in result[0]:
                    text, conf = line_data[1]
                    page_texts.append(text)
            
            page_text = ''.join(page_texts)
            if page_text.strip():
                lines.append(f'\n## 第{i+1}页\n\n{page_text}\n')
        
        pdf.close()
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(''.join(lines))
        
        elapsed = time.time() - t0
        print(f'OK ({pages}页, {elapsed:.0f}s)')
        processed += 1
        
        if processed % 5 == 0:
            print(f'  >> 已处理: {processed}, 错误: {errors}, 进度: {idx+1}/{total}')
    
    except Exception as e:
        elapsed = time.time() - t0
        print(f'FAIL ({elapsed:.0f}s): {str(e)[:80]}')
        errors += 1
    
    time.sleep(0.3)

print(f'\n=== 完成! 处理: {processed}, 错误: {errors} ===')
