from flask import Flask, jsonify, request, json
from flask_cors import CORS, cross_origin
import PIL.Image as Image
import sys
import torch 
import io
import h5py 
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from model import CSRNet
from predictDictVer import predict_population
from torchvision import transforms
from PIL import UnidentifiedImageError

app = Flask(__name__)
CORS(app)

transform=transforms.Compose([
        transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]),
                   ])

# Load the model and its weights
model = CSRNet()
model = model.cuda()
checkpoint = torch.load('0model_best.pth.tar')
model.load_state_dict(checkpoint['state_dict'])
model.eval()  # Set the model to evaluation mode

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/model', methods=['POST'])
def process_data():
    data = request.get_json()  # JSON 데이터 가져오기
    # 데이터 처리 로직 수행
    processed_data = {}  # 예시: 데이터를 처리한 결과를 저장하는 변수
    image=data["image"]
    # print(image)
    processed_data = {"answer" : "150"}
    response = jsonify(processed_data)  # 처리된 데이터를 JSON 형태로 변환하여 응답 생성
    return response

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    predicted_hours = data['predicted_hours']
    all_predictions = predict_population(predicted_hours)
    return jsonify(all_predictions)


def transform_image(image):
    return transform(image.convert('RGB')).cuda().unsqueeze(0)

def get_prediction(image):
    with torch.no_grad():  # Temporarily disable gradient calculation
        output = model(image)
    return int(output.detach().cpu().sum().numpy())

def create_plot(image):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    output = model(image).detach().cpu()
    reshaped_output = output.reshape(output.shape[2], output.shape[3])
    axis.imshow(reshaped_output, cmap='jet')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return base64.b64encode(output.getvalue()).decode()




@app.route('/crowdcount', methods=['POST'])
def crowdcount():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'no image'}), 400
    image_data = data['image']
    image_bytes = base64.b64decode(image_data)
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        return jsonify({'error': 'cannot identify image file'}), 400
    image = transform_image(image)
    prediction = get_prediction(image)
    plot = create_plot(image)
    return jsonify({'prediction': prediction, 'plot': plot})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
