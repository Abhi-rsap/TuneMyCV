
import os
import json
from fitz import open as open_pdf  # PyMuPDF
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from jsonschema import validate, ValidationError

# 1. Ensure your OpenAI key is set in the environment:
#    export OPENAI_API_KEY="your_key_here"
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

# 2. Load the INPUT_SCHEMA
INPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Master Resume Schema",
    "type": "object",
    "properties": {
        "header": {
            "type": "object",
            "properties": {
                "name":     {"type": "string"},
                "email":    {"type": "string", "format": "email"},
                "phone":    {"type": "string"},
                "linkedin": {"type": "string", "format": "uri"},
                "github":   {"type": "string", "format": "uri"}
            },
            "required": ["name", "email", "phone"]
        },
        "summary": {"type": "string"},
        "skills": {
            "type": "object",
            "properties": {
                "languages":     {"type": "array", "items": {"type": "string"}},
                "ml_frameworks": {"type": "array", "items": {"type": "string"}},
                "genai":         {"type": "array", "items": {"type": "string"}},
                "infra":         {"type": "array", "items": {"type": "string"}}
            },
            "required": ["languages", "ml_frameworks"]
        },
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title":      {"type": "string"},
                    "company":    {"type": "string"},
                    "location":   {"type": "string"},
                    "start_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}$"},
                    "end_date":   {"type": "string", "pattern": "^(\\d{4}-\\d{2}|Present)$"},
                    "bullets":    {"type": "array", "items": {"type": "string"}}
                },
                "required": ["title", "company", "start_date", "end_date", "bullets"]
            }
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "degree":     {"type": "string"},
                    "school":     {"type": "string"},
                    "start_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}$"},
                    "end_date":   {"type": "string", "pattern": "^\\d{4}-\\d{2}$"}
                },
                "required": ["degree", "school", "start_date", "end_date"]
            }
        },
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name":    {"type": "string"},
                    "details": {"type": "string"}
                },
                "required": ["name", "details"]
            }
        },
        "publications": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "link":  {"type": "string", "format": "uri"}
                },
                "required": ["title"]
            }
        }
    },
    "required": ["header", "summary", "skills", "experience", "education"]
}

# 3. System prompt for parsing
SYSTEM_PROMPT = """You are a resume parser. 
Given a block of raw resume text, extract and return a JSON object
strictly conforming to the provided INPUT_SCHEMA. 
Do not invent any information. Output only valid JSON."""

# 4. Function to extract raw text from the PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = open_pdf(pdf_path)
    pages = [page.get_text() for page in doc]
    return "\n\n".join(pages)

# 5. Main parsing function
def parse_pdf_to_json(pdf_path: str, output_json_path: str):
    # Extract text
    raw_text = extract_text_from_pdf(pdf_path)

    # Prepare LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Build messages
    system_msg = SystemMessage(content=SYSTEM_PROMPT)
    human_msg = HumanMessage(content=f"INPUT_SCHEMA:\n{json.dumps(INPUT_SCHEMA)}\n\nRAW_TEXT:\n'''\n{raw_text}\n'''")

    # Call LLM
    response = llm([system_msg, human_msg])
    result_text = response.content

    # Parse JSON
    master_json = json.loads(result_text)

    # Validate
    try:
        validate(instance=master_json, schema=INPUT_SCHEMA)
        print("✅ Master resume JSON is valid.")
    except ValidationError as ve:
        print("❌ Validation error:", ve)
        # Optionally: raise or save for inspection
        raise

    # Save
    with open(output_json_path, "w") as f:
        json.dump(master_json, f, indent=2)
    print(f"Master resume saved to {output_json_path}")

# 6. CLI interface
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse PDF resume into master JSON.")
    parser.add_argument("--pdf", required=True, help="Path to the input resume PDF")
    parser.add_argument("--out", default="master_resume.json", help="Path to output JSON file")
    args = parser.parse_args()

    parse_pdf_to_json(args.pdf, args.out)

# Usage:
#   pip install PyMuPDF langchain openai jsonschema
#   python parse_master_resume.py --pdf Resume_Abhi.pdf --out master_resume.json
