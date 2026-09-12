from pathlib import Path
from pypdf import PdfReader

PDF=Path("data/Smart_Farming_Agriculture_Knowledge_Base.pdf")
OUT=Path("knowledge_base/source_extracted.md")

def main():
    if not PDF.exists():
        raise SystemExit(f"Missing {PDF}")
    reader=PdfReader(str(PDF))
    text="\n".join(page.extract_text() or "" for page in reader.pages)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("# Source Agricultural Knowledge\n\n"+text,encoding="utf-8")
    print(f"Extracted {len(reader.pages)} PDF pages to {OUT}")

if __name__=="__main__":
    main()
