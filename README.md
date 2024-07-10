# Simple Video Transcriber

Simple Video Transcriber is a Python-based tool that uses OpenAI's Whisper model to transcribe audio from video and audio files. It provides an easy-to-use interface for transcribing audio content and saving the results to a text file.

## Features

- Transcribe audio from various video and audio file formats
- Automatic dependency installation
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

   Note: The script will attempt to install missing dependencies automatically when run.

## Usage

Run the script from the command line, providing the path to your audio or video file:

```
python simple_video_transcriber.py /path/to/your/file.mp4
```

The transcription will be saved in a text file in the same directory as the input file, with "_transcription.txt" appended to the original filename.

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