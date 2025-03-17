import re
import os
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)  # Allow requests from your Expo app

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_service_tag(result):
    """Extracts only the 7-character service tag from OCR results."""
    if result and len(result) > 0:
        full_text = ' '.join([line[1][0] for line in result[0] if line and len(line) >= 2])
        match = re.search(r'\b[A-Z0-9]{7}\b', full_text)
        if match:
            return match.group(0)
    return None

def capture_frame():
    """Captures a frame from the webcam and returns it."""
    cap = cv2.VideoCapture(0)  # Use 0 for default camera
    if not cap.isOpened():
        raise Exception("Error: Could not open camera")
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception("Error: Could not read frame.")
    
    return frame

@app.route("/")
def home():
    return "Service Tag OCR API is running."

@app.route("/capture", methods=["GET"])
def capture():
    try:
        frame = capture_frame()
        img_path = "./temp.jpg"
        cv2.imwrite(img_path, frame)  # Save frame as an image

        # Perform OCR on the image
        result = ocr.ocr(img_path, cls=True)
        service_tag = extract_service_tag(result)
        
        # Clean up the temp image
        os.remove(img_path)
        
        return jsonify({"service_tag": service_tag if service_tag else "Not Found"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(debug=True, host="0.0.0.0", port=port)

