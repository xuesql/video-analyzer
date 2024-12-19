import whisper
import torch

class SpeechToText:
    def __init__(self, model_size='base'):
        self.model = whisper.load_model(model_size)
        
    def transcribe(self, audio_path):
        """将音频转换为文本"""
        try:
            result = self.model.transcribe(audio_path)
            return result['text']
        except Exception as e:
            print(f'Error transcribing audio: {e}')
            return None
