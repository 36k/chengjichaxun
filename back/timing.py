import time
from mysql import *
from send_email import *
from confing import *
from login import *
from get_score import *
def send_timing():
    while True:
        current_time = time.localtime(time.time())
        if((current_time.tm_hour == hour) and (current_time.tm_min == min) and (current_time.tm_sec ==sec)):
            print('checking score ........')
            print('ok')
            res =select_user()
            for i in res:
                username=i[0]
                password=i[1]
                email=i[3]
                o_fin=i[2]
                try:
                    conn=login(username,password)
                    all=get_score(conn.get('conn'))
                    html=all.get('html')
                    fin=all.get('fin')
                except:
                    continue
                if(o_fin==fin):
                    print('USER: '+username+' '+email+'Sending.......')
                    update_user(username,password,fin,email)
                    sendmail(html,email)
        time.sleep(1)
