

import sys
import re
def main():
    fileName = sys.argv[1]
    getWorldFrequencies(fileName)

# function to read input file and output the result
#Runtime complexity: O(NlogN), the first N is the complexity of the for loop for eliminating the punchuation
def getWorldFrequencies(file_name):
    wordFreq={} # dictory for the wordlist
    #Handle exception
    try:
        documentText = open(file_name,'r').readlines()  #read file from user input
    except:
        print("file not found")
        exit(1)
    for allwords in documentText:
        allwords = re.sub("\\W",' ', allwords)     #When the LOCALE and UNICODE flags are not specified,
                                                   #matches any alphanumeric character and the underscore
        for word in allwords.split():
            if re.match("^[a-zA-Z0-9_]*$",word):             #eliminate no-enghlish or no digit character
                wordFreq.setdefault(word.lower(),0)               #set to lower case
                wordFreq[word.lower()] += 1                       #increment value if word appear more than once

    result = sorted(wordFreq.items(), key = lambda k:(-k[1],k[0])) # sort by values first, and then by key

    #print the result
    for wordKey, wordValue in result:
        print(wordKey+'\t', wordValue)


if __name__ == '__main__':
    main()
