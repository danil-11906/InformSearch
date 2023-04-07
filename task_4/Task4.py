import json
import os
import math

class TF_IDF_Calculator:

    @staticmethod
    def calculate(term, document_tokens_list, documents_count, documents_with_term_count):
        TF = document_tokens_list.count(term[:-1]) / len(document_tokens_list)
        IDF = math.log(documents_count / documents_with_term_count)
        return round(TF, 6), round(IDF, 6), round(TF * IDF, 6)


def tf_idf():
    print("\n-> Starting TF-IDF calculator...")
    all_filenames = os.listdir('lemmas')
    with open('invertedIndex.json') as json_file:
        inverted_index = json.load(json_file)
    result = {}
    i = 0
    for term in inverted_index.keys():
        i += 1
        print(f"{i} word into {len(inverted_index)}")
        docs_with_term = inverted_index[term]
        for doc_index in docs_with_term:
            lem_file_path = "lemmas/lemmas_" + doc_index + ".txt"

            with open(lem_file_path, 'r', encoding='UTF-8') as file:
                tokens = file.read().split(' ')
            TF, IDF, TF_IDF = TF_IDF_Calculator.calculate(term,
                                                          tokens,
                                                          len(all_filenames),
                                                          len(docs_with_term))
            try:
                result[term][doc_index] = {"TF": TF,
                                           "IDF": IDF,
                                           "TF-IDF": TF_IDF}
            except KeyError:
                result[term] = {doc_index: {"TF": TF,
                                            "IDF": IDF,
                                            "TF-IDF": TF_IDF}}

    dump = json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    text_file = open('TF-IDF.json', "w")
    text_file.write(dump)
    text_file.close()

if __name__ == '__main__':
    tf_idf()