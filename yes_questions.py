import string
#inout: one sentence, output: a yes question
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

#Testing command: print(sentence_yes_questions(["Obdama", "is", "the", "president", "."]))
#print(sentence_yes_questions(["He", "has", "been", "studying", "."]))

