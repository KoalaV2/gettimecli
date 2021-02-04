import requests
#import urlib3.request
import time
#from bs4 import BeautifulSoup
import json
def main():
    headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://web.skola24.se/timetable/timetable-viewer/it-gymnasiet.skola24.se/IT-Gymnasiet%20S%C3%B6dert%C3%B6rn/",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US;q=0.5",
    "Cookie": "ASP.NET_SessionId=5hgt3njwnabrqso3cujrrj2p"
    }
    idurl='https://web.skola24.se/api/encrypt/signature'
    payload = { "signature":"20_el_a" }
    response = requests.post(idurl, data=json.dumps(payload), headers=headers)
    response2 = str(response.text)
    response3 = response2.split('"signature": "')[1].split('"')[0]



    headers2 = {
    "Host": "web.skola24.se",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/json",
    "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "4",
    "Origin": "https://web.skola24.se",
    "Connection": "close",
    "Referer": "https://web.skola24.se/timetable/timetable-viewer/it-gymnasiet.skola24.se/IT-Gymnasiet%20S%C3%B6dert%C3%B6rn/",
    "Cookie": "ASP.NET_SessionId=5hgt3njwnabrqso3cujrrj2p",
    "Sec-GPC": "1",
    "DNT":"1"
    }
    payload2 = "null"
    secondurl='https://web.skola24.se/api/get/timetable/render/key'
    responsesecond = requests.post(secondurl, data=payload2, headers=headers2)
    responsesecond2 = (str(responsesecond.text))
    responsesecond3 = responsesecond2.split('"key": "')[1].split('"')[0]

    payload3 = {"renderKey":responsesecond3,"host":"it-gymnasiet.skola24.se","unitGuid":"ZTEyNTdlZjItZDc3OC1mZWJkLThiYmEtOGYyZDA4NGU1YjI2","startDate":"null","endDate":"null","scheduleDay":0,"blackAndWhite":"false","width":758,"height":648,"selectionType":4,"selection":response3,"showHeader":"false","periodText":"","week":5,"year":2021,"privateFreeTextMode":"false","privateSelectionMode":"null","customerKey":""}
    thirdurl='https://web.skola24.se/api/render/timetable'
    responsethird = requests.post(thirdurl,data=json.dumps(payload3),headers=headers2)

    result = json.loads(responsethird.text)
    print(responsethird.text)

    for x in result['data']['lessonInfo']:
        #print(f"Lektion namn: {x['texts'][0]}, börjar kl {x['timeStart']} och slutar kl {x['timeEnd']}")
        if {x['dayOfWeekNumber'] == 1}:
            print(f"Lektion namn: {x['texts'][0]}")
if __name__=="__main__":
    main()
