#!/usr/bin/env python3

import json
import sys
import pymongo
import mysql.connector
from sqlite3 import OperationalError

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
        #mycursor = self.nosql.cursor()
        #with open('RelationalDatabase.sql') as f:
            #mycursor = self.nosql.cursor()
            #mycursor.execute(f.read(), multi=True)
            #self.nosql.commit()
        #mycursor.execute("DROP DATABASE a")
        #mycursor.execute("DROP DATABASE IF EXISTS a SHOW DATABASES;")

        #for x in mycursor:
        #    print(x)

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

    '''
    Creates tables for relational databases
    '''
    def convertB(self):
        self.collectionB = self.db["B"]
        for x in self.collectionB.find():
            print(x)
            break

    def convertA(self):
        self.collectionA = self.db["A"]
        for x in self.collectionA.find():
            print(x)
            break

    def fetchCollection(self, collectionName):
        return self.mongodb[collectionName]

    def fetchCollectionData(self, collectionName):
        return self.mongodb[collectionName].find()


    def adjustByConstraints(self, one_data, one_constraint):
        if(one_constraint == 'U'):
            return one_data.upper()

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
        vals = self.obtainImportantData(countries, ['alpha2', 'name'], ['U', ''])

        # conversion
        sql_command = "INSERT INTO country_codes (country_code, country_name) VALUES (%s, %s)"
        self.executeMany(sql_command, vals)

    def convertInfectivity(self):
        pass



Convertor = convertData()
Convertor.createRelationalDatabase('Corona.sql')
#Convertor.convertCountries()
Convertor.convertRegions()
Convertor.convertDistricts()
#Convertor.convertB()
#Convertor.convertA()
