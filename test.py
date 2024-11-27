import re

def checkMsg(data):
    # opening the file in read mode 
    infile = open("bannedwords.txt", "r") 
    # reading the file 
    words = infile.read() 
    # replacing end of line('/n') with ' ' and 
    # splitting the text it further when '.' is seen. 
    wordList = words.replace('\n', ' ').split(" ") 
    
    words_re = re.compile("|".join(wordList))

    if words_re.search(data):
        print("found")
    else:
        print("not found")


data="hello I am selling ticke"

checkMsg(data)