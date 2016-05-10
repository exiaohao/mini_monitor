from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from config import App
import urllib.parse


def send_mail_util(recvs, subject, msg):
    s = SMTP_SSL('smtp.exmail.qq.com', 465)
    s.login(App.send_mail_sender, App.send_mail_sender_passwd)
    message = MIMEText(msg, 'plain', 'utf-8')
    for recv in recvs.split(','):
        # send_msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n{}".format(App.send_mail_sender, recv, subject, msg)
        message['From'] = Header(App.send_mail_sender, 'utf-8')
        message['To'] = Header(recv, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        try:
            print(message.as_string())
            s.sendmail(from_addr=App.send_mail_sender, to_addrs=recv, msg=message.as_string())
        except Exception as ex:
            # print('Error occured @ {}'.format(str(ex)))
            pass

    s.quit()
