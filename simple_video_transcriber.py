import sys
import os
import traceback
import time
import threading
import argparse
from importlib.metadata import version, PackageNotFoundError

def check_dependencies():
    """Exit with install instructions if a dependency is missing (never pip install at runtime)."""
    missing = []
    for dist in ('numpy', 'torch', 'openai-whisper'):
        try:
            print(f"{dist} version: {version(dist)}")
        except PackageNotFoundError:
            missing.append(dist)
    if missing:
        print(f"Error: missing {', '.join(missing)}.")
        print("Install the pinned versions with: pip install -r requirements.txt")
        sys.exit(1)

def print_progress(stop_event):
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"Still transcribing... Elapsed time: {elapsed_time:.2f} seconds", end='\r')
        time.sleep(5)  # Update every 5 seconds

def _timestamp(seconds, sep):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"

def format_srt(segments):
    blocks = []
    for i, seg in enumerate(segments, 1):
        start, end = _timestamp(seg["start"], ","), _timestamp(seg["end"], ",")
        blocks.append(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n")
    return "\n".join(blocks)

def format_vtt(segments):
    cues = [f"{_timestamp(seg['start'], '.')} --> {_timestamp(seg['end'], '.')}\n{seg['text'].strip()}\n"
            for seg in segments]
    return "WEBVTT\n\n" + "\n".join(cues)

def transcribe_audio(file_path, model, output_dir=None, formats=("txt",)):
    try:
        print(f"Transcribing file: {file_path}")
        start_time = time.time()

        # Start a thread to print progress
        stop_event = threading.Event()
        progress_thread = threading.Thread(target=print_progress, args=(stop_event,))
        progress_thread.start()

        try:
            # verbose=False so Whisper's segment printout doesn't clobber the progress line
            result = model.transcribe(file_path, verbose=False, fp16=False)
        finally:
            # Stop the progress thread
            stop_event.set()
            progress_thread.join()

        print("\nTranscription:")
        print("-" * 40)
        print(result["text"])
        print("-" * 40)

        # Determine output path stem
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.basename(file_path)
            stem = os.path.join(output_dir, os.path.splitext(base_name)[0] + "_transcription")
        else:
            stem = os.path.splitext(file_path)[0] + "_transcription"

        # Save transcription in each requested format
        writers = {"txt": lambda: result["text"],
                   "srt": lambda: format_srt(result["segments"]),
                   "vtt": lambda: format_vtt(result["segments"])}
        output_file = None
        for fmt in formats:
            path = f"{stem}.{fmt}"
            with open(path, "w", encoding='utf-8') as f:
                f.write(writers[fmt]())
            print(f"Transcription saved to: {path}")
            output_file = output_file or path

        total_time = time.time() - start_time
        print(f"Total transcription time: {total_time:.2f} seconds")

        return output_file
    except Exception as e:
        print(f"\nAn error occurred during transcription: {e}")
        print("Traceback:")
        traceback.print_exc()
        return None

def get_media_files(paths, max_depth=3):
    """Collect all media files from the provided paths (files or directories)

    Args:
        paths: List of file or directory paths
        max_depth: Maximum folder depth to scan (default: 3)
    """
    media_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.mpeg', '.flv', '.webm',
                       '.wav', '.mp3', '.m4a', '.flac', '.ogg', '.wma', '.aac'}
    media_files = []

    for path in paths:
        if os.path.isfile(path):
            # Add file if it has a supported extension
            if os.path.splitext(path.lower())[1] in media_extensions:
                media_files.append(path)
            else:
                print(f"Warning: Skipping unsupported file format: {path}")
        elif os.path.isdir(path):
            # Walk through directory with depth limit
            base_depth = path.rstrip(os.sep).count(os.sep)
            for root, dirs, files in os.walk(path):
                current_depth = root.count(os.sep) - base_depth

                # Limit depth to max_depth levels
                if current_depth >= max_depth:
                    dirs[:] = []  # Don't recurse deeper

                # Check all files in current directory
                for file in files:
                    if os.path.splitext(file.lower())[1] in media_extensions:
                        media_files.append(os.path.join(root, file))
        else:
            print(f"Warning: Path not found: {path}")

    return sorted(set(media_files))  # Remove duplicates and sort

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Transcribe audio/video files using OpenAI Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Single file
  python simple_video_transcriber.py video.mp4

  # Multiple files
  python simple_video_transcriber.py video1.mp4 video2.mp4 audio.mp3

  # Process all files in a folder
  python simple_video_transcriber.py /path/to/videos/

  # With custom output folder and model size
  python simple_video_transcriber.py video.mp4 -o ./transcriptions -m medium
        '''
    )
    parser.add_argument('paths', nargs='+', help='Path(s) to audio/video file(s) or folder(s)')
    parser.add_argument('-o', '--output-dir', help='Output directory for transcription files (default: same as input file)')
    parser.add_argument('-m', '--model',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       default='base',
                       help='Whisper model size (default: base). Larger models are more accurate but slower.')
    parser.add_argument('-f', '--formats', nargs='+', choices=['txt', 'srt', 'vtt'], default=['txt'],
                       help='Output format(s): txt (plain text), srt and/or vtt (timestamped subtitles). Default: txt')

    args = parser.parse_args()

    print("Checking dependencies...")
    check_dependencies()

    # Collect all media files
    print("\nScanning for media files...")
    media_files = get_media_files(args.paths)

    if not media_files:
        print("Error: No supported media files found.")
        sys.exit(1)

    print(f"\nFound {len(media_files)} file(s) to transcribe:")
    for i, f in enumerate(media_files, 1):
        print(f"  {i}. {f}")

    # Load the Whisper model once
    import whisper
    print(f"\nLoading Whisper model '{args.model}'...")
    print("(This may take a moment, especially for larger models)")
    model = whisper.load_model(args.model)
    print("Model loaded successfully!\n")

    # Process each file
    successful = 0
    failed = 0

    for i, media_file in enumerate(media_files, 1):
        print(f"\n{'='*60}")
        print(f"Processing file {i}/{len(media_files)}")
        print(f"{'='*60}")

        output_file = transcribe_audio(media_file, model, args.output_dir, args.formats)
        if output_file:
            successful += 1
        else:
            failed += 1

    # Print summary
    print(f"\n{'='*60}")
    print("TRANSCRIPTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total files: {len(media_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    if args.output_dir:
        print(f"Output directory: {os.path.abspath(args.output_dir)}")
    print(f"{'='*60}")