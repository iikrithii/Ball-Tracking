from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from video_processing import process_video

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_VIDEO = 'output_video.avi'
EVENT_LOG = 'event_log.txt'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'video_file' not in request.files:
            return redirect(request.url)
        
        video_file = request.files['video_file']
        
        if video_file.filename == '':
            return redirect(request.url)
        
        # Save the uploaded video file
        video_path = os.path.join(UPLOAD_FOLDER, 'input_video.mp4')
        video_file.save(video_path)
        
        # Process the video
        process_video(video_path)
        
        # Return result page
        return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', output_video=OUTPUT_VIDEO, event_log=EVENT_LOG)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
