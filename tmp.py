import json

f=open("mteam.json")
data=json.load(f)

members=data["response"]["members"]
count=0
for i in members:
    print(i["user_id"]+":"+ i["nickname"])

safefile = open("safepeople.txt", "r")
safe = safefile.read().replace("\n", "<>").split(">")
safe = [x.split(":")[0] if x[0]!=":" else "<" for x in safe]
safe.remove("<")
safefile.close()

print(safe)