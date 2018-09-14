# -*- coding: UTF-8 -*-
from email.mime.application import MIMEApplication
import datetime
import itchat
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itchat.content import ATTACHMENT

def SendMail(filename,FromUserName,FileSize,CreatTime):
    CreatTime=datetime.datetime.fromtimestamp(CreatTime)
    FileSize=int(FileSize)
    if FileSize>1024**3:
        FileSize=str(FileSize/(1024**3))+'GB'
    elif FileSize>1024**2:
        FileSize=str(FileSize/(1024**2))+'MB'
    elif FileSize>1024:
        FileSize=str(FileSize/(1024))+'KB'
    else:
        FileSize=str(FileSize)+'B'
    sender = '***@163.com'  #
    passWord = '***'
    mail_host = 'smtp.163.com'
    # receivers是邮件接收人，用列表保存，可以添加多个
    receivers = ['****@qq.com']

    # 设置email信息
    msg = MIMEMultipart()
    # 邮件主题
    msg['Subject'] = 'WeChat File'
    # 发送方信息
    msg['From'] = sender
    # 邮件正文是MIMEText:
    msg_content = '已收到微信文件，请马上查看！详情如下：\n发送者：{}\n文件名：{}\n大小：{}\n发送时间：{}\n'.format(FromUserName,filename,FileSize,CreatTime)
    # 简单文本到正文，plain
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
    # # 将附件图片嵌入正文，html
    # msg.attach(MIMEText('<html><body><h1>尽快扫码吧！</h1>' + '<p><img src="cid:0"></p>' + '</body></html>', 'html', 'utf-8'))
    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open(filename,'rb') as f:
        # 设置附件的MIME和文件名，这里是jpg类型,可以换png或其他类型:
        mime = MIMEApplication(f.read())
        # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename=('gbk','',filename))
    # 添加到MIMEMultipart:
    msg.attach(mime)

    # 登录并发送邮件
    try:
        # 163smtp服务器的端口号为465或
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        s.set_debuglevel(1)
        s.login(sender, passWord)
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender, to, msg.as_string())
            # print('Success!')
        s.quit()
        # print("All emails have been sent over!")
    except smtplib.SMTPException as e:
        print("Falied,%s", e)

@itchat.msg_register([ATTACHMENT],isFriendChat=True,isGroupChat=True)
def download_files_and_forward(msg):
    msg.download(msg.fileName)
    SendMail(msg.fileName,itchat.search_friends(userName=msg['FromUserName'])['NickName']+'('+itchat.search_friends(userName=msg['FromUserName'])['RemarkName']+')',msg['FileSize'],msg['CreateTime'])

itchat.auto_login(hotReload=True)
itchat.run()