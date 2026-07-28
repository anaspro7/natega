from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os, gzip, shutil

if not os.path.exists('results.db') and os.path.exists('results.db.gz'):
    with gzip.open('results.db.gz', 'rb') as f_in, open('results.db', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

app = Flask(__name__, static_folder='static')

MAX_DEGREE = 320

def q(sql, params=()):
    con = sqlite3.connect('results.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    return rows

def enrich(rows):
    for r in rows:
        r['total_degree'] = r['total_degree'] / 10
        r['max_degree'] = MAX_DEGREE
        r['percentage'] = round(r['total_degree'] / MAX_DEGREE * 100, 1)
    return rows

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/search')
def search():
    seat = request.args.get('seating_no', '').strip()
    name = request.args.get('name', '').strip()

    if seat:
        rows = q('SELECT * FROM results WHERE seating_no = ?', (seat,))
        return jsonify(enrich(rows))

    if name:
        rows = q('SELECT * FROM results WHERE arabic_name LIKE ? LIMIT 50', (f'%{name}%',))
        return jsonify(enrich(rows))

    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
