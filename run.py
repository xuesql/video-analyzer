from video_analyzer.main import VideoAnalyzer

if __name__ == '__main__':
    analyzer = VideoAnalyzer()
    video_path = 'your_video.mp4'  # 修改为你的视频文件路径
    
    try:
        result = analyzer.analyze_video(video_path)
        print('Video Info:', result['video_info'])
        print('\nSummary:', result['summary'])
    except Exception as e:
        print(f'Error analyzing video: {e}')
