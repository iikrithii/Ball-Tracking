# Video Processing Application
## Overview
This approach is designed to better track the movements across quadrants, and log their entry and exit events. The application uses OpenCV for video processing and object detection, leveraging a pre-trained ONNX model that uses YOLOv8 for object detection. 

The final output video is [available here](https://drive.google.com/file/d/1cYOevexaT0l6v3qxd93p4aKkKvX9UCu-/view?usp=sharing)
The output event log file can he accessed [here](https://github.com/iikrithii/Ball-Tracking/blob/main/Approach_2_YOLO/info.txt)

## Requirements
Python 3.x
OpenCV
NumPy
ONNX Runtime

## Installation

### Clone the Repository:
git clone [https://github.com/iikrithii/Ball-Tracking.git](https://github.com/iikrithii/Ball-Tracking.git)

cd Approach_2_YOLO

### Install Dependencies:
pip install opencv-python-headless numpy onnxruntime

### Run the Script:
python video_processing_script.py <input_video_path>
Replace <input_video_path> with the path to your input video file.

The script will produce two output files in the same directory:
>input_video_output.avi: Processed video with detected balls and annotations.
>
>input_video_info.txt: Log file with entry and exit events of the balls.

## Script Description

draw_text(image, text, x, y):Draws a rectangle with text on the image at the specified (x, y) coordinates.

get_quadrant(x, y): Determines the quadrant of a point (x, y) based on predefined quadrant areas.

update_ball_state(frame, initial_frame, ball_tracking): Updates the ball's state in the quadrants based on the frame's gray-scale differences.

process_frame(input_image, model_net, initial_frame, ball_tracking, frame_counter, second): Processes the input frame, detects balls, and updates their state and position.

save_initial_frame_func(frame): Saves the initial frame for comparison purposes.

main(input_video_path): Main function to handle video processing.

## Approach
Video Capture: The script captures video frames from the specified input video file.
Initial Frame Saving: The initial frame is saved and divided into quadrants for comparison.
Frame Processing: Each frame is processed to detect balls using the ONNX model.
Ball State Update: The state of balls in each quadrant is updated based on frame differences.
Annotation: Detected balls are annotated on the video with their color and quadrant information.
Logging: Entry and exit events of balls are logged to a text file.
Output: The processed video and log file are saved to the disk.

## Advantages
Real-time Processing: Efficiently processes video frames in real-time.
Detailed Logging: Provides detailed logs of ball movements and events.
Customizable: Easily customizable to detect different colors or objects.
Background and Motion Tracking: Using a Pre-trained Yolov8 helps in accurately identifying balls

## Future Improvements
The tracking and detecting still seems to be faulty in a few places and needs further state detection improvement, and motion detection parameters to enhance its accuracy. 
