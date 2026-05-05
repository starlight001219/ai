"""
周文慧 AI 聊天机器人 Web 界面 — 集成语音合成 (TTS)
基于微调后的 Qwen2.5-3B-Instruct 模型
"""
import sys
import os
import asyncio
from pathlib import Path

# Add WeClone path for model loading
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "WeClone"))

try:
    import gradio as gr
    from llamafactory.chat import ChatModel
    from llamafactory.extras.misc import get_device
    print("LLaMA Factory loaded successfully")
except ImportError as e:
    print(f"Error importing: {e}")
    print("Make sure LLaMA Factory is installed in your environment")
    sys.exit(1)

# Edge-TTS for voice synthesis
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
    print("Edge-TTS available")
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("Edge-TTS not installed — voice synthesis disabled")

# Model paths
BASE_MODEL = str(Path(__file__).resolve().parent.parent / "WeClone/models/Qwen2.5-3B-Instruct")
ADAPTER_PATH = str(Path(__file__).resolve().parent.parent / "WeClone/model_output")

AUDIO_DIR = Path(__file__).resolve().parent / "audio"
AUDIO_DIR.mkdir(exist_ok=True)


def create_chat_model():
    """Initialize the chat model with fine-tuned adapter."""
    config = {
        "model_name_or_path": BASE_MODEL,
        "adapter_name_or_path": ADAPTER_PATH,
        "template": "qwen",
        "finetuning_type": "lora",
        "quantization_bit": None,
        "infer_args": {
            "repetition_penalty": 1.1,
            "temperature": 0.7,
            "max_length": 512,
            "top_p": 0.85,
        },
        "system_prompt": "你叫周文慧，今年19岁，是一名大一女生。你正在和朋友聊天，请用你的语气回复，保持真实自然。",
    }
    return ChatModel(config)


def respond(message, history, system_prompt):
    """Generate response from the model."""
    if chat_model is None:
        yield "模型加载中，请稍候..."
        return

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    response = ""
    for new_text in chat_model.stream_chat(messages):
        response += new_text
        yield response


async def text_to_speech(text: str) -> str:
    """Generate TTS audio file from text. Returns audio file path."""
    if not EDGE_TTS_AVAILABLE or not text.strip():
        return ""

    import hashlib
    safe = hashlib.md5(text.encode()).hexdigest()[:12]
    filename = f"tts_{safe}.mp3"
    output_path = AUDIO_DIR / filename

    if output_path.exists():
        return str(output_path)

    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(str(output_path))
        if output_path.exists():
            return str(output_path)
    except Exception as e:
        print(f"TTS error: {e}")
    return ""


def main():
    global chat_model
    print("Loading model...")

    model_path = Path(BASE_MODEL)
    adapter_path = Path(ADAPTER_PATH)

    if not model_path.exists():
        print(f"Model not found at {model_path}")
        chat_model = None
    elif not adapter_path.exists():
        print(f"Adapter not found at {adapter_path}")
        print("Training hasn't been completed yet. Run train-sft first.")
        chat_model = None
    else:
        try:
            chat_model = create_chat_model()
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            chat_model = None

    css = """
    .gradio-container { font-family: 'Microsoft YaHei', sans-serif; }
    .chat-message { font-size: 16px; }
    """

    with gr.Blocks(title="周文慧 AI", css=css, theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 周文慧 AI

        你好呀！我是周文慧，19岁，大一女生。来和我聊天吧～
        """)

        chatbot = gr.Chatbot(label="对话", height=500)
        msg = gr.Textbox(label="输入消息", placeholder="说点什么吧...", lines=1)
        audio_output = gr.Audio(label="语音回复", visible=EDGE_TTS_AVAILABLE, autoplay=True)
        system_prompt = gr.Textbox(
            value="你叫周文慧，今年19岁，是一名大一女生。你正在和朋友聊天，请用你的语气回复，保持真实自然。",
            label="系统提示词", visible=False,
        )
        clear = gr.Button("清空对话")

        def user_submit(user_msg, chat_history):
            return "", chat_history + [[user_msg, None]]

        def bot_response(chat_history, system_prompt):
            if not chat_history or chat_history[-1][1] is not None:
                return chat_history, None

            user_msg = chat_history[-1][0]
            history_for_llm = [(h[0], h[1]) for h in chat_history[:-1] if h[1] is not None]

            full_response = ""
            for partial in respond(user_msg, history_for_llm, system_prompt):
                full_response = partial
                chat_history[-1][1] = partial
                yield chat_history, None

            # Generate TTS after response is complete
            if EDGE_TTS_AVAILABLE and full_response.strip():
                audio_path = asyncio.run(text_to_speech(full_response))
                if audio_path:
                    yield chat_history, audio_path

        msg.submit(user_submit, [msg, chatbot], [msg, chatbot]).then(
            bot_response, [chatbot, system_prompt], [chatbot, audio_output]
        )

        clear.click(lambda: ([], None), None, [chatbot, audio_output])

    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == "__main__":
    chat_model = None
    main()
