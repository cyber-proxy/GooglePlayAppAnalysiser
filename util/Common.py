# coding: utf-8
# Create by LC
import sys,time,datetime,json

reload(sys)
sys.setdefaultencoding('utf8')

RET_VAL = "ret_val"
RET_CONTENT = "ret_content"

def getTimeStr():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

def getTimeDayStr():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

if __name__ == '__main__':
    print time.strftime("%Y-%m-%d", time.localtime())
    aMap = {"asdf":1, "asdfasdf":False, "asdfasdfaxx":True, "x":"yyyy"}
    aMap["aas"] ="xxxx"
    aMap["aasa"] = "xxxx"
    aMap["aasv"] = "今天"
    aMap ["com.aaa"] = "z"
    print json.dumps(aMap, encoding='UTF-8', ensure_ascii=False)
    trtime= time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print trtime