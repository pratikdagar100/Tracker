from flask import Flask, request, jsonify, render_template, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'locations.csv'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/log', methods=['POST'])
def log_location():
    try:
        data = request.json
        lat = data['latitude']
        lon = data['longitude']

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), lat, lon])

        print(f"Location logged: {lat}, {lon}")
        return jsonify({"status": "ok", "message": "Location logged successfully."})
    except (TypeError, KeyError) as e:
        return jsonify({"status": "error", "message": f"Invalid data format: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500

@app.route("/get_log")
def get_log():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
