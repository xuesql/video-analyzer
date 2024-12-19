import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from .config import DOUBAN_API_KEY, DOUBAN_MODEL, CHUNK_SIZE
from .extractors.video_extractor import VideoExtractor
from .processors.speech_to_text import SpeechToText
from .processors.text_processor import TextProcessor
from .summarizer.douban_summarizer import DoubanSummarizer

class VideoAnalyzer:
    def __init__(self):
        self.video_extractor = None
        self.speech_to_text = SpeechToText()
        self.text_processor = TextProcessor(chunk_size=CHUNK_SIZE)
        self.summarizer = DoubanSummarizer(DOUBAN_API_KEY, DOUBAN_MODEL)
        
    def analyze_video(self, video_path: str) -> dict:
        """分析视频并返回总结结果"""
        # 检查文件是否存在
        if not os.path.exists(video_path):
            raise FileNotFoundError(f'Video file not found: {video_path}')
            
        # 初始化视频提取器
        self.video_extractor = VideoExtractor(video_path)
        if not self.video_extractor.load_video():
            raise Exception('Failed to load video')
            
        # 获取视频信息
        video_info = self.video_extractor.get_video_info()
        
        # 创建临时音频文件
        with NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            audio_path = temp_audio.name
            
        try:
            # 提取音频
            self.video_extractor.extract_audio(audio_path)
            
            # 转换音频为文本
            transcript = self.speech_to_text.transcribe(audio_path)
            if not transcript:
                raise Exception('Failed to transcribe audio')
                
            # 处理文本
            text_chunks = self.text_processor.split_text(transcript)
            
            # 生成总结
            summary = self.summarizer.summarize_all(text_chunks)
            
            return {
                'video_info': video_info,
                'transcript': transcript,
                'summary': summary
            }
            
        finally:
            # 清理临时文件
            if os.path.exists(audio_path):
                os.remove(audio_path)

if __name__ == '__main__':
    analyzer = VideoAnalyzer()
    # 替换为你的视频文件路径
    video_path = 'test.mp4'
    
    try:
        result = analyzer.analyze_video(video_path)
        print('Video Info:', result['video_info'])
        print('\nSummary:', result['summary'])
    except Exception as e:
        print(f'Error analyzing video: {e}')
