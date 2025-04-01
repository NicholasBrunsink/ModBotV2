import os
import requests
import re
from flask import Flask, request

# Creates list of banned words and safe users. Runs when the app is first created
infile = open("bannedwords.txt", "r") 
whitelistFile = open("whitelist.txt", "r")

# Create list of whitelisted users from file
whitelist = whitelistFile.read().replace("\n", "<>").split(">")
if whitelist[-1] == "":
    whitelist = whitelist[:-1]
whitelist = [x.split(":")[0] if x[0]!=":" else "<" for x in whitelist]
whitelist.remove("<")

# Compile RegEx of banned words from file
words = infile.read().replace('\n', ' ').split(" ") 
if words[-1] == "":
    words = words[:-1]
words_re = re.compile("|".join(words))

# exit files
infile.close()
whitelistFile.close()

app = Flask(__name__)

# is called by GroupMe API. If the message is sent by a user, it will call checkMsg
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["sender_type"] == "user" and data["sender_id"] not in whitelist:
        checkMsg(data)
    else:
        print("system or whitelisted user")
    return "ok", 200

"""
    Checks incoming message for any banned words
    Doesn't kick if a user is part of the protected user's list
""" 
def checkMsg(data):
    found = words_re.search(data["text"].lower())
    if found:
        print(f"banned word detected ({found.group()}), initiating kick")
        group = data["group_id"]
        userId = data["sender_id"]
        token = os.getenv("ACCESS_TOKEN")
        print("token obtained")
        # get source group's members list
        getUrl=f"https://api.groupme.com/v3/groups/{group}?token={token}"
        resp=requests.get(getUrl).json()
        if resp["meta"]["code"] != 200:
            print("failed to obtain group list")
            return
        else:
            print("obtained group list")
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
                print("no user or user already removed")
            return

        requests.post(f'https://api.groupme.com/v3/groups/{group}/members/{id}/remove?token={token}')
        print(f"Kicked {id} ({name}) from {group}")
