# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 26/04/2021
# Last edit: 18/05/2021
#
# only run this script when you want to create table with test data on AWS
# before run this script, you need to
# 1. select test data
# 2. enable insert function to specific table
# 3. change numbers of record when you call the init_tables()

import sys
sys.path.append("..") 
import json
from db.connector import db_instance
from db.tables import discord_channel, violated_message, clean_message, flagged_message

# Size is the numbers of record you want to insert to each message table
def init_tables(size):
    # create discord_channel table
    # create violated_message table
    # create clean_message table
    # create flagged_message table
    db_instance.create_tables()

    # select test data which you want to write into database from db/data
    files_to_read = ["../db/data/linear_algebra.json", "../db/data/webdev.json"]

    # loop over each file insert test data to tables
    for file in files_to_read:
        with open(file) as file_data:
            raw = json.load(file_data)

            channel_id = raw["channel"]["id"]
            channel_name = raw["channel"]["name"]
            
            # insert data to discord_channel table
            discord_channel.insert(channel_id, channel_name)

            messages = raw["messages"]
            count = 0
            max = size
            for message in messages:
                if (count < max): 
                    message_id = message["id"]
                    user = message["author"]
                    user_id = user["id"]
                    user_name = user["name"]
                    created_on = message["timestamp"]
                    violation_content = ""
                    message_content = message["content"]

                    # uncommnet below comment to enable insert function for sepcific table
                    
                    # violated_message.insert(message_id, user_id, user_name, channel_id, violation_content, message_content, created_on)

                    # clean_message.insert(message_id, user_id, user_name, channel_id, message_content, created_on)

                    # flagged_message.insert(message_id, user_id, created_on)

                    count += 1


if __name__ == "__main__":
    db_instance.connect()

    # uncomment this to call init_tables functions
    init_tables(1)

    db_instance.close()