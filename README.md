# Real-time Object Detection Web Application

A Flask-based web application that performs real-time object detection using YOLOv8 and streams the results to a web interface.

## Features

- **Real-time Detection**: Live object detection using your webcam
- **Web Interface**: Stream detection results directly to your browser
- **YOLOv8 Integration**: Utilizes the latest YOLO model for accurate object detection
- **Bounding Boxes**: Visual representation of detected objects with labels
- **Multi-object Detection**: Capable of detecting multiple objects simultaneously

## Technologies Used

- **Flask**: Web framework for Python
- **OpenCV**: Computer vision library for image processing
- **Ultralytics YOLOv8**: State-of-the-art object detection model
- **HTML/CSS**: Frontend for the web interface

## Prerequisites

Before running this application, make sure you have:

- Python 3.7 or higher
- A working webcam/camera
- Required Python packages (see Installation section)

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

4. **Download YOLO weights**
   - Create a `yolo-Weights` directory in your project root
   - Download the YOLOv8 nano model weights (`yolov8n.pt`) from [Ultralytics](https://github.com/ultralytics/ultralytics)
   - Place the weights file in the `yolo-Weights` directory

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
├── static/               # Static files (CSS, JS, images)
└── README.md            # Project documentation
```

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://localhost:5000`
   - Allow camera permissions when prompted

3. **View real-time detection**
   - The application will start streaming your webcam feed
   - Detected objects will be highlighted with bounding boxes and labels

## How It Works

1. **Camera Capture**: The application captures frames from your default camera using OpenCV
2. **Object Detection**: Each frame is processed through the YOLOv8 model to detect objects
3. **Visualization**: Detected objects are marked with bounding boxes and class labels
4. **Streaming**: Processed frames are streamed to the web browser in real-time using Flask's Response streaming

## API Endpoints

- `GET /`: Main page that displays the web interface
- `GET /video_feed`: Video stream endpoint that provides the processed camera feed

## Customization

### Using Different YOLO Models
You can use different YOLO models by changing the model path in `app.py`:
```python
model = YOLO("yolo-Weights/yolov8s.pt")  # Small model
model = YOLO("yolo-Weights/yolov8m.pt")  # Medium model
model = YOLO("yolo-Weights/yolov8l.pt")  # Large model
```

### Adjusting Detection Parameters
Modify detection confidence and other parameters:
```python
results = model(frame, conf=0.5, iou=0.45)  # Adjust confidence threshold
```

### Changing Camera Source
To use a different camera or video file:
```python
cap = cv2.VideoCapture(1)  # Use camera index 1
cap = cv2.VideoCapture('path/to/video.mp4')  # Use video file
```

## Troubleshooting

### Common Issues

1. **Camera not detected**
   - Ensure your camera is properly connected
   - Try changing the camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

2. **Model weights not found**
   - Verify the path to your YOLO weights file
   - Ensure the weights file is properly downloaded

3. **Poor detection performance**
   - Try using a larger YOLO model (yolov8s, yolov8m, yolov8l)
   - Adjust the confidence threshold
   - Ensure good lighting conditions

4. **Slow performance**
   - Use a smaller model (yolov8n) for faster inference
   - Consider reducing the input frame size

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ultralytics](https://ultralytics.com/) for the YOLOv8 model
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework

## Contact

For questions or support, please open an issue in the repository or contact [your-email@example.com].

---

**Note**: Make sure to replace placeholder URLs and contact information with your actual project details.