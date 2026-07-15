import cv2
import numpy as np
import random
from datetime import datetime

def apply_bw_filter(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast
    f_frame = gray.astype(np.float32)
    f_frame = f_frame * 1.2 - 10
    filtered = np.clip(f_frame, 0, 255).astype(np.uint8)
    
    # Convert back to BGR so we can add colored borders if needed
    return cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)

def add_polaroid_border(frame, quote, date_str):
    height, width, _ = frame.shape
    
    # Border sizes proportional to image size
    top = int(height * 0.05)
    bottom = int(height * 0.25)  # Thicker bottom for polaroid look
    left = int(width * 0.05)
    right = int(width * 0.05)
    
    # White border color
    border_color = [245, 245, 245] # Slightly off-white for vintage feel
    
    # Add border using cv2.copyMakeBorder
    polaroid_img = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)
    
    # Add text to the bottom border
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (50, 50, 50)  # Dark gray text
    
    # Date text at bottom right
    cv2.putText(polaroid_img, date_str, (width + left - 100, height + top + 30), font, 0.5, color, 1, cv2.LINE_AA)
    
    # Quote text at bottom center (approximate)
    text_size = cv2.getTextSize(quote, font, 0.6, 1)[0]
    text_x = left + (width - text_size[0]) // 2
    text_y = height + top + int(bottom * 0.6)
    cv2.putText(polaroid_img, quote, (text_x, text_y), font, 0.6, color, 1, cv2.LINE_AA)
    
    return polaroid_img

def main():
    quotes = [
        "Smile! You're on camera.",
        "A picture is worth a thousand words.",
        "Capturing the moment...",
        "Just be yourself!",
        "Memories in black and white.",
        "Vintage vibes.",
        "Say cheese!"
    ]
    selected_quote = random.choice(quotes)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Load the pre-trained Haar Cascade face classifier
    # cv2.data.haarcascades points to the path where haarcascade xml files are stored
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Open the default webcam (0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
        
    print("Webcam started. Press 'q' on the keyboard to quit.")
    
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
            
        # Flip the frame horizontally (mirror effect) for intuitive interaction
        frame = cv2.flip(frame, 1)
            
        # Convert the original frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Blur the background
        blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
        mask = np.zeros_like(frame, dtype=np.uint8)
        
        # Create a mask for faces to keep them sharp
        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            axes = (int(w*0.6), int(h*0.8))  # elliptical mask around face
            cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)
            
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        mask_f = mask.astype(np.float32) / 255.0
        
        frame_f = frame.astype(np.float32)
        blurred_f = blurred_frame.astype(np.float32)
        
        # Blend the sharp face and blurred background
        blended = (frame_f * mask_f + blurred_f * (1.0 - mask_f)).astype(np.uint8)
        
        # Apply the black and white filter to the blended frame
        filtered_frame = apply_bw_filter(blended)
        
        # Draw rectangles around the detected faces on the filtered frame
        for (x, y, w, h) in faces:
            cv2.rectangle(filtered_frame, (x, y), (x+w, y+h), (200, 200, 200), 2)
            cv2.putText(filtered_frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            
        # Add the physical polaroid-style border with text
        final_output = add_polaroid_border(filtered_frame, selected_quote, current_date)
        
        # Display the result in a window
        cv2.imshow('Real-time Polaroid Face Detector', final_output)
        
        # Wait for 1 ms and check if the 'q' key is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
