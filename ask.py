import nltk
import string
from bllipparser import RerankingParser
rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
import spacy
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

class Generation():
    def __init__(self, preprocessed_data, tagged_data, ner_data, n):
        self.n = n
        # list of sentences, each sentence is a list of words as strings
        self.data = preprocessed_data
        # list of list of (word, POS tag) tuples
        self.tagged = tagged_data
        # ner data in spacy format
        self.ner = ner_data
        # set of all the questions we generate (questions are in the form of strings)
        self.questions = set()

    # Returns the preceeding part of a parse_tree
    def printPhraseBefore(self, parse_tree, index):
        phrase = ""
        if index == 0:
            return phrase
        for i in range(index-1):
            phrase = phrase + parse_tree[0][i] + " "
        return phrase
    # Returns the successive part of a parse_tree
    # Someone please check my indexing - Jon
    def printPhraseAfter(self, parse_tree, index):
        phrase = ""
        if index == (len(parse_tree)-1):
            return phrase 
        for i in range(len(parse_tree[0])-index-1):
            phrase = " " + phrase + parse_tree[0][i+index+1]
        return phrase

    def printSubstitutedVP(self, parse_tree):
        for i in range(len(parse_tree)):
            self.questions.add(printSubstituted())

    # Returns a phrase with NP in index substituted for appropraite WH word
    # If no NP found within indexed subtree, returns empty string
    # Hope to eventually make this recursive:
    # NOTE: current implementation only checks top level tree,
    # TODO: implement recursion to check all levels of the tree for replacable NP
    def printSubstituted(self, parse_tree, index):
        # Get a subtree, check its label
        subtree = parse_tree[0][index]
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
            return wh_word
        # NOTE: This else case should eventually be recursive
        else:
            self.printSubstitutedVP(subtree)
            return ""
    # Get WH questions
    def generateWHQ(self):
        verb_tags = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
        # Loop through sentences
        for sentence in self.tagged:
            # Construct parse_tree
            parse_tree = rrp.parse_tagged(sentence)
            # Loop through the top layer of sentence
            for i in range(len(parse_tree[0])):
                # Get possible substitution for a NP in this index
                wh_phrase = self.printSubstituted(parse_tree, i)
                # Check for successful replacement
                if (wh_phrase != ""):
                    # Get the rest of the sentence and construct question
                    prev_phrase = self.printPhraseBefore(parse_tree, i)
                    next_phrase = self.printPhraseAfter(parse_tree, i)
                    question = prev_phrase + wh_phrase + next_phrase + " ?"
                    self.questions.add(question)

                    # Leftover from old implementation
                    # for verb_subtree in subtree:
                        # verb found
                        # if verb_subtree.label in verb_tags:
                            # now iterate over all noun phrases
                                        # NOTE: for "why" and "how", we prob
                                        # need a way besides using NER. for
                                        # example detecting words like "because"
                    
    auxi_verbs = ["am", "is", "are", "was", "were", "have", "has", 
    "had", "do", "does", "did", "will", "would", "shall", "should", 
    "may", "might", "must", "can", "could"]
    def generateYesQ(self):
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
        for sentence in self.data:
            question = sentence_yes_questions(sentence)
            if not(question == ""):
                self.questions.add(question)
        

    def generateNoQ(self):

    def getTopNQs(self):