import os

project_name = os.getenv("PROJECT_NAME", "TuneMyCV")
server_name = os.getenv("SERVER_NAME", "TuneMyCV-dev")
server_connection = os.getenv("SERVER_CONNECTION", "localhost")
server_port = int(os.getenv("SERVER_PORT", 8000))
timezone = os.getenv("TIMEZONE", "UTC")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
ollama_api_key = os.getenv("OLLAMA_API_KEY", "ollama")
default_base_tex_path = os.getenv("DEFAULT_BASE_TEX_PATH", "app/tex_templates")
