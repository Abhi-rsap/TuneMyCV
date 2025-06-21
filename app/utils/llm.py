from openai import OpenAI
from jinja2 import Template
import json
import re
from app.utils.parse_resume import parse_resume
from pydantic import ValidationError
from pydantic import BaseModel
from typing import Optional
from app.configs import timezone, OLLAMA_API_KEY, OLLAMA_BASE_URL

# Initialize Ollama client
client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OLLAMA_API_KEY,
)

# Prompt template for tailoring
def load_prompt_template():
    return Template(
        """You are a resume tailoring assistant.

Given the following:
1. A structured resume (JSON)
2. A job description

Suggest tailored improvements to the resume to make it a better match for the job. Be specific: rewrite bullet points, reword the summary, suggest new skill keywords, and remove unrelated content if necessary.

🚨 Return ONLY the tailored resume in valid JSON format. Do NOT include markdown, explanation, or comments.

Resume JSON:
{{ resume }}

Job Description:
{{ jd }}"""
    )

# JSON OUTPUT FROM LLM
def extract_json_from_llm(text: str) -> dict:
    try:
        # Remove markdown ```json``` if present
        text = re.sub(r"```(json)?", "", text).strip()

        # Try plain JSON parsing
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find first valid {...} block
        brace_count = 0
        start = None
        for i, c in enumerate(text):
            if c == '{':
                if brace_count == 0:
                    start = i
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0 and start is not None:
                    json_str = text[start:i + 1]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        continue
    return None

# Generate tailored resume using llama
def generate_response(resume_dict, jd_text, model_name="mistral"):
    prompt_template = load_prompt_template()
    prompt = prompt_template.render(resume=json.dumps(resume_dict, indent=2), jd=jd_text)

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model_name
    )

    result = response.choices[0].message.content

    tailored_resume = extract_json_from_llm(result)
    if not tailored_resume:
        print("❌ Failed to extract valid JSON from LLM response.")
        print(result)
        return None
    return tailored_resume

# Load sample job description
jd_text = open("app/etl/sample_jd.txt", "r").read()

# Get tailored response from LLM
llm_response = generate_response(resume_json, jd_text)

if llm_response:
    try:
        # Validate with Pydantic
        resume_obj = Resume(**llm_response)
        tailored_resume = resume_obj.model_dump()
        #Save
        with open("app/etl/tailored_resume.json", "w") as f:
            json.dump(tailored_resume, f, indent=2)
    except ValidationError as e:
        print("❌ LLM response did not match the expected structure.")
        print(e)
else:
    print("❌ Resume tailoring failed.")
