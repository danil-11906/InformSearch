import pymorphy2
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize


class InvertedIndex:

    def __init__(self):
        self.lemmasFile = open('lemma.txt', 'r', encoding='utf-8')
        self.infinitive = dict()
        self.infinitiveIndex = dict()
        self.invertedIndexFile = open('invertedIndex.txt', 'w')
        self.morph = pymorphy2.MorphAnalyzer()

    def getInfinitiveFromLemmas(self):
        for line in self.lemmasFile.readlines():
            lineSplit = line.split('\n')
            inf = lineSplit[0]
            self.infinitiveIndex[inf] = list()

    def checkFiles(self):
        pagesPath = 'texts/'
        for i in range(0, 100):
            print(str(i+1) + " page")
            file = open(pagesPath + str(i+1) + '.txt', 'r', encoding='utf-8')
            body = BeautifulSoup(file, features='html.parser').get_text()
            wordList = wordpunct_tokenize(body)
            words = set()
            for word in wordList:
                wordInfo = self.morph.parse(word)[0]
                normalForm = wordInfo.normal_form
                if normalForm in self.infinitiveIndex:
                    self.infinitiveIndex[normalForm].append(i+1)
            file.close()
        for key, value in self.infinitiveIndex.items():
            value.sort()

    def writeIndexToFile(self):
        for key, value in self.infinitiveIndex.items():
            vstring = []
            for v in value:
                vstring.append(str(v))
            s = key + ': ' + ' '.join(sorted(set(vstring))) + '\n'
            self.invertedIndexFile.write(s)
        self.invertedIndexFile.close()

def unique_list(list):
    ulist = []
    [ulist.append(x) for x in list if x not in ulist]
    return ulist
if __name__ == '__main__':
    invertedIndex = InvertedIndex()
    invertedIndex.getInfinitiveFromLemmas()
    invertedIndex.checkFiles()
    invertedIndex.writeIndexToFile()