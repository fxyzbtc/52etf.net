'''
从pocket下载我的收藏夹信息里面标记为52etf的书签，并写入到52etf仓库文件中。
hugo模板将这些文件渲染成页面item呈现出来，效果是reddit的列表样式，并且可以进入讨论。

'''
import requests as req
import sys
import os
import jiagu
import jieba.analyse
import html2text

try:
    dest = sys.argv[1]
except IndexError:
    dest = 'content/bookmarks/'

tpl_posts = '''---
title:  {title}
itemurl: {url}
date: {date}
tags: [{tags}]
draft: false
---
'''

# 处理时间
from datetime import (datetime, timedelta)
import pytz
china_tz = pytz.timezone("Asia/Shanghai")
today = datetime.now().astimezone(china_tz).isoformat()


# pocket 请求头
# count=20, run this every 30 minutes, so 20 is fair enough to capture all udpate


params = {
            'access_token': '04bb4c80-b441-5012-8e75-c397af',
            'consumer_key': '92001-aec2193a4a3516efe355ebfb',
            'tag': '52etf',}

# 请求地址
bookmarks_url = "https://getpocket.com/v3/get"
result = req.post(bookmarks_url, params= params)
urls = result.json()['list']

for k, item in urls.items():
    tags = '[]'
    title = item['resolved_title'] or item['given_title']
    url = item['given_url'] or item['given_url']
    fname = os.path.abspath(os.path.join(dest, k+'.md'))

    import os
    if title and (not os.path.exists(fname)):
        # html = req.get(url).text
        # #md = tomd.convert(html)
        # h = html2text.HTML2Text()
        # h.ignore_links = True
        # text = h.handle(html)
        # try:
        #     summary = '\n\n'.join(jiagu.summarize(text, 10))
        # except IndexError: #英文文档？用回excerpt
        #     summary = item['excerpt']
        
        if len(title) >= 6:
            tags = ','.join(jieba.analyse.extract_tags(title, topK=3, allowPOS=['n']))

        content = tpl_posts.format(
            title=title,
            url = url,
            #summary = summary,
            date = today,
            tags = tags,
        )

        open(fname, 'w', encoding='utf8').write(content)
        print('已保存:{}'.format(title))


#### below code is so ugly and I don't want to look at it again
#
tpl_blog = '''---
title:  {title}
itemurl: {url}
date: {date}
tags: [{tags}]
draft: false
---
'''
params = {
            'access_token': '04bb4c80-b441-5012-8e75-c397af',
            'consumer_key': '92001-aec2193a4a3516efe355ebfb',
            'tag': 'blog',}

dest = 'content/blog/'
# 请求地址
bookmarks_url = "https://getpocket.com/v3/get"
result = req.post(bookmarks_url, params= params)
urls = result.json()['list']

for k, item in urls.items():
    tags = '[]'
    title = item['resolved_title'] or item['given_title']
    url = item['given_url'] or item['given_url']
    fname = os.path.abspath(os.path.join(dest, k+'.md'))

    import os
    if title and (not os.path.exists(fname)):
        if len(title) >= 6:
            tags = ','.join(jieba.analyse.extract_tags(title, topK=3, allowPOS=['n']))

        content = tpl_blog.format(
            title=title,
            url = url,
            date = today,
            tags = tags,
        )

        open(fname, 'w', encoding='utf8').write(content)
        print('已保存:{}'.format(title))