import os
from dotenv import load_dotenv

load_dotenv()

DOUBAN_API_KEY = os.getenv('DOUBAN_API_KEY')
DOUBAN_MODEL = 'dbqa'  # 可以根据实际需要选择不同的豆包模型
CHUNK_SIZE = 2000
LANGUAGE = 'zh'
