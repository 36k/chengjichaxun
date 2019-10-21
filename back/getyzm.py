import os
import ctypes
from ctypes import *
from PIL import Image
import sys
import numpy as np
import uuid
def GetYzm(bytes,abs_dir):
    uuid3=str(uuid.uuid3(uuid.NAMESPACE_DNS, '36k.xyz'))
    yzm=''
    im = Image.frombytes('RGB',(62,22),bytes)
    # 转灰度图
    Lim = im.convert('L')
    # 设置阈值，转2BIT
    threshold = 175
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # convert to binary image by the table
    bim = Lim.point(table, '1')
    bim.save(abs_dir+uuid3+'.jpg')
    dll = ctypes.windll.LoadLibrary(abs_dir+'WmCode.dll')
    if (dll.UseUnicodeString(1, 1)):
        print('SetInUnicode Success!')
    else:
        print('etInUnicode Fail!')
    if (dll.LoadWmFromFile(abs_dir+'hlau.dat', '123')):
        print('Loaddat Success!')
        Str = create_string_buffer(4)
        dll.SetWmOption(2, 1)
        dll.SetWmOption(6, 80)
        dll.SetWmOption(7, -2)
        if (dll.GetImageFromFile(abs_dir+uuid3+'.jpg',Str)):
           yzm= Str.raw.decode("utf8")
           print('GetVcode Success!')
        else:
            print('GetVcode Fail!')
    else:
        print('Loaddat Fail!')
    os.remove(abs_dir+uuid3+'.jpg')
    return yzm
