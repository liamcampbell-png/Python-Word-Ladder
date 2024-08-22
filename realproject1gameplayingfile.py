#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 07:23:03 2024

@author: sriram
"""
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
    # Algorithm: Walk down both strings w1 and w2 and count the number of indices 
    # at which w1 and w2 have distinct characters. If this count <= 1, then the function
    # should return True; otherwise False
    
    # This algorithm can be implemented using a single for-loop
    count = 0
    for i in range(len(w1)):
        count = count + (w1[i] != w2[i])

    return (count == 1)
def readWords():
    fin = open("words.txt", "r")
    wordList = []

    # Loop to read words from the and to insert them in a list
    # and in a dictionary
    for word in fin:
        newWord = word.rstrip()
        wordList.append(newWord)

    fin.close()
    return wordList
def makeNeighborLists(wordList):
    n = len(wordList)
    
    # Create and initialize a list containing n adjacency lists
    adjList = []
    for i in range(n):
        adjList.append([])


    # Go through every pair of words in wordList, check if they are adjacent
    # and if they are, then set the appropriate slot in M to 1
    #
    # This is implemented using nested for-loops.
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







###############################################################################     
#
# Specification: This function takes a non-empty, sorted (in increasing
# alphabetical order) list of words called wordList. It takes the 
# word network of all the words in wordList, represented as the corresponding 
# list of neighbor lists. It also takes a word called source in wordList and 
# it performs a breadth first search of the word network starting from
# the word source. In addition, it takes a list of words called easyWordList,
# all of which belong to wordList. These words have weight 0, whereas the remaining
# words have weight given by the non-negative integer parameter w.
# It returns a list containing two lists: (i) the parents of all words 
# reached by the search and (ii) the distances of these words from the source word.    
#
# Definition: The length of a path is the sum of the number of edges in the path
# plus the sum of the weights of all the nodes in the path.
#
# Definition: The distance between a pair of nodes u and v is the length of the
# shortest path betwwen them.
#
# Notes: 
# (a) If the length of wordList is n, then the returned list contains two lists,
# each of length n.
# (b) If the returned list is [L1, L2] and a word w has index i in wordList, then
# the parent information of w is stored in L1[i] and the distance information of
# w is stored in L2[i].
# (c) The parent information of a word is "" if it is the source word or if it
# is not reachable from the source word.
# (d) The distance information for any word that is not reachable from the source
# word is -1.
#
###############################################################################
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

#####################################dist##########################################     
#
# Specification: This function takes a non-empty, sorted (in increasing
# alphabetical order) list of words called wordList. It also takes a word 
# called source in wordList and a list of distances of all nodes in wordList
# from this network. It returns a list of words, in aphabetical order,
# that are between distance d1 and d2 from source (inclusive of d1 and d2).
# You can assume that d1 and d2 are non-negative integers and d1 <= d2. 
#
# You can assume that distanceList has been produced by a call to searchWordNetwork
# or searchWeightedWordNetwork. 
#
###############################################################################
def wordsAtDistanceRange(wordList, source, distanceList, d1, d2):
    wordsInRange = []
    sourceIndex = wordList.index(source)

    for i in range(len(distanceList)):
        distance = distanceList[i]
        if i != sourceIndex:
            wordsInRange.append(wordList[i])

    return sorted(wordsInRange)


###############################################################################
# Main program

# Read parameters.txt; use default values if parameters.txt is missing
# The paremeters.txt file has the format:
#   p = value1
#   w = value2
#   ed1 = value3, ed2 = value4
#   hd1 = value5, hd2 = value6
#   eh = value7, hh = value8
#   r = value9
# ADD CODE HERE. Ideally, this should be a fuction call

def mainProgram():
    try:
        f = open("parameters.txt", "r")
    except FileNotFoundError:
        print("parameters.txt not found")

    

# Read gameInformation.txt 
# Create easyWordList, hardWordList, wordList, nbrsList
# if gameInformation.txt is missing, provide a message to the user and construct all these lists
# from scratch.
# ADD CODE HERE. Ideally, this should be a function call
def readGameInfo():
    try:
        f = open("gameInformation.txt","r")
        wordList = []
        easyWordList = []
        hardWordList = []
        nbrsList = []
        lines = f.readlines()
        for line in lines:
            if line[0].isalpha():
                wordList.append(line.strip())
        nbrsList = makeNeighborLists(wordList)

        for i in range(1, int(lines[0])):
            easyWordList.append(lines[i].strip())
        for word in wordList:
            if word not in easyWordList:
                hardWordList.append(word)
    except FileNotFoundError:
        print("gameInformation.txt file not found")

    return wordList, easyWordList, hardWordList, nbrsList


# Start initial user interaction
# Welcome them to the game and ask them to pick game playing mode.
# E for "easy mode" and H for "hard mode"
# ADD CODE HERE

print("Hello, welcome to the word ladder game")
print("Would you like to play the Easy Mode or Hard Mode. Type E for Easy Mode or H for Hard Mode:")
mode = input().upper()

# Once user has picked a mode, initialize parameter values for the game.
# (a) [d1, d2] = [ed1, ed2] for easy mode, [d1, d2] = [hd1, hd2] for hard mode
# (b) numWordHints = eh for easy mode, numWordHints = hh for hard mode 
# (c) distanceHintRate = r
# ADD CODE HERE
# Initialize parameter values for the game based on the chosen mode
f = open("parameters.txt","r")
if mode == "E":
    [d1, d2] = [5, 10]
    numWordHints = 5
elif mode == "H":
    [d1, d2] = [8, 13]
    numWordHints = 1

distanceHintRate = 0.2


wordList, easyWordList, hardWordList, nbrsList = readGameInfo()

# In the easy mode, pick a random word from easyWordList
# In the hard mode, pick a random word from wordList
# This is your target word.
# ADD CODE HERE
import random
f = open("gameInformation.txt","r")
if mode == "E":
    targetWord = random.choice(easyWordList)
elif mode == "H":
    targetWord = random.choice(hardWordList)
else:
    print("Invalid mode selected, Try again")






# (a) Call searchWeightedWordNetwork(wordList, nbrsList, target, easyWordList, w) 
# to get parentList and distanceList
# (b) Call wordsAtDistanceRange(wordList, target, distanceList, d1, d2)
# to obtain all words at distance in the range [d1, d2] from target.
# Pick a word at random from this list; this is your source word
# ADD CODE HERE
wordList = readWords()
nbrsList = makeNeighborLists(wordList)
parentList, distanceList = searchWeightedWordNetwork(wordList, nbrsList, "abode", easyWordList, 4)
wordsInRange = wordsAtDistanceRange(wordList, "abode", distanceList, 3, 5)
sourceWord = random.choice(wordsInRange)



# Start main user interaction
# Provide the source word and target word. Ask the user to complete the word ladder
# from source word to target word. Let them know if they need to type the source word 
# and target word also. Inform them that they can type "Q" to quit the game at any 
# point and "H" if they want a next word hint.
# MAke sure messsages are clear. For example, you could use:
# "Excellent!" if the next word they type is a valid word in the ladder
# "Not a word in my dictionary!" if the next word they typs is not a word in wordList
# "The ladder can't go from xxxxx to yyyyy!" if the current word yyyyy is not a neighbor 
# of the previous word "xxxxx"
# ADD CODE HERE

print("Your source word:", sourceWord)
print("Your target word is:", targetWord)
print("Please complete the word ladder from the source word to the target word")
print("Type 'Q' to quit the game or 'H' to receieve a Hint")

wordLadder = [sourceWord]

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
    elif nextWord == targetWord:
        print("Congrats, you win!!")
        break
    else:
        wordLadder.append(nextWord)
        print("Good Job, now keep going!")













