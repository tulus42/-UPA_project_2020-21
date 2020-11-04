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
        self.connectSQL()
        print("Connected")

    def connectMongo(self):
        self.mongo = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo["corona"]
        pass

    ### from stack overflow 
    # https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
    def executeScriptsFromFile(self, filename):
        mycursor = self.nosql.cursor()
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')
        sqlCommands = [command.strip() for command in sqlCommands if command]
        print(sqlCommands)

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                mycursor.execute(command)
            except OperationalError:
                print("Command skipped")

    def connectSQL(self):
        self.nosql = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ahojahojahoj"
        )

        self.executeScriptsFromFile('RelationalDatabase.sql')
        #mycursor = self.nosql.cursor()
        #with open('RelationalDatabase.sql') as f:
            #mycursor = self.nosql.cursor()
            #mycursor.execute(f.read(), multi=True)
            #self.nosql.commit()
        #mycursor.execute("DROP DATABASE a")
        #mycursor.execute("DROP DATABASE IF EXISTS a SHOW DATABASES;")

        #for x in mycursor:
        #    print(x)

    '''
    Creates tables for relational databases
    '''
    def createRelationalDatabase(self):
        pass

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


Convertor = convertData()
#Convertor.convertB()
#Convertor.convertA()
