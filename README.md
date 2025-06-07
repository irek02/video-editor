# Automated Video Editor CLI

This project provides a Python command-line tool to automate video editing for AI coding challenge content. It reads a YAML analysis file and processes a video using FFmpeg to create main edits, highlight reels, and YouTube Shorts.

## Features
- Reads YAML analysis files for edit instructions
- Extracts and concatenates video segments using FFmpeg
- Supports speed-up segments and vertical cropping for Shorts
- Outputs main edit, highlight edit, and multiple Shorts

## Requirements
- Python 3.7+
- FFmpeg (must be installed and available in your PATH)
- Python packages: see `requirements.txt`

## Installation
1. Install Python 3.7 or higher.
2. Install FFmpeg: https://ffmpeg.org/download.html
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
```
python video_editor.py <input_video> <yaml_analysis_file>
```
Example:
```
python video_editor.py recording.mp4 analysis_output.yaml
```

## Output
- Main edit: `output/main_edit.mp4`
- Highlight edit: `output/highlight_edit.mp4`
- Shorts: `output/short_*.mp4`

## Notes
- Ensure FFmpeg is installed and accessible from your command line.
- Replace placeholder media assets as needed.

## License
MIT
