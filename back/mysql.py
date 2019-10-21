# -*- coding:utf-8 -*-
import pymysql
from confing import *
def server_content():
    conn = pymysql.connect(host=sql_host, port=sql_port, user=sql_user, passwd=sql_passwd, db=sql_db, charset='utf8')
    return conn
def select_user():
    conn=server_content()
    cursor=conn.cursor()
    cursor.execute("select * from user")
    res=cursor.fetchall()
    cursor.close()
    return res
def insert_user(username,password,fin,email):
    conn=server_content()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO user VALUES('"+username+"','"+password+"','"+fin+"','"+email+"')")
    cursor.close()
    conn.close()
def update_user(username,password,fin,email):
    conn=server_content()
    cursor=conn.cursor()
    cursor.execute("UPDATE user set password ="+"'"+password+"'" +"where "+"username="+"'"+username+"'")
    cursor.execute("UPDATE user set fin ="+"'"+fin+"'" +"where "+"username="+"'"+username+"'")
    cursor.execute("UPDATE user set email ="+"'"+email+"'" +"where "+"username="+"'"+username+"'")
    cursor.close()
    conn.close()
