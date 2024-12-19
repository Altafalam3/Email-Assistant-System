import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API key for GROQ Llama
LLM_API_KEY = os.getenv("GROQ_API_KEY")

# Llama 3.1 configuration
config_list = [{"model": "llama-3.1-70b-versatile", "api_type": "groq", "api_key": LLM_API_KEY}]
llama_config = {"config_list": config_list, "temperature": 0.4}
