from io import BytesIO
from urllib import request
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import os
def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_input(x):
    x = np.array(x, dtype='float32')
    x = x / 255.0
    return x

def predict(url):
    # Download and preprocess image
    img = download_image(url)
    img = prepare_image(img, target_size=(200, 200))
    x = np.array(img)
    X = np.array([x])
    X = preprocess_input(X)

    interpreter = tflite.Interpreter(model_path='model_2024_hairstyle_v2.tflite')
    interpreter.allocate_tensors()

    input_index = interpreter.get_input_details()[0]['index']
    output_index = interpreter.get_output_details()[0]['index']

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    return float(preds[0][0])


def lambda_handler(event, context):
    url = event['url']
    
    files = os.listdir('.')
    print("Files in directory:", files)
    print(np.__version__)
    
    # Check if model exists
    if not os.path.exists('model_2024_hairstyle_v2.tflite'):
        return {"error": "Model file not found"}
        
    result = predict(url)
    return {'prediction': result}