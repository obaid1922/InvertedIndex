from bs4 import BeautifulSoup
import re
from os import listdir
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer as tokenizer
import sys
import regex


class Posting:
    docId = -1
    positionList = []


def writeMappings(dictionary, fileName):
    file = open(fileName, "w", encoding="utf-8")
    for key in dictionary:
        file.write(str(dictionary[key]) + "\t" + str(key) + "\n")
    file.close()


def writeSortBasedIndex(index):
    previousTerm = currentTerm = 0
    file = open("SortBasedInvertedIndex.txt", "w", encoding="utf-8")
    for term in index:
        previousDoc = 0
        currentDoc = term[1].docId
        file.write(str(term[0]) + "\t")
        wordFrequency = 0
        for i in range(1, len(term)):
            wordFrequency += len(term[i].positionList)
        file.write(str(wordFrequency) + "\t")
        file.write(str(len(term) - 1) + "\t")
        for i in range(1, len(term)):
            currentDoc = term[i].docId
            previousPostion = 0
            for position in term[i].positionList:
                file.write(str(currentDoc - previousDoc) + "\t")
                file.write(str(position - previousPostion) + "\t")
                previousPostion = position
                previousDoc = currentDoc
        file.write("\n")


def writeHashIndex(indexHashMap):
    previousTerm = currentTerm = 0

    file = open("term_index.txt", "w", encoding="utf-8")
    for key in indexHashMap:
        previousDoc = 0
        currentDoc = list(indexHashMap[key])[0]
        file.write(str(key) + "\t")
        wordFrequency = 0
        for innerKey in indexHashMap[key]:
            wordFrequency += len(indexHashMap[key][innerKey])

        file.write(str(wordFrequency) + "\t")
        file.write(str(len(indexHashMap[key])) + "\t")
        for innerKey in indexHashMap[key]:
            currentDoc = innerKey
            previousPosition = 0
            previousPosition = 0
            for position in indexHashMap[key][innerKey]:
                file.write(str(currentDoc - previousDoc) + "\t")
                file.write(str(position - previousPosition) + "\t")
                previousPosition = position
                previousDoc = currentDoc

        file.write("\n")


def sortBasedIndexer(tupleList):
    print("sorting ..............")
    tupleList.sort(key=lambda t: t[0])
    previousDocId = tupleList[0][1]
    currentDocId = tupleList[0][1]
    previousTermId = tupleList[0][0]
    currentTermId = tupleList[0][0]
    index = []
    termCounter = 0
    docCounter = 1
    post = Posting()
    post.docId = currentDocId
    post.positionList.append(tupleList[0][2])
    index = [[tupleList[0][0]]]
    index[0].append(post)

    for i in range(1, len(tupleList)):
        currentDocId = tupleList[i][1]
        currentTermId = tupleList[i][0]
        if currentTermId == previousTermId and currentDocId == previousDocId:
            index[termCounter][docCounter].positionList.append(tupleList[i][2])
        elif currentTermId != previousTermId:
            index.append([currentTermId])
            termCounter += 1
            docCounter = 1
            post = Posting()
            post.docId = currentDocId
            post.positionList = []
            post.positionList.append(tupleList[i][2])
            index[termCounter].append(post)

        elif currentDocId != previousDocId:
            post = Posting()
            post.docId = currentDocId
            post.positionList = []
            post.positionList.append(tupleList[i][2])
            index[termCounter].append(post)
            docCounter += 1

        previousDocId = currentDocId
        previousTermId = currentTermId
    return index


#path = str(sys.argv[1])
path = "/home/obaid/PycharmProjects/InvertedIndex/test"
fileNames = listdir(path)
docId = 0
termId = 0
vocabulary = {}
stopwords = {}
documentId = {}
hashInvertedIndex = {}
tupleList = []
stopFile = set(open("stoplist.txt").read().splitlines())
for line in stopFile:
    stopwords[line] = 0
for name in fileNames:
    soup = BeautifulSoup(open(path + "/" + name, 'rb').read(), "html.parser", from_encoding="iso-8859-1")
    soup = soup.find("body")
    if soup:
        print(docId)
        documentId[name] = docId
        docId += 1
        for junk in soup(["script", "style"]):
            junk.decompose()
        data = soup.get_text()
        words = re.findall(r"\b[0-9A-Za-z]+(?:['-]?[0-9A-Za-z]+)*\b", data)
        positionCounter = 0
        for word in words:
            word = word.lower()
            word = PorterStemmer().stem(word)
            if word not in vocabulary and word not in stopwords and len(word) > 1:
                vocabulary[word] = termId
                termId += 1
            if word not in stopwords and len(word) > 1:
                tupleList.append((vocabulary[word], documentId[name], positionCounter))
                if vocabulary[word] not in hashInvertedIndex:
                    innerHash = dict()
                    innerHash.setdefault(documentId[name], []).append(positionCounter)
                    hashInvertedIndex[vocabulary[word]] = innerHash
                else:
                    if documentId[name] in hashInvertedIndex[vocabulary[word]]:
                        tempList = hashInvertedIndex[vocabulary[word]][documentId[name]]
                        tempList.append(positionCounter)
                        hashInvertedIndex[vocabulary[word]][documentId[name]] = tempList
                    else:
                        tempList = [positionCounter]
                        hashInvertedIndex[vocabulary[word]][documentId[name]] = tempList
            positionCounter += 1

writeHashIndex(hashInvertedIndex)
writeSortBasedIndex(sortBasedIndexer(tupleList))
writeMappings(vocabulary, "termids.txt")
writeMappings(documentId, "docids.txt")
