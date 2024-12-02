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
    if data["sender_type"] == "user":
        infile = open("bannedwords.txt", "r") 
        safefile = open("safepeople.txt", "r")
        safe = safefile.read().replace("\n", "<>").split(">")
        safe = [x.split(":")[0] if x[0]!=":" else "<" for x in safe]
        safe.remove("<")
        words = infile.read().replace('\n', ' ').split(" ") 
        infile.close()
        safefile.close()
        words_re = re.compile("|".join(words))

        if words_re.search(data["text"].lower()):
            group = data["group_id"]
            userId = data["sender_id"]
            token = os.getenv("ACCESS_TOKEN")

            print(data)

            getUrl=f"https://api.groupme.com/v3/groups/{group}?token={token}"
            resp=requests.get(getUrl).json()
            if resp["meta"]["code"] != 200:
                return
            members = resp["response"]
            id=""; name=""
            for member in members["members"]:
                if member["user_id"] == userId:
                    name = member["name"]
                    if member["user_id"] not in safe:
                        id = member["id"]
                        print(f"kicking {id}: {name}")
                    break

            if id == "":
                print("not kicking ", end="-")
                if name=="":
                    print("no user")
                else:
                    print("protected user")
                return

            url  = f'https://api.groupme.com/v3/groups/{group}/members/{id}/remove?token={token}'
            requests.post(url)
            print(f"Kicked {id} ({name}) from {group}")

    return