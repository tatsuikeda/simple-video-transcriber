import sys
import os
import subprocess
import pkg_resources
import traceback
import time
import threading

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

def check_and_install_dependencies():
    required_packages = {
        'numpy': 'numpy',
        'torch': 'torch',
        'whisper': 'openai-whisper'
    }
    for package, pip_name in required_packages.items():
        try:
            pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            print(f"{package} not found. Installing...")
            install_package(pip_name)
    print("All dependencies are installed.")
    # Now import and print versions
    import numpy
    import torch
    import whisper
    print(f"NumPy version: {numpy.__version__}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Whisper version: {whisper.__version__}")

def print_progress(stop_event):
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"Still transcribing... Elapsed time: {elapsed_time:.2f} seconds", end='\r')
        time.sleep(5)  # Update every 5 seconds

def transcribe_audio(file_path):
    try:
        import whisper
        print(f"Loading model...")
        model = whisper.load_model("base")
        
        print(f"Transcribing file: {file_path}")
        start_time = time.time()
        
        # Start a thread to print progress
        stop_event = threading.Event()
        progress_thread = threading.Thread(target=print_progress, args=(stop_event,))
        progress_thread.start()
        
        try:
            result = model.transcribe(file_path, verbose=True, fp16=False)
        finally:
            # Stop the progress thread
            stop_event.set()
            progress_thread.join()
        
        print("\nTranscription:")
        print("-" * 40)
        print(result["text"])
        print("-" * 40)
        
        # Save transcription to file
        output_file = os.path.splitext(file_path)[0] + "_transcription.txt"
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(result["text"])
        print(f"Transcription saved to: {output_file}")
        
        total_time = time.time() - start_time
        print(f"Total transcription time: {total_time:.2f} seconds")
        
        return output_file
    except Exception as e:
        print(f"\nAn error occurred during transcription: {e}")
        print("Traceback:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("Checking and installing dependencies if necessary...")
    check_and_install_dependencies()
    if len(sys.argv) != 2:
        print("Usage: python simple_video_transcriber.py <path_to_audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}")
        sys.exit(1)
    
    output_file = transcribe_audio(audio_file)
    if output_file:
        print(f"Transcription process completed. Output saved to: {output_file}")
    else:
        print("Transcription process failed.")