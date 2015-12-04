import os
import cPickle as pickle
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from random import randint

class MyDictionary(object):
    def __init__(self):
        self.data = {}
        self.separators = [u',', u'\'', u'\"', u':', u';']
    def new(self, key, value):
        if value in self.separators:
            return
        values = self.data.get(key, {})
        occurrence = values.get(value, 0)
        values.update({value : occurrence + 1})
        self.data.update({key : values})
        
        
def parse_data(my_file, data):
    text = ''.join(my_file.readlines()).decode('utf-8')
    word_list = word_tokenize(text)
    for i, word in enumerate(word_list[0:-1]):
        data.new(word, word_list[i + 1])
    for i, word in enumerate(word_list[0:-2]):
        data.new(word + word_list[i + 1], word_list[i + 2])


def preserve_data(data):
    pickle_in = pickle.Pickler(open('statistics_data.pickle', "wb"))
    pickle_in.fast = True
    pickle_in.dump(data)


def load_data():
    return pickle.load(open('statistics_data.pickle', "rb"))


def process_corpus():
    statistics_data = MyDictionary()
    for author in os.listdir('.'):
        if os.path.isdir(author):
            for book in os.listdir(author):
                parse_data(open(author + '/' + book, "r"), statistics_data)
    preserve_data(statistics_data)
    return statistics_data


def generate_text(length, data):
    mark = ['.', '?', '!']
    text = ['.']
    text.append(roll('.', data))
    while len(text) < length or text[-1] not in mark:
        if text[-1] in mark:
            text.append(roll(text[-1], data))
        else:
            text.append(roll(text[-2] + text[-1], data))
    final_text = ''
    for word in text[1:-1]:
        if word not in mark:
            final_text = final_text + ' '
        final_text = final_text + word
    return final_text
        

def roll(prefix, data):
    if prefix not in data.data:
        return u'.'
    words = data.data[prefix].keys()
    probs = data.data[prefix].values()
    alpha = randint(1, sum(probs))
    for i, element in enumerate(probs):
        if element >= alpha:
            return words[i]
        else:
            alpha -= element


#data = process_corpus()

data = load_data()
open("text.txt", "wb").write(generate_text(12121, data).encode('utf-8'))
