#!C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe
#print("content-type: text/html; charset=euc-kr\n")

import pandas as pd
import numpy as np
import get_data
from datetime import datetime
import cgi

form=cgi.FieldStorage()
this_month = get_data.get_thismonth()
df_emp = get_data.callup_employees_db()
team_list = df_emp['Team'].unique()
def get_team():
    teams = ''
    for item in team_list:
        teams = teams + '<li><a href="index.py?id={name}">{name}</a></li>'.format(name=item)
    return teams

if 'team' in form:
    teams = form['team'].value
else:
    teams = '소속팀을 선택하세요.'

html_str = f'''
<!DOCTYPE html>

<head>
    <title>Howon's work Station</title>
    <meta charset="euc-kr">
    <link rel="stylesheet" type="text/css" href="css/styless.css"/>
</head>
<body>
    <h1><a href="index.py">직원 급량비 관리 프로그램</a></h1>
    <p>
        {this_month}
    </p>
    <ul>
        <li><a href="index.py?team=admin">복지행정팀</a></li>
        <li><a href="index.py?team=support">복지지원팀</a></li>
        <li><a href="index.py?team=service">복지서비스팀</a></li>
    </ul>
    <p>
        {teams}
    </p>
</body>
</html>
'''

print(html_str)