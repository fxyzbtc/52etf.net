
HELP_KEYWORDS = {
    '输入【关键字】获取信息':'\r\n',
    '【帮助】':'显示菜单\uE301',
    '【python】':'2GB Python教程',
    '【新闻联播】': '阅览每日精华\uE14B',
    '【国债】': '十年国债收益率\uE14A',
    #'全PE': 'A股等权重PE',
    #'全PB': 'A股等权重PB',
    #'输入沪深指数代码': '获取指数PE/PB分位',
}



echos = {

    'help': {
        'type':'TextReply',
        'keyword': '^help|帮助$',
        'content': '\r\n'.join([k+': '+v for k,v in HELP_KEYWORDS.items()]),

    },

    '段永平': {
        'type': 'TextReply',
        'keyword': '^段永平$',
        'description': '网易博客文集',
        'content': '复制这段内容后打开百度网盘手机APP，操作更方便哦 链接： https://pan.baidu.com/s/1NDC9rJyeUXVK92eaC2EmGw 提取码：sliz',
    },


    '指数基金列表': {
        'type': 'TextReply',
        'keyword': '^指数基金列表$',
        'description': '指数基金列表',
        'content': '复制这段内容后打开百度网盘手机App，操作更方便哦 链接:链接：https://pan.baidu.com/s/12rbcTy4JhvuVphM8VxlvDQ  提取码:tdp6',
    },

    '网格品种': {
        'type': 'TextReply',
        'keyword': '^网格品种|网格$',
        'content': '复制这段内容后打开百度网盘手机APP，操作更方便哦 链接： https://pan.baidu.com/s/17wbi0LUMOzU6fJGIXC_v-Q  提取码：2etf',
    },

    'python': {
        'type': 'TextReply',
        'keyword': '^python$',
        'content': '链接:https://pan.baidu.com/s/1xBILhyb0ykACDKJB3FtVmQ 提取码:c54k 复制这段内容后打开百度网盘手机App，操作更方便哦',
    },

    '指数下跌幅度': {
        'type': 'TextReply',
        'keyword': '^指数下跌幅度$',
        'content': '链接: https://pan.baidu.com/s/1d4NJlTEQT4viKjptT1dCcw 提取码: cv9h 复制这段内容后打开百度网盘手机App，操作更方便哦',
    },    

    '国债': {
        'type': 'ArticleReply',
        'keyword': '^国债$',
        'title':  '十年期国债收益率',
        'description': '实时更新',
        'url': 'http://52etf.net/dash/',
        'img': 'http://www.xinhuanet.com/english/2020-01/14/138702456_15789582423401n.jpg',
    },

    '新闻联播': {
        'type': 'ArticleReply',
        'keyword': '^新闻联播$',
        'title': '每日新闻联播',
        'description': '文字摘要精华版',
        'img': 'http://www.xinhuanet.com/video/titlepic/121059/1210599238_1588230029264_title0h.png',
        'url': 'http://52etf.net/tags/%E6%96%B0%E9%97%BB%E8%81%94%E6%92%AD/'
    },

    '猫': {
        'type': 'ArticleReply',
        'keyword': '^cat|猫$',
        'title': '吸猫一时爽',
        'description': '点击图片一直爽',
        'url': 'https://images.pexels.com/photos/33492/cat-red-cute-mackerel.jpg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800',
        'img': 'http://52etf.net/blog/cat/',
    },
    


}
