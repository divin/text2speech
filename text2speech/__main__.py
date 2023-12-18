import glob
import os

import gradio as gr  # type: ignore
import torch

from TTS.api import TTS  # type: ignore

from .constants import DESCRIPTION

LANGUAGE_CODE = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "pl": "Polish",
    "tr": "Turkish",
    "ru": "Russian",
    "nl": "Dutch",
    "cs": "Czech",
    "ar": "Arabic",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "hu": "Hungarian",
    "ko": "Korean",
}

LANGUAGE_MAPPING = {value: key for key, value in LANGUAGE_CODE.items()}


def get_app() -> gr.Interface:
    def _get_fixed_file_name(file_name: str) -> str:
        """Fix the file name to avoid errors"""
        file_name = file_name.replace(" ", "_")
        file_name = file_name.replace(".wav", "")
        file_name = file_name.replace(".", "_")
        file_name = file_name.replace(",", "_")
        return file_name

    def _generate_audio(
        prompt: str,
        voices_folder: str,
        file_name: str,
        language: str,
        length_penalty: float,
        repetition_penalty: float,
        top_k: int,
        top_p: float,
        speed: float,
        enable_text_splitting: bool,
    ) -> str:
        """Generate audio from text using the selected voices folder"""

        if file_name == "":
            raise ValueError("Please enter a file name!")

        if voices_folder == "" or not os.path.exists(voices_folder):
            raise ValueError("Please select a folder with voices!")

        if prompt == "":
            raise ValueError("Please enter the text to convert to speech!")

        speaker_wav = glob.glob(voices_folder + "/*.wav") + glob.glob(voices_folder + "/*.mp3")
        file_path = f"generated_audio/{file_name}.wav"
        file_name = _get_fixed_file_name(file_name=file_name)
        language = LANGUAGE_MAPPING[language]
        text2speech.tts_to_file(
            prompt,
            speaker_wav=speaker_wav,
            language=language,
            file_path=file_path,
            length_penalty=float(length_penalty),
            repetition_penalty=float(repetition_penalty),
            top_k=top_k,
            top_p=top_p,
            speed=speed,
            enable_text_splitting=enable_text_splitting,
        )
        return file_path

    def _get_voices_preview(voices_folder: str) -> str:
        """Get the first voice in the folder"""
        files = glob.glob(voices_folder + "/*.wav") + glob.glob(voices_folder + "/*.mp3")
        return files[0]

    def _get_available_voices() -> list[str]:
        """Get the available voices"""
        return glob.glob("voices/*")

    # Initialize the TTS
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        print("Warning: MPS is not supported yet. Using CPU instead.")
        device = "cpu"
    else:
        device = "cpu"

    text2speech = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Create the app
    with gr.Blocks(title="🗣️ Text2Speech") as app:
        gr.Markdown("# 🗣️ Text2Speech")

        with gr.Accordion("About", open=False):
            gr.Markdown(DESCRIPTION)

        # Text which will be converted to speech
        with gr.Group():
            prompt = gr.TextArea(label="Enter the Text")
            language = gr.Dropdown(
                value="English", choices=LANGUAGE_MAPPING.keys(), label="Select Language"
            )

            # Advanced options
            with gr.Accordion("Advanced Options", open=False):
                gr.Markdown(
                    "These options are for advanced users. "
                    "You can leave them as default if you are not sure what they do."
                )
                length_penalty = gr.Slider(
                    value=1.0,
                    label="Length Penalty (default: 1.0, higher value means shorter audio)",
                    minimum=0.0,
                    maximum=10.0,
                    step=0.1,
                )
                repetition_penalty = gr.Slider(
                    value=2.0,
                    label="Repetition Penalty (default: 2.0, can be used to reduce the incidence of long silences or “uhhhhhhs”, etc)",
                    minimum=0.0,
                    maximum=10.0,
                    step=0.1,
                )
                top_k = gr.Slider(
                    value=50,
                    label="Top K (default: 50, lower values mean the decoder produces more “likely” (aka boring) outputs)",
                    minimum=0,
                    maximum=100,
                    step=1,
                )
                top_p = gr.Slider(
                    value=0.8,
                    label="Top P (default: 0.8, lower values mean the decoder produces more “likely” (aka boring) outputs)",
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                )
                speed = gr.Slider(
                    value=1.0,
                    label="Speed (default: 1.0, higher values mean faster audio)",
                    minimum=0.0,
                    maximum=10.0,
                    step=0.1,
                )
                enable_text_splitting = gr.Checkbox(
                    value=True,
                    label="Enable Text Splitting (default: true, whether to split the text into sentences and generate audio for each sentence. It allows you to have infinite input length but might loose important context between sentences)",
                )

        # Select a folder with voices
        with gr.Row():
            voices_folder = gr.Dropdown(
                choices=_get_available_voices(), label="Select a Folder with Voices"
            )
            voices_preview = gr.Audio(label="Preview of Selected Voices")
            voices_folder.input(
                fn=_get_voices_preview, inputs=[voices_folder], outputs=[voices_preview]
            )

        # Generate audio from text
        with gr.Row():
            with gr.Group():
                file_name = gr.Textbox(label="Enter a File Name")
                button = gr.Button("Generate Audio")

            with gr.Column():
                generated_audio_preview = gr.Audio(label="Preview of Generated Speech")

        button.click(
            fn=_generate_audio,
            inputs=[
                prompt,
                voices_folder,
                file_name,
                language,
                length_penalty,
                repetition_penalty,
                top_k,
                top_p,
                speed,
                enable_text_splitting,
            ],
            outputs=[generated_audio_preview],
        )

    return app


if __name__ == "__main__":
    # Create folder for generated audio
    if not os.path.exists("generated_audio"):
        os.mkdir("generated_audio")

    # Launch the app
    app = get_app()
    app.launch(show_api=False)
