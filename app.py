
from flask import Flask, send_from_directory, jsonify
import os
import json

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/now_playing.json')
def now_playing():
    if os.path.exists("now_playing.json"):
        with open("now_playing.json") as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/poster/<path:filename>')
def serve_poster(filename):
    return send_from_directory('poster', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
