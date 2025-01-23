import json
import requests
import re

#更改正确的filename 
#txt中一行一个uid
filename="2024.txt"
with open(filename,"r") as f:
    data=[]
    for line in f.readlines():
        data.append(int(line))
    with open(filename[0:4]+".json","w",encoding="utf-8") as f_json:
        json.dump(data,f_json,ensure_ascii=False,indent=4)
        print("已生成{file[0:4]}.json")
