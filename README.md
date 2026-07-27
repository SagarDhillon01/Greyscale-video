# Title: Grayscale Studio

## 1. Methodology

This project uses Python and OpenCV to convert uploaded media into grayscale. The application accepts both images and videos, processes them using computer vision techniques, and allows users to download the grayscale result instantly.

## 2. Description

Grayscale Studio is a simple and elegant web application that lets users upload either a photo or a video and convert it into a grayscale version. The project is built with Flask for the web interface and OpenCV for image and video processing.

It also includes a premium-limit feature where files larger than 60 MB are blocked with a message encouraging users to upgrade to a premium membership for 1 year at ₹60.

## 3. Input / Output

Input:
- Image files such as JPG, PNG, JPEG, BMP, GIF, TIFF
- Video files such as MP4, MOV, AVI, and similar formats

Output:
- Grayscale image download for images
- Grayscale video download for videos

## 4. Live link

Live demo: https://grayscale-video-app.onrender.com/

## 5. Screenshot of the Interface

A modern upload interface allows users to drag or select a file and instantly begin the grayscale conversion process.

## About

This project was developed as a simple yet impactful media conversion web app using Flask and OpenCV. It demonstrates how basic computer vision can be wrapped in a user-friendly web experience.

## Features

- Upload and convert photos to grayscale
- Upload and convert videos to grayscale
- Modern and attractive UI
- 60 MB free upload limit with premium upsell message
- Easy deployment-ready Flask app

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SagarDhillon01/Greyscale-video.git
   ```

2. Navigate to the project folder:
   ```bash
   cd Greyscale-video
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   python app.py
   ```

5. Open the app in your browser at:
   ```bash
   http://127.0.0.1:5000
   ```

## Technologies Used

- Python
- Flask
- OpenCV
- HTML/CSS
- Render (for deployment)

## Contributors

- Sagar Dhillon
