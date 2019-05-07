# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time, datetime, threadpool, threading
from core import OnlineCheck, AppAnnieProcessor
from util import Email, FileUtil, Common
semaphore = threading.Semaphore(1)

'''
    需要解决错误：
        HTTPSConnectionPool(host='www.google.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLError('_ssl.c:710: The handshake operation timed out',),))
'''

'''
    功能需求
    1、输出的结果需要包含排名信息和包名。
    2、定时执行。
    3、自动拉取appanie信息。
    4、检测前一天的下线信息。
'''

'''周期性检测任务'''
def task():
    print "do taks..."
    all_product_maps = {}
    count = 0
    # Email.sendTaskStart()
    offline_map_email = {}
    offline_map_log = {}
    # if((not FileUtil.todayUpdated()) and FileUtil.updateEnable()):
    # AppAnnieProcessor.dumpAppFromNet()
    print "get product from file..."
    all_product_maps = FileUtil.getAllKindProductMaps()
    print "waiting vpn connected(10min)..."
    waitfor(OnlineCheck.googleAccessable)
    myThreadPool = threadpool.ThreadPool(100)
    if(OnlineCheck.googleAccessable()):
        paramsList = []
        for productMapKind in all_product_maps:
            product_map_for_kind = all_product_maps[productMapKind];
            count = count + 1
            # print "count->" + str(count) + " " + productMapKind
            # print "check %s..." % str(product_map_for_kind)
            for product_pkg in product_map_for_kind:
                # print "check pkg->%s..." % product_pkg
                paramsList.append(([product_pkg, productMapKind, product_map_for_kind, offline_map_log, offline_map_email], None))
                # checkOnlineTask(product_pkg, productMapKind, product_map_for_kind, offline_map_log, offline_map_email)
        requestsList = threadpool.makeRequests(checkOnlineTask,paramsList)
        map(myThreadPool.putRequest, requestsList)
        myThreadPool.wait()
        print "check done."
        Email.loginAndSend(offline_map_email)
        FileUtil.saveLog(offline_map_log)
        FileUtil.updateEnable()
    else:
        print "不能翻墙，请稍后再试。"


def waitfor(getter, timeout=6000, interval=0.5):
    startTime = datetime.datetime.now()
    while True:
        if(getter()):
            return
        else:
            runTime = datetime.datetime.now() - startTime
            if runTime.seconds >= timeout:
                raise Exception("time out!")
            time.sleep(interval)

def checkOnlineTask(product_pkg, productMapKind, product_map_for_kind, offline_map_log, offline_map_email):
    ret = OnlineCheck.checkProduct(product_pkg)
    if (ret[Common.RET_BOOL_VAL]):
        print "%s online" % product_pkg
    else:
        semaphore.acquire()
        print "%s offline！！！" % product_pkg
        category = FileUtil.getCategoryName(productMapKind)
        ran_name = str(product_map_for_kind[product_pkg]).split(',')
        rank = ran_name[0]
        name = ran_name[1]
        # local log content
        category_list = offline_map_log.get(category)
        if not category_list:
            category_list = []
            offline_map_log[category] = category_list
        offline_map_log[category].append({"name": name, "pkg": product_pkg, "rank": rank, " ret": ret})
        # Email content
        if ret[Common.RET_CODE] == str(404):
            category_list = offline_map_email.get(category)
            if not category_list:
                category_list = []
                offline_map_email[category] = category_list
            offline_map_email[category].append({"name": name, "pkg": product_pkg, "rank": rank})
        semaphore.release()

if __name__ == '__main__':
    task()
