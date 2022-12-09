import pandas as pd
from datetime import datetime

#월 시작 (이월)금액 가져오기
def callup_start_revenue(month):
    Monthly_start_revenue = pd.read_excel('data/Monthly_start_revenue.xlsx') 
    str_revenue = Monthly_start_revenue.loc[Monthly_start_revenue['str_month']==month]
    return str_revenue    
    
#해당 월 사용 기록 가져오기
def callup_eat_record(month):
    store_rcd = pd.read_excel('data/store_record.xlsx')
    eat_rcd = store_rcd.loc[store_rcd['Month']==month]
    return eat_rcd

#직원 소속 데이터 가져오기
def callup_employees_db():
    df_emp = pd.read_excel('data/employees_db.xlsx')
    return df_emp




#년월 값 가져오기
def get_thismonth():
    m_value = str(datetime.now().month)
    y_value = str(datetime.now().year)
    if len(m_value) == 1:
        m_value = '0'+m_value
    return y_value+'년 '+m_value+'월'