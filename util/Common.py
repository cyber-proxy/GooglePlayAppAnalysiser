# coding: utf-8
# Create by LC
import sys,time,datetime,json

reload(sys)
sys.setdefaultencoding('utf8')

RET_BOOL_VAL = "ret_bool_val"
RET_EXCEPT = "ret_except"
RET_CODE = "status_code"

def getTimeStr():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

def getTimeDayStr():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

def getYesterday_():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday.strftime('%Y-%m-%d')

def getPre2day():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=2)
    yesterday=today-oneday
    return "20190430"#yesterday.strftime('%Y%m%d')
    # 输出

if __name__ == '__main__':
    # print time.strftime("%Y-%m-%d", time.localtime())
    # aMap = {"asdf":1, "asdfasdf":False, "asdfasdfaxx":True, "x":"yyyy"}
    # aMap["aas"] ="xxxx"
    # aMap["aasa"] = "xxxx"
    # aMap["aasv"] = "今天"
    # aMap ["com.aaa"] = [{"asdf":1}, {"234":2}]
    # print json.dumps(aMap, encoding='UTF-8', ensure_ascii=False)
    # trtime= time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    # print trtime
    # if not aMap.get('a'):
    #     print "zaa"
    # list = [{"rank":"90", "name":"1"},{"rank":"2222"}, {"rank":"110"}]
    # print str(list)
    # sl = sorted(list, cmp= lambda x,y:cmp(int(x["rank"]), int(y["rank"])))
    # print str(sl)
    print getPre2day()
    print time.localtime(time.time())