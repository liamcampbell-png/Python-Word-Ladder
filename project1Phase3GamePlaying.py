def binarySearch(L, w, first, last):
    if (first > last):
        return -1
    
    mid = (first + last) // 2
    if (w == L[mid]):
        return mid
    elif (w < L[mid]):
        return binarySearch(L, w, first, mid-1)
    else:
        return binarySearch(L, w, mid+1, last)
def getIndex(L, w):
    return binarySearch(L, w, 0, len(L)-1)
def areNeighbors(w1, w2):

    count = 0
    for i in range(len(w1)):
        count = count + (w1[i] != w2[i])

    return (count == 1)
def readWords():
    fin = open("words.txt", "r")
    wordList = []

    for word in fin:
        newWord = word.rstrip()
        wordList.append(newWord)

    fin.close()
    return wordList
def makeNeighborLists(wordList):
    n = len(wordList)
    
    adjList = []
    for i in range(n):
        adjList.append([])

    for i in range(n):
        for j in range(n):
            if areNeighbors(wordList[i], wordList[j]):
                adjList[i].append(wordList[j])
                
    return adjList
def getNeighbors(wordList, nbrsList, w):
    return nbrsList[getIndex(wordList, w)]
def getIsolatedNodes(wordList, nbrsList):
    isolatedNodeList = []
    for i in range(len(wordList)):
        if len(nbrsList[i]) == 0:
            isolatedNodeList.append(wordList[i])
            
    return isolatedNodeList
def getIsolatedEdges(wordList, nbrsList):
    isolatedEdges = []
    for i in range(len(wordList)):
        if (len(nbrsList[i]) == 1):
            j = getIndex(wordList, nbrsList[i][0])
            if (j > i) and (len(nbrsList[j]) == 1) and (wordList[i] == nbrsList[j][0]):
                isolatedEdges.append([wordList[i], wordList[j]])
                
    return isolatedEdges
def sortByDegree(wordList, nbrsList):
    degreeWordList = []
    for i in range(len(wordList)):
        degreeWordList.append([len(nbrsList[i]), wordList[i]])
        
    degreeWordList.sort()
    sortedWordList = []
    for i in range(len(degreeWordList)):
        sortedWordList.append(degreeWordList[i][1])
        
    return sortedWordList
def degreeDistribution(wordList, nbrsList):
    degreeList = []
    for i in range(len(wordList)):
        degreeList.append(len(nbrsList[i]))
        
    distributionList = [0]*(max(degreeList) + 1)
    for i in range(len(degreeList)):
        distributionList[degreeList[i]] = distributionList[degreeList[i]] + 1
        
    return distributionList
def searchWordNetwork(wordList, nbrsList, source):
    parents = [""] * len(wordList)
    distances = [-1] * len(wordList)
    sourceIndex = getIndex(wordList, source)
    parents[sourceIndex] = ''
    distances[sourceIndex] = 0
    q = [source]

    while q:
        c = q.pop(0)       
        ci = getIndex(wordList, c) 
        
        for neighbor in nbrsList[ci]:
            neighborIndex = getIndex(wordList, neighbor)
            if distances[neighborIndex] == -1:
                parents[neighborIndex] = c
                distances[neighborIndex] = distances[ci] + 1
                q.append(neighbor)

    return [parents, distances]
def findPath(wordList, nbrsList, source, target):
    if source == target:
        return []
    parents = searchWordNetwork(wordList, nbrsList, source)[0]
    path = []
    c = target
    while c != source:
        path.append(c)
        ci = getIndex(wordList, c)
        c = parents[ci]
        if c == '': 
            return []
    path.append(source)
    return path[::-1]

def findComponents(wordList, nbrsList):
    
            
    components = []
    visited = [False] * len(wordList)

    
    for i in range(len(wordList)):
        if not visited[i]:
            component = []
            reached = [wordList[i]]
            while reached:
                current = reached.pop()
                component.append(current)
                index = getIndex(wordList, current)
                visited[index] = True

                neighbors = nbrsList[index]
                for elem in neighbors:
                    indexN = getIndex(wordList, elem)
                    if not visited[indexN]:
                        reached.append(elem)
                        visited[indexN] = True
            component.sort()
            components.append(component)

    return components

    components.sort(key = sort_key)
    return components


def searchWeightedWordNetwork(wordList, nbrsList, source, easyWordList, w):
    parents = [""] * len(wordList)
    distances = [-1] * len(wordList)

    source_index = wordList.index(source)
    parents[source_index] = source
    distances[source_index] = 0

    queue = [source]
    while queue:
        current_word = queue.pop(0)
        current_index = wordList.index(current_word)

        for neighbor in nbrsList[current_index]:
            neighbor_index = wordList.index(neighbor)
            if parents[neighbor_index] == "":
                parents[neighbor_index] = current_word
                distances[neighbor_index] = distances[current_index] + w

                if neighbor in easyWordList:
                    distances[neighbor_index] = distances[current_index]

                queue.append(neighbor)

    return [parents, distances]

def wordsAtDistanceRange(wordList, source, distanceList, d1, d2):
    wordsInRange = []
    sourceIndex = wordList.index(source)

    for i in range(len(distanceList)):
        distance = distanceList[i]
        if d1 <= distance <= d2 and i != sourceIndex:
            wordsInRange.append(wordList[i])

    return sorted(wordsInRange)


def mainProgram():
    try:
        f = open("parameters.txt", "r")
    except FileNotFoundError:
        print("parameters.txt not found")

    
def readGameInfo():
    try:
        f = open("gameInformation.txt","r")
        easyWordList = [easyWords]
        hardWordList = [hardWords]
        wordList = readWords()
        nbrsList = makeNeighborLists(wordList)
    except:
        print("gameInformation.txt file not found")
        

print("Hello, welcome to the word ladder game")
print("Would you like to play the Easy Mode or Hard Mode. Type E for Easy Mode or H for Hard Mode:")
mode = input().upper()


f = open("parameters.txt","r")
if mode == "E":
    [d1, d2] = [ed1, ed2]
    numWordHints = eh
elif mode == "H":
    [d1, d2] = [hd1, hd2]
    numWordHints = hh

distanceHintRate = r

import random

if mode == "E":
    targetWord = random.choice(easyWordList)
elif mode == "H":
    targetWord = random.choice(hardWordList)
    
print("Your target word is:", targetWord)

parentList, distanceList = searchWeightedWordNetwork(wordList, nbrsList, targetWord, easyWordList, w)
wordsInRange = wordsAtDistanceRange(wordList, targetWord, distanceList, d1, d2)
sourceWord = random.choice(wordsInRange)

print("Source word:", sourceWord)

print("Your source word:", sourceWord)
print("Your target word is:", targetWord)
print("Please complete the word ladder from the source word to the target word")
print("Type 'Q' to quit the game or 'H' to receieve a Hint")

wordLadder = [source_word]

while True:
    nextWord = input("Enter the next word: ")

    if nextWord == "Q":
        print("Quitting the Game.")
        break
    elif nextWord == "H":
        print("Hint: your next word should be a neighbor of", wordLadder[-1])
    elif nextWord not in wordList:
        print("This is not a word in my dictionary")
    elif not areNeighbors(wordLadder[-1], nextWord):
        print("The ladder can't go from", wordLadder[-1],"to", nextWord)
    else:
        wordLadder.append(nextWord)
        print("Good Job")











