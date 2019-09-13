def readHashInvertedIndex(fileName):
    invertedIndex = {}
    fileContents = open(fileName, 'r').readlines()
    for posting in fileContents:
        entries = posting.split(sep="\t")
        previousDoc = 0
        previousPosition = 0
        currentDoc = int(entries[3].split(",")[0])
        currentPosition = int(entries[3].split(",")[1])
        previousDoc = currentDoc
        previousPosition = currentPosition
        if int(entries[0]) not in invertedIndex:
            innerHash = dict()
            innerHash.setdefault(currentDoc, []).append(currentPosition)
            invertedIndex[int(entries[0])] = innerHash
        else:
            if currentDoc in invertedIndex[int(entries[0])]:
                tempList = invertedIndex[int(entries[0])][currentDoc]
                tempList.append(currentPosition)
                invertedIndex[int(entries[0])][currentDoc] = tempList
            else:
                tempList = [currentPosition]
                invertedIndex[int(entries[0])][currentDoc] = tempList

        for i in range(4, len(entries)):
            docPositionPair = entries[i].split(",")
            currentDoc = int(docPositionPair[0])
            currentPosition = int(docPositionPair[1])
            decodedDocId = currentDoc + previousDoc
            if decodedDocId != previousDoc:
                previousPosition = 0
            decodedPosition = currentPosition + previousPosition
            if decodedDocId in invertedIndex[int(entries[0])]:
                tempList = invertedIndex[int(entries[0])][decodedDocId]
                tempList.append(decodedPosition)
                invertedIndex[int(entries[0])][decodedDocId] = tempList
            else:
                tempList = [decodedPosition]
                invertedIndex[int(entries[0])][decodedDocId] = tempList
            previousPosition = decodedPosition
            previousDoc = decodedDocId
    return invertedIndex


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


index = readHashInvertedIndex("term_index.txt")
vocab = readVocabulary()
docs = readDocIds()
