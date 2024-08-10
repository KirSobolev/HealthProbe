import time
import psycopg2
from grove.grove_loudness_sensor import GroveLoudnessSensor

connection = psycopg2.connect(
	host='127.0.01',
	user='project',
	password='project3',
	database='project')
cursor = connection.cursor()

PIN = 0
sensor = GroveLoudnessSensor(PIN)

def get_sensor_value():
    return sensor.value

if __name__ == "__main__":
    print("Sensor script is running...")
    while True:
        value = get_sensor_value()
        if value > 900:
            cursor.execute(f"INSERT INTO alert_history"
			f"(problem, sensor_value, icon_link, timestamp)"
			f"VALUES ('Noise alert', {value}," 
			f"'https://static.vecteezy.com/system/resources/previews/000/531/611/original/sound-icon-vector-illustration.jpg',"
			f" NOW());")
            connection.commit()
        print("Sensor value:", value)
        time.sleep(.5)
