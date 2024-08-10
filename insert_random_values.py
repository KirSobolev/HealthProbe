import time
import psycopg2
from random import randint

connection = psycopg2.connect(
	host='127.0.01',
	user='project',
	password='project3',
	database='project')
	
cursor = connection.cursor()

def collect_data():
	while True:
		cursor.execute(f"INSERT INTO air_data"
		f"(timestamp, humidity,temperature) "
		f"VALUES (NOW(), 99, 99)")
		connection.commit()
		print("Inerted random value")
		time.sleep(1)
		
def truncate_table():
	cursor.execute(f"TRUNCATE TABLE air_data")
	print("Table truncated successfully")

truncate_table()        
#collect_data()

