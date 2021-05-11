'''
Implements two different NLP methods for creating summaries of a document.
Method 1 produces a ton of garbage.
Method 2 gives a small amount of garbage.
The problem is that these methods don't work very well with chat messages, as opposed to an organised text. 
'''
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import mysql.connector
import pandas as pd
from collections import Counter
from heapq import nlargest
from db.connector import db_instance


def sumy_nlp(messages):
    parser = PlaintextParser.from_string(messages, Tokenizer("english"))

    modulesumm_lsa = LsaSummarizer()
    final_summary = modulesumm_lsa(parser.document, 5)

    #for f_sentence in final_summary:
        #print(f_sentence)
    return final_summary

def nlp_method_1(messages):
    docx = nlp(messages)

   # generates dict of tokens and frequency with simple count method
    all_words = [word.text for word in docx]
    Freq_word = {}
    for w in all_words:
        w1 = w.lower()
        if w1 not in extra_words and w1.isalpha():
            if w1 in Freq_word.keys():
                Freq_word[w1] += 1
            else:
                Freq_word[w1] = 1
    #print(Freq_word)

    # implements tf-idf algo to generate frequency
    val = sorted(Freq_word.values())
    max_freq = val[-3:]
    for word in Freq_word.keys():
        Freq_word[word] = (Freq_word[word] / max_freq[-1])
    #print(Freq_word)

    # calculates relevance of each sentence to the overall topic
    sent_strength = {}
    for sent in docx.sents:
        for word in sent:
            if word.text.lower() in Freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += Freq_word[word.text.lower()]
                else:
                    sent_strength[sent] = Freq_word[word.text.lower()]
            else:
                continue
    #print(sent_strength)

    # creates a summary of the document
    top_sentences = (sorted(sent_strength.values())[::-1])
    top30percent_sentence = int(0.1 * len(top_sentences))
    top_sent = top_sentences[:top30percent_sentence]

    summary = []
    for sent, strength in sent_strength.items():
        if strength in top_sent:
            summary.append(sent)

        else:
            continue

    #for i in summary:
    #    print(i, end="")

    return summary

def nlp_method_2(messages):
    doc = nlp(messages)
    len(list(doc.sents))

    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if token.text in stopwords or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            keyword.append(token.text)

    freq_word = Counter(keyword)
    #print(freq_word.most_common(5))

    type(freq_word)

    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)
    freq_word.most_common(5)

    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    #print(sent_strength)
    #print("")

    summarized_sentences = nlargest(1, sent_strength, key=sent_strength.get)
    #print(summarized_sentences)
    #print(type(summarized_sentences[0]))

    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    #print(summary)

    return summary


extra_words = list(STOP_WORDS) + list(punctuation) + ['\n']
nlp = spacy.load('en_core_web_sm')

# connecting to database
db_instance.connect()
cx = db_instance.get_connect()

# dataframe querying and filtering
df = pd.read_sql("SELECT * from clean_message", cx)

txt = df.message_content.str.lower()
all_messages = ""
for line in txt:
    all_messages = all_messages + line + ". " 



# applying nlp methods
#result1 = nlp_method_1(all_messages)
#result2 = nlp_method_2(all_messages)
#sumy_nlp(all_messages)
#print(f'Text analysis with method #1: \n {result1}')
#print(f'Text analysis with method #2: \n {result2}')