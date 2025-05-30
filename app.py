# Initialize using environment variables
import sqlite3
import redis
import os
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
print(logging.getLoggerClass().root.handlers[0].baseFilename)
load_dotenv()


app = Flask(__name__)
apm = ElasticAPM(app)
redis_conn = redis.Redis(host="localhost", port=6379, db=0)


@app.route('/')
def index():
    app.logger.warning(f"Warning Index route")
    return '<h1>Hello, World!</h1>'
@app.route('/logs', methods=["GET"])
def getLogs():
    app.logger.warning(f"Warning log route info logs route")
    return '<h1>Hello, World! Logs</h1>'
@app.route("/log", methods=["GET"])
def log():
    # Get the current date and time
    now = datetime.now()

# Format the datetime object into a readable string
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    message = f'Log {current_time}' #request.form["message"]
    app.logger.warning(f"Warning log route info {current_time}")
   

    # Store the message in SQLite
    sqlite_conn = sqlite3.connect("logs.db")
    cursor = sqlite_conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (message text)")
    cursor.execute("INSERT INTO logs (message) values (?)", (message,))
    sqlite_conn.commit()
    sqlite_conn.close()

    # Store the message in Redis
    redis_conn.rpush("logs", message)

    return "Logged: {}".format(message)

if __name__ == "__main__":
    app.run(debug=True)