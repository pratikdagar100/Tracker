# app.py
from flask import Flask, request, jsonify, send_from_directory
import csv, os, smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/log', methods=['POST'])
def log_location():
    data = request.json
    lat = data['latitude']
    lon = data['longitude']

    # Log to CSV
    with open("locations.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([lat, lon])

    # Optional: send email
    send_email(lat, lon)

    return jsonify({"status": "ok"})

def send_email(lat, lon):
    sender = "your_email@gmail.com"
    receiver = "receiver_email@gmail.com"
    password = "your_app_password"

    message = MIMEText(f"Device location: https://maps.google.com/?q={lat},{lon}")
    message['Subject'] = 'GPS Location Update'
    message['From'] = sender
    message['To'] = receiver

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Email error: {e}")

if __name__ == '__main__':
    app.run(debug=False)
