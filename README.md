# Project_bot

## 1. How to Collaborate

### Cloning the repo to local machine

This will require git to be installed on your device. If you have not installed git. ![Geti it here](https://git-scm.com/downloads) and follow the instructions.

You will need to clone this repository to your local machine to colaborate on the project.

To do this, above the section that shows all the files and directories of the repostory you will see this:
![how_to_1](https://user-images.githubusercontent.com/12618900/115331570-7f42ee00-a1d9-11eb-9808-c0648178ec98.png)
Click on the green code button then you should see a dropdown appear

![how_to_2](https://user-images.githubusercontent.com/12618900/115331763-e2348500-a1d9-11eb-9e2b-fffe021b04b1.png)

Https is the easiest way to copy the repository so click the button next to the URL to copy to your clipboard or highlight the url and ctrl+v

Now in your device open up command prompt / terminal. You can check which version of git is installed using `git --version`.

Navigate to the directory where you want the project to be placed using `cd d:/path/to/directory/`.

Use `git clone https://github.com/Kalani91/Project_bot.git` to clone. **You will be prompted to authenticate either through Github or username & password.** This will create a new folder that has the name of the repository, and will set up the connection so that you can push changes to the repository on Github.

All done with setup.

### Editing and making changes to code

**Note:** You should never modify files when in the `main\master` branch as this is considered the most stable point of the project.

Most IDE's come with source control management inbuilt which should automatically detect version control being used in project directory, makes creating branches, commiting, pushing, and pulling simpler with GUI and buttons.

## 2. Installing Packages

```shell
python3 -m pip install -r requirements.txt
```

## 3. Deploying bot

To be written

## 4. Data Visualization Instructions

### Deploying dashboard

#### Dashboard dependencies

Streamlit:

- `$ pip install streamlit`

Graphing libraries:

- `$ pip install plotly==4.14.3`
- `$ pip install wordcloud`
- `$ python -m pip install -U matplotlib`

Spacy (for nlp_summary.py):

- `$ pip install -U pip setuptools wheel`
- `$ pip install -U spacy`
- `$ python -m spacy download en_core_web_sm`

Other:

- `$ pip install pandas`
- `$ pip install nltk`

Database connection:

- `$ pip install mysql-connector-python`

#### Running the dashboard

Must use command line.

1. On first run, go to dashboard.py and uncomment line 12 to install the NLTK Punkt Tokenizer Model when the file is run. It does not automatically install via pip. Afterwards you can comment it out again.
2. Navigate to src folder and execute the following command: `streamlit run dashboard.py`
3. There may be errors relating to the nlp_summary.py if you're unable to install the Spacy dependencies mentioned above. If so, comment out lines 11, 172, and 174. The rest of the dashboard should show up as normal.

## 5. Database module

### Installing MySQL Connector/Python

MySQL Connector/Python is available on PyPI:

```console
$ pip install mysql-connector-python
```

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

# get connection object
db_instance.get_connect()
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

## 6. Logging

### Installing PyYAML

PyYAML is available on PyPI:

```console
$ pip install PyYAML
```

### Logging level

This logging module has defined three different levels of logging.

- INFO: can be used for general information purpose, such as confirmation information
- DEBUG: can be used for debugging purpose, such as critical variable during a loop
- ERROR: can be used for critical error

INFO level output will be displayed in the terminal and stored in src/logs/debug.log.

DEBUG level output will be stored in src/logs/debug.log.

ERROR level output will be stored in src/logs/error.log.

At development stage, all three levels of logging are enabled. Once our app went to production version, only ERROR level will be enabled. So please make sure to use ERROR logging when you want to log any error while our bot is online.

### How to use

In the main python file

```python
import utils.logger

if __name__ == "__main__":
  # initialise logger with customized configuration
  utils.logger.setup_logging()
```

At any sub python file which you want to use logging function, for exmaple: connector.py

```python
import logging

# at the global scope or any scope you want to include logging function
# get main logger, you can also put .current_file name after main. By doing this, logger can log your file name as well
logger = logging.getLogger("main.connector")

# you can pass string or variable
logger.info("Confirmation")

logger.debug(some_variable)

# please note if you want to also log the traceback information of an error, please use logger.exception()
logger.error(error_message)
logger.exception(error_message)
```
