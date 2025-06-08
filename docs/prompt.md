# AI Analysis Prompt for Video Editing

## Instructions

For each video project, all assets (original, trimmed, transcript, YAML, outputs) are stored in a dedicated subfolder under the `assets/` directory (which is git-ignored). For example: `assets/home-booking-new/`.

- By the time you use this prompt, the exported mp4 (`original.mp4`) and the transcript (`transcript.txt`) are already present in the subfolder.
- Your task is to analyze the transcript and generate the analysis YAML file (`analysis.yaml`) in the same subfolder.
- The output videos should also be saved in the same subfolder.

This structure keeps all files for a single project together and prevents workspace clutter.

---

## Example YAML Analysis File

**Analyze this timestamped transcript using the AI-Assisted Video Content Creation Guide. Output your analysis in YAML format in the input folder following this exact structure:**

```
# analysis_output_[video_name].yaml
video_info:
  app_type: ""
  duration: ""
  final_outcome: ""

main_edit:
  target_length: "35-45 minutes"
  keep_segments:
    - start: "00:00:00"
      end: "00:00:00"
      reason: ""
      title: "" # will be shown during segment transition in the video
      priority: "high/medium/low"

  speed_up_segments:
    - start: "00:00:00"
      end: "00:00:00"
      speed: "2x"
      title: ""
      reason: ""

  cut_segments:
    - start: "00:00:00"
      end: "00:00:00"
      reason: ""

highlight_edit:
  target_length: "15-20 minutes"
  segments:
    - name: "Setup & Planning"
      start: "00:00:00"
      end: "00:00:00"
      title: ""
      description: ""
    - name: "Key Development"
      start: "00:00:00"
      end: "00:00:00"
      title: ""
      description: ""

shorts:
  - title: ""
    hook: ""
    segments:
      - start: "00:00:00"
        end: "00:00:00"
        description: ""
    text_overlays:
      - text: ""
        timing: "00:00:00-00:00:00"
    estimated_engagement: "high/medium/low"

seo_suggestions:
  main_video_titles:
    - ""
  highlight_titles:
    - ""
  thumbnail_moments:
    - timestamp: "00:00:00"
      description: ""

key_learnings:
  technical_insights: []
  ai_capabilities_shown: []
  human_intervention_points: []
```

**CRITICAL TIMESTAMP FORMAT REQUIREMENT:**

- ALL timestamps MUST use the exact format HH:MM:SS with leading zeros
- For videos under 1 hour, always use 00:MM:SS format (e.g., '00:15:30', NOT '15:30:00')
- Examples: '00:05:07', '00:31:59', '00:42:11'
- NEVER use MM:SS:SS format as it will cause video processing errors

**Fill in all sections with specific timestamps from the transcript following the HH:MM:SS format above.
Here's my timestamped transcript.

Be specific with timestamps and provide clear reasoning for each editing decision.**
