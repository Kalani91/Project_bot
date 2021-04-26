# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 26/04/2021
# Last edit: 26/04/2021

from connector import db_instance

if __name__ == "__main__":
    # connect to database
    db_instance.connect()

    # create tables
    db_instance.create_tables()

    # close database connection
    db_instance.close()
