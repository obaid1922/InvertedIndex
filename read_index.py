def readHashInvertedIndex(fileName):
    invertedIndex = {}
    fileContents = open(fileName, 'r').readlines()
    for posting in fileContents:
        entries = posting.split(sep="\t")
        previousDoc = 0
        previousPosition = 0
        currentDoc = int(entries[3])
        currentPosition = int(entries[4])
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

        for i in range(5, len(entries) - 1, 2):
            currentDoc = int(entries[i])
            currentPosition = int(entries[i + 1])
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
    print(1)


readHashInvertedIndex("term_index.txt")
