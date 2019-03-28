# -*- coding: UTF-8 -*-

import os
import string
import os,sys,re
import subprocess
import urllib2,urllib,json
import socket
from threading import Timer
import EmailSender

'''设置网络延时'''
socket.setdefaulttimeout(20.0)

products = ["com.lm.powersecurity"]
URL = "https://play.google.com/store/apps/details?id="

'''解析json配置文件'''
def readJson(path):
    products = {}
    with open(path) as jsonFile:
        products = json.load(jsonFile)
        return products


'''超时，关闭句柄'''
def timeHandler(handle):
    print "timeout..."
    handle.close()

'''检测网络可达，验证可行'''
def http_validate(target_url):
    print "test vpn..."
    try:
       urllib2.urlopen(target_url)
       return True
    except:
       return False

'''查看产品页面是否存在'''
def checkProduct(product):
    try:
        addr = ('%s%s' % (URL, product))
        print "request->" +addr
        req = urllib2.Request(addr)
        res = urllib2.urlopen(req)
        t = Timer(20.0, timeHandler, [res])
        t.start()
        # res = res.read()
        # print(res)
        return True
    except:
        return False


"""main"""
if __name__ == '__main__':
    productMap = readJson("C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\product.json")
    if(http_validate("https://www.google.com/")):
        print "翻墙有效"
        for product in productMap.values():
            if(checkProduct(product)):
                print "产品在线"
            else:
                print "产品下线"
                EmailSender.login()
                EmailSender.send(product)
    else:
        print "翻墙失效"