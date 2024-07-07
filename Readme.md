# Assignment: Ball Tracking and Detection 

Task:
Create a program using Computer Vision to track the movement of the balls of different colors across various quadrants in the video provided. The program should record the event of each ball entering and exiting each numbered quadrant. The event data should be recorded in the below format.
Time, Quadrant Number, Ball Colour, Type (Entry or Exit)
Timestamp: consider start of the video as 0 seconds and compute timestamp based on video duration.
The program should have provisions for feeding a new video and output should be saved in the local hard disk. Details of which need to be shared at the time of submission.

Video to process:
https://drive.google.com/file/d/1goI3aHVE29Gko9lpTzgi_g3CZZPjJq8w/view?usp=sharing

Output expected:
The model you create should take the video as input and give the below output

Processed Video:
The processed video should incorporate the following.
Ball tracking with color
Overlay text “Entry or Exit” & time stamp at the time of entry/exit of a numbered quadrant
Text File:
Text file with records in the format provided above (Time, Quadrant Number, Ball Colour, Event Type (Entry or Exit))

Two approaches were followed: One with [Contour Detection](https://github.com/iikrithii/Ball-Tracking/blob/main/Approach_1_Contours/readme.md), and second using a pretrained [YOLOv8 model](https://github.com/iikrithii/Ball-Tracking/blob/main/Approach_2_YOLO/readme.md). A simple [Web application](https://github.com/iikrithii/Ball-Tracking/blob/main/web-app/readme.md) was also created for enhanced user interface

The final output video is [available here](https://drive.google.com/file/d/1cYOevexaT0l6v3qxd93p4aKkKvX9UCu-/view?usp=sharing).
The output event log file can be accessed [here](https://github.com/iikrithii/Ball-Tracking/blob/main/Approach_2_YOLO/info.txt).
