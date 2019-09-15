from bs4 import BeautifulSoup
import re
from os import listdir
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer as tokenizer
import sys
import regex
import tqdm


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
    file = open("term_index_sortbased.txt", "w", encoding="utf-8")
    offsetfile = open("term_info_sortbased.txt", "w", encoding="utf-8")
    for term in tqdm.tqdm(index, ncols=120, desc="Writing sort-based index to file"):
        offsetfile.write(str(term[0]) + "\t" + str(file.tell()))
        offsetfile.write("\n")
        previousDoc = 0
        currentDoc = term[1].docId
        file.write(str(term[0]) + " ")
        wordFrequency = 0
        for i in range(1, len(term)):
            wordFrequency += len(term[i].positionList)
        file.write(str(wordFrequency) + " ")
        file.write(str(len(term) - 1))
        for i in range(1, len(term)):
            currentDoc = term[i].docId
            previousPostion = 0
            for position in term[i].positionList:
                file.write(" ")
                file.write(str(currentDoc - previousDoc) + ",")
                file.write(str(position - previousPostion))
                previousPostion = position
                previousDoc = currentDoc
        file.write("\n")
    offsetfile.close()
    file.close()


def writeHashIndex(indexHashMap):
    previousTerm = currentTerm = 0

    file = open("term_index.txt", "w", encoding="utf-8")
    offsetfile = open("term_info.txt", "w", encoding="utf-8")
    for key in tqdm.tqdm(indexHashMap, ncols=120, desc="Writing HashMap index to file"):
        offsetfile.write(str(key) + "\t" + str(file.tell()))
        offsetfile.write("\n")
        previousDoc = 0
        currentDoc = list(indexHashMap[key])[0]
        file.write(str(key) + " ")
        wordFrequency = 0
        for innerKey in indexHashMap[key]:
            wordFrequency += len(indexHashMap[key][innerKey])

        file.write(str(wordFrequency) + " ")
        file.write(str(len(indexHashMap[key])))
        for innerKey in indexHashMap[key]:
            currentDoc = innerKey
            previousPosition = 0
            previousPosition = 0
            for position in indexHashMap[key][innerKey]:
                file.write(" ")
                file.write(str(currentDoc - previousDoc) + ",")
                file.write(str(position - previousPosition))
                previousPosition = position
                previousDoc = currentDoc

        file.write("\n")
    offsetfile.close()
    file.close()
    offsetfile.close()


def sortBasedIndexer(tupleList):
    print("Creating Sort Based Index ..............")
    print("Sorting Tuples ..............")
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


if len(sys.argv) > 1:
    path = str(sys.argv[1])
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
    for name in tqdm.tqdm(fileNames, ncols=120, desc="Parsing Documents and creating Index"):
        soup = BeautifulSoup(open(path + "/" + name, 'rb').read(), "html.parser", from_encoding="iso-8859-1")
        soup = soup.find("body")
        if soup:
            documentId[name] = docId
            docId += 1
            for junk in soup(["script", "style"]):
                junk.decompose()
            data = soup.get_text()
            words = regex.findall(r"\b[0-9A-Za-z]+(?:['-]?[0-9A-Za-z]+)*\b", data)
            positionCounter = 0
            for word in words:
                word = word.lower()
                unsetemmed = word
                word = PorterStemmer().stem(word)
                if word not in vocabulary and unsetemmed not in stopwords and len(word) > 1:
                    vocabulary[word] = termId
                    termId += 1
                if unsetemmed not in stopwords and len(word) > 1:
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
    print("\n")
    writeHashIndex(hashInvertedIndex)
    writeSortBasedIndex(sortBasedIndexer(tupleList))
    writeMappings(vocabulary, "termids.txt")
    writeMappings(documentId, "docids.txt")
else:
    print("Please Enter the path of your corpus")
