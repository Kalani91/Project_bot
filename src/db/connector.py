# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 30/03/2021
# Last edit: 27/04/2021

from db_conf import server
from data import table_desc
import mysql.connector
from mysql.connector import errorcode

# Db_helper object contains all the method realted to connecting database and CRUD methods
class Db_helper:
    def __init__(self, user, password, host, port, database):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__database = database
        self.__cnx = None
        self.__cursor = None

    # sets up a connection, establishing a session with the MySQL server
    def connect(self):
        try:
            self.__cnx = mysql.connector.connect(
                user = self.__user,
                password = self.__password,
                host = self.__host,
                port = self.__port,
                database = self.__database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err.msg)
        else:
            print("Database connection successful")
            return True
            
    # method to return connection object
    def get_connect(self):
        if (self.__cnx):
            return self.__cnx
        else:
            return None

    # close database connection
    def close(self):
        if self.__cnx:
            self.__cnx.close()
            print("Database close successful")

    # create a cursor object
        # if buffered is true, the cursor fetches all row from the server after an opeartion is executed
    def __create_cursor(self):
        if self.__cnx:   
            self.__cursor = self.__cnx.cursor(buffered=True)
    
    # close a cursor object
    def __close_cursor(self):
        if self.__cursor:
            self.__cursor.close()

    # method to create tables in database
        # open cursor
        # assign Table description to schemas
        # loor over each table schema to create table on the server
        # error will be catched by try except
        # close cursor
    def create_tables(self):
        self.__create_cursor()
        TABLES = table_desc.TABLES
        for table_name in TABLES:
            table_schema = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.__cursor.execute(table_schema)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Table already exists.")
                else:
                    print(err.msg)
            else:
                print("Table creation successful")
        self.__close_cursor()

    # method to execute insert, update and delete query
        # open cursor
        # execute query
        # commit query result to database
        # return the number of row affected by query
        # close cursor
        # if error happens, undoing all data changes from the query, then close cursor
    def __cud(self, sql, params):
        try:
            self.__create_cursor()
            self.__cursor.execute(sql, params)
            count = self.__cursor.rowcount
            self.__cnx.commit()
            return count
        except mysql.connector.Error as err:
            print(err.msg)
            self.__cnx.rollback()
        finally:
            self.__close_cursor()

    # public insert method to be called 
    def insert(self, sql, params):
        return self.__cud(sql, params)

    # public update method to be called 
    def update(self, sql, params):
        return self.__cud(sql, params)

    # public delete method to be called 
    def delete(self, sql, params):
        return self.__cud(sql, params)


    # method to execute select query
        # by default, the method returns all the rows of a query result
        # the method also can returns the number of row specified by size argument
    def select(self, sql, params = None, size = None):
        try:
            self.__create_cursor()
            self.__cursor.execute(sql, params)
            if size:
                rs = self.__cursor.fetchmany(size)
            else:
                rs = self.__cursor.fetchall()
            return rs
        except mysql.connector.Error as err:
            print(err.msg)
        finally:
            self.__close_cursor()

# initialise an instance of Db_helper with mysql server config
db_instance = Db_helper(server["user"], server["password"], server["host"], server["port"], server["database"])
