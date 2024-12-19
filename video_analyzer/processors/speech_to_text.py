import whisper
import torch

class SpeechToText:
    def __init__(self, model_size='base'):
        # Check if CUDA is available
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = whisper.load_model(model_size).to(device)
        self.device = device
        
    def transcribe(self, audio_path):
        """将音频转换为文本"""
        try:
            result = self.model.transcribe(audio_path)
            return result['text']
        except Exception as e:
            print(f'Error transcribing audio: {e}')
            return None
