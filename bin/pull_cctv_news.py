import sys
import jiagu
import os.path

KEYS = "纳斯达克 中概股 国债 债券 养老 红利 消费 5G 科技 一带一路 稳健 湾区 消费价格 通信 创业板 证券 新能源 汽车 医药 龙头 金融 人工智能 传媒 国企改革 军工 房地产 半导体 原油".split(' ')
KEYS.extend('航空 海运 交运 保险 公用 农牧 制造 券商 化工 医疗 贸易 安防 建材 房地产 旅游 金属 服务 机械 材料 民航 机场 水泥 水运 汽车 港口 煤炭 物流 环保 电信 电力 电子 石油 船舶 装修 装饰 设备 金属 通讯 酒店 银行 公路'.split(' '))
KEYS.extend('货币 利率 准备金 央行 国债 股市 房地产 房产 贸易战 关税 原油 局势'.split(' '))

#hugo 文章模板
tpl = '''---
title:  {title}
date: {date}
tags: [新闻联播, {keywords}]
draft: false
---

{content}
'''

# 文章保存的相对目录
dest = sys.argv[1]

# 处理时间
from datetime import (datetime, timedelta)
import pytz
china_tz = pytz.timezone("Asia/Shanghai")

try:
    today_str = sys.argv[2]
except IndexError:
    today_str = datetime.now().astimezone(china_tz).isoformat()[:10].replace('-','')
finally:
    updated_str = datetime.now().astimezone(china_tz).isoformat()

#init tushare
import tushare as ts
TOKEN = '2ecdcdc049841ad3c28d13653925f79d41da86fe73dd49f5897f1ec4'
ts.set_token(TOKEN)
pro = ts.pro_api()
news = pro.cctv_news(date=today_str.replace('-',''))


if not news.empty:
    #title 昨日
    title = 'CCTV新闻联播摘要{date}'.format(date=today_str)
    fname = 'xwlb{date}'.format(date=today_str)

    #已更新，退出
    if os.path.exists(dest+fname+'.md'):
        sys.exit(0)

    #content
    import jiagu
    import jieba.analyse
    text = ''.join(news.iloc[:,2].to_list())
    content = '\n\n'.join(jiagu.summarize(text, 10))

    # keywords
    text = ''.join(news.iloc[:,2].to_list())
    #text_keywords = jiagu.keywords(text, 5) # 关键词
    #text_keywords = [x for x in text_keywords if len(x)>=2]
    text_keywords = jieba.analyse.extract_tags(text, topK=3, allowPOS=['n']) # 关键词

    # extend the keywords
    eco_keywords = []
    for k in KEYS:
        if k in content:
            eco_keywords.append(k)

    # 高亮显示关键字，需要hugo默认打开支持html，参考config.yaml
    for k in text_keywords:
        content = content.replace(k, '<span class="keywords_content">'+k+'</span>')

    for k in eco_keywords:
        content = content.replace(k, '<span class="keywords_fund">'+k+'</span>')

    text_keywords.extend(eco_keywords)
    text_keywords = set(text_keywords)
    keywords = ','.join(text_keywords)


    # 更新输出内容
    md = tpl.format(
        title=title,
        date=updated_str,
        keywords=keywords,
        content=content
    )


    open(os.path.abspath(dest+fname+'.md'), 'w', encoding='utf8').write(md)

else:
    print('nothing to update')
