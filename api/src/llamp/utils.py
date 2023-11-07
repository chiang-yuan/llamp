'''
import os

import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
MP_API_KEY = os.getenv("MP_API_KEY", None)

openai.api_key = OPENAI_API_KEY
'''
