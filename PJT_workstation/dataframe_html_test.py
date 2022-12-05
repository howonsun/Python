#!C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe
print("content-type: text/html; charset=euc-kr\n")
import pandas as pd
import numpy as np
import datetime
import cgi

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

swn = 419

#주차에 해당하는 주단위 일정표 Frame 생성(empty)
df_thisweek = pd.DataFrame()

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

#주차 선택하기
col_thisweek = get_cols(swn)

for day in col_thisweek:
    dfs = df.loc[df['unique_date']==day,['TASK_CODE']]  #해당 날짜에 맞는 업무코드를 가져오기 (DataFrame)
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
pd.set_option('colheader_justify', 'left')   # FOR TABLE <th>
html_string = f'''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="css/index_platform_test.css"/>
  <body>
    {table}
  </body>
</html>.
'''

with open('myhtml2.html', 'w') as f:
    f.write(html_string)

print(html_string)