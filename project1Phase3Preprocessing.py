#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 17:12:30 2024

@author: Sriram Pemmaraju
"""
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

def areNeighbors(w1, w2):
    # Algorithm: Walk down both strings w1 and w2 and count the number of indices 
    # at which w1 and w2 have distinct characters. If this count <= 1, then the function
    # should return True; otherwise False
    
    # This algorithm can be implemented using a single for-loop
    count = 0
    for i in range(len(w1)):
        count = count + (w1[i] != w2[i])

    return (count == 1)
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
    

##################################################################
#
# Specification: The function reads words from the file "words.txt" and creates and
# returns a list with these words. The words should in the same order in the list
# as they appear in the file. Each string in the list of words should be exactly
# 5 characters long.
#
# NEW: if the file word.txt is missing, this function should just return [] instead
# of causing the program to cause an exception.
#
# Examples:
# >>> L = readWords()
# >>> len(L)
# 5757
# >>> L[len(L)-1]
# 'zowie'
# >>> L[0:10]
# ['aargh',
#  'abaca',
#  'abaci',
#  'aback',
#  'abaft',
#  'abase',
#  'abash',
#  'abate',
#  'abbey',
#  'abbot']
# >>> L[1000]
# 'coney'
# >>> sorted(L)==L
# True
#
###############################################################################
def readWords():
    wordList = []
    try:
        fin = open("words.txt", "r")
        for line in fin:
            wordList.append(line.strip())
        fin.close()
    except FileNotFoundError:
        print("File was not found")
    return wordList
    
###############################################################################     
#
# Specification:  This function takes a list of words and a list of file names.
# It reads from each file in the given list of file names and extracts words from
# the file. For each word in the list of words, it computes the frequency of this
# word in all the files in the given list of file names. The function returns
# the list of frequencies. The order in which frequencies appear in the frequency
# list should match the order in which words appear in the given word list. In other
# words, the frequency in slot 0 should be the frequency of smallerWordList[0],
# the frequency in slot 1 should be the frequency of smallerWordList[1], etc.
# The function should use "try and except" to gracefully deal with missing files.
# If a file is missing, it should just skip over to the next file. If all files
# are missing, then the frequency list returned should contain all 0's.
#
###############################################################################   
def computeFrequencies(smallerWordList, fileNameList):
    frequency = []
    fileList = []
    for file in fileNameList:
        try:
            f = open(file,"r")
            for line in f:
                for word in line.split():
                    if word.isalpha():
                        fileList.append(word.strip().lower())
            f.close()
        except FileNotFoundError:
            print("File was not found")
    for word2 in smallerWordList:
        freq = fileList.count(word2)
        frequency.append(freq)
    return frequency
    
        

############################################################################### 
# You can add as many other functions as you want to make your code streamlined,
# readable, and efficient
############################################################################### 


############################################################################### 
# main program starts here
############################################################################### 

# STEP 1: Identify the list of words in the largest connected component
# (a) Read the list of all words in words.txt. Make sure that the 
# program exits gracefully if words.txt is not available
# (b) Build the adjacency list representation of the word network of this list of 
# words
# (c) Find all connected components of this word network
# (d) Identify the largest connected component and create a list with the words 
# in the largest connected component in sorted order
#
# Code for STEP 1 goes here
wordList = readWords()

if wordList != []:
    nbrsList = makeNeighborLists(wordList)
    
    cList = findComponents(wordList, nbrsList)
    
    maxnum = 0
    for i in cList:
        if len(i) > maxnum:
            maxnum = len(i)
    largeComponent = []
    for i in cList:
        if len(i) == maxnum:
            largeComponent = i
        


# STEP 2: Compute the frequencies of all the words in the largest connected component
# and designate the p % of the words with highest frequency as "easy" words  
# (a) Create a list containing all the names of text files downloaded from Project Gutenberg
# (b) Call the function computeFrequencies to read from these files, extract words, and
# update the frequencies of the words in the largest connected component  
# (c) Read from the file parameters.txt to get the value of parameter p
# (d) Designate the most frequent  p % of these words as "easy" words and the rest
# as "hard" words 
#
# Code for STEP 2 goes here
text_files = ["pg84.txt", "pg1342.txt", "pg2701.txt","pg2641.txt","pg37106.txt","pg64317.txt"]


frequency = (computeFrequencies(largeComponent, text_files))

try:
    target = "p"
    with open("parameters.txt","r") as file:
        for line in file:
            if line.strip().startswith(f"{target} = "):
                value = int(line.split("=")[-1].strip())
                break
except FileNotFoundError:
    print("The file parameters.txt was not found")


wordsNum = dict(zip(largeComponent, frequency))
sortedWords = dict(sorted(wordsNum.items(), key=lambda x: x[1]))
sortedWords = list(sortedWords)

num = int(len(largeComponent) * (1 - (value/100)))
hardWords = [''] * num
easyWords = []
for i in range(0,num):
    hardWords[i] = sortedWords[i]

for word in sortedWords:
    if word not in hardWords:
        easyWords.append(word)


# STEP 3: Write into the file gameInformation.txt
# (a) Open the file "gameInformation.txt" for writing
# (b) Write the number of easy words, followed by the easy words themselves in alphabetical order
# (c) Write the number of hard words, followed by the hard words themselves in alphabetical order
# (d) Write the adjacency list representation of the word network of the largest connected component
# Make sure that everything is written into the file gameInformation.txt as per the specifications
# in the project 1 handout
#
# Code for STEP 3 goes here
sorted(easyWords)
sorted(hardWords)
adjList = makeNeighborLists(largeComponent)
                          
try:
    f = open("gameInformation.txt","w")
    
    
    f.write (str(len(easyWords)))
    f.write("\n")
    for word in easyWords:
        f.write(word + "\n")
        
    f.write(str(len(hardWords)))
    f.write("\n")
    for word in hardWords:
        f.write(word + "\n")
        
    f.write(str(len(adjList)))
    f.write("\n")
    for word in adjList:
        f.write(str(word) + "\n")
except FileNotFoundError:
    print("File could not be written to")
f.close()
        
    



















