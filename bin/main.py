import re
from werobot.replies import TextReply, ArticlesReply, Article
#nginx docker
#docker run --name 52etf -p 80:80 -v /home/ali/52etf/:/usr/share/nginx/html:ro -v /home/ali/52etf_wexin/:/home/ali/52etf_wexin -d 52etf
#run this within in docker


WELCOME = '''终于等到你\u2764！\r\n我们不为投资，只为更好的认知这个世界\r\n'''

import werobot

robot = werobot.WeRoBot(token='IloVeY0UjEssica1314')

#HELP_KEYWORDS = {
#    '输入【关键字】获取信息':'\r\n',
#    '【帮助】':'显示菜单\uE301',
#
#   '【python】':'2GB Python教程',
#    '【新闻联播】': '阅览每日精华\uE14B',
#    '【国债】': '十年国债收益率\uE14A',
    #'全PE': 'A股等权重PE',
    #'全PB': 'A股等权重PB',
    #'输入沪深指数代码': '获取指数PE/PB分位',
#}

@robot.subscribe
def subscribe(message):
    delimiter = '\uE32E'*10
    return WELCOME + delimiter + '\r\n' + '\r\n'.join([k+': '+v for k,v in HELP_KEYWORDS.items()])

#import re
#@robot.filter(re.compile("帮助"))
#@robot.filter(re.compile("help", re.IGNORECASE))
#def echo(message):
#    return '\r\n'.join([k+': '+v for k,v in HELP_KEYWORDS.items()])


# @robot.filter(re.compile("python", re.IGNORECASE))
# def echo(message):
#     msg='''链接:https://pan.baidu.com/s/1xBILhyb0ykACDKJB3FtVmQ 提取码:c54k 复制这段内容后打开百度网盘手机App，操作更方便哦'''
#     return msg

# @robot.filter(re.compile("段永平", re.IGNORECASE))
# def echo(message):
#     msg='''复制这段内容后打开百度网盘手机APP，操作更方便哦 链接： https://pan.baidu.com/s/1NDC9rJyeUXVK92eaC2EmGw 提取码：sliz'''
#     return msg

# @robot.filter(re.compile("网格品种", re.IGNORECASE))
# def echo(message):
#     msg='''复制这段内容后打开百度网盘手机APP，操作更方便哦 链接： https://pan.baidu.com/s/1HPNiHYzfipq_zBV5sA4ivg 提取码：s65l'''
#     return msg


from datetime import datetime
from werobot.replies import ArticlesReply, Article
import requests


import os
robot.config['HOST'] = '127.0.0.1'
robot.config['PORT'] = 8080
robot.config['APP_ID'] = os.environ['APP_ID']
robot.config['APP_SECRET'] = os.environ['APP_SECRET']
robot.config['ENCODING_AES_KEY'] = os.environ['ENCODING_AES_KEY']
from echos import echos

keywords = ','.join(list(echos.keys()))
msgsuffix = f'\n欢迎使用其他关键字O(∩_∩)O: 【{keywords}】'

@robot.text
def echo(message):
    
    import re
    for k,v in echos.items():
        if re.match(v['keyword'], message.content.strip(), re.IGNORECASE):
            if v['type'] == 'TextReply':
                reply = TextReply(message=message, content=v['content']+msgsuffix)
                return reply
            
            if v['type'] == 'ArticleReply':
                reply = ArticlesReply(message=message)
                article = Article(
                    title = v['title'],
                    description = v['description'],
                    img = v['img'],
                    url = v['url'],
                )
                reply.add_article(article)
                return reply
                

client=robot.client
button = [
    {
        "type":"click",
        "name":"今日歌曲",
        "key":"V1001_TODAY_MUSIC"
    },
    {
        "name":"菜单",
        "sub_button":[
        {
            "type":"view",
            "name":"搜索",
            "url":"http://www.soso.com/"
        },
        {
            "type":"view",
            "name":"视频",
            "url":"http://v.qq.com/"
        },
        {
            "type":"click",
            "name":"赞一下我们",
            "key":"V1001_GOOD"
        }]
    }]

matchrule = {
    "group_id":"2",
    "sex":"1",
    "country":"中国",
    "province":"广东",
    "city":"广州",
    "client_platform_type":"2",
    "language":"zh_CN"
}
#48001 尚未开通权限
#client.create_custom_menu(button, matchrule)

@robot.click
def echo(message):
    if message.key=="V1001_TODAY_MUSIC":
        return "Hello,World!"


robot.run()
