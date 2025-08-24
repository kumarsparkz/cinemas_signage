
import socket
import re
import json
import requests
import os

KALEIDESCAPE_IP = "192.168.1.171"
PORT = 10000
BUFFER_SIZE = 1024
TMDB_API_KEY = "ac06a05e32991d43f4748daf9b291b7a"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w780"
TMDB_TRAILER_URL = "https://api.themoviedb.org/3/movie/{}/videos"

def get_tmdb_data(title):
    print(f"[DEBUG] Fetching TMDB data for title: {title}")
    try:
        res = requests.get(TMDB_SEARCH_URL, params={
            "api_key": TMDB_API_KEY,
            "query": title
        })
        res.raise_for_status()
        data = res.json()
        if data["results"]:
            movie = data["results"][0]
            poster_url = TMDB_POSTER_BASE + movie["poster_path"] if movie.get("poster_path") else ""
            movie_id = movie["id"]
            trailer_res = requests.get(TMDB_TRAILER_URL.format(movie_id), params={
                "api_key": TMDB_API_KEY
            })
            trailer_key = ""
            if trailer_res.status_code == 200:
                trailers = trailer_res.json().get("results", [])
                for t in trailers:
                    if t["site"] == "YouTube" and t["type"] == "Trailer":
                        trailer_key = t["key"]
                        break
            trailer_url = f"https://www.youtube.com/embed/{trailer_key}?autoplay=1&mute=1&controls=0" if trailer_key else ""
            return title, poster_url, trailer_url
    except Exception as e:
        print(f"[ERROR] Failed to fetch TMDB data: {e}")
    return title, "", ""

def write_now_playing(title, poster_url, trailer_url):
    try:
        with open("now_playing.json", "w") as f:
            json.dump({
                "now_playing": {
                    "title": title,
                    "poster_url": poster_url,
                    "trailer_url": trailer_url
                }
            }, f)
        print("[INFO] now_playing.json updated.")
    except Exception as e:
        print(f"[ERROR] Failed to write JSON: {e}")

def listen_for_title(ip, port):
    try:
        print(f"[INFO] Connecting to Kaleidescape at {ip}:{port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.settimeout(3600)
        print("[INFO] Connected. Listening for TITLE_NAME...")
        buffer = b""
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                print("[WARN] No data received. Reconnecting...")
                break
            buffer += data
            lines = buffer.split(b"\n")
            buffer = lines[-1]
            for line in lines[:-1]:
                decoded = line.decode("utf-8", errors="ignore").strip()
                print("[RECV]", decoded)
                if "TITLE_NAME:" in decoded:
                    match = re.search(r"TITLE_NAME:(.*)", decoded)
                    if match:
                        raw_title = match.group(1).strip()
                        clean_title = raw_title.split(":")[0].strip()
                        print(f"[INFO] Movie Title Detected: {clean_title}")
                        title, poster_url, trailer_url = get_tmdb_data(clean_title)
                        write_now_playing(title, poster_url, trailer_url)
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
    finally:
        s.close()
        print("[INFO] Socket closed. Listener stopped.")

if __name__ == "__main__":
    listen_for_title(KALEIDESCAPE_IP, PORT)
