# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 16/04/2021
# Last edit: 27/04/2021

from connector import db_instance

# Channel object contains all the data manipulation methods realted to discrod_channel table
class Discord_channel:

    # get table schema
    def get_schema(self):
        schema = {
            "attributes": {"channel_id": "int", "channel_name": "string"},
            "primary key": "channel_id"
        }
        return schema 

    # get any numbers of row from a table
    def select(self, size = None):
        self.__sql = ("select * from discord_channel")
        rs = db_instance.select(self.__sql, None, size)
        return rs

    # find record with specified channel id
    # data type of value is integer
    def select_with_channel_id(self, channel_id, size = None):
        self.__data = {
            "channel_id": channel_id
        }
        self.__sql = ("select * from discord_channel " "where channel_id = %(channel_id)s")
        rs = db_instance.select(self.__sql, self.__data, size)
        return rs

    # insert data
    def insert(self, channel_id, channel_name):
        self.__data = {
            "channel_id": channel_id,
            "channel_name": channel_name
        }
        self.__sql = ("insert into discord_channel ""(channel_id, channel_name) " "values (%(channel_id)s, %(channel_name)s)")
        rs = db_instance.insert(self.__sql, self.__data)
        return rs

    # update data
    def update_channel_name(self, channel_id,channel_name):
        self.__data = {
            "channel_id": channel_id,
            "channel_name": channel_name
        }
        self.__sql = ("update discord_channel set channel_name = %(channel_name)s " "where channel_id = %(channel_id)s")
        rs = db_instance.update(self.__sql, self.__data)
        return rs

# create channel instance
discord_channel = Discord_channel()

# Violated object contains all the data manipulation methods realted to violated message table
class Violated_message:
    # get table schema
    def get_schema(self):
        schema = {
            "attributes": {"message_id": "int", "user_id": "int", "user_name": "string", "channel_id": "int", "violation_content": "string", "message_content": "string",
            "created_on": "timestamp"},
            "primary key": "message_id",
            "foreign key": "channel_id reference discord_channel"
        }
        return schema 

    # get any numbers of row from a table
    def select(self, size = None):
        self.__sql = ("select * from violated_message")
        rs = db_instance.select(self.__sql, None, size)
        return rs

    # find record with specified channel id
    # data type of value is integer
    def select_with_message_id(self, message_id, size = None):
        self.__data = {
            "message_id": message_id
        }
        self.__sql = ("select * from violated_message " "where message_id = %(message_id)s")
        rs = db_instance.select(self.__sql, self.__data, size)
        return rs

    # count numbers of record with specified primary key
    def count_numbers_of_violation(self, user_id):
        self.__data = {
            "user_id": user_id
        }
        self.__sql = ("select count(*) from violated_message " "where user_id = %(user_id)s")
        rs = db_instance.select(self.__sql, self.__data)
        return rs

    # insert data
    def insert(self, message_id, user_id, user_name, channel_id, violation_content, message_content, created_on):
        self.__data = {
            "message_id": message_id,
            "user_id": user_id,
            "user_name": user_name,
            "channel_id": channel_id,
            "violation_content": violation_content,
            "message_content": message_content,
            "created_on": created_on
        }
        self.__sql = ("insert into violated_message ""(message_id, user_id, user_name, channel_id, violation_content, message_content, created_on) " "values (%(message_id)s, %(user_id)s, %(user_name)s, %(channel_id)s, %(violation_content)s, %(message_content)s, %(created_on)s)")
        rs = db_instance.insert(self.__sql, self.__data)
        return rs

# create channel instance
violated_message = Violated_message()

# Clean_message object contains all the data manipulation methods realted to clean message table
class Clean_message:
    # get table schema
    def get_schema(self):
        schema = {
            "attributes": {"message_id": "int", "user_id": "int", "user_name": "string", "channel_id": "int", "message_content": "string",
            "created_on": "timestamp"},
            "primary key": "message_id",
            "foreign key": "channel_id reference discord_channel"
        }
        return schema 

    # get any numbers of row from a table
    def select(self, size = None):
        self.__sql = ("select * from clean_message")
        rs = db_instance.select(self.__sql, None, size)
        return rs

    # find record with specified channel id
    # data type of value is integer
    def select_with_message_id(self, message_id, size = None):
        self.__data = {
            "message_id": message_id
        }
        self.__sql = ("select * from clean_message " "where message_id = %(message_id)s")
        rs = db_instance.select(self.__sql, self.__data, size)
        return rs

    # insert data
    def insert(self, message_id, user_id, user_name, channel_id, message_content, created_on):
        self.__data = {
            "message_id": message_id,
            "user_id": user_id,
            "user_name": user_name,
            "channel_id": channel_id,
            "message_content": message_content,
            "created_on": created_on
        }
        self.__sql = ("insert into clean_message ""(message_id, user_id, user_name, channel_id, message_content, created_on) " "values (%(message_id)s, %(user_id)s, %(user_name)s, %(channel_id)s, %(message_content)s, %(created_on)s)")
        rs = db_instance.insert(self.__sql, self.__data)
        return rs

# create channel instance
clean_message = Clean_message()


# Flagged_message object contains all the data manipulation methods realted to flagged message table
class Flagged_message:
    # get table schema
    def get_schema(self):
        schema = {
            "attributes": {"message_id": "int", "user_id": "int", "created_on": "timestamp"},
            "primary key": "message_id, user_id",
        }
        return schema 

    # get any numbers of row from a table
    def select(self, size = None):
        self.__sql = ("select * from flagged_message")
        result = db_instance.select(self.__sql, None, size)
        return result

    # find record with specified channel id
    # data type of value is integer
    def select_with_pks(self, message_id, user_id, size = None):
        self.__data = {
            "message_id": message_id,
            "user_id": user_id,
        }
        self.__sql = ("select * from flagged_message " "where message_id = %(message_id)s and user_id = %(user_id)s")
        rs = db_instance.select(self.__sql, self.__data, size)
        return rs

    # count numbers of record with specified primary key
    def count_numbers_of_flag(self, user_id):
        self.__data = {
            "user_id": user_id
        }
        self.__sql = ("select count(*) from flagged_message " "where user_id = %(user_id)s")
        rs = db_instance.select(self.__sql, self.__data)
        return rs

    # insert data
    def insert(self, message_id, user_id, created_on):
        self.__data = {
            "message_id": message_id,
            "user_id": user_id,
            "created_on": created_on
        }
        self.__sql = ("insert into flagged_message " "(message_id, user_id, created_on) " "values (%(message_id)s, %(user_id)s, %(created_on)s)")
        rs = db_instance.insert(self.__sql, self.__data)
        return rs

    # delete all flaged message for a particular user with given user id
    def delete(self, user_id):
        self.__data = {
            "user_id": user_id,
        }
        self.__sql = ("delete from flagged_message " "where user_id = %(user_id)s")
        rs = db_instance.delete(self.__sql, self.__data)
        return rs

# create channel instance
flagged_message = Flagged_message()