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
    safe = safefile.read().replace('\n', " ").split(" ")
    words = infile.read().replace('\n', ' ').split(" ") 
    infile.close()
    safefile.close()
    
    words_re = re.compile("|".join(words))

    if words_re.search(data["text"].lower()):
        group = data["group_id"]
        userId = data["sender_id"]
        token = os.getenv("ACCESS_TOKEN")

        getUrl=f"https://api.groupme.com/v3/groups/{group}?token={token}"
        resp=requests.get(getUrl).json()
        if resp["meta"]["code"] != 200:
            return
        members = resp["response"]
        id=""

        for member in members["members"]:
            if member["user_id"] == userId and member["id"] not in safe:
                id = member["id"]
                print("kicking")
                break
        # print(id)
        if id == "":
            print("not kicking (no user or protected user)")
            return

        url  = f'https://api.groupme.com/v3/groups/{group}/members/{id}/remove?token={token}'
        print(url)
        print(requests.post(url))

    return