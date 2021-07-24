#coding=utf-8
import time
import re
import requests
import datetime
import smtplib


#輸入想要追蹤的網址，可以增加或刪除
site=['https://newhouse.591.com.tw/housing-list.html?rid=5&sids=54&room=2&sort=9', #竹北2房
      'https://newhouse.591.com.tw/housing-list.html?rid=5&sids=54&room=3&sort=9', #竹北3房
      'https://newhouse.591.com.tw/housing-list.html?rid=5&sids=56&room=2&sort=9', #新豐2房
      'https://newhouse.591.com.tw/housing-list.html?rid=5&sids=56&room=3&sort=9', #新豐2房
      'https://www.rakuya.com.tw/nc/result?search=city&city=6&parkings=4&zipcode=302%2C304&sort=21&room=2%7E3', #竹北新豐
      'https://hsinchu.housetube.tw/searchhouse?do=search&cid=314,575,570&price=p00&order=create_time&desc=desc&select1=3&room=2', #新竹竹北新豐2房
      'https://hsinchu.housetube.tw/searchhouse?do=search&cid=314,575,570&price=p00&order=create_time&desc=desc&select1=3&room=3' #新竹竹北新豐2房
     ]

def qingqiu(site):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
                    (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}     #设置headers信息，模拟成浏览器取访问网站
    req = requests.get(site, headers=headers)   #向网站发起请求，并获取响应对象
    content = req.text   #获取网站源码
    pattern = re.compile('.html(.*?)</a>').findall(content)  #正则化匹配字符，根据网站源码设置
    return pattern  #运行qingqiu()函数，会返回pattern的值

def send_email(site):
    HOST = 'gmail.com'   # 网易邮箱smtp
    PORT = '465'
    fajianren = 'tsuna6954@gamil.com'   #发送人邮箱
    shoujianren = 'tsuna6954@gmail.com'   #收件人邮箱
    title = site+' 更新了!'     # 邮件标题
    new_pattern = qingqiu(site)  #提取网页内容列表
    context = new_pattern[0]  # 邮件内容
    smtp = smtplib.SMTP_SSL(HOST, 465)  # 启用SSL发信, 端口一般是465
    res = smtp.login(user='tsuna6954', password='alice319') # 登录验证，password是邮箱授权码而非密码，需要去网易邮箱手动开启
    print('发送结果：', res)
    msg = '\n'.join(
        ['From: {}'.format(fajianren), 'To: {}'.format(shoujianren), 'Subject: {}'.format(title), '', context])
    smtp.sendmail(from_addr=fajianren, to_addrs=shoujianren, msg=msg.encode('utf-8')) # 发送邮件
    print(context)

def update():
    print('通知系統啟動中')
    old_pattern = [''] * 7
    new_pattern = [''] * 7
    for i in range(len(site)):
        old_pattern[i] = qingqiu(site[i])  #记录原始内容列表
        while True:
            new_pattern[i] = qingqiu(site[i])  #记录新内容列表
            if (new_pattern[i]!= old_pattern[i]):  #判断内容列表是否更新
                old_pattern[i]=new_pattern[i]    #原始内容列表改变
                send_email()   #发送邮件
            else:
                now=datetime.datetime.now()
                print(now,"尚无更新")
            time.sleep(86400) # 一天檢查一次
            
update()
