#!/usr/bin/env python3

import nltk
import string
from bllipparser import RerankingParser
rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
import spacy
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

class Generator():
    def __init__(self, preprocessed_data, tagged_data, ner_data):
        # list of sentences, each sentence is a list of words as strings
        self.data = preprocessed_data
        # list of list of (word, POS tag) tuples
        self.tagged = tagged_data
        # ner data in spacy format
        self.ner = ner_data
        # set of all the questions we generate (questions are in the form of strings)
        self.questions = set()

    # capitalize first letter in the sentence
    def capitalizeSent(self, sentence):
        firstLetter = sentence[0].upper()
        restOfSent = sentence[1:len(sentence)]
        return firstLetter + restOfSent

    # Returns the preceeding part of a parse_tree
    # NOTE: Includes a trailing whitespace if non-empty
    def printPhraseBefore(self, parse_tree, index):
        phrase = ""
        if index == 0:
            return phrase
        for i in range(index):
            phrase = phrase + parse_tree[i].token + " "
        return phrase

    # Returns the successive part of a parse_tree
    # NOTE: Includes a leading whitespace if non-empty
    def printPhraseAfter(self, parse_tree, index):
        phrase = ""
        if index == (len(parse_tree)-1):
            return phrase 
        for i in range(index + 1, len(parse_tree)):
            phrase = " " + phrase + parse_tree[i].token
        return phrase
    
    # Recursive helper for getSubstitutions, loops through a non-NP phrase
    def getSubRecursive(self, parse_tree):
        # Initialize an empty set
        result = set()
        # Loop through each labeled part of the phrase
        for i in range(len(parse_tree)):
            # Recursive call to search for possible substitutions
            poss_subs = self.getSubstitutions(parse_tree, i)
            # For each substitution, make that change in our phrase
            for sub in poss_subs:
                prev_phrase = self.printPhraseBefore(parse_tree, i)
                next_phrase = self.printPhraseAfter(parse_tree, i)
                comb_phrase = prev_phrase + sub + next_phrase
                # Add the changed phrase to result set
                result.add(comb_phrase)
        # Return (possibly empty) set of all(?) possible changes
        return result

    # Returns a set of phrases, where each phrase makes a substitution
    # of a NP with an appropriate WH word
    # If no NP found within indexed subtree, returns empty string
    # Hope to eventually make this recursive:
    # NOTE: current implementation only checks top level tree,
    # TODO: implement recursion to check all levels of the tree for replacable NP
    def getSubstitutions(self, parse_tree, index):
        # Get a subtree, check its label
        subtree = parse_tree[index]
        # (Replacable) noun phrase found
        if subtree.label == 'NP':
            # Find the entity type of the NP
            doc = nlp(subtree.token)
            # Hopefully these top level NP are fairly simple
            # Guess every relevant WH word for substitution
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    # WH-word = who
                    wh_word = {"who"}
                elif ent.label_ == "DATE":
                    # WH-word = when
                    wh_word = {"when"}
                elif ent.label == "TIME":
                    # WH-word = when
                    wh_word = {"when"}
                elif ent.label_ == 'LOCATION':
                    # WH-word = where
                    wh_word = {"where"}
                else:
                    # WH-word = what
                    wh_word = {"what"}
                # NOTE: Read note in generateWHQ
            return wh_word
        # Recurse and try to look for inner substitutions
        else:
            # If length is 1, there can be no subsitutions
            if len(subtree) <= 1:
                return set()
            # Otherwise, phrase can be further broken down
            else:
                return self.getSubRecursive(subtree)


    # Get WH questions
    def generateWHQ(self):
        # Loop through sentences
        for sentence in self.tagged:
            # Construct parse_tree
            parse_tree = rrp.parse_tagged(sentence)
            # Loop through the top layer of sentence
            for i in range(len(parse_tree[0])):
                # Get possible substitution for a NP in this index
                sub_phrases = self.getSubstitutions(parse_tree[0], i)
                # Check for successful replacement
                for sub in sub_phrases:
                    # Get the rest of the sentence and construct question
                    prev_phrase = self.printPhraseBefore(parse_tree[0], i)
                    next_phrase = self.printPhraseAfter(parse_tree[0], i)
                    question = prev_phrase + sub + next_phrase + "?"
                    # capitalize first letter in sentence
                    question = self.capitalizeSent(question)
                    self.questions.add(question)

        # NOTE: for "why" and "how", we probably
        # need a way besides using NER. for
        # example detecting words like "because" or "due to"
    

    auxi_verbs = ["am", "is", "are", "was", "were", "have", "has", 
    "had", "do", "does", "did", "will", "would", "shall", "should", 
    "may", "might", "must", "can", "could"]
    def sentence_yes_questions(sentence):
        result = []
        for i in range(len(sentence)):
            if (sentence[i] in auxi_verbs):
                for j in range(i):
                    result.append(sentence[j])
                if (i < len(sentence)-1):
                    for k in range(i+1, len(sentence)-1):
                        result.append(sentence[k])
        
                result.insert(0, sentence[i][0].swapcase() + sentence[i][1:])
                result2 = ""
                for word in result:
                    result2+=" "+word
                result2+="?"
                return result2[1:]
        return ""

    def generateYesQ(self):
        for sentence in self.data:
            question = self.sentence_yes_questions(sentence)
            if not(question == ""):
                self.questions.add(question)

    def generateNoQ(self):

    def getTopNQs(self, n):

if __name__ == "__main__":
    # Files
    data_file = sys.argv[1]
    nquestions = sys.argv[2]

    data = open_file(data_file)
    (preprocessed_data, tagged_data) = pos_tokenize(data)
    ner_data = ner(data)

    qGenerator = Generator(preprocessed_data, tagged_data, ner_data)
    qGenerator.generateWHQ()
    qGenerator.generateYesQ()
    qGenerator.generateNoQ()

    questions = qGenerator.getTopNQs(nquestions)
    for question in questions:
        print(question + '\n')