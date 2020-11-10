#!/usr/bin/env python3

import json
import sys
import pymongo
import mysql.connector
from sqlite3 import OperationalError
import datetime
import time

class convertData:
    '''
    Creates connection to MongoDB and MySQL database
    '''
    def __init__(self):
        self.connectMongo()
        self.connectSQL()

    def connectMongo(self):
        self.mongo = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mongodb = self.mongo["corona"]

    def connectSQL(self):
        self.mysql = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ahojahojahoj"
        )
        self.mysqlCursor = self.mysql.cursor()

    ### from stack overflow 
    # https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
    def createRelationalDatabase(self, filename):
        mycursor = self.mysql.cursor()
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')
        sqlCommands = [command.strip() for command in sqlCommands if command]

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                mycursor.execute(command)
            except OperationalError:
                print("Command skipped")

    def fetchCollection(self, collectionName):
        return self.mongodb[collectionName]

    def fetchCollectionData(self, collectionName):
        return self.mongodb[collectionName].find()


    def getWeekFirstDay(self, p_year, p_week):
        firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
        return firstdayofweek

    def getWeekLastDay(self, p_year, p_week):
        firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
        lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
        return lastdayofweek

    def adjustByConstraints(self, one_data, one_constraint):
        if(one_constraint == 'UPPER'):
            if(one_data == ''):
                return None
            else:
                return one_data.upper()

        elif(one_constraint == 'UPPER_C'):
            if(one_data == ''):
                return None
            else:

                # fix inconsistency
                if(one_data == 'UK'):
                    one_data = 'GB'
                elif(one_data == 'EL'):
                    one_data = 'GR'

                one_data = one_data.upper()
                if one_data in self.countries:
                    return one_data
                else:
                    sys.stderr.write("Missing country code for " + str(one_data) + '\n')
                    return None
        elif(one_constraint == 'BOOL'):
            if(one_data == 'False'):
                return 0
            elif(one_data == 'True'):
                return 1
        elif(one_constraint == 'LAU'):
            if one_data in self.districts:
                return one_data
            else:
                return None
        elif(one_constraint == 'NUTS'):
            if one_data in self.regions:
                return one_data
            else:
                return None
        elif(one_constraint == 'WEEK_BEFORE'):
            to_convert = one_data.split('-')
            year = to_convert[0]
            week = to_convert[1].replace('W', '')
            return self.getWeekFirstDay(year, week)
        elif(one_constraint == 'WEEK_AFTER'):
            to_convert = one_data.split('-')
            year = to_convert[0]
            week = to_convert[1].replace('W', '')
            return self.getWeekLastDay(year, week)


    def obtainImportantData(self, dataset, labels, constraints):
        val = []

        # iterate over the obtained dataset
        for data in dataset:
            important_data = []
            for i in range(0,len(labels)):

                # check for constraints
                if(constraints[i] != ''):
                    currentData = self.adjustByConstraints(data[labels[i]], constraints[i])
                else:
                    currentData = data[labels[i]]

                # append it to list
                important_data.append(currentData)

            # crete the final tuple
            val.append(tuple(important_data))
        return val


    def executeMany(self, sql_command, vals):
        self.mysqlCursor.executemany(sql_command, vals)
        self.mysql.commit()
        print(self.mysqlCursor.rowcount, " was inserted")


    def convertRegions(self):
        # get the dataset 
        nuts_lau = self.fetchCollectionData('nuts_lau')

        # select appropriate values
        vals = self.obtainImportantData(nuts_lau, ['nuts_code', 'nuts_name'], ['', ''])

        # we only need distinct values
        vals = list(set(vals))

        # conversion
        sql_command = "INSERT INTO region_codes (region_code, region_name) VALUES (%s, %s)"
        self.executeMany(sql_command, vals)

        
    def convertDistricts(self):
        # get the dataset 
        nuts_lau = self.fetchCollectionData('nuts_lau')

        # select appropriate values
        vals = self.obtainImportantData(nuts_lau, ['lau_code', 'lau_name', 'nuts_code'], ['', '', ''])
        
        # conversion
        sql_command = "INSERT INTO district_codes (district_code, district_name, region_code) VALUES (%s, %s, %s)"
        self.executeMany(sql_command, vals)

    def convertCountries(self):
        # get the dataset 
        countries = self.fetchCollectionData('countries')

        # select appropriate values
        vals = self.obtainImportantData(countries, ['alpha2', 'name'], ['UPPER', ''])

        # conversion
        sql_command = "INSERT INTO country_codes (country_code, country_name) VALUES (%s, %s)"
        self.executeMany(sql_command, vals)

    def convertInfectivity(self):
        # get the dataset
        collectionB = self.fetchCollectionData('B')

        # select appropriate values
        vals = self.obtainImportantData(collectionB, ['datum', 'kraj_nuts_kod', 'okres_lau_kod', 'kumulativni_pocet_nakazenych'], ['', '', '', '', ''])
        
        # conversion
        sql_command = "INSERT INTO infectivity (date_of_infection, region_code, district_code, num_of_ill) VALUES (%s, %s, %s, %s)"
        self.executeMany(sql_command, vals)

    def prepareDistinctRegionsAndDistricts(self):
        self.mysqlCursor.execute("SELECT DISTINCT region_code FROM region_codes")
        out = self.mysqlCursor.fetchall()

        self.regions = [item for t in out for item in t]

        self.mysqlCursor.execute("SELECT DISTINCT district_code FROM district_codes")
        out = self.mysqlCursor.fetchall()

        self.districts = [item for t in out for item in t]

    def prepareCountryCodes(self):
        self.mysqlCursor.execute("SELECT DISTINCT country_code FROM country_codes")
        out = self.mysqlCursor.fetchall()

        self.countries = [item for t in out for item in t]

    def convertIll(self):
        # prepare distinct regions and districts
        

        # get the dataset
        collectionA = self.fetchCollectionData('A')

        # select appropriate values
        vals = self.obtainImportantData(collectionA, ['datum', 'vek', 'pohlavi', 'kraj_nuts_kod', 'okres_lau_kod', 'nakaza_v_zahranici', 'nakaza_zeme_csu_kod'], ['', '', '', 'NUTS', 'LAU', 'BOOL', 'UPPER_C'])

        # conversion
        sql_command = "INSERT INTO ill (date_of_infection, age, gender, region_code, district_code, imported, country_code) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.executeMany(sql_command, vals)

        batchSize = 10000
        i = 0
        #for batch in self.batchProvider(vals, batchSize):
            #self.executeMany(sql_command, batch)

    def batchProvider(self, data, batch_size=100):
        # create the generator
        for i in range(0, len(data), batch_size):
            yield data[i:i+batch_size]

    def convertPositivityRate(self):
        # get the dataset
        collectionC = self.fetchCollectionData('C')

        # select appropriate values
        # vals = self.obtainImportantData(collectionC, ['country_code', 'year_week', 'year_week', 'new_cases', 'tests_done', 'population', 'testing_rate'], ['', '', '', '', '', '', ''])
        vals = self.obtainImportantData(collectionC, ['country_code', 'year_week', 'year_week', 'new_cases', 'tests_done', 'population'], ['UPPER_C', 'WEEK_BEFORE', 'WEEK_AFTER', '', '', ''])


        sql_command = "INSERT INTO country_rates(country_code, start_date, end_date, new_cases, tests_done, population) VALUES (%s, %s, %s, %s, %s, %s)"
        self.executeMany(sql_command, vals)
        



Convertor = convertData()
Convertor.createRelationalDatabase('Corona.sql')
Convertor.convertCountries()
Convertor.prepareCountryCodes()
Convertor.convertRegions()
Convertor.convertDistricts()
Convertor.prepareDistinctRegionsAndDistricts()
Convertor.convertInfectivity()
Convertor.convertIll()
Convertor.convertPositivityRate()




#Call function to get dates range 
#firstdate, lastdate =  getDateRangeFromWeek('2019','2')

#print('print function ',firstdate,' ', lastdate)
