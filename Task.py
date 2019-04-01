# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from core import OnlineCheck, AppAnnieProcessor
from util import Email, FileUtil, Common

'''
    需要解决错误：
        HTTPSConnectionPool(host='www.google.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLError('_ssl.c:710: The handshake operation timed out',),))
'''


'''
    待添加的功能需求
    1、输出的结果需要包含排名信息和包名。
'''


'''周期性检测任务'''
def task():
    print "do taks..."
    all_product_maps = {}
    count = 0
    Email.sendTaskStart()
    offline_map = {}
    if((not FileUtil.todayUpdated()) and FileUtil.updateEnable()):
        print "get product from file..."
        AppAnnieProcessor.dumpAppFromNet()
    all_product_maps = FileUtil.getAllKindProductMaps()
    print "waiting vpn connected(20s)..."
    time.sleep(20)
    if(OnlineCheck.googleAccessable()):
        for productMapKind in all_product_maps:
            product_map_for_kind = all_product_maps[productMapKind];
            count = count + 1
            if(count > 10):
                break
            print "count->" + str(count)
            print "check %s..." % str(product_map_for_kind)
            for product_pkg in product_map_for_kind:
                print "check pkg->%s..." % product_pkg
                ret = OnlineCheck.checkProduct(product_pkg)
                if (ret[Common.RET_VAL]):
                    print "%s online" % product_pkg
                else:
                    print "%s offline！！！" % product_pkg
                    offline_map[product_pkg] = "ranking->" + str(product_map_for_kind[product_pkg]) + " reason->" + ret[Common.RET_CONTENT] + " category->" + FileUtil.getCategoryName(productMapKind)
        print "check done."
        Email.loginAndSend(str(offline_map))
        FileUtil.saveLog(offline_map)
        FileUtil.updateEnable()
    else:
        print "不能翻墙，请稍后再试。"

if __name__ == '__main__':
    task()
