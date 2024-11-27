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
    safefile = open("safepeople.txt", "r")
    words = infile.read() 
    wordList = words.replace('\n', ' ').split(" ") 
    words_re = re.compile("|".join(wordList))
    print(data)
    print(data["text"])
    if words_re.search(data["text"].lower()):
        group = data["group_id"]
        userId = data["sender_id"]
        token = os.getenv("ACCESS_TOKEN")

        getUrl=f"https://api.groupme.com/v3/groups/{group}?token={token}"
        resp=requests.get(getUrl).json()
        print(getUrl)
        print(resp)
        if resp["meta"]["code"] != 200:
            return
        members = resp["response"]
        id=""

        for member in members["members"]:
            if member["user_id"] == userId:
                id = member["id"]
                break
        print(id)

        url  = f'https://api.groupme.com/v3/groups/{group}/members/{id}/remove?token={token}'
        print(url)
        # print(requests.post(url))
    infile.close()
    safefile.close()

    return