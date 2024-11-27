import os
import json
import requests

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

    url  = f'https://api.groupme.com/v3/bots/groups/{data["group_id"]}/members/{data['membership_id']}/remove?token={os.getenv('ACCESS_TOKEN')}'
    print(url)

    # $ curl -X POST -H https://api.groupme.com/v3/groups?token=YOUR_ACCESS_TOKEN
    
#   data = {
#           'bot_id' : os.getenv('BOT_ID'),
#           'text'   : msg,
#          }
#   request = Request(url, urlencode(data).encode())
#   json = urlopen(request).read().decode()
    return