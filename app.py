from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='static')

def q(sql, params=()):
    con = sqlite3.connect('results.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
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
        return jsonify(rows)

    if name:
        rows = q('SELECT * FROM results WHERE arabic_name LIKE ? LIMIT 50', (f'%{name}%',))
        return jsonify(rows)

    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
