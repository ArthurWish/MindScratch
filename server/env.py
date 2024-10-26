import os

MODEL = "gpt-4-0613"

def init_env():
    
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

    # back up api key
    os.environ["OPENAI_API_KEY"] = "your_api_key"
    os.environ["SERPAPI_API_KEY"] = "your_api_key"

