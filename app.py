import os
import json
import requests
import re

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    checkMsg(data)
    return "ok", 200

def checkMsg(data):
    infile = open("bannedwords.txt", "r") 
    words = infile.read() 
    wordList = words.replace('\n', ' ').split(" ") 
    words_re = re.compile("|".join(wordList))
    print(data["text"])
    print(words_re)
    if words_re.search(data["text"].lower()):
        print("WEWOWEWOWEWOWEWO")

    infile.close()
    print(data["group_id"], data["membership_id"], os.getenv("ACCESS_TOKEN"))
    # url  = f'https://api.groupme.com/v3/bots/groups/{data["group_id"]}/members/{data["membership_id"]}/remove?token={os.getenv('ACCESS_TOKEN')}'
    # print(url)

    # $ curl -X POST -H https://api.groupme.com/v3/groups?token=YOUR_ACCESS_TOKEN
    
#   data = {
#           'bot_id' : os.getenv('BOT_ID'),
#           'text'   : msg,
#          }
#   request = Request(url, urlencode(data).encode())
#   json = urlopen(request).read().decode()
    return