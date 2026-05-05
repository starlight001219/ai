# 🌸 周文慧 AI 聊天机器人

基于 **Qwen2.5-3B-Instruct** 微调 + **Edge-TTS 语音合成** 的 AI 聊天机器人 Web 界面。

模仿**周文慧**（19岁大一女生）的语气和性格，支持文字和语音交互。

---

## 📋 项目概述

本项目通过对 Qwen2.5-3B-Instruct 大语言模型进行 **LoRA 微调**，将微信聊天记录中的对话风格注入模型，使其能以特定人物的语气进行自然对话。同时集成 **Edge-TTS 语音合成**，每次回复自动生成语音。

核心流程：

```
用户输入 → 拼接历史对话 → Qwen2.5 模型推理 → 流式输出回复 → 自动生成语音
```

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **AI 角色扮演** | 模仿周文慧（19岁大一女生）的语气和性格 |
| **流式输出** | 实时流式生成回复，无需等待完整输出 |
| **对话历史** | 自动保留当前会话的所有历史记录 |
| **语音合成 (TTS)** | 每次 AI 回复完成后自动生成语音并播放 |
| **可定制提示词** | 支持自定义系统提示词，调整角色设定 |
| **Web 界面** | 基于 Gradio 的友好交互界面 |

---

## 🛠️ 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Python** | 主开发语言 | 3.10+ |
| **Qwen2.5-3B-Instruct** | 基座大语言模型 | 3B 参数 |
| **LLaMA Factory** | LoRA 微调训练框架 | 最新版 |
| **Gradio** | Web 交互界面框架 | 最新版 |
| **Edge-TTS** | 微软 Edge TTS 语音合成（免费） | ≥6.0.0 |
| **PyTorch** | 深度学习框架 | 2.x |
| **Transformers** | HuggingFace 模型加载 | 最新版 |
| **PEFT** | LoRA 参数高效微调 | 最新版 |

---

## 🔧 环境要求

### 运行环境

| 依赖项 | 要求 | 说明 |
|--------|------|------|
| **操作系统** | Windows 10/11 或 Linux | Gradio Web 界面跨平台 |
| **Python** | 3.10 或更高 | 推荐 3.10.11 |
| **内存** | ≥8GB RAM | 模型加载约需 6GB |
| **GPU（推荐）** | NVIDIA RTX 4060 8GB+ | 用于模型推理加速 |
| **显存** | ≥6GB | Qwen2.5-3B 推理约需 5-6GB |
| **磁盘空间** | ≥10GB | 模型文件约 6GB + 训练数据 |
| **网络** | 需要联网 | 首次下载模型 / Edge-TTS 语音模型 |

### 训练环境（如需自行训练）

| 依赖项 | 要求 |
|--------|------|
| **GPU** | NVIDIA RTX 4060 8GB+ |
| **CUDA** | 12.1+ |
| **显存** | ≥8GB（3B 模型 QLoRA 需要 6-7GB） |

---

## 📥 安装与配置

### 1. 克隆项目并安装依赖

```bash
# 推荐使用虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 安装依赖
pip install gradio edge-tts
pip install llamafactory  # 用于加载微调模型
```

### 2. 准备模型文件

需要将以下文件放在指定位置：

```
WeClone/
├── models/
│   └── Qwen2.5-3B-Instruct/        # 基座模型（需自行下载）
│       ├── config.json
│       ├── model.safetensors
│       └── tokenizer.json
└── model_output/                    # LoRA 微调权重
    ├── adapter_config.json
    ├── adapter_model.safetensors
    └── tokenizer.json
```

**基座模型下载：**

```bash
# 从 HuggingFace 下载
git lfs install
git clone https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
# 移动到 WeClone/models/ 目录
```

### 3. 启动 Web 界面

```bash
python app.py
```

访问 http://localhost:7860 即可聊天。

---

## 🚀 使用方法

### 聊天界面

打开浏览器访问 `http://localhost:7860`：

1. 在输入框输入消息，按回车发送
2. AI 会以周文慧的语气流式回复
3. 回复完成后自动生成语音并播放
4. 点击"清空对话"重置会话

### 语音功能

- 语音回复自动播放（显示在聊天界面下方的音频播放器）
- 基于 Edge-TTS，**完全免费**，无需 API Key
- 使用 `zh-CN-XiaoxiaoNeural` 女声音色
- 音频文件缓存在 `audio/` 目录（已在 `.gitignore` 中排除）

---

## 🎯 训练过程

### 开发背景

通过微调让大语言模型模仿特定人物的说话风格。使用微信聊天记录作为训练数据，通过 LoRA 方法对 Qwen2.5 进行参数高效微调。

### 训练流程

```
聊天记录导出 → 格式标准化 → 构造训练样本 → LoRA 微调 → 合并权重 → 部署推理
```

### 训练配置

| 参数 | 值 |
|------|------|
| **基座模型** | Qwen2.5-1.5B-Instruct (首次) → Qwen2.5-3B-Instruct (最终) |
| **微调方法** | LoRA (秩 r=8, alpha=16) |
| **训练数据** | 989 条对话样本 |
| **训练轮次** | 3 epochs |
| **最终 Loss** | 3.296 |
| **训练耗时** | ~14 分钟（RTX 4060）|
| **VRAM 峰值** | ~6.7GB |
| **输出** | LoRA 权重 8.7MB → 合并后完整模型 3GB |

### 训练命令

```bash
# 使用 LLaMA Factory CLI
weclone-cli train-sft

# 或使用训练脚本
python WeClone/train_zhouwenhui_v2.py
```

### 输出文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `model_output/adapter_model.safetensors` | 8.7MB | LoRA 权重 |
| `model_output/merged/model.safetensors` | 3GB | 合并后的完整模型 |
| `model_output/checkpoint-124/` | — | 训练检查点 |
| `model_output/checkpoint-496/` | — | 训练检查点 |

### 技术细节

- **数据格式**：单轮对话，指令格式 `[用户消息 → AI 回复]`
- **LoRA 配置**：应用于所有线性层，rank=8，alpha=16
- **优化器**：AdamW
- **学习率**：2e-4
- **精度**：fp16 混合精度训练
- **梯度累积**：4 步

### 常见训练问题

| 问题 | 解决方案 |
|------|----------|
| **3B 模型 OOM** | 降级到 1.5B 模型，或使用 QLoRA 4-bit 量化 |
| **bitsandbytes Windows 报错** | 使用 fp16 而非 4-bit 量化 |
| **gradient_checkpointing 不兼容** | 使用 `device_map="cuda:0"` 单 GPU 直接加载 |

---

## 🏗️ 项目结构

```
chatbot/
├── app.py                    # 主程序：Gradio Web 界面 + 模型加载 + TTS
├── README.md                 # 项目文档
├── .gitignore                # Git 忽略规则
├── audio/                    # TTS 生成的音频缓存（不上传）
└── requirements.txt
```

---

## 📁 GitHub 仓库

- 项目地址：[github.com/starlight001219/ai](https://github.com/starlight001219/ai)

### 相关项目

- [WeChat AI Bot](https://github.com/starlight001219/wechat-clone-bot) — 微信智能机器人（对接本地模型）
- [WeClone](https://github.com/xming521/WeClone) — 微信聊天记录提取与 AI 微调框架

---

## ⚠️ 注意事项

1. **模型文件需自行下载** — 因文件较大（6GB+），未包含在仓库中
2. **训练数据涉及隐私** — 微信聊天记录包含个人信息，注意保护
3. **首次运行需联网** — 加载模型需要连 HuggingFace 或本地已有缓存
4. **Edge-TTS 首次需联网** — 第一次使用语音合成时需下载语音模型（约 1-5MB）
5. **GPU 内存要求** — 3B 模型推理约需 5-6GB 显存，CPU 模式需要 8GB+ RAM

---

## 💬 常见问题

**Q: 启动后界面空白？**
A: 确保 Gradio 正确安装，访问 `http://localhost:7860`。

**Q: 模型加载很慢？**
A: 首次加载需要从磁盘读取 6GB 模型文件，后续会缓存。

**Q: 语音没有播放？**
A: 检查 `edge-tts` 是否正确安装，以及浏览器是否允许自动播放音频。

**Q: 回复质量不高？**
A: 训练数据仅 989 条，回复连贯性有限。采集更多对话数据重新训练可以显著改善效果。
