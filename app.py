from flask import Flask, render_template, request
import cv2
import os
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def detect_road_condition(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Resize image
    img = cv2.resize(img, (500, 300))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blur, 50, 150)

    # Count edge pixels
    edge_pixels = np.sum(edges > 0)

    # Simple condition logic
    if edge_pixels < 5000:
        condition = "Good Road"
    elif edge_pixels < 15000:
        condition = "Moderate Damage"
    else:
        condition = "Bad Road / Potholes"

    return condition


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    image_file = None

    if request.method == 'POST':
        file = request.files['image']

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            result = detect_road_condition(filepath)
            image_file = filepath

    return render_template('index.html', result=result, image_file=image_file)


if __name__ == '__main__':
    app.run(debug=True)