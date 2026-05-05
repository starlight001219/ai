# 周文慧 AI 聊天机器人

基于 Qwen2.5-3B 微调的周文慧 AI 聊天机器人，支持文字和语音交互。

## 功能

- 模仿周文慧（19岁大一女生）的语气和性格
- Web 聊天界面（Gradio）
- **语音合成 (TTS)** — 每次回复自动生成语音，支持自动播放
- REST API 支持

## 技术栈

- 模型: Qwen2.5-3B-Instruct (QLoRA 微调)
- 框架: LLaMA Factory + Gradio
- TTS: Microsoft Edge-TTS（免费，无需 API Key）
- 训练数据: WeChat 聊天记录

## 启动

```bash
pip install gradio edge-tts
python app.py
```

访问 http://localhost:7860

## TTS 语音合成

- 基于 Edge-TTS，完全免费
- 使用 `zh-CN-XiaoxiaoNeural`（女声）发音
- 每次 AI 回复完成后自动生成并播放语音
- 首次使用需要联网下载语音模型
