import os
import json
import requests
import re

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request


app = Flask(__name__)

# is called by GroupMe API. If the message is sent by a user, it will call checkMsg
@app.route('/', methods=['POST'])
def webhook():
    # Creates list of banned words and safe users. Runs when the app is first created
    infile = open("bannedwords.txt", "r") 
    safefile = open("safepeople.txt", "r")
    safe = safefile.read().replace("\n", "<>").split(">")
    safe = [x.split(":")[0] if x[0]!=":" else "<" for x in safe].remove("<")
    words = infile.read().replace('\n', ' ').split(" ") 
    infile.close()
    safefile.close()
    data = request.get_json()
    words_re = re.compile("|".join(words))

    if data["sender_type"] == "user" and data["sender_id"] not in safe:
        checkMsg(data, words_re)
    else:
        print("Protected User and/or system message")

    return "ok", 200

"""
    Checks incoming message for any banned words
    Doesn't kick if a user is part of the protected user's list
""" 
def checkMsg(data, words):
    if words.search(data["text"].lower()):
        group = data["group_id"]
        userId = data["sender_id"]
        token = os.getenv("ACCESS_TOKEN")

        # get source group's members list
        getUrl=f"https://api.groupme.com/v3/groups/{group}?token={token}"
        resp=requests.get(getUrl).json()
        if resp["meta"]["code"] != 200:
            return
        
        # searches members list to find user's group_id of sent message
        # Also grabs their name for logging purposes
        members = resp["response"]
        id=""; name=""
        for member in members["members"]:
            if member["user_id"] == userId:
                name = member["name"]
                id = member["id"]
                break

        # Logging statements
        if id == "":
            print("not kicking ", end="-")
            if name=="":
                print("no user")
            return

        requests.post(f'https://api.groupme.com/v3/groups/{group}/members/{id}/remove?token={token}')
        print(f"Kicked {id} ({name}) from {group}")