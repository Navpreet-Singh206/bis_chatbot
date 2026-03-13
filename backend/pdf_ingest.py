import json
from pypdf import PdfReader
import os

PDF_PATH = '../bis-presents-the-open-standard-summit-brochure.pdf'
PAGES_PATH = 'backend/data/bis_pages.json'

pdf_text = ''

with open(PDF_PATH, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        pdf_text += page.extract_text() + '\\n\\n'

# Clean and chunk large text
chunks = []
for i in range(0, len(pdf_text), 2000):
    chunk = pdf_text[i:i+2000].strip()
    if len(chunk) > 100:
        chunks.append(chunk)

pages = []
for chunk in chunks:
    pages.append({
        "title": "Hackathon Problem Statement & BIS Standards Activity",
        "content": chunk,
        "source": "bis-presents-the-open-standard-summit-brochure.pdf"
    })

# Load existing
with open(PAGES_PATH, 'r', encoding='utf-8') as f:
    existing = json.load(f)

print(f"Existing pages: {len(existing)}")
existing.extend(pages)
print(f"Total pages after PDF: {len(existing)}")

# Save
with open(PAGES_PATH, 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print("✅ PDF ingested to bis_pages.json")
print(f"Added {len(pages)} PDF chunks")

