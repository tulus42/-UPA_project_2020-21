#!/usr/bin/env python3

import mysql.connector
import datetime

class MySQLDb:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ahojahojahoj",
            database="corona"
        )
        self.cursor = self.database.cursor()

    def get_table(self):
        self.cursor.execute("SELECT * FROM ill LIMIT 10")
        
        table = self.cursor.fetchall()

        return table

    def get_ill_increase_in_time(self, date_from, date_to):
        date_from = "2020-0"+str(date_from)+"-01" if date_from < 10 else "2020-"+str(date_from)+"-01"
        date_to = "2020-0"+str(date_to)+"-30" if date_to < 10 else "2020-"+str(date_to)+"-30"
        self.cursor.execute("SELECT date_of_infection,COUNT(*) as count FROM ill WHERE date_of_infection >= %s AND date_of_infection <= %s GROUP BY date_of_infection ORDER BY date_of_infection", (date_from, date_to,))

        return self.cursor.fetchall()

