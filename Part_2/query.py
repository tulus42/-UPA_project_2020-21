#!/usr/bin/env python3

import mysql.connector

class MySQLDb:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ahojahojahoj",
            database="corona"
        )
        self.cursor = self.database.cursor()

    # primitive function for tests
    def get_table(self):
        self.cursor.execute("SELECT * FROM ill WHERE age > '90'")
        
        table = self.cursor.fetchall()

        return table

    def get_ill_increase_in_time(self, date_from, date_to, age_from, age_to, gender, imported):
        command = "SELECT date_of_infection,COUNT(*) as count FROM ill WHERE date_of_infection >= %s AND date_of_infection <= %s AND age > %s AND age < %s "
        if gender == 0:
            command += "AND gender = 'M' "
        elif gender == 1:
            command += "AND gender = 'Z' "

        if imported == 1:
            command += "AND imported = 1 "
        
        command += "GROUP BY date_of_infection ORDER BY date_of_infection"

        self.cursor.execute(command, (date_from, date_to, age_from, age_to,))

        table = self.cursor.fetchall()

        return table

    def get_country_code(self, country):
        self.cursor.execute("SELECT country_code FROM country_codes WHERE country_name = %s", (country,))

        code = self.cursor.fetchone()

        # fetchone() returns tuple: (value,) -> so get only first value
        return code[0]

    def get_country_population(self, country):
        self.cursor.execute("SELECT population FROM country_codes WHERE country_code = %s", (country,))

        population = self.cursor.fetchone()

        # fetchone() returns tuple: (value,) -> so get only first value
        return population[0]

    def get_districts(self):
        self.cursor.execute("SELECT DISTINCT district_name FROM district_codes")

        districts = self.cursor.fetchall()
        
        return [x[0] for x in districts]

    def get_regions(self):
        self.cursor.execute("SELECT DISTINCT region_name FROM region_codes")

        regions = self.cursor.fetchall()

        return [x[0] for x in regions]

    def get_districts_in_region(self, region):
        self.cursor.execute("SELECT region_code FROM region_codes WHERE region_name = %s", (region,))

        region_code = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT DISTINCT district_name FROM district_codes WHERE region_code = %s", (region_code,))

        districts = self.cursor.fetchall()

        return [x[0] for x in districts]

##################
# testing section

# db = MySQLDb()
# table = db.get_districts_in_region("Zlínský kraj")
# print(table)