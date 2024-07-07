
# **Video Processing Web Application**

This web application allows users to upload a video file, detect colored balls within the video, track their movements across predefined quadrants, and log their entry and exit events. It utilizes OpenCV for video processing and Flask for the web interface.

## Directory Structure

>web-app/
>
>│
>
>├── templates/
>
>│   ├── index.html        # HTML template for uploading a video
>
>│   └── result.html       # HTML template for displaying processing results
>
>│
>
>├── app.py                # Flask application script
>
>├── video_processing.py   # Script containing video processing logic
>
>├── output_video.avi      # Processed output video file
>
>└── event_log.txt         # Event log file containing timestamps and events

## Description
app.py: Flask application script handling HTTP requests, video upload, and result rendering.

video_processing.py: Script containing video processing logic using OpenCV for ball detection, quadrant tracking, and event logging.

output_video.avi: Processed video file generated after uploading and processing a video.

event_log.txt: Text file logging event timestamps, quadrants, colors, and event types during video processing.

## Requirements
Python 3.x
Flask (pip install flask)
OpenCV (pip install opencv-python)


## How to Run

**Install Dependencies**:
pip install flask opencv-python

**Clone the Repository**:
git clone [https://github.com/iikrithii/Ball-Tracking.git](https://github.com/iikrithii/Ball-Tracking.git)
cd web-app

**Run the Flask Application**:
python app.py

**Access the Application**:
Open a web browser and go to http://localhost:5000. This will display the upload form (index.html).

**Upload a Video**:
Click on the "Choose File" button and select a video file (*.mp4 format).
Click on the "Upload" button to start processing the video.

**View Processing Results**:
Once the video processing is complete, you will be redirected to the result page (result.html).
The processed video with annotations and event log will be displayed.
You can download the event log by clicking on the provided link.

**Terminate the Application**:
Press Ctrl + C in the terminal where Flask is running to stop the application.

The current application uses a preliminary version of the video-processing, this can be upgraded later with improvements to the model

>Notes
>Ensure the video file uploaded is in *.mp4 format for compatibility with OpenCV.
