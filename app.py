# app.py
from flask import Flask, Response, flash, redirect, render_template, request, url_for
import cv2
from ultralytics import YOLO
import os
import time # Import time for timestamp
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Get SECRET_KEY from environment variable, provide a fallback for local dev
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-default-key-for-dev')
app.config['UPLOAD_FOLDER'] = 'assets'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'}

# --- Ensure necessary directories exist ---
# Railway will automatically create this if it's written to, but explicit creation is good practice
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# The yolo-Weights folder should be part of your Git repository


model = YOLO("yolo-Weights/yolov8n.pt")

# Current video file path (global variable)
current_video_file = None # This will store the *absolute* path on the server


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_frames():
    global current_video_file
    
    # Check if there's a current video file
    # This check is crucial for Railway's ephemeral storage:
    # If the app restarts, current_video_file might still point to a path
    # but the file might be gone.
    if not current_video_file or not os.path.exists(current_video_file):
        # Optionally flash an error here or log it if no video is found
        # flash('No video uploaded or video not found.', 'error') # Cannot flash from generator
        print("No current video file or file not found. Returning empty frames.")
        return # Return empty generator if no valid video

    cap = cv2.VideoCapture(current_video_file)
    
    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error opening video file: {current_video_file}. Might be corrupted or not present.")
        # Attempt to reset current_video_file if it's truly not available
        current_video_file = None
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            # If we reach the end of the video, restart it
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue # Continue to read the first frame again
        
        # Perform object detection
        results = model(frame, stream=True)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                confidence = float(box.conf[0])
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label with confidence
                label_text = f"{label}: {confidence:.2f}"
                # Adjust text position if it goes off-screen
                text_x = x1
                text_y = y1 - 10
                if text_y < 10: # Ensure text is not too high
                    text_y = y1 + 20 # Place below if too high
                if text_x < 0: # Ensure text is not too far left
                    text_x = 0
                
                cv2.putText(frame, label_text, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2) # Reduced font size for better fit
        
        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Pass whether a video is currently loaded to the template
    return render_template('index.html', has_video=current_video_file is not None and os.path.exists(current_video_file))

@app.route('/upload', methods=['POST'])
def upload_video():
    global current_video_file
    
    if 'video' not in request.files:
        flash('No video file selected', 'error') # Use 'error' category for red flash
        return redirect(request.url)
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No video file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Remove previous video if exists
        if current_video_file and os.path.exists(current_video_file):
            try:
                os.remove(current_video_file)
            except Exception as e:
                print(f"Error removing old video: {e}")
                # Don't flash an error here, as it might not be critical if new file saves
        
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time())) # Using time for timestamp
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}" # Unique filename
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        current_video_file = filepath # Update global variable
        flash('Video uploaded successfully!', 'success') # Use 'success' category for green flash
    else:
        flash('Invalid file type. Please upload a video file (mp4, avi, mov, mkv, wmv, flv, webm)', 'error')
    
    return redirect(url_for('index'))

@app.route('/remove_video')
def remove_video():
    global current_video_file
    
    if current_video_file and os.path.exists(current_video_file):
        try:
            os.remove(current_video_file)
            current_video_file = None
            flash('Video removed successfully!', 'success')
        except Exception as e:
            print(f"Error removing video file: {e}")
            flash('Error removing video file', 'error')
    else:
        flash('No video to remove.', 'error') # Added message if no video is present
    
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Flask's built-in server is for development only.
    # For production, Railway will use a WSGI server like Gunicorn.
    # You generally don't need to change this block for Railway unless
    # you want to test Gunicorn locally (e.g., gunicorn -w 4 app:app).
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))