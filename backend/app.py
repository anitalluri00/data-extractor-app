from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        data = df.to_dict(orient='records')
        return jsonify({'columns': df.columns.tolist(), 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return 'Backend running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)