#!/usr/bin/env python3

import json
import sys
import pymongo
import mysql.connector

class convertData:
    '''
    Creates connection to MongoDB and MySQL databases
    '''
    def __init__(self):
        self.mongo = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo["corona"]
        self.nosql = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ahojahojahoj"
        )

        mycursor = self.nosql.cursor()

        mycursor.execute("DROP DATABASE a")
        mycursor.execute("CREATE DATABASE a")
        mycursor.execute("SHOW DATABASES")

        for x in mycursor:
            print(x)

        print("Connected")

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
Convertor.convertB()
Convertor.convertA()
