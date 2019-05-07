# coding: utf-8
# Create by LC
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import json,requests
import socket
from util import Email, Common

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
    print "check vpn..."
    try:
        # requests.adapters.DEFAULT_RETRIES = 5
        # s = requests.sessions()
        # s.keep_alive = False
        status_code = requests.get(target_url, timeout=30).status_code
        print "status code->%s"%status_code
        if (status_code == 200):
            return True
        else:
           return False
    except Exception, e:
        print str(Exception) + "\n" + str(e)
        return False

'''查看产品页面是否存在'''
def checkProduct(product):
    ret = {Common.RET_BOOL_VAL: False, Common.RET_EXCEPT: Common.RET_NONE, Common.RET_CODE:-1}
    try:
        addr = ('%s%s' % (URL, product))
        print "request->" +addr
        session = requests.session()
        session.keep_alive = False
        status_code = requests.head(addr, timeout=20).status_code
        print "status code->%s"%status_code
        if(status_code == 200):
            ret[Common.RET_BOOL_VAL] = True
        else:
            ret[Common.RET_CODE] = str(status_code)
            ret[Common.RET_BOOL_VAL] = False
        return ret
    except Exception, e:
        ret[Common.RET_BOOL_VAL] = False
        ret[Common.RET_EXCEPT] = str(Exception) + "\n" + str(e)
        print str(Exception)
        print str(e)
        return ret

'''检测翻墙可用'''
def googleAccessable():
    return http_validate("https://www.google.com/")

"""main"""
if __name__ == '__main__':
    productMap = readJson("C:\\Users\Administrator\\PycharmProjects\\AppDetectorScheduleTask\\json\product\\20190330181834.json")
    if(googleAccessable()):
        print "翻墙有效"
        for product in productMap:
            ret = checkProduct(product)
            if(ret[Common.RET_BOOL_VAL]):
                print "产品在线"
            else:
                print "产品下线"
                # Email.login()
                # Email.sendTaskResult(product + "\n" + ret[Common.RET_CONTENT])
    else:
        print "翻墙失效"