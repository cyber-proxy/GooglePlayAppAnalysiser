# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import AppAnieParse, EmailSender, OnlineDetector

'''周期性检测任务'''
def task():
    print "do taks..."
    content = AppAnieParse.getAppsAddres()
    appList = AppAnieParse.parseApp(content)
    for app in appList:
        print "check %s..." % app
        online = OnlineDetector.checkProduct(app)
        if (online):
            print "%s 在线" % app
        else:
            print "%s 已经下线！！！" % app
            EmailSender.login()
            time.sleep(3)
            EmailSender.send(app)


if __name__ == '__main__':
    task()
