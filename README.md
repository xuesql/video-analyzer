# Video Analyzer

A Python-based tool for analyzing and summarizing video content using AI.

## Features

- Local video file processing
- Audio extraction
- Speech-to-text conversion
- AI-powered content summarization
- Modular design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/xuesql/video-analyzer.git
cd video-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file and set your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

```python
from video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer()
result = analyzer.analyze_video('path/to/your/video.mp4')

print('Video Info:', result['video_info'])
print('Summary:', result['summary'])
```

## Project Structure

```
video_analyzer/
├── __init__.py
├── config.py
├── extractors/
│   ├── __init__.py
│   ├── video_extractor.py
│   └── audio_extractor.py
├── processors/
│   ├── __init__.py
│   ├── text_processor.py
│   └── speech_to_text.py
├── summarizer/
│   ├── __init__.py
│   └── ai_summarizer.py
└── main.py
```
