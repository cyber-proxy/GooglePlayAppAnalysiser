# coding: utf-8
# Create by LC
import os
import sys
import json
import datetime
from util import Common

reload(sys)
sys.setdefaultencoding('utf8')

CONFIG_FILE = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\json\cfg\\appanniedownload.json"
PRODUCT_FILE = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\products"
CHECK_LOG = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\json\log\\"
CATEGORY_FILE = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\json\cfg\category.json"
# 天数/产品类别.json
PRODUCT_DICT_PATH = "C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\json\product\%s\\"

'''读取json文件'''
def getJsonObject(filePath):
    print "read %s ..." % filePath
    file = open(filePath, "r")
    jsonObj = json.load(file)
    return jsonObj


'''判断当天是否已经拉取了最新的前500个包名'''
def todayUpdated():
    print "update config"
    cfgR = open(CONFIG_FILE, "r")
    cfgJson = json.load(cfgR)
    cfgR.close()
    today = datetime.date.today()
    lastUpdate = cfgJson["last_download_app_time"]
    print "lastUpdate->%s" % lastUpdate + " today->%s" % today.day
    if (datetime.date.today().day - lastUpdate > 1):
        cfgJson["last_download_app_time"] = datetime.date.today().day
        cfgW = open(CONFIG_FILE, 'w')
        json.dump(cfgJson, cfgW)
        cfgW.close()
        return False
    else:
        return True


'''读取已经拉取的产品列表'''
def getProductsContent():
    print "reading %s" % PRODUCT_FILE
    product = open(PRODUCT_FILE, 'r').read();
    productList = product.split('\n')
    return productList


def updateEnable():
    cfgR = open(CONFIG_FILE, "r")
    cfgJson = json.load(cfgR)
    cfgR.close()
    return cfgJson["enable_update"]


def saveLog(contentMap):
    print "save map..."
    logFile = open(CHECK_LOG + Common.getTimeStr() + ".json", 'w')
    json.dump(contentMap, logFile, encoding='UTF-8', ensure_ascii=False)
    logFile.close()

'''
    从json\product\\本地获取产品信息
    :returns 
'''
def getAllKindProductMaps():
    productMaps = {}
    pathdir = PRODUCT_DICT_PATH % Common.getYesterday()
    if os.path.exists(pathdir):
        files = os.listdir(pathdir)
        for productFile in files:
            file = open(os.path.join(pathdir,productFile), 'r')
            # print productFile + " ----" + productFile.split('.')[0]
            productMaps[productFile.split('.')[0]] = json.load(file)
            # break # for test
    print str(productMaps)
    return productMaps

def saveProduct(category, content):
    print "saving..."
    pathdir = PRODUCT_DICT_PATH % Common.getTimeDayStr()
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)
    saveFile = pathdir + str(category) + ".json"
    file = open(saveFile,'w')
    json.dump(content, file)
    # saveStr = "\n".join(str(app) for app in  content)
    # file.writelines(saveStr)
    file.close()
    print "saved"

'''
    获取类别
    :param 应用类别号
    :returns 类别的中文名
'''
def getCategoryName(cagegory_code):
    print "read category->%s"%cagegory_code
    category_map = json.load(open(CATEGORY_FILE, "r"));
    for item in  category_map.items():
        if(str(item[1]) == str(cagegory_code)):
            print "get->" + item[0]
            return str(item[0])
    return "No Category"

if __name__ == '__main__':
    print "FileUtil."
    print getCategoryName(33)
    # products = getAllKindProductMaps()
    # print str(products)
    # aMap = {"asdf": 1, "asdfasdf": False, "asdfasdfaxx": True, "x": "yyyy"}
    # saveLog(aMap)
    # if (updateEnable()):
    #     print "updated"
    # else:
    #     print "no updated"

