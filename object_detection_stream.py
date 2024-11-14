import cv2
import torch
from flask import Flask, Response

# Initialize Flask application
app = Flask(__name__)

# Load the pre-trained YOLOv5 model (you can replace 'yolov5n' with other models like 'yolov5s' or 'yolov5m')
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # You can change 'yolov5n' to 'yolov5s' or 'yolov5m'

# Open the camera (0 for the default camera, or you can try 1, 2, etc. if you have external cameras)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Function to generate video frames for streaming
def gen():
    while True:
        ret, frame = cap.read()  # Read frame from camera
        if not ret:
            break

        # Perform YOLOv5 inference on the frame
        results = model(frame)  # Inference (YOLOv5 object detection)

        # Render bounding boxes and labels on the frame
        frame = results.render()[0]  # results.render() returns a list of frames with annotations

        # Convert frame to JPEG format to send over HTTP
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_data = jpeg.tobytes()

        # Yield the JPEG frame as part of an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

# Route to stream video
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Main entry point for the Flask app
if __name__ == '__main__':
    print("Starting the Flask server... (http://172.16.35.35:5000)")
    app.run(host='0.0.0.0', port=5000)  # Host on all IPs (0.0.0.0) and use port 5000
