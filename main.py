from flask import Flask, jsonify, request, render_template
import sqlite3
import re

app = Flask(__name__, static_folder = "templates")
db_file = 'main.db'

def query_data(filters=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if filters:
        query = f"SELECT * FROM data WHERE {' AND '.join(filters)}"
    else:
        query = "SELECT * FROM data"

    print(query)
    cursor.execute(query + ";")
    data = cursor.fetchall()

    conn.close()
    return data, cursor.description


@app.route('/data', methods=['GET'])
def get_data():
    filters = []
    between_vals = {
        "price": [0, 9999999999999],
        "year": [0, 9999999999999],
        "kilometer": [0, 9999999999999],
        "engine_cc": [0, 9999999999999],
        "max_power_hp": [0, 9999999999999],
        "max_torque_nm": [0, 9999999999999],
        "seating_capacity": [0, 9999999999999],
        "fuel_tank_capacity": [0, 9999999999999]
    }
    for key, value in request.args.items():
        if value:
            key = key.replace(" ", "_").lower()
            if re.match(r".+_lower", key):
                between_vals[key[:-6]][0] = value
            elif re.match(r".+_upper", key):
                between_vals[key[:-6]][1] = value
            elif key in ["make", "fuel_type", "transmission", "location"]:
                filters.append(f"{key} LIKE '%{value}%'") 
                
    
    for key, value in between_vals.items():
        filters.append(f"{key} BETWEEN {value[0]} AND {value[1]}")


    data, cursor_data = query_data(filters)
    
    columns = [column[0].replace("_", " ").capitalize() for column in cursor_data] if cursor_data else []

    return render_template('main.html', data=data, columns=columns)

if __name__ == '__main__':
    app.run()
