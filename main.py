from flask import Flask, render_template
import requests

app = Flask(__name__)
TMDB_API_KEY = 'ac06a05e32991d43f4748daf9b291b7a'

def fetch_tmdb_data(movie_title):
    print(f"[INFO] Fetching TMDB data for: {movie_title}")
    search_url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': TMDB_API_KEY, 'query': movie_title}
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        print(f"[DEBUG] Search response: {data}")
        if data['results']:
            movie = data['results'][0]
            poster_path = f"https://image.tmdb.org/t/p/w1280{movie.get('poster_path', '')}"
            movie_id = movie['id']
            video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
            video_data = requests.get(video_url).json()
            print(f"[DEBUG] Trailer response: {video_data}")
            trailer_key = next((v['key'] for v in video_data.get('results', []) if v['site'] == 'YouTube' and v['type'] == 'Trailer'), None)
            trailer_url = f"https://www.youtube.com/embed/{trailer_key}" if trailer_key else "https://www.youtube.com/embed/dQw4w9WgXcQ"
            return {'title': movie['title'], 'poster_url': poster_path, 'trailer_url': trailer_url}
    except Exception as e:
        print(f"[ERROR] TMDB fetch failed: {e}")
    return {'title': movie_title, 'poster_url': '', 'trailer_url': "https://www.youtube.com/embed/dQw4w9WgXcQ"}

@app.route('/')
def homepage():
    now_title = 'The Dark Knight'
    now = fetch_tmdb_data(now_title)
    now_playing = {
        'title': now['title'],
        'poster_url': now['poster_url'],
        'trailer_url': now['trailer_url'],
        'start_time': '07:30 PM',
        'duration_minutes': 152,
        'status': 'Now Playing'
    }

    upcoming_titles = ['Inception', 'Dune', 'Avatar']
    coming_soon = []
    for title in upcoming_titles:
        data = fetch_tmdb_data(title)
        if data:
            coming_soon.append({'title': data['title'], 'poster_url': data['poster_url']})

    return render_template('index.html', now_playing=now_playing, coming_soon=coming_soon)

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
