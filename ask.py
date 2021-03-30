import nltk

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
    
    def assignWHWord(self)

    # input is list of 3 tuples returned by self.assignWHWord()
    def generateWHWord(self, assignments)
        (verb, index, whword) = assignments
    
    def generateYesQ(self)

    def generateNoQ(self)

    def getTopNQs(self)