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
        # (verb, index, whword) = assignments
        for (i in range(len(assignments))):
            # read in the ith element of assignments
            (verb, index, whword) = assignments[i]
            # get the ith sentence corresponding to assignment, tagged
            sentence = self.tagged[i]
            # initialize blank list representing question
            question = []
            question.append(whword)
            question.append(verb)
            # now need a way to determine whether to use noun phrase from
            # before or after the verb


        
    
    def generateYesQ(self)

    def generateNoQ(self)

    def getTopNQs(self)