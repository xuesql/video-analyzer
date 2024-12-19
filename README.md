# Video Analyzer

这是一个视频分析工具，可以处理视频的音频和图像内容，并生成分析报告。

## 主要功能

1. 音频处理
   - 提取视频中的音频
   - 将音频转换为文本
   - 分析音频内容

2. 图像处理
   - 提取视频关键帧
   - 使用AI模型分析关键帧内容
   - 生成图像分析报告

3. 报告生成
   - 生成美观的Markdown格式报告
   - 包含音频分析结果
   - 包含关键帧分析结果
   - 自动生成内容总结

## 依赖安装

```bash
pip install -r requirements.txt
```

## 使用方法

1. 克隆仓库
```bash
git clone https://github.com/xuesql/video-analyzer.git
cd video-analyzer
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行分析器
```bash
python video_analyzer.py
```

## 输出示例

程序会生成一个markdown格式的报告，包含：
- 视频的音频内容转录
- 关键帧截图和分析结果
- 总体内容摘要