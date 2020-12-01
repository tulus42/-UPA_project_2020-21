#!/bin/bash

if [ ! -f /usr/bin/mongod ]
	then 
		wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
		echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
		sudo apt-get update -y
		sudo apt-get install -y mongodb-org
		sudo systemctl start mongod
	else
		echo "MongoDB already installed."
fi

if [ ! -f /usr/bin/mysql ]
	then
		sudo apt-get update -y
		sudo apt-get install -y mysql-server

		sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'ahojahojahoj';"
		sudo mysql -e "DROP DATABASE test;"
		sudo mysql -e "FLUSH PRIVILEGES;"
	else
		echo "MySQL already installed."
fi

if [! -f /usr/bin/pip* ]
	then
		sudo apt-get update -y
		sudo apt-get install -y python3-pip
		sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
		sudo apt-get install -y python3-venv

		python3 -m venv env
		source env/bin/activate

		pip3 install -r requirements.txt
	else
		python3 -m venv env
		source env/bin/activate

		pip3 install -r requirements.txt
fi
