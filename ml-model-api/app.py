import torch
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms

app = Flask(__name__)

# Load your trained model (change the path to your actual model)
model = torch.load('model.pt')
model.eval()  # Set the model to evaluation mode

# Define the necessary image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Inference function
def predict_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    image = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        output = model(image)
        prediction = output.argmax(dim=1).item()  # Example: get the class with the highest probability
    return prediction

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    image_bytes = file.read()
    prediction = predict_image(image_bytes)
    
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
