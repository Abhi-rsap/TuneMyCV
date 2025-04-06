import uvicorn
from fastapi import FastAPI
import config.config as config

app = FastAPI(title=config.project_name)

if __name__ == "__main__":
    uvicorn.run(app)