import operator
import nltk
import time
# nltk.download('punkt')        # download nltk requirements for first time
from nltk.util import ngrams
import collections
import re


def main():
        # list of our text file, tokens
        # text = []
        global unigram    # uni-gram dictionary
        unigram = {}
        global bigram     # bi-gram dictionary        # basic implementation
        bigram = {}
        text_split()
        create_dictionary()
        operations()


def text_split():
    start_time = time.time()
    with open("shakespeare.txt", 'rt') as text_file:  # open text file in read mode
        read_file = text_file.read().lower()
        global text
        text = re.sub(r"[?|`|<>;\\/~!@#$%^&*()'.:,\[\]\"{}_+=-]", "", read_file).split()    # regular expression remove symbols faster than .replace()

    # symbols = "~!@#$%^&*()_+=-|}{:\"?><[]\;',./'`"
    # with open("shakespeare.txt", 'rt') as text_file:    # open text file in read mode
    #     read_file = text_file.read().lower().split()    # split file on basis of space
    #
    #     for words in read_file:                 # create list for terms in file
    #         for i in symbols:
    #             words = words.replace(i, '')
    #             # words = re.sub(str(i), "", words)     # optimized
    #
    #         if len(words) > 0:
    #             text.append(words)
    #     print(words)

    with open("segmented.txt", 'wt') as new_file:       # write terms in new file
        for item in text:
            new_file.write(item + '\n')
    file_ngram = open("segmented.txt", 'rt').read()  # used package nltk to create fourgram
    # fil = " ".join(text)        # crete sentences from list
    token = nltk.word_tokenize(file_ngram)
    trigram = ngrams(token, 3)
    fourgrams = ngrams(token, 4)

    global tri, four                # make trigram and fourgram available globally
    tri = collections.Counter(trigram)
    four = collections.Counter(fourgrams)  # make generator object of fourgram, a dictionary
    print("The total number of words : ", len(text))
    print("Time taken: ", time.time()-start_time)


def create_dictionary():
    start_time = time.time()
    for word in text:
        if word in unigram:
            unigram[word] += 1
        else:
            unigram[word] = 1

    sort = sorted(unigram.items(), key=operator.itemgetter(1), reverse=True)        # sorted in descending order
    # reverse for descending order

    # question 1.2.1 Part A 1
    first_20 = sort[:20]            # top 20 items selected
    val = [(i+1, first_20[i][0], first_20[i][1]) for i in range(len(first_20))]         # adding S.N in dictionary
    # print(first_20)
    print('\n The top 20 frequent words are: ')
    print(val)

    # question 1.2.1 Part A 2
    tup = []
    counter = 0
    for i in range(10, 0, -1):      # decreasing loop in 10 to 1
        count = 0

        word = []
        for items in sort[::-1]:       # [::-1] to reverse the list, i.e. in ascending order
            counter += 1
            if items[1] <= i:          #
                if items[1] is i:
                    count += 1
                    word.append(items[0])
                continue        # continue in case of smaller values
            elif items[1] > i:
                break       # break to stop loop after finding bigger value

        tup.append((i, count, word[:3]))    # create tuple with no. of word that has frequency i
    print('\n The bottom words are: ')
    print(tup)
    print("Time taken: ", time.time() - start_time)
    bigram_collector()
    # print(counter)  # total no of iterations


def bigram_collector():
    start_time = time.time()
    for i in range(len(text)-1):        # text[i+1] gives last value so len()-1 to prevent index out of bound
        values = (text[i], text[i+1])

        if values in bigram:      # fix the tuple check part dictionary keys not responding on tuples
            bigram[values] += 1

        else:
            bigram[values] = 1

        # question 1.2.1 Part A 3

    # to create the bigram file
    # with open("bigram.txt", 'wt') as new_file:
    #     for keys in bigram.keys():
    #         new_file.write(str(keys)+'  :  '+str(bigram[keys]) + '\n')

    sort = sorted(bigram.items(), key=operator.itemgetter(1), reverse=True)     # sorting in descending order
    # reverse for descending order
    first_20 = sort[:20]        # taking first 20 items
    val = [(i + 1, first_20[i][0], first_20[i][1]) for i in range(len(first_20))]  # adding S.N value in tuple in dictionary
    # print(first_20)
    print('\n The top 20 frequent bigrams are: ')
    print(val)
    print("Time taken: ", time.time() - start_time)


# Part B
def operations():

    # 1
    print('\n B1')
    print("Probability of word \"the\" is: ", probability('the'))
    print("Probability of word \"become\" is: ", probability('become'))
    print("Probability of word \"brave\" is: ", probability('brave'))
    print("Probability of word \"treason\" is: ", probability('treason'))

    # 2
    print('\n B2')
    print("Probability of \"court | the\" is: ", conditional_probability('court', 'the'))
    print("Probability of \"word | his\" is: ", conditional_probability('word', 'his'))
    print("Probability of \"qualities | rare\" is: ", conditional_probability('qualities', 'rare'))
    print("Probability of \"men | young\" is: ", conditional_probability('men', 'young'))

    # 3
    print('\n B3')
    print("Probability of \"have, sent\" is: ", dependent("have sent"))
    print("Probability of \"will, look, upon\"is: ", dependent("will look upon"))
    print("Probability of \"I, am, no , baby \" is: ",dependent("I am no baby"))
    print("Probability of \"wherefore, art, thou, romeo\" is: ", dependent("wherefore art thou romeo"))

    # 4
    print('\n B4')
    print("Probability of \"have, sent\" if independent is: ", independent('have sent'))
    print("Probability of \"will, look, upon\" if independent is: ", independent('will look upon'))
    print("Probability of \"I, am, no , baby \" if independent is: ", independent('I am no baby'))
    print("Probability of \"wherefore, art, thou, romeo\" if independent is: ", independent('wherefore art thou romeo'))

    # 5
    predict_using_lib("I am no")
    predict_using_lib("wherefore art thou")


def probability(a):
    # for key in unigram.keys():            # comparing every key is too slow so used try: method
    #     if key == a:
    #         return unigram[key] / len(text)         # frequency of word / no. of words
    try:
        return unigram[a]/len(text)
    except KeyError:
        print("No such key", KeyError)


def conditional_probability(a, b):
    # for key in bigram.keys():
    #     if key == (b, a):
    #         return bigram[key] / (probability(key[0]) * len(text))  # freq of bigram / no. of words
    try:
        return bigram[(b, a)] / len(text)
    except KeyError:
        print("No such key", KeyError)


def dependent(sentence):            # for dependent events i.e P(A, B) = P(A) * P(B|A)
    string = sentence.lower().split()
    initial_probability = 1
    for i in range(len(string)):
        if i == 0:
            initial_probability *= probability(string[i])   # calculate P(A)
        else:
            initial_probability *= conditional_probability(string[i], string[i - 1])  # calculate P(B|A)
    return initial_probability


def independent(sentence):              # for independent events i.e P(A, B) = P(A) * P(B)
    string = sentence.lower().split()
    initial_probability = 1
    for i in range(len(string)):
        initial_probability *= probability(string[i])
    return initial_probability


# 2
def predict_using_lib(sentence):        # calculate P’(A,B,C,D) = P(A,B,C,D) * P(D| A, B, C) )
                                        # P(A,B,C,D) = P(A)*P(B|A)*P(C|B)*P(D|C)
    start_time = time.time()
    string = sentence.lower().split()
    # initial_probability = dependent(sentence)   # calculate P(A)*P(B|A)*P(C|B)
    initial_probability = 1
    last_text = string[len(string)-1]
    all_items = {}
    max_prob = {}

    for key in bigram:
        if key[0] == last_text:
            all_items[key] = initial_probability * conditional_probability(key[1], last_text)   # calc P(A,B,C,D) = P(A)*P(B|A)*P(C|B)*P(D|C)


    # for i in all_items():
    #     print(i)

    sort = sorted(all_items.items(), key=operator.itemgetter(1), reverse=True)
    val = [(string[0], string[1], string[2], sort[i][0][1]) for i in range(len(sort))]  # val is list of fourgram with all possible combination
    # print(val[0])              # not accurate prediction made so used below code in try: block
    # print(result.keys())
    # for i in range(len(val)):
    #     for key in result:
    #         if key == val[i]:
    #             # print(key, result[key])
    #             # print(val)
    #             max_prob[key] = all_items[key[2:4]] * result[key]/len(text)     # calculate P’(A,B,C,D) = P(A,B,C,D) * P(D| A, B, C) )
    #             # print(all_items[key[2:4]])

    for i in range(len(val)):
        try:
            max_prob[val[i]] = all_items[val[i][2:4]] * (tri[val[i][1:4]] / len(text)) * four[val[i]] / len(text)   # calculate P’(A,B,C,D) = P(A,B,C,D)* P(D| B, C) * P(D| A, B, C) )
        except ValueError:
            print("No such key ", ValueError)

    # print(max_prob.keys())
    sort = sorted(max_prob.items(), key=operator.itemgetter(1), reverse=True)
    # print(sort[:3])
    print("\nThe most probable word to follow \"" + sentence + "\" is: ", sort[:1][0][0][3])    # get the predicted word from key

    print("Prediction made in: ", time.time() - start_time)


if __name__ == "__main__":
    main()

