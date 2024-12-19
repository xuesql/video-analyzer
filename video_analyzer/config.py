import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = 'gpt-3.5-turbo'
CHUNK_SIZE = 2000  # 文本分块大小
LANGUAGE = 'zh'  # 默认语言
