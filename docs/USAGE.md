# Cinema Signage Usage Guide

## Command Reference

### Basic Usage
```bash
# Demo mode with different layouts
python app.py --layout poster --demo
python app.py --layout trailer --demo --video-scale 2.0
python app.py --layout combo --demo

# Live production mode
python app.py --layout trailer --video-scale 2.0
```

### Video Scaling Options
- `1.0`: Original size (letterboxed)
- `1.5`: Moderate scaling (minimal crop)
- `2.0`: Full portrait fill (recommended)
- `2.5`: Maximum zoom (heavy crop)

### Demo Modes
- `--demo`: Shows current movie from demo file
- `--demo idle`: Shows upcoming movies carousel

## Setup Instructions

### TMDB API Configuration
1. Get API key from https://www.themoviedb.org/settings/api
2. Update `TMDB_API_KEY` in `kale_listener.py` and `tmdb_processor.py`

### Kaleidescape Configuration
1. Update `KALEIDESCAPE_IP` in `kale_listener.py`
2. Ensure network connectivity to Kaleidescape system

## Troubleshooting

### No movies showing
- Check TMDB API key validity
- Verify demo files exist and are processed
- Check browser console for errors

### Videos not scaling properly
- Try different `--video-scale` values
- Check browser support for CSS transforms
- Verify YouTube embed URLs are accessible

### Kaleidescape connection issues
- Test network connectivity to IP address
- Check firewall settings
- Verify Kaleidescape API is enabled