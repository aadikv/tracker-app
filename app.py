from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sqlite3
import os
from detect_expiration import detect_expiration_date
from notification import send_notification

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        expiration_date = request.form['expiration_date']
        device_token = request.form['device_token']
        return save_to_database(name, expiration_date, device_token)
    return render_template('index.html')  # Save the HTML template as 'index.html' in a 'templates' folder

def save_to_database(name, expiration_date, device_token):
    notify_date = expiration_date - timedelta(days=7)
    conn = sqlite3.connect('expiration_tracker.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, expiration_date, notify_date, device_token) VALUES (?, ?, ?, ?)',
              (name, expiration_date, notify_date, device_token))
    conn.commit()
    conn.close()

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'device_token' not in request.form:
        return jsonify({"error": "Missing image or device_token"}), 400

    image_file = request.files['image']
    device_token = request.form['device_token']
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    expiration_date = detect_expiration_date(image_path)
    os.remove(image_path)

    if expiration_date:
        save_to_database('Unknown Item', expiration_date, device_token)
        return jsonify({"expiration_date": expiration_date.strftime('%Y-%m-%d')}), 200
    else:
        return jsonify({"error": "Expiration date not found"}), 404

def check_for_notifications():
    conn = sqlite3.connect('expiration_tracker.db')
    c = conn.cursor()
    c.execute("SELECT name, expiration_date, device_token FROM products WHERE notify_date = ?", (datetime.now().date(),))
    products = c.fetchall()
    conn.close()

    for product in products:
        send_notification(product[0], product[1], product[2])

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_for_notifications, trigger="interval", days=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)