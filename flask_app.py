from flask import Flask, render_template, request, jsonify, abort, send_from_directory
from werkzeug.contrib.cache import SimpleCache
from datetime import datetime, timedelta

DEBUG = False
BIND = '127.0.0.1'
SSL = False

REFRESH_INTERVAL = 60  # Seconds
CACHE_RETENTION = REFRESH_INTERVAL * 2
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480


cache = SimpleCache()
app = Flask(__name__)


class RoomCache:
    def __init__(self):
        self.cache = {}

    def add(self, user, image):
        self.cache[user] = (datetime.utcnow(), image)

    def get(self):
        self.__clean()

        result = {}
        for key, value in list(self.cache.items()):
            result[key] = value[1]

        return result

    def __clean(self):
        for key, value in list(self.cache.items()):
            delta = timedelta(seconds=CACHE_RETENTION)
            if value[0] + delta < datetime.utcnow():
                del self.cache[key]


@app.route('/')
def default():
    return render_template('index.html',
                           refresh_interval=REFRESH_INTERVAL * 1000,
                           capture_width=CAPTURE_WIDTH,
                           capture_height=CAPTURE_HEIGHT)


@app.route('/presence/<room_name>', methods=['GET'])
def get_presence(room_name):
    cache_entry = cache.get(room_name)
    if cache_entry is None:
        abort(404)
    else:
        return jsonify({'room_name': room_name, 'members': cache_entry.get()})


@app.route('/presence/<room_name>', methods=['POST'])
def presence(room_name):
    cache_entry = cache.get(room_name)

    args = request.get_json()
    if args is None:
        abort(500)

    display_name = args.get('display_name')
    image = args.get('image', None)
    if len(display_name) == 0 or len(image) == 0:
        abort(500)

    if cache_entry is None:
        cache_entry = RoomCache()

    cache_entry.add(display_name, image)
    cache.set(room_name, cache_entry, timeout=CACHE_RETENTION)

    return ''


@app.route('/webcamjs/<path:path>')
def webcamjs(path):
    return send_from_directory('webcamjs', path)


if __name__ == '__main__':
    app.run(debug=DEBUG,
            host=BIND,
            ssl_context='adhoc' if SSL else None)
