import re,sys
def main():
    firstFile = sys.argv[1]
    secondFile = sys.argv[2]
    intersection(firstFile,secondFile)

#Runtime complexity: Nestad loop may has O(n^2) runtime complexity. For each individual list, it has one nested loop
#so it would be O(n^2) in total
def intersection(input1, input2):
    dict1 = {}
    dict2 = {}
    try:
        list1 = open(input1,'r').readlines() #read file 1 line by line
        list2 = open(input2,'r').readlines() #read file 2 line by line
    except:                                  #Handle exception
        print("file not found")
        exit(1)
    for allwords in list1:
            allwords = re.sub("\\W",' ',allwords)  #When the LOCALE and UNICODE flags are not specified,
                                                   #matches any alphanumeric character and the underscore
            for word in allwords.split():  # read each word individually from the wordList
                if re.match("^[a-zA-Z0-9_]*$", word):  # eliminate no-enghlish or no digit character
                    dict1.setdefault(word.lower(), 0)  # set to lower case

    for allwords2 in list2:
            allwords2 = re.sub("\\W",' ', allwords2)
            for word2 in allwords2.split():  # read each word individually from the wordList
                if re.match("^[a-zA-Z0-9_]*$", word2):  # eliminate no-enghlish or no digit character
                    dict2.setdefault(word2.lower(), 0)  # set to lower case
#print the result
    count = int(0)    #counter for the same word
    for wordkey,wordvalue in dict1.items():
        if wordkey in dict2:                #if key also found in dict2, increment
                count = count+1
    print(count)
if __name__ == '__main__':
        main()
