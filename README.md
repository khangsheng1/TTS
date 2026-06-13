# TTS Audiobook Builder

An automated, batch-processing Text-to-Speech (TTS) pipeline designed to convert text files into narrated audiobooks cleanly and efficiently. This repository tracks the evolution of the project from a cloud-dependent system to a lightning-fast, fully offline, GPU-accelerated engine.

## Prerequisites & System Setup

Before running the installation commands, ensure your machine meets the following environment requirements:

### 1. System Requirements & Hardware Acceleration
* **Operating System:** Windows 10/11
* **NVIDIA GPU Support (CUDA):** To utilize hardware acceleration for the Kokoro pipeline, ensure you have an NVIDIA graphics card installed with up-to-date graphics drivers. 
* **C++ Build Tools:** PyTorch or audio processing modules occasionally require compilation components. Install the [Visual Studio Community Edition](https://visualstudio.microsoft.com/vs/community/) with the **Desktop development with C++** workload checked during setup.

### 2. Phonetic Translation Engine (Required for Kokoro)
Kokoro requires an external processing utility called **espeak-ng** to translate raw text strings into phonemes.
1. Download the standard Windows installer (`.msi`) directly from the [espeak-ng GitHub releases page](https://github.com/espeak-ng/espeak-ng/releases).
2. Run the installer and note the path (typically `C:\Program Files\eSpeak NG`).
3. Add this installation folder to your Windows System Environment Variables (`PATH`) so Python can execute the utility globally.

---

## Installation & Dependency Commands

Once the prerequisites are installed on your machine, initialize your Python environment and run the following setup commands in your terminal:

```bash
# 1. Install GPU-enabled PyTorch matching your hardware setup
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu117](https://download.pytorch.org/whl/cu117)

# 2. Install the core Text-to-Speech engines and file system packages
pip install edge-tts kokoro soundfile huggingface_hub

# 3. Install utility libraries for dataframes, tracking, and audio playback
pip install pandas tqdm pygame