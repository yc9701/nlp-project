#!/usr/bin/env python3

import nltk
import string
from bllipparser import RerankingParser
rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
import spacy
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()
import sys
import preprocessing as preprocess
from nltk.corpus import wordnet

auxi_verbs = ["am", "is", "are", "was", "were", "have", "has", 
    "had", "do", "does", "did", "will", "would", "shall", "should", 
    "may", "might", "must", "can", "could"]

class Answerer():
    def __init__(self, preprocessed_data, tagged_data, ner_data, preprocessed_questions, tagged_questions, ner_questions):
        # list of sentences, each sentence is a list of words as strings
        self.data = preprocessed_data
        # list of list of (word, POS tag) tuples
        self.tagged = tagged_data
        # ner data in spacy format
        self.ner = ner_data
        # list of questions, each question is a list of words as strings
        self.questions = preprocessed_questions
        # list of list of (word, POS tag) tuples
        self.tagged_questions = tagged_questions
        # ner questions in spacy format
        self.ner_questions = ner_questions
        # list of all the answers in order of questions asked
        # (questions are in the form of strings)
        self.answers = []

    # returns True if question at self.questions[i] is a WH-question
    # returns False otherwise
    wh_tags = ['WDT', 'WP', 'WRB']
    def isWHQuestion(self, i):
        for (word, tag) in self.tagged_questions[i]:
            if tag in wh_tags:
                return True
        return False
    
    def answerWHQuestion(self, i):
        # make a set of important words in question
        
        # go through each sentence in data and find sentences that 
        # could contain the answer to the question
        possibleAnswers = set()
        for sentence in self.data:
            # check if the sentence contains the important words
            # if this sentence possibly contains the answer,
            # find answer in sentence by going through each NP in the sentence
            # and seeing if the NP is in the question. If it is, we ignore.
            # If it isn't, then we check the NER of the NP. If the named entity
            # matches our WH-word, we add this NP as the answer to possible answers

    def answerYesNoQuestion(self, question):

    # answers questions in self.questions and puts answers in same order
    # in self.answers
    def answerQuestions(self):
        for i in range(len(self.questions)):
            if isWHQuestion(i):
                answerWHQuestion(i)
            else:
                # TODO
                answerYesNoQuestion(self.questions[i])

    def printAnswers(self):
        for answer in self.answers:
            print(answer + '\n')

if __name__ == "__main__":
    # Files
    data_file = sys.argv[1]
    questions_file = sys.argv[2]

    # preprocess data
    data = preprocess.open_file(data_file)
    (preprocessed_data, tagged_data) = preprocess.pos_tokenize(data)
    ner_data = preprocess.ner(data)

    # preprocess questions
    questions = preprocess.open_file(questions_file)
    (preprocessed_questions, tagged_questions) = preprocess.pos_tokenize(questions)
    ner_questions = preprocess.ner(questions)

    qAnswerer = Answerer(preprocessed_data, tagged_data, ner_data, preprocessed_questions, tagged_questions, ner_questions)
    # TODO: qAnswerer.generateWHQ()

    qAnswerer.printAnswers()