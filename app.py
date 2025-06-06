from flask import Flask, Response, flash, redirect, render_template, request, url_for
import cv2
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages
app.config['UPLOAD_FOLDER'] = 'assets'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'}

model = YOLO("yolo-Weights/yolov8n.pt")

# Current video file path (global variable)
current_video_file = None

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_frames():
    global current_video_file
    
    # Check if there's a current video file
    if not current_video_file or not os.path.exists(current_video_file):
        return
    
    cap = cv2.VideoCapture(current_video_file)
    
    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error opening video file: {current_video_file}")
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            # If we reach the end of the video, restart it
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
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
                cv2.putText(frame, label_text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', has_video=current_video_file is not None)

@app.route('/upload', methods=['POST'])
def upload_video():
    global current_video_file
    
    if 'video' not in request.files:
        flash('No video file selected')
        return redirect(request.url)
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No video file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Remove previous video if exists
        if current_video_file and os.path.exists(current_video_file):
            try:
                os.remove(current_video_file)
            except:
                pass
        
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        current_video_file = filepath
        flash('Video uploaded successfully!')
    else:
        flash('Invalid file type. Please upload a video file (mp4, avi, mov, mkv, wmv, flv, webm)')
    
    return redirect(url_for('index'))

@app.route('/remove_video')
def remove_video():
    global current_video_file
    
    if current_video_file and os.path.exists(current_video_file):
        try:
            os.remove(current_video_file)
            current_video_file = None
            flash('Video removed successfully!')
        except:
            flash('Error removing video file')
    
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)