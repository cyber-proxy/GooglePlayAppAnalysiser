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
import time

# 设置smtplib所需的参数
# 下面的发件人，收件人是用于邮件传输的。
smtpserver = 'smtp.163.com'
username = 'tsotumu@163.com'
password = 'Licheng@5*'
sender = 'tsotumu@163.com'
receiver='tsotumu@qq.com'
# 收件人为多个收件人
receiver = ['tsotumu@qq.com']#,"196835241@qq.com", "568935836@qq.com"]

subject = '重要邮件：googleplay产品在线检测报告汇总'
# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
# subject = '中文标题'
subject=Header(subject, 'utf-8').encode()
# 构造邮件对象MIMEMultipart对象
# 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = 'tsotumu@163.com <tsotumu@163.com>'
msg['To'] = 'tsotumu@qq.com.com'
# 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
msg['To'] = ";".join(receiver)
msg['Date']='2019-3-28'

'''附件'''
# text_html = MIMEText(html, 'html', 'utf-8')
# text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
# msg.attach(text_html)


'''构造邮件内容'''
def emailContent(product, extraMsg):
    print ""
    # 构造文字内容
    text = "邮件发送自定时检测任务:\n\t%s未能检测到在线！\nExtra msg:\n%s\n\n\tDon't Reply" % (product, extraMsg)
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

smtp = smtplib.SMTP()

'''登陆'''
def login():
    print "login..."
    smtp.connect('smtp.163.com')
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    # smtp.set_debuglevel(1)
    smtp.login(username, password)

'''发送邮件'''
def send(product, extraMsg):
    print "send..."
    emailContent(product, extraMsg)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    login()
    time.sleep(3)
    send("com.lm.powersecurit")