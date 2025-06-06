# Real-time Object Detection Web Application

A Flask-based web application that performs real-time object detection using YOLOv8 and streams the results to a web interface.

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd <your-project-directory>
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```


## Project Structure

```
your-project/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── yolo-Weights/
│   └── yolov8n.pt        # YOLO model weights
├── templates/
│   └── index.html        # Web interface template
└── README.md            # Project documentation
```

## Usage

1. **Start the application**
   ```bash
   export FLASK_APP=app
   export FLASK_ENV=development
   flask run
   ```
   Open the link in the terminal

2. **View real-time detection**
   - The application will start streaming your webcam feed
   - Detected objects will be highlighted with bounding boxes and labels


## Customization

### Changing Camera Source
To use a different camera or video file:
```python
cap = cv2.VideoCapture(1)  # Use camera index 1
cap = cv2.VideoCapture('path/to/video.mp4')  # Use video file
```


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request


