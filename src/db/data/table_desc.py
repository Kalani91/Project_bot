# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 26/04/2021
# Last edit: 26/04/2021
#
# Define table schema
TABLES = {}

TABLES['discord_channel'] = (
    "CREATE TABLE `discord_channel` ("
    "  `channel_id` BIGINT NOT NULL,"
    "  `channel_name` VARCHAR(100) NOT NULL,"
    "  PRIMARY KEY (`channel_id`)"
    ") ENGINE=InnoDB")

TABLES['violated_message'] = (
    "CREATE TABLE `violated_message` ("
    "  `message_id` BIGINT NOT NULL,"
    "  `user_id` BIGINT NOT NULL,"
    "  `user_name` VARCHAR(100) NOT NULL,"
    "  `channel_id` BIGINT NOT NULL,"
    "  `violation_content` TEXT NOT NULL,"
    "  `message_content` TEXT NOT NULL,"
    "  `created_on` TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`message_id`),"
    "  CONSTRAINT `channel_idfk_1` FOREIGN KEY (`channel_id`) "
    "     REFERENCES `discord_channel` (`channel_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['clean_message'] = (
    "CREATE TABLE `clean_message` ("
    "  `message_id` BIGINT NOT NULL,"
    "  `user_id` BIGINT NOT NULL,"
    "  `user_name` VARCHAR(100) NOT NULL,"
    "  `channel_id` BIGINT NOT NULL,"
    "  `message_content` TEXT NOT NULL,"
    "  `created_on` TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`message_id`),"
    "  CONSTRAINT `channel_idfk_2` FOREIGN KEY (`channel_id`) "
    "     REFERENCES `discord_channel` (`channel_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['flagged_message'] = (
    "CREATE TABLE `flag_message` ("
    "  `message_id` BIGINT NOT NULL,"
    "  `user_id` BIGINT NOT NULL,"
    "  `user_name` VARCHAR(100) NOT NULL,"
    "  `channel_id` BIGINT NOT NULL,"
    "  `message_content` TEXT NOT NULL,"
    "  `created_on` TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`message_id`),"
    "  CONSTRAINT `channel_idfk_3` FOREIGN KEY (`channel_id`) "
    "     REFERENCES `discord_channel` (`channel_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")