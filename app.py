from flask import Flask, request, jsonify, render_template
import csv
import os # Import the os module

app = Flask(__name__)

# It's good practice to define the CSV file path
# to ensure it's created in a known location.
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
        
        # 'a' (append mode) creates the file if it doesn't exist
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([lat, lon])

        print(f"Location logged: {lat}, {lon}")
        return jsonify({"status": "ok", "message": "Location logged successfully."})
    except (TypeError, KeyError) as e:
        # Handle cases where the request body is not JSON or missing keys
        return jsonify({"status": "error", "message": f"Invalid data format: {e}"}), 400
    except Exception as e:
        # Generic error handler for other issues (e.g., file permissions)
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500


if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 to make the server publicly accessible
    app.run(host='0.0.0.0', port=port)
