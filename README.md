# Abandoned Baggage Detection System

![Project Badge](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Screenshots](#screenshots)
4. [Architecture](#architecture)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Technologies Used](#technologies-used)
8. [Future Enhancements](#future-enhancements)
9. [Contributing](#contributing)
10. [License](#license)

---

## Overview
The **Abandoned Baggage Detection System** is an AI-powered surveillance solution designed to automatically detect unattended or abandoned baggage in public areas such as airports, train stations, and shopping malls. Leveraging **computer vision** and **deep learning**, the system monitors live video feeds, detects objects, and tracks individuals in real-time, ensuring timely alerts and increased security.  

---

## Features
- Real-time video processing and object detection  
- Identification of abandoned or unattended baggage  
- Automatic tracking of people near detected objects  
- Alerts for security personnel  
- Scalable for multiple camera feeds  

---

## Screenshots
### Real-Time Detection
![Detection Example 1](https://github.com/VANSH-ml/Abandoned-Baggage-Detection-Using-Computer-visiom/blob/main/Screenshot%202025-07-02%20191538.png)

### Tracking Individuals
![Detection Example 2](./images/detection2.jpg)

---

## Architecture
The system uses a **YOLOv8/ Faster R-CNN** object detection model (can be customized) to identify bags and persons. The workflow:  
1. **Video Capture** → Collect live feed from CCTV cameras  
2. **Object Detection** → Detect baggage and humans  
3. **Tracking** → Track individuals near detected objects  
4. **Alert Generation** → Trigger alert if baggage is unattended  

![Architecture Diagram](./images/architecture.jpg)

---

## Installation
1. Clone the repository:  
```bash
git clone https://github.com/yourusername/abandoned-baggage-detection.git
cd abandoned-baggage-detection
Create a virtual environment and activate:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Run the main detection script:

bash
Copy code
python main.py --video_path path/to/video.mp4
For live webcam detection:

bash
Copy code
python main.py --webcam 0
View real-time detection and tracking in the display window.

Technologies Used
Python 3.x

OpenCV

TensorFlow / PyTorch

YOLOv8 / Faster R-CNN

Numpy, Pandas, Matplotlib

Future Enhancements
Multi-camera support

Integration with alert messaging systems (SMS/Email)

Dashboard for monitoring multiple feeds

Edge deployment for faster processing

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m 'Add feature')

Push to the branch (git push origin feature-name)

Open a Pull Request

License
This project is licensed under the MIT License. See the LICENSE file for details.
