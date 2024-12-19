import openai
from typing import List

class AISummarizer:
    def __init__(self, api_key, model_name='gpt-3.5-turbo'):
        self.api_key = api_key
        openai.api_key = api_key
        self.model_name = model_name
        
    def summarize_chunk(self, text: str) -> str:
        """使用 AI 总结单个文本块"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': '你是一个专业的内容总结助手。请简明扼要地总结以下内容的要点:'},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f'Error summarizing text: {e}')
            return None
            
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
            final_text = '\n\n'.join(summaries)
            return self.summarize_chunk(final_text)
            
        return summaries[0]
