# real-estate

## How to start backend

1. change dir to backend folder: `cd ./backend`
2. setup virtual environment: `python3 -m venv venv`
3. activate virtual environment: `source ./venv/bin/activate` (for Mac and Linux)
4. install all requirements: `pip install -r requirements.txt`
5. start backend with command: `gunicorn app:app`

## how to start frontend

1. change dir to backend folder: `cd ./frontend`
2. install all requirements: `npm i`
3. start frontend: `npm run dev`

## To start the project you need to add .env file in **backend** folder

It should include your user name, password and DB_CONNECT tring that contains IP address, port and protocol (like this `11.11.11.11:1521/SQLD`):

DB_USER=""
DB_PASSWORD=""
DB_CONNECT_STRING=""

If everything is installed, service can be started with one command `./start-app.sh`
