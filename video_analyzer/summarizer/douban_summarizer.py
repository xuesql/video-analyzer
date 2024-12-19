import requests
from typing import List
from urllib.parse import urljoin

class DoubanSummarizer:
    def __init__(self, api_key: str, model: str = 'dbqa'):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.doubao.com/v1/chat/completions"  # 请替换为实际的豆包 API 地址
        
    def _make_request(self, messages: List[dict]) -> str:
        """发送请求到豆包 API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            print(f"Error calling Douban API: {e}")
            return None
    
    def summarize_chunk(self, text: str) -> str:
        """使用豆包 AI 总结单个文本块"""
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的内容总结助手。请简明扼要地总结以下内容的要点:"
            },
            {
                "role": "user",
                "content": text
            }
        ]
        
        return self._make_request(messages)
    
    def summarize_all(self, chunks: List[str]) -> str:
        """总结所有文本块并合并结果"""
        summaries = []
        for chunk in chunks:
            summary = self.summarize_chunk(chunk)
            if summary:
                summaries.append(summary)
        
        if not summaries:
            return None
        
        # 如果有多个总结，再次总结
        if len(summaries) > 1:
            final_text = "\n\n".join(summaries)
            return self.summarize_chunk(final_text)
        
        return summaries[0]