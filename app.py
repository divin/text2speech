import os
import glob
import torch
import gradio as gr
from TTS.api import TTS

APP_NAME = "Text2Speech"

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
    "ko": "Korean"
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

    def _generate_audio(prompt: str, voices_folder: str, file_name: str, language: str):
        """Generate audio from text using the selected voices folder"""
        speaker_wav = glob.glob(voices_folder + "/*.wav") + glob.glob(voices_folder + "/*.mp3")
        file_path = f"generated_audio/{file_name}.wav"
        file_name = _get_fixed_file_name(file_name=file_name)
        language = LANGUAGE_MAPPING[language]
        text2speech.tts_to_file(prompt, speaker_wav=speaker_wav, language=language, file_path=file_path)
        return file_path
    
    def _get_voices_preview(voices_folder):
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
    with gr.Blocks(title=APP_NAME) as app:

        gr.Markdown(f"# {APP_NAME}")

        with gr.Accordion("About", open=False):
            gr.Markdown(f"""
            # {APP_NAME}
            This app uses [TTS](https://github.com/coqui-ai/TTS) to generate speech from text.
            
            ## How to use it?
            1. Write the text you want to convert to speech.
            2. Select the language of the text.
            3. Select a folder with voices.
                - You can listen to the voices in the respective folder in the `Voices Preview` section.
                - You can add your own voices in the `voices` folder.
            4. Write a file name for the generated audio without the extension.
                - The file will be saved as a `.wav` file in the `generated_audio` folder.
            5. Click on `Generate Audio` to generate the audio.
                - You can listen to the generated audio in the `Generated Audio Preview`.
            """)

        # Text which will be converted to speech
        with gr.Group():
            prompt = gr.TextArea(label="Enter the Text")
            language = gr.Dropdown(value="English", choices=LANGUAGE_MAPPING.keys(), label="Select Language")

        # Select a folder with voices
        with gr.Row():
            voices_folder = gr.Dropdown(choices=_get_available_voices(), label="Select a Folder with Voices")
            voices_preview = gr.Audio(label="Preview of Selected Voices")
            voices_folder.input(fn=_get_voices_preview, inputs=[voices_folder], outputs=[voices_preview])

        # Generate audio from text
        with gr.Row():

            with gr.Group():
                file_name = gr.Textbox(label="Enter a File Name")
                button = gr.Button("Generate Audio")
            
            with gr.Column():
               generated_audio_preview = gr.Audio(label="Preview of Generated Speech")
        
        button.click(fn=_generate_audio, inputs=[prompt, voices_folder, file_name, language], outputs=[generated_audio_preview])
    
    return app

if __name__ == "__main__":

    # Create folder for generated audio
    if not os.path.exists("generated_audio"):
        os.mkdir("generated_audio")

    # Launch the app
    app = get_app()
    app.launch(show_api=False)