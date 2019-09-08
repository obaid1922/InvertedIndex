def readHashInvertedIndex(fileName):
    invertedIndex = {}
    fileContents = open(fileName, 'r').readlines()
    for posting in fileContents:
        previousDoc = 0
        previousPosition = 0
        currentDoc = int(entries[3])
        currentPosition = int(entries[4])
        entries = posting.split(sep="\t")
        if int(entries[0]) not in invertedIndex:
            innerHash = dict()
            innerHash.setdefault(currentDoc, []).append(currentPosition)
            invertedIndex[int(entries[0])] = innerHash
        else:
            if currentDoc in

        for i in range(5, len(entries), 2):
            currentDoc = entries[i]
            currentPosition = entries[i + 1]
            decodedDocId = currentDoc + previousDoc
            decodedPosition = currentPosition + previousPosition
            if decodedDocId not in invertedIndex[int(entries[0])]:





readHashInvertedIndex("InvertedIndex.txt")
