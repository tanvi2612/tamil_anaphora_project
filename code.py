#witness the end product of an deadline fueled full speed code smash and dash

import sys

import nltk
from nltk.corpus import names
from itertools import islice

def window(seq, n):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

nominal_labels = ["NN", "NNS", "NNP", "NNPS", "PRP"]

number_info = \
    {"NN": "singular",
     "NNP": "singular",
     "அவரை": "singular", #
     "அவளை": "singular", #
     "அவன்": "singular", #
     "அவர்": "singular", #
     "அவள்": "singular", #
     "அது": "singular", #
     "NNS": "plural",
     "NNPS": "plural",
     "அவர்கள்": "plural",#
     "அவர்களுக்கு": "plural", #
     "தங்களை": "plural", #
     "அவர்களே": "plural", #
     "PRP": None
     }

group_pronouns=["அவர்களே","தங்களை","அவர்களுக்கு","அவர்கள்"]
male_pronouns = ["அவர்","அவன்", "அவரை"]
female_pronouns = ["அவள்", "அவளை"]
neuter_pronouns = ["அது"]

def detect_anaphores(sentence): #returns a list of words for resolution
    anaphores=[]
    for i in sentence:
        word=i.split('/')

        if len(word)!=2:
            continue

        if word[0] in male_pronouns or word[0] in group_pronouns or word[0] in female_pronouns or word[0] in neuter_pronouns:
            anaphores.append(i)
            print("Anaphora detected in sentence:- ",sentence)

    return anaphores

def number_match(candidate, pro):
    # the pronoun both map to the same number feature, they match
    candidate=candidate.split('/')
    pro=pro.split('/')

    if candidate[1] in nominal_labels and number_info[candidate[1]] == number_info[pro[0]]: #if it is a tag that should be considered and the tags number info is the same as number info of the pronoun
        return True
    return False

def gender_match(candidate, pro):
    """ Takes a proposed antecedent and pronoun and checks whether
    they match in gender. Only checks for mismatches between singular
    proper name antecedents and singular pronouns.
    """


    male_names = (name.lower() for name in names.words('male.txt'))
    female_names = (name.lower() for name in names.words('female.txt'))

    candidate=candidate.split('/')
    pro = pro.split( '/' )

    if candidate[1] in nominal_labels: #one of the tags to be considered

        if candidate[0].lower() in male_names:
            if (pro[0] in female_pronouns or pro[0] in neuter_pronouns):
                return False

        # If the proposed antecedent is a recognized female name,
        # but the pronoun being resolved is either male or
        # neuter, they don't match
        elif candidate[0].lower() in female_names:
            if (pro[0] in male_pronouns or pro[0] in neuter_pronouns):
                return False

        # If the proposed antecedent is a numeral, but the
        # pronoun being resolved is not neuter, they don't match
        elif candidate[0].isdigit():
            if (pro[0] in male_pronouns or pro[0] in female_pronouns):
                return False

    #note no checks for group pronouns because honorific use of group pronouns is possible
    return True

def process_sentences(three_sent):
    process_sentences.counter += 1  #keeps track of the window number

    three_sent=[s for s in three_sent ]
    for itr,sent in enumerate(three_sent): #itr is from 0 to 2 cos of the window
        sent=sent.split('\n')
        sent=sent[0].split(' ')

        if itr+process_sentences.counter not in process_sentences.skip: #if not an already anaphora processed sentence
            anaphores=detect_anaphores(sent) #passing a list to find the presence of an anaphora that needs resolution

            if len(anaphores) > 0: #resolution needed for the list of anaphores

                print("the anaphores detected to be resolved are "+ str(anaphores))
                for num in range(itr-1,-1,-1): #iterating back through the window of 3 sentences
                    sentence=three_sent[num]

                    #formatting
                    sentence = sentence.split( '\n' )
                    sentence = sentence[0].split( ' ' )
                    #done

                    for an in anaphores: #for the current considered anaphore
                        for w in sentence: #for the words of the sentence
                            if (number_match(w,an) and gender_match(w,an)):# if fitting antecedent found
                                print(" Antecedent for \'"+an+"\' is :- "+w)
                                process_sentences.skip.append(process_sentences.counter+itr)
                                anaphores.remove(an)    #removing resolved anaphore
                                break


process_sentences.counter = 0
process_sentences.skip = []

def main(argv):
    if len(sys.argv) != 2 :
        print("Enter the file as an arguement please ")

    elif len(sys.argv) == 2:
        fname = sys.argv[1]

        with open(fname) as f:
            sents = f.readlines()



        three_sent=window(sents,3)
        for x in three_sent:
            process_sentences(x)


if __name__ == "__main__":
    main(sys.argv)
