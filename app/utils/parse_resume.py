from unstructured.partition.pdf import partition_pdf
import re
import logging

SECTION_HEADERS = [
    "education", 
    "experience", 
    "skills", 
    "projects"
]

def segment_text(elements):
    """
    Segments parsed elements into sections based on SECTION_HEADERS.
    Returns structured dictionary.
    """
    sections = {}
    current_section = "header"
    sections[current_section] = ""

    for el in elements:
        if not el.text:
            continue
        
        text = el.text.strip()
        text_lower = text.lower()

        matched = False
        for header in SECTION_HEADERS:
            pattern = rf"^{header}\b"
            if re.match(pattern, text_lower):
                current_section = header
                sections[current_section] = ""
                matched = True
                break
        
        if not matched:
            sections[current_section] += text + "\n"
    header_lines = sections["header"].strip().split("\n")
    sections["header"] = "\n".join(header_lines[:2]).strip()
    summary_line = " ".join(header_lines[2:]).strip() if header_lines else ""
    sections["summary"] = summary_line
    return sections

def parse_resume(pdf_data):
    """
    Main function — parses PDF resume and writes structured JSON.
    """
    logging.info(f"Parsing resume...")

    # Step 1: Parse with unstructured.io
    elements = partition_pdf(file=pdf_data)
    logging.info(f"Extracted {len(elements)} elements from PDF")

    # Step 2: Segment text
    sections = segment_text(elements)
    print(f"Segmented into {len(sections)} sections")

    logging.info(f"Parsed sections: {sections.keys()}")

    # Step 3: Write to JSON
    # with open(output_path, "w", encoding="utf-8") as f:
    #     json.dump(sections, f, indent=4, ensure_ascii=False)

    # print(f"Resume parsed and saved to: {output_path}")

    return sections

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser(description="Parse Resume PDF to structured JSON.")
#     parser.add_argument("--pdf_path", type=str, required=True, help="Path to Resume PDF")
#     parser.add_argument("--output_path", type=str, required=True, help="Path to output JSON")

#     args = parser.parse_args()

#     parse_resume(args.pdf_path, args.output_path)
