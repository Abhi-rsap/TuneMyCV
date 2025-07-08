from ollama import chat
from app.models.Resume import Resume
from pydantic import ValidationError
import json
from app.prompt_templates.extract_keyword_prompts import KEYWORDS_EXTRACTION_SYSTEM_PROMPT, KEYWORDS_EXTRACTION_USER_PROMPT
from app.prompt_templates.tailor_resume_prompts import TAILOR_RESUME_SYSTEM_PROMPT, TAILOR_RESUME_USER_PROMPT
    
# --- STEP 1: Extract skills from JD --- #
async def extract_keywords_from_jd(jd_text: str, model_name="llama3") -> str:
    system_prompt = KEYWORDS_EXTRACTION_SYSTEM_PROMPT

    user_prompt = KEYWORDS_EXTRACTION_USER_PROMPT.format(jd_text=jd_text)

    response = chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    raw_skills = response.message.content.strip()
    # clean_skills = re.sub(r"[^\w\s,+\-#./]", "", raw_skills)
    return raw_skills

# --- STEP 2: Generate summary from skills and experience --- #
async def tailor_resume_from_jd(skills: str, job_description: str, resume_content_json, model_name="llama3") -> str:

    system_prompt = TAILOR_RESUME_SYSTEM_PROMPT

    user_prompt = TAILOR_RESUME_USER_PROMPT.format(
        job_description=job_description,
        skills=skills,
        resume_content_json=json.dumps(resume_content_json)
    )

    response = chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        format=Resume.model_json_schema()
    )

    response_text = response.message.content.strip()
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}") from e
    except ValidationError as e:
        raise ValueError(f"LLM response did not match expected structure: {str(e)}") from e