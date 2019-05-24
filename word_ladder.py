import re

# much like the variables within the scope of a function, the arguments and parameters passed in for the defining of the function
# work somewhat the same, though they're more akin to placeholders.

def FindSolutionPath(word, words, seenWords, targetWord, instancePath) :
    global pathChosen #Declares both variables as global to be used both inside and out of the current scope
    global rareLetters
    tempList = [] #much like many variables within these functions, they are scope bound and as such are somewhat temporary
    for i in range(len(word)): #for loop which iterates through the word's letters based on the length of the chosen word.
        tempList += BuildListOfPatternWords(word[:i] + "." + word[i + 1:], words, seenWords, tempList)

    if len(tempList) == 0 :
        return False

    if pathChosen == True:
        tempList = sorted([(same(w, targetWord), w) for w in tempList], reverse=True)
    else:
        rareLetters = []
        tempList = sorted([(same(w, targetWord), w) for w in tempList])

    for (hit, item) in tempList: #iterating through the match and word pairs in list
        for letter in rareLetters:
            if letter in item:
                tempList.remove((hit, item))
        if hit >= len(targetWord) - 1:
            if hit == len(targetWord) - 1:
                instancePath.append(item)
            return True
        seenWords[item] = True

    for (hit, item) in tempList:
        instancePath.append(item)
        if FindSolutionPath(item, words, seenWords, targetWord, instancePath):
            return True
        instancePath.pop()

# This function undertakes the process of adding to the second parameter which is a list.
def BuildListOfPatternWords(pattern, wordsOfSameLength, seenWords, potentialSolutionPath):
    return [word for word in wordsOfSameLength
                if re.search(pattern, word) and word not in seenWords.keys() and
                    word not in potentialSolutionPath]


# This primarily handles their inputs and ensures that it's as expected
def ChoosePathOption(option):
    while True:
        if len(option) > 1:
            option = input("You must type either 'S' for short and 'L' for long, nothing more. ").lower()

        elif (option.isdigit()):
            option = input("The input must either be a 'S' or a 'L', please try again. ").lower()

        else:
            if option == 'l':
                print("'L' Chosen, please follow the next prompts")
                return False
            elif option == 's':
                print("'S' Chosen, please follow the next prompts")
                return True
            else:
                option = input("You must type either 'S' or 'L', please try again.").lower()
                continue

# Handles the input words and make sure that they are not numerical or contain any special characters.
def initialWordValidation(word):
    while True:
        if len(word) < 3:  # Prevents any initial words from being less than 2 characters
            word = input("The word requires 3 or more characters, please type a new starting word : ")
        elif word.isdigit(): # Ensures it's actual letters opposed to numbers.
            word = input("The Word must not be numerical, please type a new starting word : ")
        elif word.isalpha(): # Checks if the word is of alphabetical characters only
            word.replace(" ", "")
            return word


# The file input sanitisation utilises an inbuilt exception for just the scenario where it'll be raised if no file is found
def fileInputValidation():
    while True:
        try:
            fileName = input("Please type the file name of your dictionary (default = dictionary.txt) : ")
            return open(fileName, 'r')
        except FileNotFoundError:
            print("File is missing, double check your spelling or directory.\n")


# Similar to initialWordSanitisation function except it also ensures that the target word word the user inputs is the same length as the start word.
def targetWordValidation(word):
    global startWord
    while True :
        if len(word) != len(startWord) : #swapped them around to be more symmetrical with the inital word sanitisation
            word = input("Both the initial word and the target word must be the same length, please try again with said parameters")
        elif word.isdigit():
            word = input("Target word must not be numerical, please type a new target word : ")
        elif word.isalpha():
            word.replace(" ", "")
            return word

# Function returns indices and no. in words that match
def same(item, targetWord):
  return len([item for (item, targetWord) in zip(item, targetWord) if item == targetWord])


wordsOfSameLength = []
userCommand = 'y'
dictionaryFile = fileInputValidation()
dictionaryLines = dictionaryFile.readlines()

while userCommand == 'y':

    # This handles the decision between both short and long for word-ladder. Utilises the choosePathOption function above
    #and passes in the input forced into lowercase
    path = input("Please select your preferred word-ladder format. Type 'S' for short or 'L' for long : ")
    pathChosen = ChoosePathOption(path.lower())

    # Here, the user is prompted for a start word and an end word. They are handled seperately by 2 different functions.
    holdingWord = input("Please enter your initial word :") # Temporarely stores both the initial and target word
    startWord = initialWordValidation(holdingWord)        #in 1 variable right after eachother as to not require
                                                            #more unnecessary variables
    holdingWord = input("Please enter your final word :")
    targetWord = targetWordValidation(holdingWord)        #It then runs each word temporarely in holding through their
                                                    #respective sanitisation functions to handle them ->
                                                #and then also assigns the return of the function to the proper variable

    # Get all of the words that are the same length as the given start word.
    for word in dictionaryLines : #Looping through every word pulled from the dictionary
        word = word.rstrip() #as the name suggests, strips all empty space away
        if len(startWord) == len(word) : #checks if the length is the same as the initial word, in which case it holds
            wordsOfSameLength.append(word) #onto it in the list 'wordsOfSameLength'

    # Find the path with the least amount of hops as the solution.
    rareLetters = ["z", "x"] #better to filter out any letters that are generally rarer to be within words
    finalPath = [startWord]
    seenWords = {startWord : True}
    if FindSolutionPath(startWord, wordsOfSameLength, seenWords, targetWord, finalPath) :
        finalPath.append(targetWord)  #Goes through th Findsolution function and finally adds the target word to the end
        print(len(finalPath) - 1, finalPath)  #prints both the amount of steps it took and the end result.
    else :
        print("No path was found.")

    # A small check to see if the user would like to play again.
    userCommand = input("Would you like to try again? (y/n) : ").lower()
