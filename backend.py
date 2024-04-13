# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json

app = Flask(__name__)
CORS(app)

@app.route('/decode', methods=['POST'])
def decode_base64():
    data = json.loads(request.args.get('data'))
    try:
        decoded_text = base64.b64decode(data['input']).decode("ascii")
        return jsonify({'decoded_text': decoded_text})
    except UnicodeDecodeError:
        try:
            decoded_text = base64.b64decode(data['input']).decode("utf-8")
            return jsonify({'decoded_text': decoded_text})
        except Exception as e:
            return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
