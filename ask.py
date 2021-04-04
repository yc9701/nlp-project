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

    # Prints the preceeding part of a parse_tree
    def printPhraseBefore(self, parse_tree, index):
        phrase = ""
        for i in range(index-1):
            phrase = phrase + parse_tree[0][i] + " "
        return phrase
    # Printes the successding part of a parse_tree
    def printPhraseAfter(self, parse_tree, index):
        phrase = ""
        for i in range(len(parse_tree[0])-index-1):
            phrase = " " + phrase + parse_tree[0][i+index+1]
        return phrase
    def assignWHWord(self):
        verb_tags = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
        verbs = []
        for sentence in self.tagged:
            parse_tree = rrp.parse_tagged(sentence)
            for i in range(len(parse_tree[0])):
                subtree = parse_tree[0][i]
                if subtree.label == 'VP':
                    for verb_subtree in subtree:
                        # verb found
                        if verb_subtree.label in verb_tags:
                            # now iterate over all noun phrases
                            for j in range(len(parse_tree[0])):
                                noun_subtree = parse_tree[0][j]
                                if noun_subtree.label == 'NP':
                                    # TODO: JUST TO HELP U JON:
                                    # i : index of VP
                                    # j : index of NP
                                    # verb_subtree.token : the actual verb
                                    # verb_subtree.label : the specific verb tag
                                    # noun_subtree.token : the noun phrase
                                    doc = nlp(noun_subtree.token)
                                    # should have just 1 entity b/c we have just
                                    # 1 noun phrase
                                    # case whether VP comes before/after NP
                                    if 0 < i and i < j:
                                        # Get the phrase before this VP
                                        prev_NP = parse_tree[0][i-1]
                                        for ent in doc.ents:
                                            if ent.label_ == 'PERSON':
                                                # WH-word = who
                                                question = subtree.token + " who?"
                                                self.questions.add(question)
                                            elif ent.label_ == "DATE":
                                                # WH-word = when
                                                question = subtree.token + " what date?"
                                                self.questions.add(question)
                                            elif ent.label == "TIME":
                                                # WH-word = when
                                                question = subtree.token + " what time?"
                                                self.questions.add(question)
                                            elif ent.label_ == 'LOCATION':
                                                # WH-word = where
                                                question = subtree.token + " where?"
                                                self.questions.add(question)
                                            else:
                                                # WH-word = what
                                                question = subtree.token + " what?"
                                                self.questions.add(question)
                                    else:
                                        for ent in doc.ents:
                                            if ent.label_ == 'PERSON':
                                                # WH-word = who
                                                question = "Who did" + noun_subtree.token + " " + verb_subtree.token + "?"
                                                self.questions.add(question)
                                            elif ent.label_ in ['DATE', 'TIME']:
                                                # WH-word = when
                                                self.questions.add()
                                            elif ent.label_ == 'LOCATION':
                                                # WH-word = where
                                                self.questions.add()
                                            else:
                                                # WH-word = what
                                                self.questions.add()
                                        # NOTE: for "why" and "how", we prob
                                        # need a way besides using NER. for
                                        # example detecting words like "because"
                    

    # input is list of tuples returned by self.assignWHWord()
    def generateWHWord(self, assignments):
        # (verb, whword) = assignments
        for (i in range(len(assignments))):
            # read in the ith element of assignments
            (verb, whword) = assignments[i]
            # get the ith sentence corresponding to assignment, tagged
            sentence = self.tagged[i]
            # initialize blank list representing question
            question = []
            question.append(whword)
            question.append(verb)
            # now need a way to determine whether to use noun phrase from
            # before or after the verb
            # lazy implementation is just adding both


        
    
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