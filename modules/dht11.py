import time
import seeed_dht
import psycopg2

connection = psycopg2.connect(
	host='127.0.01',
	user='project',
	password='project3',
	database='project')
	
cursor = connection.cursor()

def collect_data():
    # for DHT11/DHT22
	sensor = seeed_dht.DHT("11", 12)
	while True:
		humi, temp = sensor.read()
		print(f"{humi} , {temp}")
		cursor.execute(f"INSERT INTO air_data"
		f"(timestamp, humidity,temperature) "
		f"VALUES (NOW(), {humi}, {temp})")
		if humi < 15 or humi > 60:
			cursor.execute(f"INSERT INTO alert_history"
			f"(problem, sensor_value, icon_link, timestamp)"
			f"VALUES ('Humidity alert', {humi}," 
			f"'https://static.vecteezy.com/system/resources/previews/000/442/471/original/vector-humidity-vetor-icon.jpg',"
			f" NOW());")
		if temp < 16 or temp > 25:
			cursor.execute(f"INSERT INTO alert_history"
			f"(problem, sensor_value, icon_link, timestamp)"
			f"VALUES ('Temperature alert', {temp}," 
			f"'https://static.vecteezy.com/system/resources/previews/000/441/265/original/temperature-vector-icon.jpg',"
			f" NOW());")
		connection.commit()
		time.sleep(1)
        
collect_data()
