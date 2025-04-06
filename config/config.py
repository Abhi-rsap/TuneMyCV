import os

project_name = os.getenv("PROJECT_NAME", "TuneMyCV")
server_name = os.getenv("SERVER_NAME", "TuneMyCV-dev")
server_connection = os.getenv("SERVER_CONNECTION", "localhost")
server_port = int(os.getenv("SERVER_PORT", 8000))
