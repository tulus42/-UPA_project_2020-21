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

    def get_data_per_day_groupby_region(self, date):
        #self.cursor.execute("SELECT region_code FROM region_codes WHERE region_name = %s", (region,))

        #region_code = self.cursor.fetchone()[0]

        # IDK what you want, here is reg_code, maybe you want region names then swap region_code for region_name in SELECT and add 
        # INNER JOIN region_codes USING(region_code) after FROM infectivity, or if just numbers, you know what to do. :D 
        self.cursor.execute("SELECT region_name, SUM(num_of_ill) FROM infectivity INNER JOIN region_codes USING(region_code) WHERE date_of_infection=%s GROUP BY region_code ORDER BY region_name;", (date,))

        data = self.cursor.fetchall()

        #return [x[1] for x in data]
        return data

    def get_data_per_day_groupby_district_in_region(self, date, region):
        self.cursor.execute("SELECT region_code FROM region_codes WHERE region_name = %s", (region,))

        region_code = self.cursor.fetchone()[0]

        # IDK what you want, here is district_code, maybe you want district names then swap district_code for district_name in SELECT and add 
        # INNER JOIN district_codes USING(district_code) after FROM infectivity and change infectivity.region_code='<region_code>', or if just numbers, you know what to do. :D 
        self.cursor.execute("SELECT district_name, SUM(num_of_ill) FROM infectivity INNER JOIN district_codes USING(district_code) WHERE date_of_infection=%s AND infectivity.region_code=%s GROUP BY district_code ORDER BY district_name;", (date, region_code,))

        data = self.cursor.fetchall()

        #return [x[1] for x in data]
        return data

    def get_rates_cases_tests_from_to_country(self, start_date, end_date, country):
        self.cursor.execute("SELECT country_code FROM country_codes WHERE country_name = %s", (country,))

        country_code = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT start_date, new_cases, tests_done, ((tests_done/population)*100000) FROM country_rates INNER JOIN country_codes USING(country_code) WHERE start_date>=%s AND end_date<=%s AND country_code=%s ORDER BY start_date", (start_date, end_date, country_code,))

        data = self.cursor.fetchall()

        #return [x[1] for x in data]
        return data

    def get_percenage_per_country_from_to(self, start_date, end_date, country):
        self.cursor.execute("SELECT country_code FROM country_codes WHERE country_name = %s", (country,))

        country_code = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT start_date, ((new_cases/tests_done)*100) FROM country_rates WHERE start_date>=%s AND end_date<=%s AND country_code=%s ORDER BY start_date", (start_date, end_date, country_code,))

        data = self.cursor.fetchall()

        #return [x[1] for x in data]
        return data

"""
    def get_cases_country_from_to(self, start_date, end_date, country):
        self.cursor.execute("SELECT country_code FROM country_codes WHERE country_name = %s", (country,))

        country_code = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT start_date, new_cases FROM country_rates WHERE start_date>=%s AND end_date<=%s AND country_code=%s ORDER BY start_date", (start_date, end_date, country_code,))

        data = self.cursor.fetchall()

        #return [x[1] for x in data]
        return data

    def get_percenage_per_country_from_to(self, start_date, end_date, country):
        self.cursor.execute("SELECT country_code FROM country_codes WHERE country_name = %s", (country,))

        country_code = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT start_date, ((new_cases/tests_done)*100) FROM country_rates WHERE start_date>=%s AND end_date<=%s AND country_code=%s ORDER BY start_date", (start_date, end_date, country_code,))

        data = self.cursor.fetchall()

        #return [x[1] for x in data]
        return data
"""

##################
# testing section

#db = MySQLDb()
#table = db.get_data_per_day_groupby_district_in_region("2020-11-04", "Zlínský kraj")
#table = db.get_data_per_day_groupby_region("2020-11-04")
#table = db.get_rates_cases_tests_from_to_country("2020-10-12", "2020-12-12", "Německo")
#print(table)
