# VoiceToText-AI

## Description of Scripts

### **1. whisper_benchmark.py**
This script benchmarks the performance of Whisper by running transcriptions with different thread counts and measuring the processing time.

- Runs Whisper CLI on a test audio file with various thread settings.
- Extracts processing times from Whisper's output.
- Saves the benchmark results in a CSV file.
- Helps determine the optimal thread count for your system.

#### **Usage:**
```sh
python whisper_benchmark.py
```
The script will print results and save them in `whisper_benchmark_results_<filename>.csv`.

---

### **2. transcriptAudio.py**
This script automates the transcription of multiple audio files in a specified folder and stores the results in a JSON file.

- Scans the `Audio/` folder for supported audio files (`.wav`, `.mp3`, `.m4a`, `.flac`).
- Runs Whisper CLI to transcribe each file.
- Saves the transcript, processing time, and timestamp in `Audio.json`.
- Skips files that have already been transcribed to avoid redundant processing.

#### **Usage:**
```sh
python transcriptAudio.py
```
The script will transcribe all new audio files and update `Audio.json`.

---

# Whisper Installation & Setup Guide

This guide explains how to set up and run **Whisper** (a speech-to-text engine) using a pre-downloaded release in `WhisperRelease`. If the release does not work, follow the installation steps below. For more details, visit the official repository: [Whisper.cpp GitHub](https://github.com/ggerganov/whisper.cpp).

## 1. Using the Pre-Downloaded Whisper Release

### **Step 1: Extract the Release**
Ensure you have a copy of the `WhisperRelease` folder in your working directory. If the files are compressed, extract them first.

### **Step 2: Verify Executable Files**
Inside `WhisperRelease`, you should have the following:

- `whisper-cli.exe` (Windows) or `whisper` (Linux/macOS)
- `models/` (folder containing Whisper model files)
- Required dependencies

### **Step 3: Test Whisper CLI**
Run the following command to check if Whisper is working:

```sh
cd WhisperRelease
./whisper-cli --help  # For Linux/macOS
whisper-cli.exe --help  # For Windows
```

If this prints out usage information, the installation was successful.

### **Step 4: Run a Transcription**
To transcribe an audio file (e.g., `audio.wav`):

```sh
./whisper-cli -f path/to/audio.wav -m models/ggml-base.en.bin  # Linux/macOS
whisper-cli.exe -f path\to\audio.wav -m models\ggml-base.en.bin  # Windows
```

If the above steps **do not work**, follow the installation guide below.

---

## 2. Installing Whisper Manually

### **Step 1: Install Dependencies**
Ensure you have the following installed:

- **Windows**: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with C++ support.
- **Linux/macOS**: Install `gcc`, `g++`, `make`, and `cmake`:
  ```sh
  sudo apt update && sudo apt install build-essential cmake
  ```
  (For macOS, use `brew install cmake`)

### **Step 2: Clone Whisper.cpp Repository**

```sh
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
```

### **Step 3: Build Whisper**

#### **Windows (Using MSVC)**

```sh
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

#### **Linux/macOS**

```sh
make
```

### **Step 4: Download a Model**
[More audio Models "CLICK"](https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#more-audio-samples)

You need at least one model to transcribe audio. Example:

```sh
./models/download-ggml-model.sh base.en
```

For Windows, manually download a model from: [https://huggingface.co/ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp)

### **Step 5: Run a Transcription**

```sh
./whisper -f path/to/audio.wav -m models/ggml-base.en.bin  # Linux/macOS
whisper.exe -f path\to\audio.wav -m models\ggml-base.en.bin  # Windows
```

---

## 3. Troubleshooting

- **Missing `whisper-cli.exe` or `whisper` binary?**
  - Ensure you compiled Whisper correctly (see Step 3 above).
  
- **Model not found error?**
  - Ensure the model file is downloaded and correctly referenced in the `-m` argument.

- **Permission errors?**
  - Try running with elevated permissions (`sudo` on Linux/macOS or `Run as Administrator` on Windows).

For further issues, visit the official [Whisper.cpp GitHub Issues](https://github.com/ggerganov/whisper.cpp/issues) page.

---

## 4. Additional Notes
- If using a GPU, install CUDA and build with GPU support.
- Check the [Whisper.cpp README](https://github.com/ggerganov/whisper.cpp) for advanced options and optimizations.
