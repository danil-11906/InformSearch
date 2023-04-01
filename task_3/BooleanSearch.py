import pymorphy2


class BooleanSearch:

    def __init__(self):
        self.invertedIndexFile = open('invertedIndex.txt', 'r')
        self.infinitiveIndex = self.getInfinitiveIndexArray()
        self.morph = pymorphy2.MorphAnalyzer()

    def getInfinitiveIndexArray(self):
        d = dict()
        lines = self.invertedIndexFile.readlines()
        for line in lines:
            strings = line.split('\n')[0].split(': ')
            k = strings[0]
            other = strings[1].strip().split(' ')
            d[k] = []
            for i in other:
                d[k].append(i)
        self.invertedIndexFile.close()
        return d

    def getInfinitive(self, q):
        wordInfo = self.morph.parse(q)[0]
        normalForm = wordInfo.normal_form if wordInfo.normalized.is_known else q.lower()
        return normalForm

    def getInfinitiveIndex(self, q):
        q = self.getInfinitive(q)
        if q in self.infinitiveIndex.keys():
            return self.infinitiveIndex[q]
        else:
            list()

    def __and__(self, q1, q2):
        if type(q1) is str:
            v1 = self.getInfinitiveIndex(q1)
        else:
            v1 = q1[:]
        if type(q2) is list:
            v2 = q2[:]
        else:
            v2 = self.getInfinitiveIndex(q2)
        res = list()
        for i in v1:
            if i in v2:
                res.append(i)
        return res

    def __or__(self, q1, q2):
        if type(q1) is str:
            v1 = self.getInfinitiveIndex(q1)
        else:
            v1 = q1[:]
        if type(q2) is list:
            v2 = q2[:]
        else:
            v2 = self.getInfinitiveIndex(q2)
        for i in v2:
            v1.append(i)
        return list(set(v1))

    def __not__(self, q1):
        v1 = self.getInfinitiveIndex(q1)
        v2 = v1[:]
        v2.clear()
        for i in range(100):
            v2.append(str(i+1))
        for i in v1:
            v2.remove(i)
        return v2


if __name__ == '__main__':
    bs = BooleanSearch()
    print(bs.__and__(bs.__not__('агроновость'), bs.__or__(bs.__not__('авто'), 'администрация')))

