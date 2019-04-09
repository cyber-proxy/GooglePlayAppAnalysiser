# coding=utf-8
# Create by LC
import sys, time

reload(sys)
sys.setdefaultencoding('utf8')


import re,  urllib2, requests,json
from util import FileUtil, Email,Common

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

'''page'''
MAXPAGE = 500

'''category'''
CATEGORY_APPLICATIONS = 11
CATEGORY_TOOLS = 33
categoryList = [CATEGORY_TOOLS, CATEGORY_APPLICATIONS]

'''地址'''
AppAnnieSite = "https://www.appannie.com/apps/google-play/top-chart/?country=US&category=11&device=&date=2019-03-27&feed=Free&rank_sorting_type=rank&page_number=0&page_size=100&table_selections=&metrics=grossing_rank,new_free_rank,category,all_avg,all_count,first_release_date,last_updated_date,est_download,est_revenue,dau&order_type=desc&order_by=free_rank"
# "https://www.appannie.com/apps/google-play/top-chart/?country=US&category=11&device=&date=2019-03-27&feed=All&rank_sorting_type=rank&page_number=0&page_sie=500"
AppAnnieAppAddr = "https://www.appannie.com/ajax/top-chart/table/?market=google-play&country_code=US&category=%s&date=%s&rank_sorting_type=rank&page_size=500&order_type=desc"

'''POST请求头'''
POST_HEADERS = {
    ':authority': 'www.appannie.com',
    ':method': 'POST',
    ':path': '/ajax/top-chart/table/update_metrics',
    ':scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es-ES;q=0.8,es;q=0.7,tr-TR;q=0.6,tr;q=0.5,pt-BR;q=0.4,pt;q=0.3,bez-TZ;q=0.2,bez;q=0.1,fr-FR;q=0.1,fr;q=0.1,de-BE;q=0.1,de;q=0.1,ug-CN;q=0.1,ug;q=0.1,ar-JO;q=0.1,ar;q=0.1,ja-JP;q=0.1,ja;q=0.1,as-IN;q=0.1,as;q=0.1,zh-CN;q=0.1,zh;q=0.1,ko-KR;q=0.1,ko;q=0.1,yo-NG;q=0.1,yo;q=0.1,sr-RS;q=0.1,sr;q=0.1,luo-KE;q=0.1,luo;q=0.1,en-XA;q=0.1,az-AZ;q=0.1,az;q=0.1,bm-ML;q=0.1,bm;q=0.1,yue-HK;q=0.1,yue;q=0.1,id-ID;q=0.1,id;q=0.1,fr-CA;q=0.1',
    'content-length': '459',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'optimizelyEndUserId=oeu1553692578700r0.6751054685689206; csrftoken=OkjUyLjK9dmK5boFO5ZXdvoibZSmVAPc; aa_language=cn; django_language=zh-cn; _gcl_au=1.1.1312902289.1553692597; _ga=GA1.2.71132698.1553692597; _gid=GA1.2.313966484.1553692597; _mkto_trk=id:071-QED-284&token:_mch-appannie.com-1553692597540-52664; rid=dac906e0b3e441849bb86c708b49ed3a; aa_user_token=".eJxrYKotZNQI5SxNLqmIz0gszihkClVIMjSxMLZINE6zSDFLNDVLS0w0NjMxSrVMTktLNTZKTQ0Vik8sLcmILy1OLYpPSkzOTs1LKWQONShPTUrMS8ypLMlMLtZLTE7OL80r0XNOLE71zCtOzSvOLMksS_XNT0nNcYLqYQnlRTIpM6WQ1WtZjyBDqR4A_qY0hA:1h98eM:f_4dRSZ06tEE5FL__8a6odqAE5w"; __adroll_fpc=d1ce82e55cb17caddf3e11cd2060944f-1553693503622; __ar_v4=%7C4IJGT2ZDGJFZLAACNH4TVF%3A20190326%3A1%7CPSAAGT4MFBB2ROIM33X7L2%3A20190326%3A1%7CHIOYWRB44ZGAPB3KUNXVWY%3A20190326%3A1; sessionId=".eJxNjc1Kw0AURtO0WokUrbgRRFzqJoT-mWztSoub4oC74Wbm2g6Nk0zunUoFwZVQ8Dl8Kne-iBSquDt8cM73Fr66xoXoEhKZ0lZYkyFGy2vR2W6SGGqeBGKvADvzMMOHMAgCZUVHgue59IS1NPr286MbiINfCy3kBepJKFpARotzgDTpa-hf9UYw6A2GGWajxzxTKoFUpzAU-1yS9JUGRu3CtTj6l89BLdBqkTxjDhaKFRtFMShVesvxGAhvLKElw2aJd6XG4nprHEKBNUs1R7WQbJ5QbQ42EP2Ba4qo_d08bZydtL-OVbXil0iK-3HkWpdTt_M-dbs-_gFHFGeX:1h9Js9:mho6_Dvmg2Qbt0GQBoBKUDjo0Uk"; _hp2_ses_props.3646280627=%7B%22r%22%3A%22https%3A%2F%2Fwww.appannie.com%2Fapps%2Fgoogle-play%2Ftop-chart%2F%3Fcountry%3DUS%26category%3D1%26device%3D%26date%3D2019-03-27%26feed%3DAll%26rank_sorting_type%3Drank%26page_number%3D0%26page_size%3D100%26table_selections%3D%22%2C%22ts%22%3A1553736639797%2C%22d%22%3A%22www.appannie.com%22%2C%22h%22%3A%22%2Fapps%2Fgoogle-play%2Ftop-chart%2F%22%7D; _gat_UA-2339266-6=1; _hp2_id.3646280627=%7B%22userId%22%3A%227479114902357474%22%2C%22pageviewId%22%3A%227159833395434283%22%2C%22sessionId%22%3A%227774555840726555%22%2C%22identity%22%3A%221150118%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D',
    'dnt': '1',
    'origin': 'https://www.appannie.com',
    'referer': 'https://www.appannie.com/apps/google-play/top-chart/?country=US&category=11&device=&date=2019-04-08&feed=Free&rank_sorting_type=rank&page_number=0&page_size=100&table_selections=&metrics=grossing_rank,new_free_rank,category,all_avg,all_count,first_release_date,last_updated_date,est_download,est_revenue,dau&order_type=desc&order_by=free_rank',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'x-csrftoken': 'OkjUyLjK9dmK5boFO5ZXdvoibZSmVAPc',
    'x-newrelic-id': 'VwcPUFJXGwEBUlJSDgc=',
    'x-requested-with': 'XMLHttpRequest'
}
# https://www.appannie.com/ajax/top-chart/table/?market=google-play&country_code=US&category=1&date=2019-03-28&rank_sorting_type=rank&page_size=100&order_type=desc
# 查找Name: market=google-play&country_code=US&category=1&date=2019-03-28&rank_sorting_type=rank&page_size=100&order_type=desc

'''get请求头'''
GET_HEADERS = {
    'authority': 'www.appannie.com',
    'method': 'GET',
    'path': '/ajax/top-chart/table/?market=google-play&country_code=US&category=17&date=2019-04-08&rank_sorting_type=rank&page_size=500&order_type=desc',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es-ES;q=0.8,es;q=0.7,tr-TR;q=0.6,tr;q=0.5,pt-BR;q=0.4,pt;q=0.3,bez-TZ;q=0.2,bez;q=0.1,fr-FR;q=0.1,fr;q=0.1,de-BE;q=0.1,de;q=0.1,ug-CN;q=0.1,ug;q=0.1,ar-JO;q=0.1,ar;q=0.1,ja-JP;q=0.1,ja;q=0.1,as-IN;q=0.1,as;q=0.1,zh-CN;q=0.1,zh;q=0.1,ko-KR;q=0.1,ko;q=0.1,yo-NG;q=0.1,yo;q=0.1,sr-RS;q=0.1,sr;q=0.1,luo-KE;q=0.1,luo;q=0.1,en-XA;q=0.1,az-AZ;q=0.1,az;q=0.1,bm-ML;q=0.1,bm;q=0.1,yue-HK;q=0.1,yue;q=0.1,id-ID;q=0.1,id;q=0.1,fr-CA;q=0.1',
    'cookie': 'optimizelyEndUserId=oeu1553692578700r0.6751054685689206; csrftoken=OkjUyLjK9dmK5boFO5ZXdvoibZSmVAPc; aa_language=cn; _gcl_au=1.1.1312902289.1553692597; _ga=GA1.2.71132698.1553692597; _mkto_trk=id:071-QED-284&token:_mch-appannie.com-1553692597540-52664; rid=dac906e0b3e441849bb86c708b49ed3a; __adroll_fpc=d1ce82e55cb17caddf3e11cd2060944f-1553693503622; __ar_v4=%7C4IJGT2ZDGJFZLAACNH4TVF%3A20190326%3A1%7CPSAAGT4MFBB2ROIM33X7L2%3A20190326%3A1%7CHIOYWRB44ZGAPB3KUNXVWY%3A20190326%3A1; django_language=zh-cn; _gid=GA1.2.1618420305.1554791025; usbls=1; _hp2_ses_props.3646280627=%7B%22ts%22%3A1554791027922%2C%22d%22%3A%22www.appannie.com%22%2C%22h%22%3A%22%2Faccount%2Flogin%2F%22%7D; sessionId=".eJxNjc1Kw0AURmMaq0aK1o1bl7oJoX8mW-tGi5vigLvhZubaDo2TTO6dSgXBlVDwEVz7Yr6IFKq4O3xwzvcWvrqdc9ElJDKVrbEhQ4yW16Kz3SQxNDwJxH4JduZhhg9hEATKio4Ez3PpCRtp9O3XRzcQR78WWihK1JNQREBGizOALO1r6F_2RjDoDYY55qPHIlcqhUxnMBSHXJH0tQZG7cK1OPmXL0At0GqRPmMBFsoVG0UJKFV5y8kYCG8soSXDZol3lcbyamscQ4kNSzVHtZBsnlBtDjYQ_4FriXjvOzponyatz2tVr_glluJ-HLvoYup236eu7ZMfRNVnhA:1hDkAc:-NetTjQpf_X0WRVJntXUPQ3CCHk"; aa_user_token=".eJxrYKotZNQI5SxNLqmIz0gszihkClVIMjSxMLZINE6zSDFLNDVLS0w0NjMxSrVMTktLNTZKTQ0Vik8sLcmILy1OLYpPSkzOTs1LKWQONShPTUrMS8ypLMlMLtZLTE7OL80r0XNOLE71zCtOzSvOLMksS_XNT0nNcYLqYQnlRTIpM6WQ1WtZjyBDqR4A_qY0hA:1hDkAi:5tK1z-QCPHWgWqMu6AFfHGAvXyY"; _hp2_id.3646280627=%7B%22userId%22%3A%227479114902357474%22%2C%22pageviewId%22%3A%224070205657606859%22%2C%22sessionId%22%3A%223988909577692512%22%2C%22identity%22%3A%221150118%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D',
    'dnt': '1',
    'referer': 'https://www.appannie.com/apps/google-play/top-chart/?country=US&category=17&device=&date=2019-04-08&feed=All&rank_sorting_type=rank&page_number=0&page_size=500&table_selections=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'x-csrftoken': 'OkjUyLjK9dmK5boFO5ZXdvoibZSmVAPc',
    'x-newrelic-id': 'VwcPUFJXGwEBUlJSDgc=',
    'x-requested-with': 'XMLHttpRequest'
}

data = {
    "page": {"market": "google-play", "feed": "Free",
             "metrics": {"category": 'true', "dau": 'true', "grossing_rank": 'true', "all_count": 'true',
                         "new_free_rank": 'true',
                         "last_updated_date": 'true', "est_download": 'true', "first_release_date": 'true',
                         "est_revenue": 'true', "all_avg": 'true'}},
    "column_config": {"category": 'true', "dau": 'true', "grossing_rank": 'true', "all_count": 'true',
                      "new_free_rank": 'true',
                      "last_updated_date": 'true', "est_download": 'true', "first_release_date": 'true',
                      "est_revenue": 'true',
                      "all_avg": 'true'}
}

'''查看每个美国地区前200个应用（每个子类别：工具、游戏等）是否下线'''


def AppAniueScan():
    print "scanining..."


'''登陆appanuie'''


def login():
    print "login..."
    raw_cookies = open("C:\Users\Administrator\PycharmProjects\AppDetectorScheduleTask\cookie").read()
    req = urllib2.Request(AppAnnieAppAddr)
    req.add_header('cookie', raw_cookies)
    req.add_header('User-Agent',
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    resp = urllib2.urlopen(req)
    print (resp.read()).decode('utf-8')


'''请求并解析给定类别的所有app'''
def getAppsAddres(category):
    print "getApps..."
    timeStamp = Common.getYesterday_()#"2019-03-30"#time.strftime("%Y-%m-%d", time.localtime())#
    path = AppAnnieAppAddr%(category,timeStamp)
    print "path->" + path
    GET_HEADERS["path"] = path
    response = requests.get(AppAnnieAppAddr%(category,timeStamp), data=None, headers=GET_HEADERS)
    result =  response.text
    # print result
    resultJson = json.loads(result)
    rowsList = resultJson["table"]['rows']
    # print "result->" + result
    print "code->" + str(response.status_code)
    return rowsList

'''解析出免费的app排名'''
def parseToRankMap(rows_ist):
    print "parse..."
    appRankMap = {}
    pkgCount = 0
    for row in  rows_ist:
        print "url->%s"%row
        try:
            rank = row[0]
            free_app_info =  row[1][0]
            url =  free_app_info['url']
            app_name = free_app_info['name']
            if(pkgCount > 200):
                break
            # "url": "/apps/google-play/app/com.tencent.ig/details/"
            app = re.findall(r"/apps/google-play/app/(.+?)/details/", url)
            if(app):
                pkg_name = app[0]
                pkgCount = pkgCount + 1
                appRankMap[pkg_name] = str(rank) + "," + app_name
                print str(appRankMap)
            else:
                continue
        except Exception:
            print str(Exception)
            continue
    return appRankMap

'''解析app类别'''

'''验证是否下线'''

'''获取app详情'''


def getAppDetail(product):
    facebookAddr = "https://www.appannie.com/apps/google-play/app/%s/details/" % product
    response = requests.get(facebookAddr, headers=GET_HEADERS);
    print response.text
    # req = urllib2.Request(AppAnnieAppAddr, data=None, headers=GET_HEADERS)
    # resp = urllib2.urlopen(req)
    # print (resp.read()).decode('utf-8')

def getProductOnline():
    result = getAppsAddres()
    return parseToRankMap(result)

'''返回产品包名列表'''
def getProductList():
    print "getting product list..."
    dumpAppFromNet()

'''获取免费的应用类别里面所有app及其排名'''
def dumpAppFromNet():
    # Email.sendContent("获取免费的应用类别里面所有app及其排名,开始执行（每2天执行一次）。")
    categoryMap = FileUtil.getJsonObject(FileUtil.CATEGORY_FILE)
    categoryList = categoryMap.values()
    print "category: " + str(categoryList)
    for category in categoryList:
        print "read category->%s" % category
        result = getAppsAddres(category)
        appRankMap = parseToRankMap(result)
        print str(appRankMap)
        FileUtil.saveProduct(category, appRankMap)
        print "wait 5s..."
        time.sleep(5)
    # Email.sendContent("获取免费的应用类别里面所有app及其排名，完成执行。")

'''main'''
if __name__ == '__main__':
    print "main"
    dumpAppFromNet()
    # login()
    # AppAniueScan()
    # for app in appList:
    #     print "check %s ..."%app
    #     if(OnlineDetector.checkProduct(app)):
    #         print "在线"
    #     else:
    #         print "被下线"
    # readJson("");
    # getAppDetail("com.facebook.orca")