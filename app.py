from flask import Flask, send_from_directory, jsonify, render_template_string
import os
import json
import argparse

app = Flask(__name__, static_folder='.')

# Global variables
LAYOUT_MODE = 'combo'  # default
DEMO_MODE = False
DEMO_IDLE = False  # New flag for demo idle mode
VIDEO_SCALE = 2.0  # Default 2.0x scaling for portrait fill

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/now_playing.json')
def now_playing():
    if DEMO_MODE:
        if DEMO_IDLE:
            # In demo idle mode, return no current movie to trigger carousel
            return jsonify({
                'now_playing': None,
                'layout_mode': LAYOUT_MODE,
                'video_scale': VIDEO_SCALE
            })
        else:
            # In normal demo mode, read from demo file if it exists
            demo_file = "demo_data_now_playing.json"
            if os.path.exists(demo_file):
                with open(demo_file) as f:
                    data = json.load(f)
                    data['layout_mode'] = LAYOUT_MODE
                    data['video_scale'] = VIDEO_SCALE
                    return jsonify(data)
            else:
                # Fallback if demo file doesn't exist
                return jsonify({
                    'layout_mode': LAYOUT_MODE,
                    'video_scale': VIDEO_SCALE
                })
    
    if os.path.exists("now_playing.json"):
        with open("now_playing.json") as f:
            data = json.load(f)
            # Add layout mode and video scale to the response
            data['layout_mode'] = LAYOUT_MODE
            data['video_scale'] = VIDEO_SCALE
            return jsonify(data)
    return jsonify({
        'layout_mode': LAYOUT_MODE,
        'video_scale': VIDEO_SCALE
    })

@app.route('/poster/<path:filename>')
def serve_poster(filename):
    return send_from_directory('poster', filename)

@app.route('/history.json')
def history():
    """Endpoint for upcoming movies when nothing is currently playing"""
    if DEMO_MODE:
        # In demo mode, read from demo file if it exists
        demo_file = "demo_data_coming_up.json"
        if os.path.exists(demo_file):
            with open(demo_file) as f:
                data = json.load(f)
                data['layout_mode'] = LAYOUT_MODE
                data['video_scale'] = VIDEO_SCALE
                return jsonify(data)
        else:
            # Fallback if demo file doesn't exist
            return jsonify({
                'layout_mode': LAYOUT_MODE,
                'video_scale': VIDEO_SCALE
            })
    
    if os.path.exists("history.json"):
        with open("history.json") as f:
            data = json.load(f)
            data['layout_mode'] = LAYOUT_MODE
            data['video_scale'] = VIDEO_SCALE
            return jsonify(data)
    return jsonify({
        'layout_mode': LAYOUT_MODE,
        'video_scale': VIDEO_SCALE
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cinema Signage Display')
    parser.add_argument('--layout', choices=['trailer', 'poster', 'combo'], 
                       default='combo', help='Display layout mode')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--demo', action='store_true', 
                       help='Run in demo mode with sample data')
    parser.add_argument('--video-scale', type=float, default=2.0,
                       help='Video scaling factor for portrait displays (default: 2.0 for full fill)')
    parser.add_argument('demo_mode', nargs='?', choices=['idle'], 
                       help='Demo mode type: idle (shows upcoming movies carousel)')
    
    args = parser.parse_args()
    LAYOUT_MODE = args.layout
    DEMO_MODE = args.demo
    DEMO_IDLE = args.demo and args.demo_mode == 'idle'
    VIDEO_SCALE = args.video_scale
    
    if DEMO_MODE:
        if DEMO_IDLE:
            print(f"🎬 Starting cinema signage in DEMO IDLE MODE")
            print(f"📺 Layout: {LAYOUT_MODE}")
            print(f"🔄 Mode: Upcoming movies carousel")
            print(f"📁 Demo file: demo_data_coming_up.json")
        else:
            print(f"🎬 Starting cinema signage in DEMO MODE")
            print(f"📺 Layout: {LAYOUT_MODE}")
            print(f"🎞️  Mode: Current movie display")
            print(f"📁 Demo file: demo_data_now_playing.json")
        
        print(f"🎯 Video Scale: {VIDEO_SCALE}x (for portrait optimization)")
        print(f"🌐 Access at: http://localhost:{args.port}")
        print(f"🎭 TMDB API will be used for live poster/trailer fetching")
    else:
        print(f"🎬 Starting cinema signage with layout mode: {LAYOUT_MODE}")
        print(f"🎯 Video Scale: {VIDEO_SCALE}x (for portrait optimization)")
        print(f"🔗 Connecting to Kaleidescape at 192.168.1.171")
    
    app.run(host=args.host, port=args.port)