import multiprocessing
from flask import Flask, url_for
from flask_cors import CORS
from flask_restful import request
from hlau_jwxt import *
from send_email import *
from mysql import *
from confing import *
from timing import *
app = Flask(__name__)
CORS(app,supports_credentials=True)
@app.route('/POST/',methods=['POST'])
def api_post():
    username=request.form.to_dict().get('username')
    password=request.form.to_dict().get('password')
    email=request.form.to_dict().get('email')
    conn=login(username,password)
    try:
        all=get_score(conn.get('conn'))
        html=all.get('html')
        fin=all.get('fin')
        sendmail(html,email)
        try:
            insert_user(username,password,fin,email)
        except:
            update_user(username,password,fin,email)
    finally:
        return conn.get('isok')
#设置SSL(自行添加参数) 和多线程
def run_api():
    app.run(host='0.0.0.0', port=5000,threaded=True)
def run_timing():
    send_timing()
if __name__ == '__main__':
    p = multiprocessing.Process(target=run_api)
    p.start()
    p = multiprocessing.Process(target=run_timing)
    p.start()
    p.join()
