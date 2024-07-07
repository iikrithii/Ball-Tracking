

This document outlines the video processing approach implemented in the application for detecting colored balls, tracking their movements across predefined quadrants, and logging entry and exit events. The application uses OpenCV for computer vision tasks and Flask for web interface integration.

Overview
The video processing approach involves several key steps:

Video Input: The application accepts a video file (*.mp4 format) uploaded by the user through a web interface.

Frame Rotation: Each frame of the video is rotated 180 degrees to adjust for any potential orientation issues.

Ball Detection: Using the HSV color space, the application detects colored balls (green, white, orange, yellow) within each frame. This is achieved by applying color thresholding and contour detection techniques.

Quadrant Tracking: The video frame is divided into four predefined quadrants. The application tracks the movement of each detected ball across these quadrants.

Event Logging: Entry and exit events of balls in each quadrant are logged based on their movement between frames.

Output Generation: The processed video with annotated balls and event timestamps, along with an event log file (event_log.txt), are generated as output.

Functions
rotate_frame(frame)
Description: Rotates a given frame by 180 degrees.
Usage: Ensures consistent orientation of video frames for processing.
detect_balls(frame)
Description: Detects colored balls (green, white, orange, yellow) within a given frame using HSV color space.
Usage: Applies color thresholding and contour detection to identify balls.
process_video(video_path)
Description: Processes the entire video file by iterating through its frames, applying ball detection and quadrant tracking, and logging events.
Usage: Integrates rotate_frame() and detect_balls() functions to process each frame sequentially.
upload() and result()
Description: Handles file upload and result rendering through Flask routes (/upload, /result).
Usage: Manages user interaction, file handling, and output display using HTML templates (index.html, result.html).
Limitations
While effective for basic applications, this video processing approach has limitations: