#!C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe
print("content-type: text/html; charset=euc-kr\n")

import pandas as pd
import numpy as np
import datetime
import cgi, os

form=cgi.FieldStorage()
df_mt = pd.read_excel('data/maintask.xlsx')
df_dt = pd.read_excel('data/date_std.xlsx')
df_mt.fillna('', inplace=True)

#date DB에서 merge 필요한 column만 추출
df_dt2 = df_dt[['DATE', 'WN_SERIAL NO', 'STD_CODE']]
#MMM-DD포멧으로 Column 생성하여 붙여넣기
df_dt2['unique_date'] = np.nan

#mmm-dd형식의 날짜 데이터 생성
i=0
while i < len(df_dt2):
    x = df_dt2.iloc[i,0].strftime('%b %d, %Y') #std 코드에 해당하는 날짜를 가져옴
    df_dt2.loc[i,['unique_date']] = x
    i+=1

#Main Task DB에 날짜 데이터 붙이기
df = pd.merge(df_mt, df_dt2, how='left', left_on='DUE DATE', right_on='DATE')

url_id = 'http://127.0.0.1:81/PJT_workstation/index.py?id='
def make_clickable(url, code):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url, code)
    #return f'{url}" rel="noopener noreferrer" target="_blank">{name}'

df['link'] = df.apply(lambda x: make_clickable(url_id+x['TASK_CODE'], x['TASK_CODE']), axis=1)



#wn 지정하고 날짜 리스트 생성
def get_cols(wn):
    cols = []
    wn = str(wn)
    for i in range(1,8):
        a = wn+'_'+str(i)
        x = df_dt.loc[df_dt['STD_CODE']==a,['DATE']]
        x2 = x.iloc[0,0].strftime('%b %d, %Y')
        cols.append(x2)
    return cols

#redirection
print('Location: index.py')
print()