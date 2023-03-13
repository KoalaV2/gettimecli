#!/usr/bin/env python3
import requests
import json
import datetime
import argparse

def getData(classid):
    s = requests.Session()
    s.headers.update({
        "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
    })

    now = datetime.datetime.now()
    weeknumber = datetime.date(now.year, now.month, now.day).isocalendar()[1]
    weekday = datetime.datetime.today().isoweekday()
    if not 1 <= weekday <= 5:
        weekday =  0

    # Pass through classid as the signature.
    signature = {"signature": classid}
    response = s.post("https://web.skola24.se/api/encrypt/signature", data=json.dumps(signature)).json()

    # Get the key for the third request
    responsesecond = s.post("https://web.skola24.se/api/get/timetable/render/key", data="null").json()

    # Make the final request to get the timetable
    timetable = {
        "renderKey": responsesecond['data']['key'],
        'host':"it-gymnasiet.skola24.se",
        'unitGuid':"ZTEyNTdlZjItZDc3OC1mZWJkLThiYmEtOGYyZDA4NGU1YjI2",
        "scheduleDay": weekday,
        "width": 1,
        "height": 1,
        "selectionType": 4,
        "selection": response['data']['signature'],
        "week": weeknumber,
        "year": 2023,
    }
    thirdurl = 'https://web.skola24.se/api/render/timetable'
    responsethird = s.post(thirdurl, data=json.dumps(timetable))
    return responsethird

def main():

    parser = argparse.ArgumentParser(description="Prints out the schedule for skola24.se NTI Södertörn")
    parser.add_argument('-c', '--classid', type=str, help='Select the current class ID')
    classid = parser.parse_args().classid
    result = json.loads(getData(classid).text)
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
    except KeyError:
        print("No class found")

if __name__ == "__main__":
    main()

