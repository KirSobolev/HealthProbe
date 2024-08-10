Requirements:
	# Backend flask app
	pip install flask
	# For real time updating 
	pip install flask-socketio
	
	pip install flask_cors


	# MAtplotlib
	pip install matplotlib

	# Postgresql database
	pip install postgresql
		sudo su postgres
		create user project -P --interactive
			password: project3
	# Postgresql library for python
	pip install psycopg2
	
	# DHT11 sensor
	cd ~
	git clone https://github.com/Seeed-Studio/Seeed_Python_DHT.git
	cd Seeed_Python_DHT
	sudo python3 setup.py install
	
	# Loudness sensor
	cd ~
	git clone https://github.com/Seeed-Studio/grove.py
	
	
	#Camera moduel 
	sudo nano /boot/firmware/config.txt
		dtoverlay=imx219
		camera_auto_detect=0
