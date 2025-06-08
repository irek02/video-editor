# Flow for processing the video

The flow:

1. record the video in ScreenFlow
2. export the video to mp4
3. trim silence via the below command and

    ```sh
    cd ~/Documents/youtube_series
    docker run --rm -v $(pwd):/workspace my-auto-editor home-booking-new.mp4 --margin 0.2s
    ```

4. extract timestamped transcript from the trimmed video using Whisper Transcription and place it in the input folder as txt file
5. use docs/promt.md to have the AI to generate the analisys yaml file and put it in the input folder
6. have the AI execute the video_editor.py script process the trimmed video and output processed video in the ouput folder
