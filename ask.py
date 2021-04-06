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

class Generator():
    def __init__(self, preprocessed_data, tagged_data, ner_data):
        # list of sentences, each sentence is a list of words as strings
        self.data = preprocessed_data
        # list of list of (word, POS tag) tuples
        self.tagged = tagged_data
        # ner data in spacy format
        self.ner = ner_data
        # set of all the questions we generate (questions are in the form of strings)
        self.noQuestions = set()
        self.whQuestions = set()
        self.yesQuestions = set()

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
            phrase = phrase + " ".join(parse_tree.__getitem__(i).tokens()) + " "
        return phrase

    # Returns the successive part of a parse_tree
    # NOTE: Includes a leading whitespace if non-empty
    def printPhraseAfter(self, parse_tree, index):
        phrase = ""
        if index == (len(parse_tree)-1):
            return phrase 
        for i in range(index + 1, len(parse_tree)):
            phrase = " " + phrase + " ".join(parse_tree.__getitem__(i).tokens())
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
        subtree = parse_tree.__getitem__(index)
        # (Replacable) noun phrase found
        if subtree.label == 'NP':
            # Find the entity type of the NP
            doc = nlp(" ".join(subtree.tokens()))
            # Hopefully these top level NP are fairly simple
            # Guess every relevant WH word for substitution
            wh_word = set()
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    # WH-word = who
                    wh_word.add("who")
                elif ent.label_ == "DATE":
                    # WH-word = when
                    wh_word.add("when")
                elif ent.label == "TIME":
                    # WH-word = when
                    wh_word.add("when")
                elif ent.label_ == 'LOCATION':
                    # WH-word = where
                    wh_word.add("where")
                else:
                    # WH-word = what
                    wh_word.add("what")
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
        for sentence in self.data:
            # Construct parse_tree
            scored_parse_obj = rrp.parse(sentence)
            # Loop through the top layer of sentence
            for i in range(scored_parse_obj[0].ptb_parse.__len__()):
                # Get possible substitution for a NP in this index
                sub_phrases = self.getSubstitutions(scored_parse_obj[0].ptb_parse, i)
                # Check for successful replacement
                for sub in sub_phrases:
                    # Get the rest of the sentence and construct question
                    prev_phrase = self.printPhraseBefore(scored_parse_obj[0].ptb_parse, i)
                    next_phrase = self.printPhraseAfter(scored_parse_obj[0].ptb_parse, i)
                    question = prev_phrase + sub + next_phrase + "?"
                    # capitalize first letter in sentence
                    question = self.capitalizeSent(question)
                    self.whQuestions.add(question)

        # NOTE: for "why" and "how", we probably
        # need a way besides using NER. for
        # example detecting words like "because" or "due to"
    

    
    def sentence_yes_questions(self, sentence):
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
                self.yesQuestions.add(question)

    def generateNoQ(self):
        for sentence in self.tagged:
            result = []

            for i in range(len(sentence)):
                if sentence[i][0] in auxi_verbs:
                    for j in range(i):
                        result.append(sentence[j][0])

                    result.append("not")

                    if i < len(sentence) - 1:
                        for k in range(i+1, len(sentence)):
                            result.append(sentence[k][0])
                    
                    result.insert(0, sentence[i][0][0].swapcase() + sentence[i][0][1:])
                    result.append("?")

            self.noQuestions.add(" ".join(result))

            result = []
            for i in range(len(sentence)):
                if sentence[i][0] in auxi_verbs:
                    for j in range(i):
                        result.append(sentence[j][0])

                    if i < len(sentence) - 1:
                        for k in range(i+1, len(sentence)):
                            # if punctuation, pass
                            if sentence[k][0] in string.punctuation:
                                continue

                            # check if there's an adjective that can be negated
                            if sentence[k][1] == 'JJ':
                                antonyms = []
                                for syn in wordnet.synsets(sentence[k][0]):
                                    for lemma in syn.lemmas():
                                        if lemma.antonyms():
                                            antonyms.append(lemma.antonyms()[0].name())
                                            break
                                # for now, just add the first antonym; but later, should be able to add all antonyms
                                if len(antonyms) > 0:
                                    result.append(antonyms[0])

                            else:
                                result.append(sentence[k][0])
                    
                    result.insert(0, sentence[i][0][0].swapcase() + sentence[i][0][1:])
                    result.append("?")
            self.noQuestions.add(" ".join(result))

    def getTopNQs(self, n):
        print("wh questions")
        count = 0
        for i in self.whQuestions:
            count += 1
            print(i)
            if count == 10: break

        print("yes questions")
        count = 0
        for i in self.yesQuestions:
            count += 1
            print(i)
            if count == 10: break
        
        print("no questions")
        count = 0
        for i in self.noQuestions:
            count += 1
            print(i)
            if count == 10: break

if __name__ == "__main__":
    # Files
    data_file = sys.argv[1]
    nquestions = sys.argv[2]

    data = preprocess.open_file(data_file)
    (preprocessed_data, tagged_data) = preprocess.pos_tokenize(data)
    ner_data = preprocess.ner(data)

    qGenerator = Generator(preprocessed_data, tagged_data, ner_data)
    print("WHQ")
    qGenerator.generateWHQ()
    print("YESQ")
    qGenerator.generateYesQ()
    print("NOQ")
    qGenerator.generateNoQ()

    qGenerator.getTopNQs(nquestions)
    # for question in questions:
    #     print(question + '\n')