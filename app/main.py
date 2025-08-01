import uvicorn
from fastapi import FastAPI
import app.configs.config as config
from app.controllers import document_parser_controller, resume_tailor_controller, keyword_extractor_controller
from app.configs.logging_config import setup_logging


setup_logging()

app = FastAPI(title=config.project_name)
@app.get("/")
def root():
    return {"message": f"{config.project_name} API is running."}
app.include_router(document_parser_controller.router)
app.include_router(resume_tailor_controller.router)
app.include_router(keyword_extractor_controller.router)


if __name__ == "__main__":
    
    uvicorn.run(app)