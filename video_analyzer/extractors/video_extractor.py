import cv2
from moviepy.editor import VideoFileClip

class VideoExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.video = None
        
    def load_video(self):
        """加载视频文件"""
        try:
            self.video = VideoFileClip(self.file_path)
            return True
        except Exception as e:
            print(f'Error loading video: {e}')
            return False
            
    def extract_audio(self, output_path):
        """提取音频"""
        try:
            audio = self.video.audio
            audio.write_audiofile(output_path)
            return output_path
        except Exception as e:
            print(f'Error extracting audio: {e}')
            return None
            
    def get_video_info(self):
        """获取视频信息"""
        if self.video:
            return {
                'duration': self.video.duration,
                'fps': self.video.fps,
                'size': self.video.size
            }
        return None
