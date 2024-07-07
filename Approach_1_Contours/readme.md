
## Approach 1

This document outlines the video processing approach implemented in the application for detecting colored balls, tracking their movements across predefined quadrants, and logging entry and exit events. The application uses OpenCV for computer vision tasks and Flask for web interface integration.

## Overview
The video processing approach involves several key steps:

Video Input: The application accepts a video file (*.mp4 format) uploaded by the user through a web interface.

Frame Rotation: Each frame of the video is rotated 180 degrees to adjust for any potential orientation issues.

Ball Detection: Using the HSV color space, the application detects colored balls (green, white, orange, yellow) within each frame. This is achieved by applying color thresholding and contour detection techniques.

Quadrant Tracking: The video frame is divided into four predefined quadrants. The application tracks the movement of each detected ball across these quadrants.

Event Logging: Entry and exit events of balls in each quadrant are logged based on their movement between frames.

Output Generation: The processed video with annotated balls and event timestamps, along with an event log file (event_log.txt), are generated as output.

## Functions
rotate_frame(frame): Rotates a given frame by 180 degrees.
detect_balls(frame): Detects colored balls (green, white, orange, yellow) within a given frame using HSV color space.
process_video(video_path): Processes the entire video file by iterating through its frames, applying ball detection and quadrant tracking, and logging events.

## Limitations

This is a basic rudimentary apprach to detection and tracking of balls. Due to the backgorund being white, this apprach often incorrectly classifies the backgrouns as white coloured balls which tampers with the event record. In addition, specifying colour ranges also lead to confusion where skin was detected as orange. 
