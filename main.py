import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import csv
import re
from datetime import datetime, timedelta, date
import uuid
import yaml
import os

import logging
logging.basicConfig(level=logging.INFO)

class login:
    SSO_LOGIN = 'https://sso.buaa.edu.cn/login'
    JWAPP = 'https://byxt.buaa.edu.cn/jwapp/sys/homeapp/index.do'
    SHCEDULE_URL = 'https://byxt.buaa.edu.cn/jwapp/sys/homeapp/api/home/student/getMyScheduleDetail.do'
    
    def __init__(self, username: str = '', password: str = '', term: str = ''):
        self.session = requests.session()
        self.username = username
        self.password = password
        self.term = term
        self.execution = None
        
        if not self.username or not self.password:
            logging.error("Username or password is empty.")
            return False
        
        if not self.term:
            logging.error("Term is empty.")
            return False
            
        if logging.getLogger().level == logging.DEBUG:
            self.session.proxies = {
                "http": "http://127.0.0.1:8080",
                "https": "http://127.0.0.1:8080",
            }
            from requests.packages import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.session.verify = False
        
    def get_execution(self):
        logging.info("Fetching execution value...")
        response = self.session.get(self.SSO_LOGIN, 
            params={'service':self.JWAPP})
        soup = BeautifulSoup(response.text, 'html.parser')
        execution_input = soup.find('input', {'name': 'execution'})
        if execution_input:
            self.execution = execution_input['value']
        else:
            logging.error("Failed to find execution input field.")
            return False
            
        logging.info("Finished fetching execution value.")
        return True
        
    def login(self):
            
        logging.info("Starting login process...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Referer": self.SSO_LOGIN,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = self.session.post(
            self.SSO_LOGIN,
            data={
                'username': self.username,
                'password': self.password,
                'submit': quote('登录'),
                'type': 'username_password',
                'execution': self.execution,
                '_eventId': 'submit'
            },
            headers=headers,
            allow_redirects=False
        )
        if response.status_code != 302:
            logging.error("Login failed, please try again.")
            logging.debug(f"Response status code: {response.status_code =}, Response text: {response.text}")
            return False
        
        logging.info("Login successful.")
        relocation_url = response.headers.get('Location', '')
        if not relocation_url:
            logging.error("No relocation URL found after login.")
            return False
        
        logging.info(f"Redirecting to {relocation_url}")
        response = self.session.get(relocation_url, allow_redirects=True)
        
        final_url = response.url
        logging.info(f"Final URL after redirection: {final_url}")
        if final_url == self.JWAPP:
            logging.info("Successfully logged into the academic system.")
            return True
        
        logging.error("Failed to log into the academic system.")
        return False
    
    def get_schedule(self):
        logging.info("Fetching schedule...")
        response = self.session.post(
            self.SHCEDULE_URL,
            data = {
                'termCode': self.term,
                'campusCode': '',
                'type': 'term',
            }
        )
        
        try:
            return_json = response.json()
            logging.info("Schedule fetched successfully.")
            return return_json
        except:
            logging.error("Failed to parse schedule response as JSON.")
            return None
            
    def run(self):
        if not self.get_execution():
            return False
        
        if not self.login():
            return False
            
        schedule = self.get_schedule()
        if schedule is None:
            return False
            
        data = schedule.get('datas', [])
        if not data:
            logging.error("No schedule data found.")
            return False
        
        arranged_list = data.get('arrangedList', [])
        if not arranged_list:
            logging.error("No arranged list found in schedule data.")
            return False
            
        return arranged_list
        
class convert:
    def __init__(self, schedule_list=[]):
        self.first_day = datetime.today()
        self.daily_time = {
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
        self.schedule_list = schedule_list
        self.list_for_csv = []
        
    def convert_schedule_to_csv(self):
        with open("schedule.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["课程名称", "星期", "开始节数", "结束节数", "老师", "地点", "周数"])
        
    
        for each_class in self.schedule_list:
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
                self.list_for_csv.append(append_list)
        
        with open("schedule.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerows(self.list_for_csv)
    
        return True
    
    def set_the_first_day_of_term(self, year, month, day):
        input_day = datetime(year, month, day)
        if input_day.weekday() != 0:
            logging.error("输入的日期不是周一，请重新输入！")
            return False
        self.first_day = datetime(year, month, day)
        return True
    
    def set_the_default_first_day_of_term(self):
        today = datetime.today()
        today_weekday = today.weekday()
        if today_weekday != 0:
            self.first_day = today - timedelta(days=today_weekday)
        else:
            self.first_day = today
        logging.info(f"Set the first day：{self.first_day.strftime('%Y-%m-%d')}")
        return True
    
    def convert_schedule_to_icaleander(self):
        with open("schedule.ics", "w") as f:
            f.write("BEGIN:VCALENDAR\n")
            f.write("VERSION:2.0\n")
            f.write("PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n")
            f.write("CALSCALE:GREGORIAN\n")
            for each_class in self.list_for_csv:
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
                    start_day = (self.first_day + timedelta(days=(int(day) - 1) + (int(start_week) - 1) * 7)).strftime("%Y%m%d")
                    end_day = (self.first_day + timedelta(days=(int(day) - 1) + (int(end_week) - 1) * 7)).strftime("%Y%m%d")
                    DTSTART = start_day + "T" + self.daily_time[int(start_section)][0] + "Z"
                    DTEND = start_day + "T" + self.daily_time[int(end_section)][1] + "Z"
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
    if not os.path.exists("config.yaml"):
        logging.error("File `config.yaml` isn't exist, please create one.")
        exit(1)
        
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    username = config.get("username", "")
    password = config.get("password", "")
    term = config.get("term", "")
    first_day_input : date = config.get("first_day_of_term", None)
    if first_day_input:
        year, month, day = first_day_input.year, first_day_input.month, first_day_input.day
    else:
        year = month = day = None
        
    obj = login(username, password, term)
    schedule = obj.run()
    if not schedule:
        logging.error("Failed to retrieve schedule.")
        exit(1)
        
    conv = convert(schedule_list=schedule)
    if year and month and day:
        if not conv.set_the_first_day_of_term(year, month, day):
            exit(1)
    else:
        conv.set_the_default_first_day_of_term()
        
    conv.convert_schedule_to_csv()
    conv.convert_schedule_to_icaleander()
    