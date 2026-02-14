import os
import io
import base64
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify
from PIL import Image
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max 

# Путь к моделям
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')

# Словарь для хранения загруженных моделей
loaded_models = {}

def load_model(model_name):
    if model_name not in loaded_models:
        model_path = os.path.join(MODEL_DIR, f"{model_name}.h5")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model {model_name} not found")
        loaded_models[model_name] = keras.models.load_model(model_path)
    return loaded_models[model_name]

def predict_center(image_array, model_name):
    model = load_model(model_name)
    
    img_for_model = cv2.resize(image_array, (128, 128)).astype('float32') / 255.0
    
    prediction = model.predict(np.expand_dims(img_for_model, axis=(0, -1)), verbose=0)[0]
    
    x_orig = prediction[1] * (image_array.shape[1] / 128)  
    y_orig = prediction[0] * (image_array.shape[0] / 128)  
    
    return float(x_orig), float(y_orig)

def draw_crosshair(image_array, x, y, size=20, color=(255, 0, 0), thickness=2):
    if len(image_array.shape) == 2:
        image_rgb = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = image_array.copy()
    
    x, y = int(x), int(y)
    
    # Горизонтальная линия
    cv2.line(image_rgb, (x - size, y), (x + size, y), color, thickness)
    
    # Вертикальная линия
    cv2.line(image_rgb, (x, y - size), (x, y + size), color, thickness)
    
    return image_rgb

def numpy_to_base64(image_array):
    if len(image_array.shape) == 3:
        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    else:
        image_bgr = image_array
    
    _, buffer = cv2.imencode('.png', image_bgr)
    img_str = base64.b64encode(buffer).decode()
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    """Главная страница"""
    models = ['allData_v2', 'cnn_M_20x_k_4', 'cnn_M_20x_k_6', 'cnn_M_20x_k_8']
    return render_template('index.html', models=models)

@app.route('/predict', methods=['POST'])
def predict():
    """Обработка запроса на предсказание"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        model_name = request.form.get('model', 'allData_v2')
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            return jsonify({'error': 'Failed to read image'}), 400
        
        x, y = predict_center(image, model_name)
        
        result_image = draw_crosshair(image, x, y)
        
        # Конвертируем в base64
        result_base64 = numpy_to_base64(result_image)
        
        return jsonify({
            'success': True,
            'coordinates': {
                'x': round(x, 2),
                'y': round(y, 2)
            },
            'result_image': result_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint для CI/CD"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)