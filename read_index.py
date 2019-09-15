from nltk.stem import PorterStemmer
import tqdm
import sys


def readHashInvertedIndex(offset):
    docHash = {}
    stats = {}
    file = open("term_index.txt", 'r')
    file.seek(offset)
    posting = file.readline()
    entries = posting.split(sep=" ")
    previousDoc = 0
    previousPosition = 0
    currentDoc = int(entries[3].split(",")[0])
    currentPosition = int(entries[3].split(",")[1])
    previousDoc = currentDoc
    previousPosition = currentPosition
    statList = [int(entries[1]), int(entries[2])]
    stats[int(entries[0])] = statList
    if currentDoc in docHash:
        tempList = docHash[currentDoc]
        tempList.append(currentPosition)
    else:
        tempList = [currentPosition]
        docHash[currentDoc] = tempList
    for i in range(4, len(entries)):
        decodedDoc = int(entries[i].split(",")[0]) + previousDoc

        if decodedDoc != previousDoc:
            previousPosition = 0
        decodedPosition = int(entries[i].split(",")[1]) + previousPosition
        if decodedDoc in docHash:
            tempList = docHash[decodedDoc]
            tempList.append(decodedPosition)
        else:
            tempList = [decodedPosition]
            docHash[decodedDoc] = tempList
        previousDoc = decodedDoc
        previousPosition = decodedPosition
    file.close()
    return docHash, stats


def readVocabulary():
    vocabulary = {}
    fileContents = open("termids.txt", 'r').read().splitlines()
    for dictEntry in fileContents:
        key = dictEntry.split("\t")[1]
        value = int(dictEntry.split("\t")[0])
        vocabulary[key] = value
    return vocabulary


def readDocIds():
    docIds = {}
    fileContents = open("docids.txt", 'r').read().splitlines()
    for dictEntry in fileContents:
        key = dictEntry.split("\t")[1]
        value = int(dictEntry.split("\t")[0])
        docIds[key] = value
    return docIds


def readOffset():
    offsets = {}
    fileContents = open("term_info.txt", 'r').read().splitlines()
    for dictEntry in fileContents:
        key = int(dictEntry.split("\t")[0])
        value = int(dictEntry.split("\t")[1])
        offsets[key] = value
    return offsets


if len(sys.argv) > 1:
    vocab = readVocabulary()
    docs = readDocIds()

    query = str(sys.argv[1])
    query = PorterStemmer().stem(query)
    offsets = readOffset()

    if query in vocab:
        index, stats = readHashInvertedIndex(offsets[vocab[query]])
        print("Listing for term : ", str(sys.argv[1]))
        termId = vocab[query]
        print("TERM ID : ", termId)
        print("Number of documents containing term : ", stats[termId][1])
        print("Term Frequency in corpus : ", stats[termId][0])
    else:
        print("Word not found")
else:
    print("Please Enter The Query Word")
