from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)
db_file = 'main.db'

def query_data(filters=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if filters:
        query = f"SELECT * FROM data WHERE {' AND '.join(filters)}"
    else:
        query = "SELECT * FROM data"

    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data


@app.route('/data', methods=['GET'])
def get_data():
    filters = []
    for key, value in request.args.items():
        filters.append(f"{key}='{value}'")

    data = query_data(filters)
    return render_template('main.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
