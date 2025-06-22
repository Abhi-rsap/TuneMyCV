from openai import OpenAI
from jinja2 import Template
import json
import re
from app.configs.config import ollama_api_key, ollama_base_url

# Initialize Ollama client
client = OpenAI(
    base_url=ollama_base_url,  # OLLAMA_BASE_URL
    api_key=ollama_api_key  # OLLAMA_API_KEY
)

# Prompt template for tailoring
async def load_tailoring_prompt_template():
    return Template("""
You are an ATS optimization and resume tailoring expert.

Your task is to revise the following structured resume JSON based on the provided job description. Your goal is to maximize ATS compatibility and match quality.

### Instructions:

1. **Skills**
   - Extract all hard and soft skills required by the job description.
   - Retain only those skills from the resume that are relevant to the job.
   - Add missing but **supported** skills from the job description that the candidate’s experience justifies.
   - Use keyword phrasing as found in the job description (e.g., "Natural Language Processing" over "NLP" if the JD says so).

2. **Summary**
   - Rewrite the summary to align with the job description and the candidate's actual experience.
   - Must contain **relevant keywords** from the JD.
   - Limit to **350 characters**.
   - Avoid subjective terms like “hardworking” or “passionate”. Be concise, factual, and role-aligned.

3. **ATS Friendliness**
   - Use standard JSON only — no markdown, no formatting.
   - Avoid emojis, fancy characters, or non-standard section labels.
   - Do not modify formatting or nesting — only replace values where necessary.

🚨 Return **only the tailored resume JSON**. No explanation, comments, or extra text.

Resume JSON:
{{ resume }}

Job Description:
{{ jd }}
"""
    )

# JSON OUTPUT FROM LLM
async def extract_json_from_llm(text: str) -> dict:
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
async def generate_response(resume_dict, jd_text, model_name="mistral"):
    prompt_template = await load_tailoring_prompt_template()
    prompt = prompt_template.render(resume=json.dumps(resume_dict, indent=2), jd=jd_text)

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model_name
    )

    result = response.choices[0].message.content

    tailored_resume = await extract_json_from_llm(result)
    if not tailored_resume:
        print("❌ Failed to extract valid JSON from LLM response.")
        print(result)
        return None
    return tailored_resume