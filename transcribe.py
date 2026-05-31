#!/usr/bin/env python3
"""
Minimal batch transcription wrapper for OpenAI Whisper inside Docker.
Processes either a single audio file or all audio files within a directory.
"""

import argparse
import os
import subprocess
import sys

# Supported audio extensions
AUDIO_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.flac', '.ogg', '.mp4')


def main():
    parser = argparse.ArgumentParser(description="Whisper Batch Transcriber")
    parser.add_argument("--input", default="/in", help="Path to file or directory to transcribe")
    parser.add_argument("--output-dir", default="/out", help="Directory to save text outputs")
    parser.add_argument("--model", default="medium", help="Whisper model size")
    parser.add_argument("--language", default="de", help="Language of the audio")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Gather target files
    files_to_process = []
    if os.path.isfile(args.input):
        files_to_process.append(args.input)
    elif os.path.isdir(args.input):
        for f in sorted(os.listdir(args.input)):
            if f.lower().endswith(AUDIO_EXTENSIONS):
                files_to_process.append(os.path.join(args.input, f))
    else:
        print(f"Error: Input path '{args.input}' not found.")
        sys.exit(1)

    if not files_to_process:
        print(f"No valid audio files found in '{args.input}'.")
        return

    print(f"Processing {len(files_to_process)} file(s)...")

    # Run Whisper CLI sequentially for each file
    for idx, file_path in enumerate(files_to_process, 1):
        print(f"\n[{idx}/{len(files_to_process)}] Transcribing: {os.path.basename(file_path)}")

        whisper_cmd = [
            "whisper",
            file_path,
            "--language", args.language,
            "--model", args.model,
            "--device", "cuda",
            "--output_format", "txt",
            "--output_dir", args.output_dir
        ]

        try:
            subprocess.run(whisper_cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to process: {file_path}")


if __name__ == "__main__":
    main()
