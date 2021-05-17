from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import mysql.connector
import pandas as pd
from db.connector import db_instance

def sumy_nlp(messages):
    parser = PlaintextParser.from_string(messages, Tokenizer("english"))

    modulesumm_lsa = LsaSummarizer()
    final_summary = modulesumm_lsa(parser.document, 5)

    #for f_sentence in final_summary:
        #print(f_sentence)
    return final_summary

'''
DEBUGGING
# connecting to database
db_instance.connect()
cx = db_instance.get_connect()

# dataframe querying and filtering
df = pd.read_sql("SELECT * from clean_message", cx)

txt = df.message_content.str.lower()
all_messages = ""
for line in txt:
    all_messages = all_messages + line + ". " 

result = sumy_nlp(all_messages)
for line in result:
    print(line)
'''
