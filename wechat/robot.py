# -*- coding: utf-8 -*-
import json
import requests
KEY="a7631abb40f640ab994e90ff31cae872"
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api/v2'
    data = {
        "perception": {
            "inputText": {
                "text": msg
            },
        },
        "userInfo": {
            "apiKey": KEY,
            "userId": "1"
        }
    }
    datas = json.dumps(data)
    html = requests.post(apiUrl, datas).json()
    if html['intent']['code'] == 4003:
        print("resource run out")
        return "resource run out"
    return html['results'][0]['values']['text']
