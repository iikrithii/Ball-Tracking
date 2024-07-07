import cv2
import numpy as np
import time
import sys
import os

# Constants
WIDTH = 416
HEIGHT = 416
THRESHOLD_SCORE = 0.45
THRESHOLD_NMS = 0.70
THRESHOLD_CONFIDENCE = 0.60

# Text parameters
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 0.9
TEXT_THICKNESS = 2

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

# Quadrant Constants
QUADRANT_WIDTH = 539
QUADRANT_HEIGHT = 560

# Quadrant Definitions
QUADRANT_AREAS = {
    "1": ((0, QUADRANT_WIDTH), (0, QUADRANT_HEIGHT)),
    "2": ((QUADRANT_WIDTH, 2 * QUADRANT_WIDTH), (0, QUADRANT_HEIGHT)),
    "3": ((QUADRANT_WIDTH, 2 * QUADRANT_WIDTH), (QUADRANT_HEIGHT, 2 * QUADRANT_HEIGHT)),
    "4": ((0, QUADRANT_WIDTH), (QUADRANT_HEIGHT, 2 * QUADRANT_HEIGHT))
}

# Initial Ball Info
BALL_TRACKING = {
    "1": {"previous_state": 0, "current_state": 0, "time": " ", "color": " "},
    "2": {"previous_state": 0, "current_state": 0, "time": " ", "color": " "},
    "3": {"previous_state": 0, "current_state": 0, "time": " ", "color": " "},
    "4": {"previous_state": 0, "current_state": 0, "time": " ", "color": " "}
}

BALL_DATA = []  # Store all information
save_initial_frame = True
second = 0
frame_counter = 0

# List of class names
class_names = ["Green", "Orange", "White", "Yellow"]

# Function to draw text on the image
def draw_text(image, text, x, y):
    text_size = cv2.getTextSize(text, TEXT_FONT, TEXT_SCALE, TEXT_THICKNESS)
    dimensions, baseline = text_size[0], text_size[1]
    cv2.rectangle(image, (x, y), (x + dimensions[0], y + dimensions[1] + baseline), (255, 255, 255), cv2.FILLED)  # white background
    cv2.putText(image, text, (x, y + dimensions[1]), TEXT_FONT, TEXT_SCALE, (0, 0, 0), TEXT_THICKNESS, cv2.LINE_AA)  # black text

# Function to find the quadrant of a point
def get_quadrant(x, y):
    for q, (x_range, y_range) in QUADRANT_AREAS.items():
        if x in range(x_range[0], x_range[1]) and y in range(y_range[0], y_range[1]):
            return q
    return None

# Function to check the ball state in the quadrants
def update_ball_state(frame, initial_frame, ball_tracking):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    quadrant_frames = [
        frame_gray[0:QUADRANT_HEIGHT, 0:QUADRANT_WIDTH],
        frame_gray[0:QUADRANT_HEIGHT, QUADRANT_WIDTH:2*QUADRANT_WIDTH],
        frame_gray[QUADRANT_HEIGHT:2*QUADRANT_HEIGHT, QUADRANT_WIDTH:2*QUADRANT_WIDTH],
        frame_gray[QUADRANT_HEIGHT:2*QUADRANT_HEIGHT, 0:QUADRANT_WIDTH]
    ]
    
    for i in ball_tracking.keys():
        ih, iw = initial_frame[int(i)-1].shape[:2]
        diff = cv2.subtract(initial_frame[int(i)-1], quadrant_frames[int(i)-1])
        err = np.sum(diff**2)
        mse = err / (float(ih * iw))
        
        if mse < 5:
            ball_tracking[i]["current_state"] = 0
        else:
            ball_tracking[i]["current_state"] = 1
    
    return ball_tracking

# Function to preprocess the input image and postprocess detections
def process_frame(input_image, model_net, initial_frame, ball_tracking, frame_counter, second):
    # Preprocess
    blob = cv2.dnn.blobFromImage(input_image, 1/255, (WIDTH, HEIGHT), [0, 0, 0], 1, crop=False)
    model_net.setInput(blob)
    outputs = model_net.forward(model_net.getUnconnectedOutLayersNames())
    
    # Postprocess
    bounding_boxes = []
    class_ids = []
    confidences = []
    scaling_factor = 2.59615384615  # value to convert pixel value from frame size 416 to 1080
    outputs = np.transpose(outputs[0][0])  # shape (8, 3549) to shape (3549,8)
    
    for row in outputs:
        box = row[:4]
        class_scores = row[4:]
        
        for i in range(4):
            if class_scores[i] >= THRESHOLD_SCORE:
                class_ids.append(class_names[i])
                confidences.append(class_scores[i])
                bounding_boxes.append(box)
                
    indices = cv2.dnn.NMSBoxes(bounding_boxes, confidences, THRESHOLD_CONFIDENCE, THRESHOLD_NMS)
    
    for i in indices:
        box = bounding_boxes[i]
        color = class_ids[i]
        
        center_x, center_y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cx = int(center_x * scaling_factor) 
        cy = int(center_y * scaling_factor)
        radius = int((w + h) / 4 * scaling_factor)
        
        cv2.circle(input_image, (cx, cy), radius, COLOR_BLUE, 2)
        
        quadrant_num = get_quadrant(cx, cy)
        
        ball_tracking[quadrant_num]["color"] = color
        ball_tracking = update_ball_state(input_image, initial_frame, ball_tracking)
        
        label = f"Color:{color} Q:{quadrant_num}"
        draw_text(input_image, label, cx - radius, cy - radius)
        
        if frame_counter == 30:
            ball_tracking = update_ball_state(input_image, initial_frame, ball_tracking)
            
            for j in ball_tracking.keys():
                if ball_tracking[j]["previous_state"] != ball_tracking[j]["current_state"] and ball_tracking[j]["color"] != " ":
                    if ball_tracking[j]["current_state"] == 1:
                        x, y = QUADRANT_AREAS[j][0][0] + 20, QUADRANT_AREAS[j][1][0] + 40
                        
                        BALL_DATA.append([second, j, ball_tracking[j]["color"], "Entry"])
                        draw_text(input_image, f"{ball_tracking[j]['color']} Ball Entered at {second}", x, y)
                    else:
                        x, y = QUADRANT_AREAS[j][0][0] + 20, QUADRANT_AREAS[j][1][0] + 40
                        
                        BALL_DATA.append([second, j, ball_tracking[j]["color"], "Exit"])
                        draw_text(input_image, f"{ball_tracking[j]['color']} Ball Exit at {second}", x, y)
                    
                    ball_tracking[j]["previous_state"] = ball_tracking[j]["current_state"]
    
    return input_image, ball_tracking

# Function to save the initial frame
def save_initial_frame_func(frame):
    iframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    quadrant_frames = [
        iframe[0:QUADRANT_HEIGHT, 0:QUADRANT_WIDTH],
        iframe[0:QUADRANT_HEIGHT, QUADRANT_WIDTH:2*QUADRANT_WIDTH],
        iframe[QUADRANT_HEIGHT:2*QUADRANT_HEIGHT, QUADRANT_WIDTH:2*QUADRANT_WIDTH],
        iframe[QUADRANT_HEIGHT:2*QUADRANT_HEIGHT, 0:QUADRANT_WIDTH]
    ]
    return quadrant_frames

# Video capture and model loading
def main(input_video_path):
    video_capture = cv2.VideoCapture(input_video_path)
    model_path = "weights.onnx"
    net = cv2.dnn.readNet(model_path)

    base_name = os.path.splitext(os.path.basename(input_video_path))[0]
    output_video_path = f"{base_name}_output.avi"
    info_text_path = f"{base_name}_info.txt"

    file_data = open(info_text_path, "w")
    file_data.write("Time, Quadrant, Color, Event Type\n")
    file_data.close()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter(output_video_path, fourcc, 30, (1080, 1030))

    while cv2.waitKey(1) < 1:
        frame_exists, input_frame = video_capture.read()
        second = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
        
        if not frame_exists:
            break
        
        rotated_image = cv2.rotate(input_frame, cv2.ROTATE_180)

        # Crop the rotated image to focus on the quadrant area
        height, width = rotated_image.shape[:2]
        input_frame = rotated_image[50:1130, 150:1230]
        
        frame_height, frame_width = input_frame.shape[:2]
        start = time.time()
        
        if save_initial_frame:
            initial_frame = save_initial_frame_func(input_frame)
            save_initial_frame = False
        
        output_frame, BALL_TRACKING = process_frame(input_frame.copy(), net, initial_frame, BALL_TRACKING, frame_counter, second)

        if frame_counter == 30:
            frame_counter = 0
        
        frame_counter += 1
        end = time.time()
        
        output_video.write(output_frame)
        
        if BALL_DATA:
            with open(info_text_path, 'a') as file:
                for row in BALL_DATA:
                    file.write(",".join(map(str, row)) + "\n")
            
            BALL_DATA.clear()
    
    video_capture.release()
    output_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python video_processing_script.py <input_video_path>")
        sys.exit(1)
    
    input_video_path = sys.argv[1]
    main(input_video_path)
