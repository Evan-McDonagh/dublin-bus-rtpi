import os
import json
import numpy 
import mysql.connector
from config import database_config

def connect_to_db():
    mydb = mysql.connector.connect(
        host = database_config["host"],
        user = database_config["user"],
        passwd=  database_config["password"],
        database = database_config["database"],
        port = database_config["port"]
    )
    return mydb

def get_stop_locations():
    sql_statement = ("select * from stops")

    try:
        mydb = connect_to_db()
        mycursor = mydb.cursor()
        mycursor.execute(sql_statement)

        print(mycursor)

        mycursor.close()
        mydb.close()
    except mysql.connector.Error as error:
        print("SOMETHING WENT WRONG", error)


get_stop_locations()