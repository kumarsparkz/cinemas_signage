# Digital Signage System

A modern digital signage system for cinemas that displays current movies and upcoming attractions with support for portrait displays.

## Features

- 🎬 **Multiple Layout Modes**: Poster-only, Trailer-only, or Combo layouts
- 📱 **Portrait Optimized**: Perfect for 3840×2160 vertical displays
- 🎯 **Video Scaling**: Configurable video scaling to eliminate black bars
- 🔄 **Auto-Refresh**: Real-time updates from Kaleidescape system
- 🎭 **Demo Mode**: Test layouts without hardware connection
- 🎞️ **TMDB Integration**: Live poster and trailer fetching
- 🎪 **Upcoming Movies Carousel**: Scrolling display when idle

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set TMDB API Key
Edit `kale_listener.py` and `tmdb_processor.py` to add your TMDB API key.

### 3. Run Demo Mode
```bash
# Create demo data
python create_demo_data.py
python tmdb_processor.py

# Run with full portrait video scaling
python app.py --layout trailer --demo --video-scale 2.0
```

### 4. Access Display
Open browser to `http://localhost:5000`

## Layout Modes

- **Poster** (`--layout poster`): Full-screen movie posters
- **Trailer** (`--layout trailer`): Full-screen video trailers  
- **Combo** (`--layout combo`): Split poster and trailer

## Video Scaling

- `--video-scale 1.0`: Original size (black bars)
- `--video-scale 2.0`: Full portrait fill (default)
- `--video-scale 2.5`: Maximum zoom

## Production Setup

1. Configure Kaleidescape IP in `kale_listener.py`
2. Start listener: `python kale_listener.py`
3. Start web server: `python app.py --layout poster --video-scale 2.0`

## Demo Commands

```bash
# Current movie display
python app.py --layout poster --demo

# Upcoming movies carousel
python app.py --layout poster --demo idle

# Custom video scaling
python app.py --layout trailer --demo --video-scale 1.5
```

## Requirements

- Python 3.7+
- Flask
- Requests
- BeautifulSoup4 (optional, for better HTML parsing)
- TMDB API Key

## Hardware Compatibility

- Kaleidescape media servers
- Any display resolution (optimized for 3840×2160 portrait)
- Web browser support (Chrome, Firefox, Safari, Edge)

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request

## License

MIT License - see LICENSE file for details