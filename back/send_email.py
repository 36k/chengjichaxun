#"-*- coding: utf-8 -*-"
from hlau_jwxt import *
import smtplib
from email.mime.text import MIMEText
from confing import *
#使用SSL链接
def sendmail(html,mailto):
    me="36k"+"<"+mail_user+">"
    msg=MIMEText(html,"html","utf-8")
    msg['Subject']='您的成绩有更新'
    msg['From']=me
    msg['To']=mailto
    try:
        server=smtplib.SMTP_SSL()
        server.connect(mail_host, 465)
        server.login(mail_user,mail_password)
        server.sendmail(me,mailto,msg.as_string())
        server.quit()
        print('Send email success')
        return True
    except Exception as e:
        print('Send email Fail')
        print (e)
        return False
