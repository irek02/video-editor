# Prompt for analyzing the timestamped transcript

**Analyze this timestamped transcript using the AI-Assisted Video Content Creation Guide. Output your analysis in YAML format in the output folder following this exact structure:**

```
# analysis_output.yaml
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

**Fill in all sections with specific timestamps from the transcript. For each timestamp, use the format HH:MM:SS (e.g., '00:15:30').
Here's my timestamped transcript.

Be specific with timestamps and provide clear reasoning for each editing decision.
