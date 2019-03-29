# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import AppAnnieProcessor, Email, OnlineCheck,Common,FileUtil

'''周期性检测任务'''
def task():
    print "do taks..."
    app_list = []
    if((not FileUtil.todayUpdated()) or not FileUtil.updateEnable()):
        print "get product from file..."
        app_list = FileUtil.getProductsContent()
    else:
        app_list = AppAnnieProcessor.getProductOnline()
    print "waiting vpn connected(20s)..."
    time.sleep(20)
    if(OnlineCheck.googleAccessable()):
        for app in app_list:
            print "check %s..." % app
            ret = OnlineCheck.checkProduct(app)
            if (ret[Common.RET_VAL]):
                print "%s 在线" % app
            else:
                print "%s 已经下线！！！" % app
                Email.login()
                time.sleep(5)
                Email.send(app, ret[Common.RET_CONTENT])
    else:
        print "不能翻墙，请稍后再试。"


if __name__ == '__main__':
    task()
