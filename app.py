from flask import Flask, request, jsonify, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/log', methods=['POST'])
def log_location():
    data = request.json
    lat = data['latitude']
    lon = data['longitude']
    
    with open("locations.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([lat, lon])

    print(f"Location logged: {lat}, {lon}")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run()
