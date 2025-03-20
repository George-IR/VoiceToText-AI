import os
import json
import subprocess
import sys
import time

# --- Configuration ---
# Path to the Whisper CLI executable
WHISPER_EXE     = r"WhisperRelease\whisper-cli.exe"
# Folder that contains audio files to transcribe
AUDIO_FOLDER    = r"Audio"
# JSON file to store processed transcripts
TRANSCRIPTS_JSON= f"{AUDIO_FOLDER}.json"
# Model
MODEL           = r"WhisperRelease\Model\ggml-base.en.bin"

# Whisper command arguments (modify as needed, e.g., threads, processors, etc.)
DEFAULT_ARGS = ["-t", "4", "-p", "3", "-m", MODEL]
# Supported audio file extensions
SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac"}

def load_transcripts(json_file):
    """Load the transcripts JSON file if exists, otherwise return an empty dict."""
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_transcripts(json_file, data):
    """Save transcripts dictionary to a JSON file."""
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def transcribe_file(audio_filepath):
    """
    Run Whisper CLI on a given audio file.
    Returns a tuple of (raw output, elapsed time in seconds).
    """
    command = [WHISPER_EXE, "-f", audio_filepath] + DEFAULT_ARGS
    print(f"Transcribing: {audio_filepath}")
    start_time = time.time()
    
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Elapsed time: {elapsed:.2f} sec")
    
    # DEBUG: Print error (if any)
    #print(process.stderr + "\n\n")

    # For debugging, print the output:
    print("Transcript output:")
    print(process.stdout)
    
    return process.stdout, elapsed

def transcribe_all_files(folder=AUDIO_FOLDER, transcripts_json=TRANSCRIPTS_JSON):
    """
    Iterate over all supported audio files in the folder.
    For each file that hasn't been processed yet (based on transcripts_json),
    run the transcription, print the output, and update the JSON file.
    """
    transcripts = load_transcripts(transcripts_json)
    
    # Walk the folder and filter for audio files
    for root, dirs, files in os.walk(folder):
        for filename in files:
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, filename)
                # Use file name only as key
                key = filename
                if key in transcripts:
                    print(f"Skipping already processed file: {key}")
                else:
                    # Transcribe the file and get processing time
                    transcript, elapsed = transcribe_file(os.path.abspath(file_path))
                    transcripts[key] = {
                        "transcript": transcript,
                        "processing_time_sec": round(elapsed, 2),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    # Save after each file to keep progress
                    save_transcripts(transcripts_json, transcripts)
    
    print("\nAll files processed.")
    return transcripts

# If this script is run directly, call transcribe_all_files.
if __name__ == "__main__":
    transcribe_all_files()
