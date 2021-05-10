import nltk
import argparse
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_md
nlp = en_core_web_md.load()
from pprint import pprint
import neuralcoref
import string

# https://medium.com/@muddaprince456/categorizing-and-pos-tagging-with-nltk-python-28f2bc9312c3
# https://medium.com/@ODSC/intro-to-language-processing-with-the-nltk-59aa26b9d056 
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

def open_file(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if len(line) > 1 and line[-2] in string.punctuation:
                data.append(line)
            if line == "References" or line == "Notes" or line == "See also" or line == "Further reading" or line == "Bibliography" or line == "External links":
                break
    return "\n".join(data)


# returns (list of words, list of POS tags)
def pos_tokenize(data):
    words = []
    tags = []
    sentences = nltk.sent_tokenize(data)
    for sentence in sentences:
        tokenized = nltk.word_tokenize(sentence)
        words.append(tokenized)
        tagged = nltk.pos_tag(tokenized)
        tags.append(tagged)
    return (words, tags)

# returns a list of the nlp represenation of each sentence
# removes common stopwords for said representation to improve similarity use
def vectors(data):
    common_words = set(stopwords.words('english'))
    sentences = nltk.sent_tokenize(data)
    vectors = []
    for sentence in sentences:
        sentence_list = nltk.word_tokenize(sentence)
        common_removed = list(filter(lambda w: not w.lower() in common_words, sentence_list))
        doc = nlp(" ".join(common_removed))
        vectors.append(doc)
    return vectors


def ner(data):
    result = nlp(data)
    return [(X.text, X.label_) for X in result.ents]