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
VERSION = '1.0.3'

cache = SimpleCache()
app = Flask(__name__)


class RoomCache:
    def __init__(self):
        self.cache = {}

    def add(self, unique_id, display_name, image, time):
        self.cache[unique_id] = (datetime.utcnow(), display_name, image, time)

    def get(self):
        self.__clean()

        results = []
        for key, value in list(self.cache.items()):
            result = {}
            result['unique_id'] = key
            result['display_name'] = value[1]
            result['image'] = value[2]
            result['time'] = value[3]
            results.append(result)

        return results

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
                           capture_height=CAPTURE_HEIGHT,
                           version=VERSION,
                           base_url=request.base_url)


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

    unique_id = args.get('unique_id')
    display_name = args.get('display_name')
    image = args.get('image', None)
    time = args.get('time', None)
    if len(unique_id) == 0 or \
       len(display_name) == 0 or \
       len(image) == 0 or \
       len(time) == 0:
        abort(500)

    if cache_entry is None:
        cache_entry = RoomCache()

    cache_entry.add(unique_id, display_name, image, time)
    cache.set(room_name, cache_entry, timeout=CACHE_RETENTION)

    return ''


@app.route('/version', methods=['GET'])
def version():
    return jsonify({'version': VERSION})


if __name__ == '__main__':
    app.run(debug=DEBUG,
            host=BIND,
            ssl_context='adhoc' if SSL else None)
