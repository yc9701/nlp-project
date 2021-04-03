import nltk
import argparse
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from pprint import pprint
import neuralcoref

# https://medium.com/@muddaprince456/categorizing-and-pos-tagging-with-nltk-python-28f2bc9312c3
# https://medium.com/@ODSC/intro-to-language-processing-with-the-nltk-59aa26b9d056 
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

def open_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    
    return data

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

def ner(data):
    result = nlp(data)
    return [(X.text, X.label_) for X in result.ents]

# you'll need this in command line: $ python -m spacy download en_core_web_lg
coreferences = spacy.load('en_coref_lg')
neuralcoref.add_to_pipe(coreferences)
def coref(preprocessed):
    result = preprocessed
    for i in range(preprocessed):
        sentence = preprocessed[i]
        for j in range(sentence):
            token = sentence[j]
            if token.pos_ == 'PRON' and token._.in_coref:
                for cluster in token._.coref_clusters:
                    result[i][j] = cluster.main.text
    return result

parser = argparse.ArgumentParser()
parser.add_argument("articles", help="Articles to parse from") # will make a list later on
parser.add_argument("--questions", help="Questions to parse, if answering")
args = parser.parse_args()

data = open_file(args.articles)
(data_preprocessed, data_tagged) = pos_tokenize(data)
data_ner = ner(data)
pprint(data_ner)
print(data_tagged[0])
print(data_preprocessed)
test = coreferences("Obama was the president. He is great.")
(test_preprocessed, test_tagged) = pos_tokenize(test)
print(coref(test_preprocessed))