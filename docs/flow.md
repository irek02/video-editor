# Flow for processing the video

The flow:

1. I record the video in ScreenFlow and export it as `assets/[project_name]/original.mp4`
2. AI trims silence via the below command and output to `trimmed.mp4` in the same subfolder:

    ```sh
    docker run --rm -v $(pwd)/assets/[project_name]:/workspace my-auto-editor original.mp4 --margin 0.2s -o trimmed.mp4
    ```

3. I extract timestamped transcript from `trimmed.mp4` using Whisper Transcription app on Mac and save as `transcript.txt` in the same subfolder
4. AI uses `docs/prompt.md` to generate the analysis YAML file and put it in the same subfolder as `analysis.yaml`
5. AI executes the `video_editor.py` script to process `trimmed.mp4` using `analysis.yaml` and output the final videos in the same subfolder

    ```sh
    python3 video_editor.py assets/[project_name]/trimmed.mp4 assets/[project_name]/analysis.yaml
    ```

---

All assets for a single video project are kept together in a dedicated subfolder under `assets/`, which is git-ignored. This keeps your workspace organized and prevents clutter as you work on more videos.
