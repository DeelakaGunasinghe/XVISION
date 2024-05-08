from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
from uuid import uuid4

app = Flask(__name__, template_folder='/Users/deelakagunasinghe/Downloads/Xvision/templates', static_folder='/Users/deelakagunasinghe/Downloads/Xvision/static')

model2 = load_model('curr.h5')

class_names = ['Rs.10', 'Rs.100', 'Rs.20', 'Rs.200', 'Rs.2000', 'Rs.50', 'Rs.500']

@app.route('/')
def index():
    return render_template('recog.html')

import cv2

import cv2

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = f"{uuid4().hex}.jpg"
        upload_dir = os.path.join(app.root_path, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        img_path = os.path.join(upload_dir, filename)
        file.save(img_path)

        try:
            img = cv2.imread(img_path)
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            min_area = 7000  
            max_aspect_ratio = 1.8 
            
            banknote_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h
                    if aspect_ratio < max_aspect_ratio:
                        banknote_contours.append(contour)
            
            if len(banknote_contours) > 0:
                img = image.load_img(img_path, target_size=(256, 256))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0
                
                prediction = model2.predict(img_array)
                predicted_class_index = np.argmax(prediction[0])
                predicted_class_name = class_names[predicted_class_index]
                
                return jsonify({'predicted_class': predicted_class_name})
            else:
                return jsonify({'error': 'No banknote detected'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        finally:
            os.remove(img_path)
            
    return jsonify({'error': 'Error'}), 400

if __name__ == '__main__':
    app.run(debug=True)
