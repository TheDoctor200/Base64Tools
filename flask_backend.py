from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode_base64():
    data = request.json
    try:
        decoded_text = base64.b64decode(data['input']).decode("utf-8")
        return jsonify({'decoded_text': decoded_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
