import requests
from bs4 import BeautifulSoup
import re
from confing import *
from login import *
#获取成绩，并以HTML表格的形式返回成绩信息，以Str的方式现有成绩的科目数
def get_score(conn):
    scoer_data=conn.get(server_host+'/xszqcjglAction.do?method=queryxscj')
    soup = BeautifulSoup(scoer_data.content, 'html.parser')
    value=int(soup.find('input', {'name': 'totalPages'}).get('value'))
    k=value
    flag=True
    temp=' '
    fin=' '
    html="""
          <table border="1" cellspacing='0' width=100% >
          <tr><td colspan='2' bgcolor='gray' align='center'>您的成绩如下</td></tr>
    """
    body={}
    while k>=1:
        scoer_data = conn.get(server_host+'/xszqcjglAction.do?method=queryxscj&&PageNum='+str(k))
        soup = BeautifulSoup(scoer_data.content, 'html.parser')
        s=soup.findAll('td')
        i =len(s)-1
        while i >=0:
            string=str(s[i].string)
            if (re.match(r'[0-9]{4}-[0-9]{4}-[0-9]',string) and (s[i+2].string!='系统正在读取数据信息， 请稍候...') and not(s[i+1].string.strip().isdigit())):
                if(string in body.keys()):
                    body[string].append(s[i+1].string+','+s[i+2].string)
                else:
                    body[string]=[s[i+1].string+','+s[i+2].string]
                i=i-2
            else:
                i=i-1
        k=k-1
    body=dict(sorted(body.items(), key=lambda d:d[0], reverse=True))
    fin=0
    for key in body:
        html=html+"<tr><td colspan='2'  bgcolor='green' align='center'>"+key+"</td></tr>"
        html=html+"<tr><td>科目</td><td>成绩</td></tr>"
        for s in body[key]:
            string=s.split(',')
            try:
                score=int(string[1])
            except:
                if(string[1]=='不及格'):
                    score=59
            finally:
                if(score<60):
                    html=html+"<tr><td>"+string[0]+"</td><td bgcolor='red'>"+string[1]+"</td></tr>"
                    fin=fin+1;
                else:
                    html=html+"<tr><td>"+string[0]+"</td><td>"+string[1]+"</td></tr>"
                    fin=fin+1;
    html=html+'</table>'
    print('Get Score Success')
    return {'html':html,'fin':str(fin)}
