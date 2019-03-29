# coding: utf-8
# Create by LC
import sys
import json
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

CONFIG_FILE = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\cfg.json"
PRODUCT_FILE = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\products"

'''判断当天是否已经拉取了最新的前500个包名'''
def todayUpdated():
    print "update config"
    cfgR= open(CONFIG_FILE, "r")
    cfgJson = json.load(cfgR)
    cfgR.close()
    today = datetime.date.today()
    lastUpdate = cfgJson["last_download_app_time"]
    print "lastUpdate->%s"%lastUpdate + " today->%s"%today.day
    if(datetime.date.today().day - lastUpdate > 1):
        cfgJson["last_download_app_time"] = datetime.date.today().day
        cfgW = open(CONFIG_FILE, 'w')
        json.dump(cfgJson, cfgW)
        cfgW.close()
        return False
    else:
        return True

'''读取已经拉取的产品列表'''
def getProductsContent():
    print "reading %s"%PRODUCT_FILE
    product = open(PRODUCT_FILE, 'r').read();
    productList = product.split('\n')
    return productList

def updateEnable():
    cfgR= open(CONFIG_FILE, "r")
    cfgJson = json.load(cfgR)
    cfgR.close()
    return cfgJson["enable_update"]



if __name__ == '__main__':
    if(updateEnable()):
        print "updated"
    else:
        print "no updated"
