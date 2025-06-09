#!/usr/bin/env python3
"""
Automated Video Editor for AI Coding Challenge Content
Reads YAML analysis file and processes video using FFmpeg
"""

import yaml
import subprocess
import os
import sys
from datetime import datetime, timedelta
import tempfile
import shutil

class VideoEditor:
    def __init__(self, input_video, yaml_file, output_dir=None):
        self.input_video = input_video
        self.yaml_file = yaml_file
        # If output_dir is not specified, use the input video's folder
        if output_dir is None:
            self.output_dir = os.path.dirname(os.path.abspath(input_video))
        else:
            self.output_dir = output_dir
        self.temp_dir = tempfile.mkdtemp()

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Load YAML analysis
        with open(yaml_file, 'r') as f:
            self.analysis = yaml.safe_load(f)

        print(f"Loaded analysis for: {self.analysis['video_info']['app_type']}")
        print(f"Original duration: {self.analysis['video_info']['duration']}")

    def timestamp_to_seconds(self, timestamp):
        """Convert HH:MM:SS to total seconds"""
        try:
            h, m, s = map(int, timestamp.split(':'))
            return h * 3600 + m * 60 + s
        except:
            print(f"Error parsing timestamp: {timestamp}")
            return 0

    def seconds_to_timestamp(self, seconds):
        """Convert seconds back to HH:MM:SS"""
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def run_ffmpeg(self, command, description="Processing"):
        """Execute FFmpeg command with error handling"""
        print(f"{description}...")
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"✓ {description} completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error in {description}:")
            print(f"Command: {' '.join(command)}")
            print(f"Error: {e.stderr}")
            return False

    def extract_segment(self, start, end, output_file):
        """Extract a video segment"""
        command = [
            'ffmpeg', '-y',  # -y to overwrite files
            '-i', self.input_video,
            '-ss', start,
            '-to', end,
            '-c:v', 'libx264',  # Re-encode for reliability
            '-c:a', 'aac',
            '-avoid_negative_ts', 'make_zero',
            output_file
        ]

        return self.run_ffmpeg(command, f"Extracting {start}-{end}")

    def create_main_edit(self):
        """Create the main edit (35-45 minutes)"""
        print("\n=== Creating Main Edit ===")

        segments = []
        segment_files = []

        # Extract all keep segments
        for i, segment in enumerate(self.analysis['main_edit']['keep_segments']):
            if segment['priority'] in ['high', 'medium']:  # Include high and medium priority
                segment_file = os.path.join(self.temp_dir, f"segment_{i:03d}.mp4")
                
                print(f"Processing: {segment['title']} ({segment['start']}-{segment['end']})")
                
                if self.extract_segment(segment['start'], segment['end'], segment_file):
                    segment_files.append(segment_file)
                    segments.append(f"file '{segment_file}'")

        # Create concat file
        concat_file = os.path.join(self.temp_dir, 'main_edit_concat.txt')
        with open(concat_file, 'w') as f:
            f.write('\n'.join(segments))

        # Concatenate all segments
        output_file = os.path.join(self.output_dir, 'main_edit.mp4')
        command = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            output_file
        ]

        if self.run_ffmpeg(command, "Creating main edit"):
            print(f"✓ Main edit saved to: {output_file}")
            return output_file
        return None

    def create_highlight_edit(self):
        """Create the highlight edit (15-20 minutes)"""
        print("\n=== Creating Highlight Edit ===")

        segments = []
        segment_files = []

        for i, segment in enumerate(self.analysis['highlight_edit']['segments']):
            segment_file = os.path.join(self.temp_dir, f"highlight_segment_{i:03d}.mp4")

            if self.extract_segment(segment['start'], segment['end'], segment_file):
                segment_files.append(segment_file)
                segments.append(f"file '{segment_file}'")

        # Create concat file
        concat_file = os.path.join(self.temp_dir, 'highlight_concat.txt')
        with open(concat_file, 'w') as f:
            f.write('\n'.join(segments))

        # Concatenate segments
        output_file = os.path.join(self.output_dir, 'highlight_edit.mp4')
        command = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            output_file
        ]

        if self.run_ffmpeg(command, "Creating highlight edit"):
            print(f"✓ Highlight edit saved to: {output_file}")
            return output_file
        return None

    def create_shorts(self):
        """Create YouTube Shorts"""
        print("\n=== Creating YouTube Shorts ===")

        created_shorts = []

        for i, short in enumerate(self.analysis['shorts']):
            print(f"\nCreating Short: {short['title']}")

            # Extract segments for this short
            short_segments = []
            segment_files = []

            for j, segment in enumerate(short['segments']):
                segment_file = os.path.join(self.temp_dir, f"short_{i}_segment_{j}.mp4")

                if self.extract_segment(segment['start'], segment['end'], segment_file):
                    segment_files.append(segment_file)
                    short_segments.append(f"file '{segment_file}'")

            if short_segments:
                # Create concat file for this short
                concat_file = os.path.join(self.temp_dir, f'short_{i}_concat.txt')
                with open(concat_file, 'w') as f:
                    f.write('\n'.join(short_segments))

                # Create horizontal short first
                temp_short = os.path.join(self.temp_dir, f'short_{i}_horizontal.mp4')
                command = [
                    'ffmpeg', '-y',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', concat_file,
                    '-c', 'copy',
                    temp_short
                ]

                if self.run_ffmpeg(command, f"Concatenating short {i+1}"):
                    # Convert to vertical format (9:16)
                    safe_title = "".join(c for c in short['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    output_file = os.path.join(self.output_dir, f'short_{i+1}_{safe_title.replace(" ", "_")}.mp4')

                    # Crop to vertical format - adjust these values based on your screen recording
                    command = [
                        'ffmpeg', '-y',
                        '-i', temp_short,
                        # '-vf', 'crop=ih*9/16:ih,scale=1080:1920',  # Crop to 9:16 and scale to 1080x1920
                        '-c:a', 'copy',
                        output_file
                    ]

                    if self.run_ffmpeg(command, f"Converting to vertical format"):
                        print(f"✓ Short created: {output_file}")
                        created_shorts.append(output_file)

        return created_shorts

    def create_all(self):
        """Create all video formats"""
        print(f"Starting video processing...")
        print(f"Input video: {self.input_video}")
        print(f"Analysis file: {self.yaml_file}")
        print(f"Output directory: {self.output_dir}")

        results = {
            'main_edit': None,
            'highlight_edit': None,
            'shorts': []
        }

        # Create main edit
        results['main_edit'] = self.create_main_edit()

        # Create highlight edit
        results['highlight_edit'] = self.create_highlight_edit()

        # Create shorts
        results['shorts'] = self.create_shorts()

        print(f"\n=== Processing Complete ===")
        print(f"Main edit: {'✓' if results['main_edit'] else '✗'}")
        print(f"Highlight edit: {'✓' if results['highlight_edit'] else '✗'}")
        print(f"Shorts created: {len(results['shorts'])}")

        return results

    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("✓ Temporary files cleaned up")

def main():
    if len(sys.argv) != 3:
        print("Usage: python video_editor.py <input_video> <yaml_analysis_file>")
        print("Example: python video_editor.py recording.mp4 analysis_output.yaml")
        sys.exit(1)

    input_video = sys.argv[1]
    yaml_file = sys.argv[2]

    # Verify files exist
    if not os.path.exists(input_video):
        print(f"Error: Video file not found: {input_video}")
        sys.exit(1)

    if not os.path.exists(yaml_file):
        print(f"Error: YAML file not found: {yaml_file}")
        sys.exit(1)

    # Create editor and process
    editor = VideoEditor(input_video, yaml_file)

    try:
        results = editor.create_all()

        # Print summary
        print(f"\n=== Final Results ===")
        if results['main_edit']:
            print(f"Main Edit: {results['main_edit']}")
        if results['highlight_edit']:
            print(f"Highlight Edit: {results['highlight_edit']}")
        for short in results['shorts']:
            print(f"Short: {short}")

    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        editor.cleanup()

if __name__ == "__main__":
    main()
