import cv2
import numpy as np
from collections import deque
import time

# Define color ranges for the balls (HSV)
color_ranges = {
    'green': ([40, 40, 40], [70, 255, 255]) ,
    'white': ([0, 0, 200], [180, 30, 255]),
    'orange': ([5, 100, 100], [15, 255, 255]),
    'yellow': ([20, 100, 100], [30, 255, 255])
}

def rotate_frame(frame):
    return cv2.rotate(frame, cv2.ROTATE_180)


def detect_balls(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    balls = {}
    
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 500: 
                x, y, w, h = cv2.boundingRect(contour)
                balls[color] = (x + w // 2, y + h // 2) 
    
    return balls
    pass

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    
    quadrant_width = width // 4 +50
    quadrant_height = height // 2

    quadrants = {
    1: (150, 150+quadrant_width, 50, quadrant_height),
    2: (150+quadrant_width, 100+ 2 * quadrant_width, 50, quadrant_height),
    4: (150, 150+ quadrant_width, quadrant_height, 2 * quadrant_height),
    3: (150+ quadrant_width, 100+ 2 * quadrant_width, quadrant_height, 2 * quadrant_height)
    }
    
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_video.avi', fourcc, fps, (width, height))

    event_log = []
    previous_positions = {color: None for color in color_ranges.keys()}
    annotation_queue = deque(maxlen=50)  # Queue to store annotations with a fixed length

    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Rotate the frame
        frame = rotate_frame(frame)

        # Detect balls
        balls = detect_balls(frame)

        # Track movements and log events
        for color, pos in balls.items():
            prev_pos = previous_positions[color]
            for quadrant, (x1, x2, y1, y2) in quadrants.items():
                if x1 < pos[0] < x2 and y1 < pos[1] < y2:
                    if prev_pos is None or not (x1 < prev_pos[0] < x2 and y1 < prev_pos[1] < y2):
                        # Log entry event
                        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                        event_log.append((timestamp, quadrant, color, 'Entry'))
                        annotation_queue.append((time.time(), timestamp, quadrant, color, 'Entry'))
                    previous_positions[color] = pos
                elif prev_pos is not None and x1 < prev_pos[0] < x2 and y1 < prev_pos[1] < y2:
                    # Log exit event
                    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    event_log.append((timestamp, quadrant, color, 'Exit'))
                    annotation_queue.append((time.time(), timestamp, quadrant, color, 'Exit'))
                    previous_positions[color] = None

        # Annotate balls with color
        for color, pos in balls.items():
            cv2.circle(frame, pos, 10, (255, 0, 0), -1)
            cv2.putText(frame, color, (pos[0] - 10, pos[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Annotate quadrants with entry/exit and timestamps
        current_time = time.time()
        annotation_queue = deque([(t, ts, q, c, e) for t, ts, q, c, e in annotation_queue if current_time - t < 1])  # Keep annotations for 1 second

        for t, timestamp, quadrant, color, event in annotation_queue:
            x1, x2, y1, y2 = quadrants[quadrant]
            cv2.putText(frame, f"{color} {event} at {timestamp:.2f}s", ((x1 + x2) // 2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Write the frame to the output video
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    # Save the event log to a text file
    with open('event_log.txt', 'w') as f:
        f.write("Time, Quadrant, Color, Event Type\n")
     
    
