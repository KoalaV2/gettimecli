#!/usr/bin/env python3
import requests
import json
import argparse
import datetime

def currentweekday():
    weekday = datetime.datetime.today().isoweekday()
    if 1 <= weekday <= 5:
        return weekday
    return 0

def getData(classid,weekday):
    now = datetime.datetime.now()
    weeknumber = datetime.date(now.year, now.month, now.day).isocalendar()[1]

    # Get the signature for the second request
    headers = {
        "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://web.skola24.se/timetable/timetable-viewer/it-gymnasiet.skola24.se/IT-Gymnasiet%20S%C3%B6dert%C3%B6rn/",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US;q=0.5",
        "Cookie": "ASP.NET_SessionId=5hgt3njwnabrqso3cujrrj2p"
    }
    idurl = 'https://web.skola24.se/api/encrypt/signature'

    # Pass through classid as the signature.
    signature = {"signature": classid}
    response = requests.post(idurl, data=json.dumps(signature), headers=headers)
    response3 = response.text.split('"signature": "')[1].split('"')[0]

    # Get the key for the third request
    headers2 = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://web.skola24.se/timetable/timetable-viewer/it-gymnasiet.skola24.se/IT-Gymnasiet%20S%C3%B6dert%C3%B6rn/",
        "Cookie": "ASP.NET_SessionId=5hgt3njwnabrqso3cujrrj2p",
    }
    signature2 = "null"
    keyurl = 'https://web.skola24.se/api/get/timetable/render/key'
    responsesecond = requests.post(keyurl, data=signature2, headers=headers2)
    responsesecond3 = responsesecond.text.split('"key": "')[1].split('"')[0]


    # Make the final request to get the timetable
    timetable = {
        "renderKey": responsesecond3,
        'host':"it-gymnasiet.skola24.se",
        'unitGuid':"ZTEyNTdlZjItZDc3OC1mZWJkLThiYmEtOGYyZDA4NGU1YjI2",
        "scheduleDay": weekday,
        "blackAndWhite": "true",
        "width": 758,
        "height": 648,
        "selectionType": 4,
        "selection": response3,
        "showHeader": "false",
        "periodText": "",
        "week": weeknumber,
        "year": 2022,
        "privateFreeTextMode": "false",
        "privateSelectionMode": "null",
        "customerKey": ""
    }
    thirdurl = 'https://web.skola24.se/api/render/timetable'
    responsethird = requests.post(thirdurl, data=json.dumps(timetable), headers=headers2)
    return responsethird

def main():
    parser = argparse.ArgumentParser(description="Prints out the schedule for skola24.se NTI Södertörn")
    parser.add_argument('-c', '--classid', type=str, help='Select the current class ID')
    args = parser.parse_args()
    classid = args.classid

    result = json.loads(getData(classid,currentweekday()).text)
    a = []

    # Prettify output to get readable output.
    try:
        for x in result['data']['lessonInfo']:
            temp = f"{x['timeStart']} -- {x['texts'][0]}, börjar kl {x['timeStart']} och slutar kl {x['timeEnd']}"
            try:
                temp += f" i sal {x['texts'][2]}"
            except:
                pass
            a.append(temp)
        a.sort()

        a = [i.split(' -- ')[1] for i in a]

        for x in a:
            print(x)
    except TypeError:
        print("No class found with such name")


if __name__ == "__main__":
    main()
