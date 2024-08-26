
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

def areNeighbors(w1, w2):
  
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
        
    



















