import psycopg2
import matplotlib.pyplot as plt
import base64
import threading
import time
import io
import logging
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition
from io import BytesIO
from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO


# Class for handling camera streaming output 
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


# Initialize flask app with socketio support (for real time updating)
app = Flask(__name__, static_url_path='/static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
output = StreamingOutput()

db_params = {
        'dbname':'project',
        'user':'project',
        'password':'project3',
        'host':'127.0.0.1'}

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard page
@app.route('/dashboard.html')
def dashboard():
    data = fetch_data('alert_history', 5)
    return render_template('dashboard.html', data = data)

# Output for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/data')
def get_data():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute('SELECT problem, sensor_value, '
                       'timestamp, icon_link FROM alert_history '
                       'ORDER BY timestamp DESC')
        data = cursor.fetchmany(5)
        columns = [desc[0] for desc in cursor.description]
        cursor.close()

        result = []
        for row in data:
            result.append(dict(zip(columns, row)))

        return jsonify(result)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
@socketio.on('connect')
def handle_connect():
    print('Client connected')


# Function that creates the plot for humidity and temperature
def send_plot():
    while True:
        data = fetch_data("air_data", 100)
        timestamps = [row[1] for row in data]
        humidity_values = [row[2] for row in data]
        temperature_values = [row[3] for row in data]
        max_recommended_humidity = 50
        min_recommended_humidity = 30
        max_recommended_temperature = 24
        min_recommended_temperature = 18

        # Create a plot for temperature
        plt.axhline(y=min_recommended_temperature, color='blue', linestyle='--', label='Min Recommended Temperature')
        plt.axhline(y=max_recommended_temperature, color='red', linestyle='--', label='Max Recommended Temperature')
        plt.plot(timestamps, temperature_values, label='Temperature', color='orange')
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.title('Temperature')
        plt.legend()

        # Save the temperature plot to a BytesIO object
        temperature_img_data = BytesIO()
        plt.savefig(temperature_img_data, format='png')
        temperature_img_data.seek(0)

        # Convert the BytesIO object to base64
        temperature_plot_base64 = base64.b64encode(temperature_img_data.getvalue()).decode('utf-8')

        # Emit the temperature plot to all connected clients
        socketio.emit('update_temperature_plot', {'plot': temperature_plot_base64})

        # Close the temperature plot
        plt.close()

        # Create a plot for humidity
        plt.axhline(y=min_recommended_humidity, color='red', linestyle='--', label='Min Recommended Humidity')
        plt.axhline(y=max_recommended_humidity, color='red', linestyle='--', label='Max Recommended Humidity')
        plt.plot(timestamps, humidity_values, label='Humidity')
        plt.xlabel('Time')
        plt.ylabel('Humidity')
        plt.title('Humidity')
        plt.legend()

        # Save the humidity plot to a BytesIO object
        humidity_img_data = BytesIO()
        plt.savefig(humidity_img_data, format='png')
        humidity_img_data.seek(0)

        # Convert the BytesIO object to base64
        humidity_plot_base64 = base64.b64encode(humidity_img_data.getvalue()).decode('utf-8')

        # Emit the humidity plot to all connected clients
        socketio.emit('update_humidity_plot', {'plot': humidity_plot_base64})

        # Close the humidity plot
        plt.close()

        # Wait for a specified interval (e.g., 10 seconds)
        time.sleep(10)
    
    
# Fetches 100 rows of data from database
def fetch_data(table, rows):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    # Execute a query to fetch data
    cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC ")
    # Fetch 100 rows
    data = cursor.fetchmany(rows)
    # Close the cursor and connection
    cursor.close()
    conn.close()

    return data

#------------------------------------CAMERA---------------------------------#
def generate():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def capture_frames():
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.start_recording(JpegEncoder(), FileOutput(output))
#------------------------------------END OF CAMERA--------------------------#


if __name__ == '__main__':
    # Start the thread for updating the plot
    update_thread = threading.Thread(target=send_plot)
    update_thread.start()
    
    #Start the thread for video
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.start()

    # Run the Flask app with SocketIO support

    socketio.run(app, debug=True, use_reloader=False)
