import nltk
from nltk.corpus import wordnet
import string

# downloading packages
nltk.download('wordnet')

helping_verbs = ["am", "is", "are", "was", "were",
"have", "has", "had", "do", "does", "did", "will",
"would", "shall", "should", "may", "might", "must",
"can", "could"]

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
    
    def assignWHWord(self):
        return

    # input is list of 3 tuples returned by self.assignWHWord()
    def generateWHWord(self, assignments):
        # (verb, index, whword) = assignments
        for i in range(len(assignments)):
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
    
    def generateYesQ(self):
        return

    def generateNoQ(self, input_sentence):
        result = []
        pos_tagged = nltk.pos_tag(nltk.word_tokenize(input_sentence)) # change when preprocessing finalized
        sentence = input_sentence.split()

        for i in range(len(sentence)):
            if sentence[i] in helping_verbs:
                for j in range(i):
                    result.append(sentence[j])

                result.append("not")

                if i < len(sentence) - 1:
                    for k in range(i+1, len(sentence)):
                        result.append(sentence[k])
                
                result.insert(0, sentence[i][0].swapcase() + sentence[i][1:])
                result.append("?")

        self.questions.add(" ".join(result))

        result = []
        for i in range(len(pos_tagged)):
            if pos_tagged[i][0] in helping_verbs:
                for j in range(i):
                    result.append(pos_tagged[j][0])

                if i < len(pos_tagged) - 1:
                    for k in range(i+1, len(pos_tagged)):
                        # if punctuation, pass
                        if pos_tagged[k][0] in string.punctuation:
                            continue

                        # check if there's an adjective that can be negated
                        if pos_tagged[k][1] == 'JJ':
                            antonyms = []
                            for syn in wordnet.synsets(pos_tagged[k][0]):
                                for lemma in syn.lemmas():
                                    if lemma.antonyms():
                                        antonyms.append(lemma.antonyms()[0].name())
                                        break
                            # for now, just add the first antonym; but later, should be able to add all antonyms
                            if len(antonyms) > 0:
                                result.append(antonyms[0])

                        else:
                            result.append(pos_tagged[k][0])
                
                result.insert(0, pos_tagged[i][0][0].swapcase() + pos_tagged[i][0][1:])
                result.append("?")
        self.questions.add(" ".join(result))

    def getTopNQs(self):
        return

sample = Generation("","","","")
sample.generateNoQ("Obama was the 10th president.")
print(sample.questions)