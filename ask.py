import nltk
from bllipparser import RerankingParser
rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

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
    
    # return list of (verb, WH word) tuples for each sentence
    def assignWHWord(self):
        verb_tags = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
        verbs = []
        for sentence in self.tagged:
            parse_tree = rrp.parse_tagged(sentence)
            for subtree in parse_tree[0]:
                if subtree.label == 'VP':
                    for subSubtree in subtree:
                        if subSubtree.label in verb_tags:
                            verbs.append(subSubtree.token)
                            break
                if subtree.label == 'NP':
                    

    # input is list of 3 tuples returned by self.assignWHWord()
    def generateWHWord(self, assignments):
        # (verb, index, whword) = assignments
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


        
    
    # Mira's implementation that I'm pushing for her
    def generateYesQ(self):
        auxi_verbs = ["am", "is", "are", "was", "were", "have", "has", "had", "do", "does", "did", "will", 
            "would", "shall", "should", "may", "might", "must", "can", "could"]
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
            result.append("?")
            return result
    return result

    def generateNoQ(self):

    def getTopNQs(self):