from flask import Flask
from flask import Response
from flask import request
from redis import Redis
from datetime import datetime
import MySQLdb
import sys
import redis 
import time
import hashlib
import os
import json


app = Flask(__name__)
startTime = datetime.now()
#R_SERVER = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)
#db = MySQLdb.connect("mysql","root","password")
#cursor = db.cursor()



@app.route('/health')
def healthz():
    return Response("Healthy", status=200, mimetype='application/json')



@app.route('/init')
def init():
    try:
       db = MySQLdb.connect("mysql","root","rootpass")
       cursor = db.cursor()
       cursor.execute("DROP DATABASE IF EXISTS STUDENTDB")
       cursor.execute("CREATE DATABASE STUDENTDB")
       cursor.execute("USE STUDENT")
       sql = """CREATE TABLE students (
             ID int,
             STUDENT char(30)
       )"""
       cursor.execute(sql)
       db.commit()
       return "DB Init done"
    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)


@app.route("/students/add", methods=['POST'])
def add_courses():

    try:
       db = MySQLdb.connect("mysql","root","rootpass")
       cursor = db.cursor()
       cursor.execute("USE STUDENTDB")
       req_json = request.get_json()
       cursor.execute("INSERT INTO students (ID, STUDENT) VALUES (%s,%s)", (req_json['uid'], req_json['student']))
       db.commit()
       return Response("Added\n\n", status=200, mimetype='application/json')
    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)

#Server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
