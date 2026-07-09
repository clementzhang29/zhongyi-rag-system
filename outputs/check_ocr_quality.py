import os, sys
sys.stdout.reconfigure(encoding="utf-8")

# Check PDF OCR samples
pdf_dir = r"C:\Users\Administrator\Documents\Codex\2026-07-02\harness-c-users-administrator-codex-skills\中医RAG系统\data\books\pdf_ocr"
files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.txt') and 'OCR' in open(os.path.join(pdf_dir,f),'r',encoding='utf-8',errors='ignore').read()[:200]])

print(f"含有OCR标记的文件数: {len(files)}")
print()

for fname in files[:5]:
    fpath = os.path.join(pdf_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Find OCR pages
    ocr_lines = [(i, l.strip()[:120]) for i, l in enumerate(lines) if '(OCR)' in l]
    
    # Get first few OCR text lines
    txt_content = []
    for i, l in enumerate(lines):
        if i > 0:
            txt_content.append(l)
    
    content = ''.join(txt_content[:200])  # First 200 lines
    
    print(f"=== {fname} ===")
    print(f"  总行数: {len(lines)}, OCR页: {len(ocr_lines)}")
    
    # Find first OCR page content
    first_ocr_idx = None
    for i, l in enumerate(lines):
        if '(OCR)' in l:
            first_ocr_idx = i
            break
    
    if first_ocr_idx:
        # Print the OCR text block (next ~10 lines)
        ocr_text = ''.join(lines[first_ocr_idx:first_ocr_idx+15])
        print(f"  OCR样本:")
        # Remove page headers
        import re
        sample = ocr_text[:500]
        sample = re.sub(r'##.*?\n', '', sample)
        print(f"  {sample[:400]}")
    
    print()
