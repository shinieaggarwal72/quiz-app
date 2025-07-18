import pdfplumber, re, json

PDF_PATH = '/home/shinie/Downloads/rsaggarwal.pdf'
OUT_JSON = 'questions.json'

def extract_text_by_column(pdf_path, start_page=1, end_page=None):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages[start_page-1 : end_page]
        for p in pages:
            w, h = p.width, p.height
            left  = p.crop((0,   0,   w/2, h))
            right = p.crop((w/2, 0,   w,   h))
            text += left.extract_text()  + "\n"
            text += right.extract_text() + "\n\n"
    return text

def parse_mcqs(text):
    blocks = re.split(r'(?=\n\s*\d+\.)', "\n"+text)
    mcqs = []

    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines or not re.match(r'^\d+\.', lines[0]):
            continue

        
        flat = " ".join(lines)

        
        qm = re.match(r'^\d+\.\s*(.*?)\s*(?:\(\s*a\s*\))', flat, re.IGNORECASE)
        if not qm:
            continue
        question = qm.group(1).strip()

        
        opts = re.findall(
            r'[\(\[]\s*([A-Da-d])\s*[\)\]]\s*([^(\)\[\]]+)', 
            flat
        )
        if len(opts) != 4:
            continue

        
        opts_sorted = sorted(opts, key=lambda x: x[0].lower())
        texts = [txt.strip() for (_, txt) in opts_sorted]

        mcqs.append({
            "question": question,
            "options": texts,
            "answer": None
        })

    return mcqs

if __name__ == "__main__":
    raw = extract_text_by_column(PDF_PATH, start_page=25, end_page=30)
    mcqs = parse_mcqs(raw)
    print(f"Extracted {len(mcqs)} MCQs from pages 2–3")
    with open(OUT_JSON, "w") as f:
        json.dump(mcqs, f, indent=2)
