# Database module

## Installing MySQL Connector/Python

MySQL Connector/Python is available on PyPI:

```console
$ pip install mysql-connector-python
```

## Getting Started

### Database connection and close

```python
# import db_instance from connector.py
from connector import db_instance

# connect to database
db_instance.connect()

# close database connection
db_instance.close()
```

### Table and data interaction

```python
# import db_instance from connector.py
# import discord_channel table, violated_message table, clean_message table, falgged_message table from tables.py
from connector import db_instance
from tables import discord_channel, violated_message, clean_message, flagged_message

# connect to database
db_instance.connect()

# for each table object, there are functions you can call, for example
# get_schema() to get schema of violated_message table
violated_message.get_schema()

# get all the records from violated_message table
violated_message.select()

# get any number of records from violated_message table
violated_message.select(size=3)

# insert data to violated_message table
violated_message.insert(message_id, user_id, user_name, channel_id, violation_content, message_content, created_on)

# count numbers of violation for a particular user with given user id
violated_message.count_numbers_of_violation(user_id)

# close database connection
db_instance.close()
```
