# Simple Video Transcriber

Simple Video Transcriber is a Python-based tool that uses OpenAI's Whisper model to transcribe audio from video and audio files. It provides an easy-to-use interface for transcribing audio content and saving the results to a text file.

## Features

- Transcribe audio from various video and audio file formats
- Dependency check with install instructions (pinned in requirements.txt)
- Progress tracking during transcription
- Output saved to a text file

## Supported Formats

The Simple Video Transcriber supports a wide range of audio and video formats, including but not limited to:

- Audio: WAV, MP3, M4A, FLAC, OGG, WMA, AAC
- Video: MP4, AVI, MOV, WMV, MPEG, FLV, WebM

Note: The actual range of supported formats may depend on your FFmpeg installation.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/simple-video-transcriber.git
   cd simple-video-transcriber
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   Note: The script checks dependencies at startup and exits with instructions if any are missing. It never installs packages itself.

## Usage

### Basic Usage

Transcribe a single file:
```bash
python simple_video_transcriber.py /path/to/your/file.mp4
```

### Multiple Files

Transcribe multiple files at once:
```bash
python simple_video_transcriber.py video1.mp4 video2.mp4 audio.mp3
```

### Process Entire Folders

Process all media files in a folder (searches recursively):
```bash
python simple_video_transcriber.py /path/to/videos/
```

### Custom Output Directory

Save all transcriptions to a specific folder:
```bash
python simple_video_transcriber.py file.mp4 -o ./transcriptions
```

### Choose Model Size

Select different Whisper model sizes for accuracy vs. speed tradeoff:
```bash
python simple_video_transcriber.py file.mp4 -m medium
```

Available models: `tiny`, `base`, `small`, `medium`, `large`
- **tiny**: Fastest, least accurate
- **base**: Good balance (default)
- **small**: Better accuracy, slower
- **medium**: High accuracy, much slower
- **large**: Best accuracy, slowest

### Subtitles (SRT and VTT)

Save timestamped subtitles alongside, or instead of, plain text:
```bash
python simple_video_transcriber.py file.mp4 -f txt srt vtt
```

Choices: `txt` (default), `srt`, `vtt`. Each file is saved as `<name>_transcription.<format>`.

### Combined Options

```bash
python simple_video_transcriber.py /path/to/videos/ -o ./transcriptions -m medium
```

### Get Help

```bash
python simple_video_transcriber.py --help
```

By default, transcription files are saved in the same directory as the input file with "_transcription.txt" appended to the filename.

## Requirements

- Python 3.7 or higher
- FFmpeg (for audio extraction from video files)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Tatsu Ikeda

## Acknowledgments

- OpenAI for the Whisper model
- Contributors to the various dependencies used in this project

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/your-username/simple-video-transcriber/issues) if you want to contribute.

## Disclaimer

This tool uses the Whisper model, which may have its own terms of use. Please ensure you comply with OpenAI's use-case policies when using this tool.