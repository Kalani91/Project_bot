# Instructions

## 1. Deploying bot
To be written


## 2. Deploying dashboard
### Dashboard dependencies
Streamlit: 

- ```$ pip install streamlit```

Graphing libraries:

- ```$ pip install plotly==4.14.3```
- ```$ pip install wordcloud```
- ```$ python -m pip install -U matplotlib```

Spacy (for nlp_summary.py):

- ```$ pip install -U pip setuptools wheel```
- ```$ pip install -U spacy```
- ```$ python -m spacy download en_core_web_sm```

Other:

- ```$ pip install pandas```
- ```$ pip install nltk```

Database connection:

- ```$ pip install mysql-connector-python```

### Running the dashboard
Must use command line.
1. On first run, go to dashboard.py and uncomment line 12 to install the NLTK Punkt Tokenizer Model when the file is run. It does not automatically install via pip. Afterwards you can comment it out again. 
2. Navigate to src folder and execute the following command: ```streamlit run dashboard.py```
3. There may be errors relating to the nlp_summary.py if you're unable to install the Spacy dependencies mentioned above. If so, comment out lines 11, 172, and 174. The rest of the dashboard should show up as normal.
