#!/usr/bin/env python3

import nltk
import string
from bllipparser import RerankingParser
rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
import spacy
from spacy import displacy
import en_core_web_md
nlp = en_core_web_md.load()
import sys
import preprocessing as preprocess
from nltk.corpus import wordnet

auxi_verbs = ["am", "is", "are", "was", "were", "have", "has", 
    "had", "do", "does", "did", "will", "would", "shall", "should", 
    "may", "might", "must", "can", "could"]

class Answerer():
    def __init__(self, preprocessed_data, tagged_data, vectors_data, ner_data, 
    preprocessed_questions, tagged_questions, vectors_questions, ner_questions):
        # list of sentences, each sentence is a list of words as strings
        self.data = preprocessed_data
        # list of list of (word, POS tag) tuples
        self.tagged = tagged_data
        # list of vectors of sentence meanings
        self.vectors = vectors_data
        # ner data in spacy format
        self.ner = ner_data
        # list of questions, each question is a list of words as strings
        self.questions = preprocessed_questions
        # list of list of (word, POS tag) tuples
        self.tagged_questions = tagged_questions
        # list of vectors of question meanings
        self.question_vectors = vectors_questions
        # ner questions in spacy format
        self.ner_questions = ner_questions
        # list of all the answers in order of questions asked
        # (questions are in the form of strings)
        self.answers = []
        self.wh_tags = ['WDT', 'WP', 'WRB']



    # input i: the index of the question we are identifying
    # returns True if question at self.questions[i] is a WH-question
    # returns False otherwise
    def isWHQuestion(self, i):
        for (word, tag) in self.tagged_questions[i]:
            if tag in self.wh_tags:
                return True
        return False
            
    # answers the ith question
    # given a question, parses the document looking for the sentence with the highest similarity and returns it
    # input i: the index of question to answer
    # REQUIRES: ith question is WH question
    # output: string that is the most likely answer
    def answerWHQuestion(self, i):
        # store a running tab of the index of the current most similar sentence
        candidate_index = 0
        for j in range(len(self.vectors)):
            if self.vectors[j].similarity(self.question_vectors[i]) > self.vectors[candidate_index].similarity(self.questions_vectors[i]):
                candidate_index = j
        return self.data[candidate_index]
            # find answer in sentence by going through each NP in the sentence
            # and seeing if the NP is in the question. If it is, we ignore.
            # If it isn't, then we check the NER of the NP. If the named entity
            # matches our WH-word, we add this NP as the answer to possible answers
  
    # answers the ith question
    # input i: the index of question to answer
    # REQUIRES: ith question is Yes/no question
    # output: string that is the most likely answer
    def answerYesNoQuestion(self, i):
        return

    # answers questions in self.questions and puts answers in same order
    # in self.answers
    # output: none
    def answerQuestions(self):
        for i in range(len(self.questions)):
            if self.isWHQuestion(i):
                self.answers.append(self.answerWHQuestion(i))
            else:
                # TODO: implement answerY/N
                self.answers.append(self.answerYesNoQuestion(i))
        return

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
    vectors_data = preprocess.vectors(data)
    ner_data = preprocess.ner(data)

    # preprocess questions
    questions = preprocess.open_file(questions_file)
    (preprocessed_questions, tagged_questions) = preprocess.pos_tokenize(questions)
    vectors_questions = preprocess.vectors(questions)
    ner_questions = preprocess.ner(questions)

    # make the question answerer
    qAnswerer = Answerer(preprocessed_data, tagged_data, vectors_data, ner_data, preprocessed_questions, tagged_questions, vectors_questions, ner_questions)
    # answer questions
    qAnswerer.answerQuestions()
    # print results
    qAnswerer.printAnswers()