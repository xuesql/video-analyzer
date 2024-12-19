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
        
        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)
            
    def extract_audio(self):
        video = VideoFileClip(self.video_path)
        video.audio.write_audiofile(self.audio_path)
        return self.audio_path

    def transcribe_audio(self):
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

            diff = cv2.absdiff(frame, prev_frame)
            non_zero_count = np.count_nonzero(diff)
            
            if non_zero_count > threshold:
                key_frames.append((frame_count, frame))
                
            prev_frame = frame
            frame_count += 1

        cap.release()
        return key_frames

    def analyze_frames(self, key_frames):
        image_classifier = pipeline("image-classification")
        
        for idx, (frame_count, frame) in enumerate(key_frames):
            frame_path = os.path.join(self.frames_dir, f"frame_{idx}.jpg")
            cv2.imwrite(frame_path, frame)
            
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            results = image_classifier(image)
            
            self.results["frame_analysis"].append({
                "frame_number": frame_count,
                "frame_path": frame_path,
                "analysis": results
            })

    def generate_summary(self):
        summary = []
        
        if self.results["audio_analysis"]:
            summary.append("音频内容摘要：")
            summary.append(self.results["audio_analysis"][:200] + "...")
            
        if self.results["frame_analysis"]:
            summary.append("\n关键帧分析：")
            for frame in self.results["frame_analysis"]:
                summary.append(f"- 帧 {frame['frame_number']}: "
                             f"主要内容 - {frame['analysis'][0]['label']}, "
                             f"置信度 - {frame['analysis'][0]['score']:.2f}")
        
        self.results["summary"] = "\n".join(summary)

    def generate_markdown(self):
        markdown = f"""# 视频分析报告\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## 1. 音频分析\n{self.results['audio_analysis']}\n\n## 2. 关键帧分析\n"""
        
        for frame in self.results["frame_analysis"]:
            markdown += f"""\n### 帧 {frame['frame_number']}\n![关键帧]({frame['frame_path']})\n- 分析结果：{frame['analysis'][0]['label']}\n- 置信度：{frame['analysis'][0]['score']:.2f}\n"""

        markdown += f"""\n## 3. 总结\n{self.results['summary']}\n"""
        
        return markdown

    def analyze(self):
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
        
        os.remove(self.audio_path)
        
        return markdown_report

def main():
    video_path = "example.mp4"
    analyzer = VideoAnalyzer(video_path)
    markdown_report = analyzer.analyze()
    
    with open("video_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(markdown_report)

if __name__ == "__main__":
    main()