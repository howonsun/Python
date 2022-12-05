#!C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe
#print("content-type: text/html; charset=euc-kr\n")
import set_up
import pandas as pd
import numpy as np
import datetime
import cgi

df = set_up.df

#주차 선택하기
swn = 420

#주차에 해당하는 주단위 일정표 Frame 생성(empty)
df_thisweek = pd.DataFrame()

#주차 선택하고 해당 일자 리스트로 가져오기
col_thisweek = set_up.get_cols(swn)

for day in col_thisweek:
    dfs = df.loc[df['unique_date']==day,['link']]  #해당 날짜에 맞는 업무코드를 가져오기 (DataFrame)
    dfs.columns = [day] #Column 명 날짜로 변경
    dfs.reset_index(drop=True, inplace=True) #기존 인덱스 제거하기
    df_thisweek = pd.concat([df_thisweek,dfs], axis=1) #주단위 일정표에 붙이기

#빈 인덱스 만큼 Nan으로 합치기
lst_num = len(df_thisweek) #현재 데이터 프레임 index 개수 가져오기
if lst_num < 6:
    while len(df_thisweek) <= 6:
        edf = pd.DataFrame(index=[len(df_thisweek)])
        df_thisweek = pd.concat([df_thisweek,edf], axis=0)

table = df_thisweek.to_html(classes='mystyle')
table = table.replace('&lt;','<')
table = table.replace('&gt;','>')

pd.set_option('colheader_justify', 'left')   # FOR TABLE <th>

html_str = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Howon's work Station</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="css/styless.css"/>
</head>
<body>
    <div class="grid">
        <div class="callender">
            <div class="cal_top">
                <form action="set_up.py" method="post">
                    <p><input type="submit" value="get_data"></p>
                </form>
            </div>
            <div class="cal_main">
                callender_main {swn}주차
                </br>
                {table}
            </div>
            <div class="cal_bottom">
                <div class="cal_pm">
                    previous month
                </div>
                <div class="cal_tm">
                    This Month
                </div>
                <div class="cal_nm">
                    next month
                </div>
            </div>
        </div>
        <div class="information">
            <div class="task_check">
                <div class="task_info">
                    Task information
                </div>
                <div class="task_history">
                    Task history
                </div>
            </div>
            <div class="task_buttons">
                Buttons
            </div>
            <div class="task_for_days">
                <div class="task_daily">
                    Daily check
                </div>
                <div class="task_simple">
                    Simple task
                </div>
            </div>  
        </div>
        <div class="documents">
            <div class="docs_official">
                Official docs
            </div>
            <div class="docs_material">
                Material docs
            </div>
            <div class="docs_new">
                New docs
            </div>
        </div>
    </div>
</body>
</html>
'''

print(html_str)