import uvicorn
from fastapi import FastAPI
import app.configs.config as config
from app.controllers import document_parser_controller


app = FastAPI(title=config.project_name)
app.include_router(document_parser_controller.router)


if __name__ == "__main__":
    uvicorn.run(app)