from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(filepath)
        elif file.filename.endswith('.txt'):
            with open(filepath, 'r') as f:
                content = f.read()
            return jsonify({"type": "txt", "content": content[:1000]})
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        return jsonify({"type": "table", "columns": df.columns.tolist(), "rows": df.head(10).to_dict(orient='records')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
