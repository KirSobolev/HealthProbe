import psycopg2
from psycopg2 import Error
from psycopg2 import sql

def create_tables():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="127.0.0.1",
            user='project',
            password='project3',
            database="project")

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Create tables for database 'project'
        humidity_temperature_sensor_table = """ 
            CREATE TABLE IF NOT EXISTS air_data(
            id SERIAL PRIMARY KEY, 
            timestamp TIMESTAMP NOT NULL, 
            humidity DECIMAL(4,1) NOT NULL,
            temperature DECIMAL(4,1) NOT NULL);"""
        alert_history = """
            CREATE TABLE IF NOT EXISTS alert_history(
            id SERIAL,
            problem VARCHAR(100),
            sensor_value DECIMAL(5,1) NOT NULL,
            icon_link VARCHAR(255),
            timestamp TIMESTAMP NOT NULL);"""
        
        cursor.execute(humidity_temperature_sensor_table)
        cursor.execute(alert_history)
        connection.commit()
        print("Tables created!")


    except Error as e:
        print("Error connecting to PostgreSQL database:", e)

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

# Call the function to connect to PostgreSQL
create_tables()
