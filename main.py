import requests
from bs4 import BeautifulSoup
from requests.packages import urllib3

urllib3.disable_warnings()

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

def login(id, passwd):
    
    def get_execution_and_insert_cookie():
        cookies = {
            '_7da9a': 'http://10.0.3.60:8080',
        }

        headers = {
            'Host': 'sso.buaa.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept-Language': 'zh-CN',
            'Referer': 'https://byxt.buaa.edu.cn/',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        params = {
            'service': 'https://byxt.buaa.edu.cn/jwapp/sys/homeapp/index.do',
        }

        response = requests.get('https://sso.buaa.edu.cn/login', params=params, cookies=cookies, headers=headers, verify=False, allow_redirects=False, proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')
        execution = soup.find('input', {'name': 'execution'}).get('value')
        # print(execution)
        insert_cookie = response.headers.get('Set-Cookie').split(';')[2].split('=')[-1]
        return execution, insert_cookie
    
    def get_location(id, passwd, execution, insert_cookie):
        cookies = {
            '_7da9a': 'http://10.0.3.60:8080',
            'insert_cookie': insert_cookie,
        }

        headers = {
            'Host': 'sso.buaa.edu.cn',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept-Language': 'zh-CN',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://sso.buaa.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://sso.buaa.edu.cn/login?service=https%3A%2F%2Fbyxt.buaa.edu.cn%2Fjwapp%2Fsys%2Fhomeapp%2Findex.do',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        data = {
            'username': id,
            'password': passwd,
            'submit': '登录',
            'type': 'username_password',
            'execution': execution,
            '_eventId': 'submit',
        }

        response = requests.post('https://sso.buaa.edu.cn/login', cookies=cookies, headers=headers, data=data, verify=False, allow_redirects=False, proxies=proxies)
        # print(response.headers)
        # CASTGC = response.headers.get('Set-Cookie').split(';')[0].split('=')[-1]
        location = response.headers.get("Location").strip().split("=")[-1]
        # print(CASTGC)
        return location

    def get_gs_sessionid(location):
        headers = {
            'Host': 'byxt.buaa.edu.cn',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept-Language': 'zh-CN',
            'Referer': 'https://sso.buaa.edu.cn/',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        params = {
            "ticket": location,
        }

        response = requests.get('https://byxt.buaa.edu.cn/jwapp/sys/homeapp/index.do', params=params, headers=headers, verify=False, allow_redirects=False, proxies=proxies)

        set_cookie = response.headers.get("Set-Cookie").strip().split(";")
        gs_sessionid = set_cookie[6].split("=")[-1]
        _zte_cid_ = set_cookie[0].split("=")[-1]
        _zte_sid_ = set_cookie[3].split("=")[-1]
        return gs_sessionid, _zte_cid_, _zte_sid_
    
    def get_WEU(gs_sessionid, _zte_cid_, _zte_sid_):
        cookies = {
            'GS_SESSIONID': gs_sessionid,
            '_zte_cid_': _zte_cid_,
            '_zte_sid_': _zte_sid_,
        }

        headers = {
            'Host': 'byxt.buaa.edu.cn',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept-Language': 'zh-CN',
            'Referer': 'https://sso.buaa.edu.cn/',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        response = requests.get('https://byxt.buaa.edu.cn/jwapp/sys/homeapp/index.do', cookies=cookies, headers=headers, verify=False, allow_redirects=False, proxies=proxies)
        _WEU = response.headers.get("Set-Cookie").strip().split(",")[-1].split(";")[0].split("=")[-1]
        return _WEU

    execution, insert_cookie = get_execution_and_insert_cookie()
    location = get_location(id, passwd, execution, insert_cookie)
    gs_sessionid, _zte_cid_, _zte_sid_ = get_gs_sessionid(location)
    _WEU = get_WEU(gs_sessionid, _zte_cid_, _zte_sid_)
    return gs_sessionid, _WEU

def get_schedule(gs_sessionid, _WEU, term):
    cookies = {
        'GS_SESSIONID': gs_sessionid,
        '_WEU': _WEU,
        }

    headers = {
        'Host': 'byxt.buaa.edu.cn',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'Accept-Language': 'zh-CN',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept': 'application/json',
        'Fetch-Api': 'true',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Origin': 'https://byxt.buaa.edu.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://byxt.buaa.edu.cn/jwapp/sys/homeapp/home/index.html?av=1725888244394&contextPath=/jwapp',
        'Priority': 'u=1, i',
        'Connection': 'keep-alive',
    }

    data = {
        'termCode': term,
        'campusCode': '',
        'type': 'term',
    }

    response = requests.post(
        'https://byxt.buaa.edu.cn/jwapp/sys/homeapp/api/home/student/getMyScheduleDetail.do',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    # print(response.text)
    schedule_json = response.json()
    schedule_list = schedule_json["datas"]["arrangedList"]
    return schedule_list

import csv
import re
def convert_schedule_to_csv(schedule_list):
    with open("schedule.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["课程名称", "星期", "开始节数", "结束节数", "老师", "地点", "周数"])
    list_for_csv = []

    for each_class in schedule_list:
        class_name = each_class["courseName"]
        class_day = each_class["dayOfWeek"]
        beginSection = each_class["beginSection"]
        endSection = each_class["endSection"]
        place = each_class["placeName"]
        weeks_and_teachers = each_class["cellDetail"][1]["text"].split(" ")
        for i in weeks_and_teachers:
            append_list = []
            find = re.findall(r"(.*?)\[(.*?)\]", i)
            teacher = find[0][0]
            weeks = find[0][1].split(",")
            week_list = []
            for week in weeks:
                if re.findall(r"单", week):
                    week = week[:-4]
                    week += "单"
                elif re.findall(r"双", week):
                    week = week[:-4]
                    week += "双"
                else:
                    week = week[:-1]
                week_list.append(week)
                week_all = "、".join(week_list)
            append_list.append(class_name)
            append_list.append(class_day)
            append_list.append(beginSection)
            append_list.append(endSection)
            append_list.append(teacher)
            append_list.append(place)
            append_list.append(week_all)
            list_for_csv.append(append_list)
    
    with open("schedule.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(list_for_csv)

    return list_for_csv

daily_time = {
    1: ["000000", "004500"],
    2: ["005000", "013500"],
    3: ["015000", "023500"],
    4: ["024000", "032500"],
    5: ["033000", "041500"],
    6: ["060000", "064500"],
    7: ["065000", "073500"],
    8: ["075000", "083500"],
    9: ["084000", "092500"],
    10: ["093000", "101500"],
    11: ["110000", "114500"],
    12: ["115000", "123500"],
    13: ["124000", "132500"],
    14: ["133000", "141500"],
}

from datetime import datetime, timedelta
import uuid
first_day_of_term = datetime(2024,9,10)
def set_the_first_day_of_term(year, month, day):
    global first_day_of_term
    input_day = datetime(year, month, day)
    if input_day.weekday() != 0:
        print("输入的日期不是周一，请重新输入！")
        return False
    first_day_of_term = datetime(year, month, day)
    return True

def set_the_default_first_day_of_term():
    global first_day_of_term
    today = datetime.today()
    today_weekday = today.weekday()
    if today_weekday != 0:
        first_day_of_term = today - timedelta(days=today_weekday)
    else:
        first_day_of_term = today

def convert_schedule_to_icaleander(list_for_csv):
    with open("schedule.ics", "w") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n")
        f.write("CALSCALE:GREGORIAN\n")
        for each_class in list_for_csv:
            name = each_class[0]
            day = each_class[1]
            start_section = each_class[2]
            end_section = each_class[3]
            teacher = each_class[4]
            place = each_class[5]
            weeks = each_class[6].split("、")
            for week in weeks:
                f.write("BEGIN:VEVENT\n")
                f.write("UID:buaa2ical-{}-CoolwindHF\n".format(str(uuid.uuid4())))
                # print(week)
                week = week.split("-")
                every_2_weeks = False
                if len(week) == 1:
                    start_week = int(week[0])
                    end_week = int(week[0])
                else:
                    if re.findall(r"单|双", week[1]):
                        every_2_weeks = True
                        start_week = int(week[0])
                        end_week = int(week[1][:-1])
                    else:
                        start_week = int(week[0])
                        end_week = int(week[1])
                start_day = (first_day_of_term + timedelta(days=(int(day) - 1) + (int(start_week) - 1) * 7)).strftime("%Y%m%d")
                end_day = (first_day_of_term + timedelta(days=(int(day) - 1) + (int(end_week) - 1) * 7)).strftime("%Y%m%d")
                DTSTART = start_day + "T" + daily_time[int(start_section)][0] + "Z"
                DTEND = start_day + "T" + daily_time[int(end_section)][1] + "Z"
                f.write("DTSTART:{}\n".format(DTSTART))
                f.write("DTEND:{}\n".format(DTEND))
                if len(week) == 1:
                    description = f"第{start_week}周\\n第{start_section} - {end_section}节\\n{place}\\n{teacher}\\n"
                else:
                    if not every_2_weeks:
                        description = f"第{start_week} - {end_week}周\\n第{start_section} - {end_section}节\\n{place}\\n{teacher}\\n"
                    else:
                        description = f"第{start_week} - {end_week}{week[1][-1:]}周\\n第{start_section} - {end_section}节\\n{place}\\n{teacher}\\n"
                f.write(f"DESCRIPTION:{description}\n")
                f.write(f"SUMMARY:{name}\n")
                f.write(f"LOCATION:{place} {teacher}\n")
                if not every_2_weeks:
                    f.write(f"RRULE:FREQ=WEEKLY;INTERVAL=1;UNTIL={end_day}\n")
                else:
                    f.write(f"RRULE:FREQ=WEEKLY;INTERVAL=2;UNTIL={end_day}\n")
                f.write("END:VEVENT\n")
        f.write("END:VCALENDAR\n")

if __name__ == "__main__":
    print("使用前提示，请确保已经在校园网环境下并且代理配置正确，若在下方登录中出现登录失败请查看README中的【登录失败】标题下内容！")
    id = input("请输入统一认证学号：").strip()
    passwd = input("请输入统一认证密码：").strip()
    gs_session, _WEU = login(id, passwd)
    # print(_WEU)
    if '01 Jan 1970 00:00:10 GMT' in _WEU:
        print("登陆失败，请检查代理配置！")
        exit()
    print("账号{}登陆成功！".format(id))
    year = input("请输入学年，如“2024-2025-1”代表2024-2025学年第一学期：").strip()
    schedule_list = get_schedule(gs_session, _WEU, year)
    # print(schedule_list)
    list_for_csv = convert_schedule_to_csv(schedule_list)
    print("课程表已保存为schedule.csv文件！请发送到手机后导入wakeup课程表！")
    to_ical = input("是否将课程表转换为iCalendar文件？(y/n):").strip()
    if to_ical == "y":
        while True:
            first_day = input("请输入学期第一周的周一日期，如“2024-09-02”，直接回车跳过默认以当前周作为学期第一周：").strip().split("-")
            if len(first_day) != 3:
                set_the_default_first_day_of_term()
            else:
                year, month, day = first_day[0], first_day[1], first_day[2]
                if not set_the_first_day_of_term(int(year), int(month), int(day)):
                    continue
            break
        convert_schedule_to_icaleander(list_for_csv)
        print("课程表已保存为schedule.ics文件！请导入日历软件！")
