# 🗣️ Text2Speech - Transform Text into Speech with Ease using Python 🐍

Welcome to Text2Speech, a straightforward yet powerful Python web app that converts text into speech. Leveraging the capabilities of [TTS](https://github.com/coqui-ai/TTS) for speech generation and [Gradio](https://www.gradio.app) for the web interface, this app was initially built for personal use. However, I've decided to share this handy tool with the community. 🌍

## 📸 Sneak Peek

Here's a glimpse of the application in action!

![App Screenshot](assets/screenshot.png)

## 🌟 Key Features

- 🗣️ Convert text into speech in 16 different languages.
- 💾 Save the generated speech as a WAV file.
- 🎙️ Use any recorded voice as the speaker and convert it into speech in any language.
- ⚡ Fast inference even on CPU (tested on Apple M1, MPS is not supported yet).

## 🚀 Quick Start Guide
1. 📝 Enter the text you wish to convert into speech.
2. 🌐 Choose the language of the text.
3. 📂 Select a voice (see 📚 Additional Notes)
    - 🎧 Preview the voices in the selected folder under the `Voices Preview` section.
    - ➕ Add your own voices to the `voices` folder.
4. 📄 Provide a filename for the generated audio (omit the extension).
    - 🎵 The file will be saved as a `.wav` file in the `generated_audio` folder.
5. 🖱️ Click `Generate Audio` to produce the audio.
    - 🔊 Listen to the generated audio in the `Generated Audio Preview` section.

## 📚 Dependencies
- [gradio](https://www.gradio.app) - For creating the web-based interface.
- [TTS](https://github.com/coqui-ai/TTS) - For speech generation.

## 🔧 Installation & Setup

Get Text2Speech up and running on your local machine in no time:

1. 📂 Clone this repository.
2. 🚀 Navigate to the cloned repository: `cd text2speech`.
3. 🌱 Create and activate a new Python 3.10 virtual environment using your preferred method.
4. 🛠️ Run the installation script: `bash install.sh`.
   - This will clone the TTS repository and install the requirements.
5. 🏃‍♀️ Run the app using `python -m text2speech`.
6. 🌐 Head to the URL displayed in the terminal to start using the app.

## 📚 Additional Notes

- You need to provide a `voices` folder, which should contain subfolders with the recorded voices in `.wav` or `.mp3` format. If you don't have any recorded voices, you can use [the voices folder](https://github.com/neonbjb/tortoise-tts/tree/main/tortoise/voices) from [Tortoise](https://github.com/neonbjb/tortoise-tts), another excellent TTS Python library.
- The app will save the generated speech in the `generated_audio` folder.****