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
        group = data["group_id"]
        id = data["id"]
        token = os.getenv("ACCESS_TOKEN")
        url  = f'https://api.groupme.com/v3/bots/groups/{group}/members/{id}/remove?token={token}'
        requests.post(url)
    infile.close()

    return