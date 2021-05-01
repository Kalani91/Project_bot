# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 26/04/2021
# Last edit: 27/04/2021
#
# only run this script when you want to create table with test data on AWS

import json
from db.connector import db_instance
from db.tables import discord_channel, violated_message, clean_message, flagged_message

# Size x 3 is the numbers of record you want to insert to each message table
def init_tables(size):
    # connect to database
    db_instance.connect()

    # create discord_channel table
    # create violated_message table
    # create clean_message table
    # create flagged_message table
    db_instance.create_tables()

    # test data contains discord chat history to be read
    files_to_read = ["data/irc.json", "data/cwa.json", "data/tepchats.json"]

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

                    violated_message.insert(message_id, user_id, user_name, channel_id, violation_content, message_content, created_on)

                    clean_message.insert(message_id, user_id, user_name, channel_id, message_content, created_on)

                    flagged_message.insert(message_id, user_id, created_on)

                    count += 1
    
    # close database connection
    db_instance.close()

if __name__ == "__main__":
    db_instance.connect()

    init_tables(50)

    db_instance.close()