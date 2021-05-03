# Project_bot

## How to Colaborate

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

## Installing Packages

```shell
python3 -m pip install -r requirements.txt
```

## Data Visualization Instructions

### 1. Deploying bot

To be written

### 2. Deploying dashboard

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

## Database module

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
