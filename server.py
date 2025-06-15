from flask import Flask, jsonify, request, send_from_directory
from threading import Thread
from rss_isleyici import verileri_cek_ve_isle, rss_kaynaklarini_oku

app = Flask(__name__)

@app.route('/feeds', methods=['GET'])
def get_feeds():
    return jsonify(rss_kaynaklarini_oku())

@app.route('/feeds', methods=['POST'])
def add_feed():
    data = request.get_json(force=True)
    url = data.get('url')
    if not url:
        return jsonify({'error': 'url required'}), 400
    if not url.startswith(('http://', 'https://')):
        return jsonify({'error': 'invalid url'}), 400
    feeds = rss_kaynaklarini_oku()
    if url not in feeds:
        with open('rss_kaynaklari.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
    return jsonify({'status': 'added'})

@app.route('/feeds', methods=['DELETE'])
def remove_feed():
    data = request.get_json(force=True)
    url = data.get('url')
    feeds = [u for u in rss_kaynaklarini_oku() if u != url]
    with open('rss_kaynaklari.txt', 'w', encoding='utf-8') as f:
        for u in feeds:
            f.write(u + '\n')
    return jsonify({'status': 'removed'})

@app.route('/update', methods=['POST'])
def update():
    Thread(target=verileri_cek_ve_isle).start()
    return jsonify({'status': 'updating'})

@app.route('/data.geojson')
def geojson():
    return send_from_directory('.', 'data.geojson')

@app.route('/')
def index():
    return send_from_directory('.', 'harita.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
