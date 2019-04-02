# coding: utf-8
# Create by LC
import sys

reload(sys)
sys.setdefaultencoding('utf8')


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import threading
import time,json

'''
    设置smtplib所需的参数
'''
smtpserver = "smtp.exmail.qq.com"#'smtp.163.com'
username = "fushikang@security4defender.club"#'tsotumu@163.com'
password = "PS2.com"#'Licheng@5*'
sender = 'fushikang@security4defender.club'
receiver = ['tsotumu@qq.com', '196835241@qq.com', '568935836@qq.com']
subject = '重要邮件：googleplay产品在线检测报告汇总'
# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
# subject = '中文标题'
subject=Header(subject, 'utf-8').encode()
# 构造邮件对象MIMEMultipart对象
# 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
msg = None
smtp = smtplib.SMTP()

'''构造邮件内容'''
def emailContent(text):
    print "text->" + text
    global msg
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = 'Windows 定时任务'
    msg['To'] = 'tsotumu@qq.com.com'
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receiver)
    msg['Date'] = '2019-3-28'

'''登陆'''
def login():
    print "login..."
    smtp.connect(smtpserver)#'smtp.163.com')
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    # smtp.set_debuglevel(1)
    smtp.login(username, password)

'''发送邮件'''
def sendTaskResult(productMsg):
    print "send..."
    print unicode(productMsg, encoding="utf-8")
    try:
        text = "（邮件发送自定时检测任务）\n未能检测到在线的信息如下：\n\n%s\n\n\tDon't Reply." % (productMsg)
        emailContent(text)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(Exception) + "\n" + str(e)

'''登陆和发送'''
def loginAndSend(content):
    print "login and send"
    content = str(json.dumps(content, encoding="UTF-8", ensure_ascii=False))
    print content
    try:
        login()
        time.sleep(2)
        # json.
        sendTaskResult(content)
    except Exception, e:
        print str(Exception) + "\n" + str(e)

'''发送任务开始提醒邮件'''
def sendTaskStart():
    print "sendTaskStart"
    try:
        login()
        time.sleep(2)
        text = "（邮件发送自定时检测任务）\n在线检测开始执行，1h左右会收到邮件通知检测结果\n\n\n\tDon't Reply."
        emailContent(text)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(Exception) + "\n" + str(e)


'''发送自定义内容'''
def sendContent(content):
    print "sendTaskStart"
    try:
        login()
        time.sleep(2)
        text = "（邮件发送自定时检测任务）\n%s\n\n\n\tDon't Reply."%content
        emailContent(text)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(Exception) + "\n" + str(e)

if __name__ == '__main__':
    login()
    time.sleep(3)
    sendTaskResult("com.lm.powersecurit xxxxx")