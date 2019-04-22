#!/usr/bin/python
import requests
import hashlib
import  urllib.parse
import base64

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

url = "http://deepi.sogou.com:80/api/sogouService"
pid = "52db1895b60c5a55ed5322d1b5fec684"
service = "translateOpenOcr"
salt = "1508404016012"
# base64 string file picture,too long in the case we will omit string
img_path = r'C:\Users\andan\Desktop\u=3538315233,3458173025&fm=26&gp=0.jpg'
with open(img_path,'rb') as fpic:
    img_data = str(base64.b64encode(fpic.read()),'utf-8')
if len(img_data) > 1024:
    img = img_data[0:1024]
sign = md5(pid+service+salt+img+"83ddd3234bc46e153f69a445b0b0981d");
print(sign)
payload = "from=en&to=zh-CHS&pid=" + pid + "&service=" + service + "&sign=" + sign + "&salt=" + salt + "&image=" + urllib.parse.quote(img_data)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept': "application/json"
    }
response = requests.request("POST", url, data=payload, headers=headers)
#
spam = response.text
#
print(response.text)