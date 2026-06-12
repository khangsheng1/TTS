# Python Text-to-Speech (TTS) Reader

An interactive Jupyter Notebook application that uses the `edge-tts` engine to filter high-quality neural voices and read text files aloud.

## 🚀 Features
- **Dynamic Voice Database:** Parses Microsoft Edge's hidden voice metadata into a sortable pandas DataFrame.
- **Interactive File Selection:** Uses native Windows file dialogs to browse and open `.txt` files.
- **Audio Control:** Fine-tune reading speed and choose specific regional accents (US, UK, etc.).

## 🛠️ Prerequisites
Before running the notebook, make sure you have the required packages installed:
```bash
pip install edge-tts pandas pygame aiohttp