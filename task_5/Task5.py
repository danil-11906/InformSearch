import json
import math
import operator
import os

import nltk
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from pymystem3 import Mystem


class Tokenizer:
    def clean_text(self, text):
        tokens = self.__tokenize(text)
        tokens = self.__lemmatize(tokens)
        tokens = self.__remove_stop_words(tokens)
        return tokens
    @staticmethod
    def __tokenize(text):
        tokens = nltk.word_tokenize(text)
        return tokens
    @staticmethod
    def __lemmatize(tokens):
        mystem = Mystem()
        tokens = [token.replace(token, ''.join(mystem.lemmatize(token))) for token in tokens]
        return tokens
    @staticmethod
    def __remove_stop_words(tokens):
        tokens = [re.sub(r"\W", "", token, flags=re.I) for token in tokens]
        stop_words = stopwords.words('russian')
        only_cyrillic_letters = re.compile('[а-яА-Я]')
        tokens = [token.lower() for token in tokens if (token not in stop_words)
                  and only_cyrillic_letters.match(token)
                  and not token.isdigit()
                  and token != '']
        return tokens

def dist_cosine(vec_a, vec_b):
    cosine = cosine_similarity([vec_a], [vec_b])
    return cosine[0][0]

class TF_IDF_Calculator:
    @staticmethod
    def calculate(term, document_tokens_list, documents_count, documents_with_term_count):
        TF = document_tokens_list.count(term) / len(document_tokens_list)
        IDF = math.log(documents_count / documents_with_term_count)
        return round(TF, 6), round(IDF, 6), round(TF * IDF, 6)

class VectorModelSearch:
    def __init__(self):
        self.__tokenizer = Tokenizer()
        self.__all_docs_count = len(os.listdir('lemmas'))
        with open('index.json') as json_file:
            self.__indices = json.load(json_file)
        with open('TF-IDF.json') as json_file:
            self.__tf_idf_calculations = json.load(json_file)
    def search(self, query):
        print("SEARCHING: {}".format(query))
        tokens = self.__tokenizer.clean_text(query)
        if len(tokens) == 0:
            print("Empty query")
            return
        print("LEMMATIZED: {}\n".format(' '.join(tokens)))
        query_vector = []
        for token in tokens:
            doc_with_terms_count = len(self.__tf_idf_calculations[f'{token}:'])
            _, _, tf_idf = TF_IDF_Calculator.calculate(token, tokens, self.__all_docs_count, doc_with_terms_count)
            query_vector.append(tf_idf)
        distances = {}
        for index in self.__indices.keys():
            document_vector = []
            for token in tokens:
                try:
                    tf_idf = self.__tf_idf_calculations[f'{token}:'][index]["TF-IDF"]
                    document_vector.append(tf_idf)
                except KeyError:
                    document_vector.append(0.0)
            distances[index] = dist_cosine(query_vector, document_vector)
        searched_indices = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)
        for index in searched_indices:
            doc_id, tf_idf = index

            if tf_idf < 0.05:
                continue
            print(tf_idf)
            url = self.__indices[doc_id]
            print("Index: {}\nURL:{}\nCosine:{}\n".format(doc_id, url, tf_idf))


vms = VectorModelSearch()
vms.search("всевозможный")
print("========================================")
vms.search("варианты работы гормональный")
print("========================================")
vms.search("варианты работы")