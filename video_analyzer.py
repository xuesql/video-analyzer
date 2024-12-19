import os
from moviepy.editor import VideoFileClip
from PIL import Image
import speech_recognition as sr
import cv2
import numpy as np
from transformers import pipeline
import json
import markdown2
from datetime import datetime

class VideoAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.audio_path = "temp_audio.wav"
        self.frames_dir = "key_frames"
        self.results = {
            "audio_analysis": "",
            "frame_analysis": [],
            "summary": "",
        }
        
        # 创建关键帧目录
        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)
            
    def extract_audio(self):
        """提取视频中的音频"""
        video = VideoFileClip(self.video_path)
        video.audio.write_audiofile(self.audio_path)
        return self.audio_path

    def transcribe_audio(self):
        """将音频转换为文本"""
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                self.results["audio_analysis"] = text
            except sr.UnknownValueError:
                print("无法识别音频")
            except sr.RequestError:
                print("无法连接到语音识别服务")

    def extract_key_frames(self, threshold=30):
        """提取视频关键帧"""
        cap = cv2.VideoCapture(self.video_path)
        prev_frame = None
        frame_count = 0
        key_frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if prev_frame is None:
                prev_frame = frame
                key_frames.append((frame_count, frame))
                continue

            # 计算帧差
            diff = cv2.absdiff(frame, prev_frame)
            non_zero_count = np.count_nonzero(diff)
            
            if non_zero_count > threshold:
                key_frames.append((frame_count, frame))
                
            prev_frame = frame
            frame_count += 1

        cap.release()
        return key_frames

    def analyze_frames(self, key_frames):
        """使用预训练模型分析关键帧"""
        image_classifier = pipeline("image-classification")
        
        for idx, (frame_count, frame) in enumerate(key_frames):
            # 保存关键帧
            frame_path = os.path.join(self.frames_dir, f"frame_{idx}.jpg")
            cv2.imwrite(frame_path, frame)
            
            # 分析图像
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            results = image_classifier(image)
            
            self.results["frame_analysis"].append({
                "frame_number": frame_count,
                "frame_path": frame_path,
                "analysis": results
            })

    def generate_summary(self):
        """生成分析总结"""
        summary = []
        
        # 音频分析总结
        if self.results["audio_analysis"]:
            summary.append("音频内容摘要：")
            summary.append(self.results["audio_analysis"][:200] + "...")
            
        # 视觉分析总结
        if self.results["frame_analysis"]:
            summary.append("\n关键帧分析：")
            for frame in self.results["frame_analysis"]:
                summary.append(f"- 帧 {frame['frame_number']}: "
                             f"主要内容 - {frame['analysis'][0]['label']}, "
                             f"置信度 - {frame['analysis'][0]['score']:.2f}")
        
        self.results["summary"] = "\n".join(summary)

    def generate_markdown(self):
        """生成Markdown报告"""
        markdown = f"""# 视频分析报告
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 音频分析
{self.results['audio_analysis']}

## 2. 关键帧分析
"""
        
        for frame in self.results["frame_analysis"]:
            markdown += f"""
### 帧 {frame['frame_number']}
![关键帧]({frame['frame_path']})
- 分析结果：{frame['analysis'][0]['label']}
- 置信度：{frame['analysis'][0]['score']:.2f}
"""

        markdown += f"""
## 3. 总结
{self.results['summary']}
"""
        
        return markdown

    def analyze(self):
        """执行完整的分析流程"""
        print("1. 提取音频...")
        self.extract_audio()
        
        print("2. 转录音频...")
        self.transcribe_audio()
        
        print("3. 提取关键帧...")
        key_frames = self.extract_key_frames()
        
        print("4. 分析关键帧...")
        self.analyze_frames(key_frames)
        
        print("5. 生成总结...")
        self.generate_summary()
        
        print("6. 生成报告...")
        markdown_report = self.generate_markdown()
        
        # 清理临时文件
        os.remove(self.audio_path)
        
        return markdown_report

def main():
    # 使用示例
    video_path = "example.mp4"
    analyzer = VideoAnalyzer(video_path)
    markdown_report = analyzer.analyze()
    
    # 保存报告
    with open("video_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(markdown_report)

if __name__ == "__main__":
    main()