import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
MP_API_KEY = os.getenv("MP_API_KEY", None)
