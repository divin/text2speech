DESCRIPTION = """
# 🗣️ Text2Speech
This app leverages [TTS](https://github.com/coqui-ai/TTS) to transform text into speech.

## 🚀 How to Use?
1. 📝 Enter the text you wish to convert into speech.
2. 🌐 Choose the language of the text.
3. 📂 Select a voice (see 📚 Additional Notes)
    - 🎧 Preview the voices in the selected folder under the `Voices Preview` section.
    - ➕ Add your own voices to the `voices` folder.
4. 📄 Provide a filename for the generated audio (omit the extension).
    - 🎵 The file will be saved as a `.wav` file in the `generated_audio` folder.
5. 🖱️ Click `Generate Audio` to produce the audio.
    - 🔊 Listen to the generated audio in the `Generated Audio Preview` section.

## 📚 Additional Notes

- You need to provide a `voices` folder, which should contain subfolders with the recorded voices in `.wav` or `.mp3` format. If you don't have any recorded voices, you can use [the voices folder](https://github.com/neonbjb/tortoise-tts/tree/main/tortoise/voices) from [Tortoise](https://github.com/neonbjb/tortoise-tts), another excellent TTS Python library.
- The app will save the generated speech in the `generated_audio` folder.
"""
