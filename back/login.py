import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from getyzm import GetYzm
import os
import re
from confing import *
#登陆
def login(username,password):
    conn=requests.session()
    yzm_data=conn.get(server_host+'/verifycode.servlet')
    session=yzm_data.headers['Set-Cookie'].strip('; Path=/').strip('JSESSIONID=')
    yzm_data=conn.get(server_host+'/verifycode.servlet')
    yzm_image=Image.open(BytesIO(yzm_data.content))
    bytes=yzm_image.tobytes()
    yzm_code=GetYzm(bytes,abs_dir)
    login_data={
    'USERNAME':username,
    'PASSWORD':password,
    'useDogCode':'',
    'useDogCode':'',
    'RANDOMCODE':yzm_code,
    'x':'0',
    'y':'0',
    }
    login=conn.post(server_host+'/Logon.do?method=logon',data=login_data)
    soup = BeautifulSoup(login.content, 'html.parser')
    try:
        isok=soup.find('span',id='errorinfo').get_text()
    except AttributeError as e:
        isok='恭喜您提交成功!'
        print ('login Success')
        login=conn.post(server_host+'/Logon.do?method=logonBySSO')
    finally:
        if(isok!='恭喜您提交成功!'):
            isok='账号不存在或者密码错误，请检查后重新提交!'
            print ('login Fail')
    return {'conn':conn,'isok':isok}
