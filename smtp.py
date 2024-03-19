#!/usr/bin/python3
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
import sys

# parameter setting
sendAddress = sys.argv[1]
password = sys.argv[2]

subject = 'hoge'
bodyText = 'fugafuga'
fromAddress = 'home node'
toAddress = sys.argv[1]

# SMTPサーバに接続
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
smtpobj.starttls()
smtpobj.login(sendAddress, password)

# メール作成
msg = MIMEText(bodyText)
msg['Subject'] = subject
msg['From'] = fromAddress
msg['To'] = toAddress
msg['Date'] = formatdate()

# 作成したメールを送信
smtpobj.send_message(msg)
smtpobj.close()