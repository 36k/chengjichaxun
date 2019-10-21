from multiprocessing import process,Pool
import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlencode
from confing import *
from login import *
import threading
#一键评教
def auto_pj(conn,i):
    pj=conn.get(server_host+'/jiaowu/jxpj/jxpjgl_queryxs.jsp')
    soup = BeautifulSoup(pj.content, 'html.parser')
    xnxq=soup.select('[name=xnxq] option')[2].get('value')
    pjpc=soup.select('.p9 [name=pjpc] option')[1].get('value')
    pjfl=soup.select('.p9 [name=pjfl] option')[1].get('value')
    pjkc=soup.select('.p9 [name=pjkc] option')
    pj_data={
    'cmdok': '查  询',
    'ok':'',
    'xnxq':xnxq,
    'pjpc':pjpc,
    'pjfl':pjfl,
    'pjkc':pjkc[i].get('value'),
    'sfxsyjzb':'1',
    'zbnrstring':''
    }
    pjym=conn.post(server_host+'/jxpjgl.do?method=queryJxpj&type=xs',data=pj_data)
    soup = BeautifulSoup(pjym.content, 'html.parser')
    teachers=soup.select('[class=smartTr]  td a')
    if(len(teachers)!=0):
        for j in teachers:
            jsstring=j.get('onclick').replace(' ','')[19:-32]
            threading.Thread(target=pjofte,args=(conn,jsstring,)).start()

def pjofte(conn,jsstring):
    pjxq=conn.get(server_host+jsstring)
    soup = BeautifulSoup(pjxq.text, 'html.parser')
    type='2'
    pj09id=soup.select('[name=pj09id]')[0].get('value')
    pj01id=soup.select('[name=pj01id]')[0].get('value')
    pj05id=soup.select('[name=pj05id]')[0].get('value')
    jg0101id=soup.select('[name=jg0101id]')[0].get('value')
    pjdw=soup.select('[name=pjdw]')[0].get('value')
    xsflid=soup.select('[name=xsflid]')[0].get('value')
    typejsxs=soup.select('[name=typejsxs]')[0].get('value')
    jx0404id=soup.select('[name=jx0404id]')[0].get('value')
    pj0502id=soup.select('[name=pj0502id]')[0].get('value')
    pjfl=soup.select('[name=pjfl]')[0].get('value')
    jx02id=soup.select('[name=jx02id]')[0].get('value')
    isxytj=soup.select('[name=isxytj]')[0].get('value')
    item_dict={}
    post_data={
        'type':type,
        'pj09id':pj09id,
        'pj01id':pj01id,
        'pj05id':pj05id,
        'jg0101id':jg0101id,
        'pjdw':pjdw,
        'xsflid':xsflid,
        'typejsxs':typejsxs,
        'jx0404id':jx0404id,
        'pj0502id':pj0502id,
        'pjfl':pjfl,
        'jx02id':jx02id,
        'isxytj':isxytj,
    }
    payload=''
    val=''
    try:
        radios=soup.select('[radioxh=0]')
        finradios=soup.select('[radioxh=1]')
        finradio=finradios[len(finradios)-1]
        radios.remove(radios[len(radios)-1])
        radios.append(finradio)
        for i in soup.select('[name=zbmc]') :
            item=i.get('value')
            if(item in item_dict.keys()):
                item_dict[item]=item_dict[item]+1
            else:
                item_dict[item]=1
        for i in item_dict.keys():
            post_data['ischeck']='on'
            post_data['zmbc']=i
            for i in range(item_dict[i]):
                post_data[radios[0].get('name')]=radios[0].get('value')
                val=val+radios[0].get('value')+'*'
                radios.remove(radios[0])
            payload=payload+urlencode(post_data)+'&'
            post_data.clear()
        val=val[:-1]
        payload='&'+payload[:-1]
    except:
        payload=payload+'&'+urlencode(post_data)
    finally:
        result=conn.post(server_host+'/jxpjgl.do?method=savePj&tjfs=2&val='+val+payload)
        print(result.text.replace("<script language='javascript'>alert('","").replace("window.parent.returnValue='ok';window.close();</script>')",""))
if __name__ == '__main__':
    conn = login('20164081112','Aa196117')['conn']
    p=Pool(8)
    for i in range(4):
        p.apply_async(auto_pj,(conn,i,))
    p.close()
    p.join()
