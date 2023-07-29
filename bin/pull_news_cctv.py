# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import akshare
import jieba.analyse

LANGUAGE = "chinese"
SENTENCES_COUNT = 3

def summarize_text(text, lange=LANGUAGE, sentences_count=SENTENCES_COUNT):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    return '\r\n'.join([s._text for s in summarizer(parser.document, SENTENCES_COUNT)])



KEYS = "纳斯达克 中概股 国债 债券 养老 红利 消费 5G 科技 一带一路 稳健 湾区 消费价格 通信 创业板 证券 新能源 汽车 医药 金融 人工智能 传媒 房地产 半导体 原油".split(' ')
KEYS.extend('货币 利率 准备金 央行 国债 股市 房地产 房产 贸易战 关税 原油 局势'.split(' '))


def pull_news_cctv(date, keys=KEYS):
    news = akshare.news_cctv(date)

    def _is_key(_str):
        my_keys = jieba.analyse.extract_tags(_str, topK=10, allowPOS=['n'])
        if set(KEYS).intersection(set(my_keys)):
            return True

    news['key'] = news['content'].apply(_is_key)
    news['sum'] = news['content'].apply(summarize_text)
    # _news = news.drop(news[news['key'] == True].index, ax)
    news = news[news['key'] == True]

    if news.sum:
        return (2*'\r\n').join(news['sum'])
    else:
        print('no news is good news')
        


def save_file(fp, tpl, **kwargs):
    with open(fp, 'w', encoding='utf8') as fw:
        fw.write(tpl.format(**kwargs))
        print(f'successfully write file {fp}')


TPL = '''
    file: {fname}
    tags: #新闻联播
    references: https://tv.cctv.com/lm/xwlb/
   
     {content}
    '''
    
if __name__ == '__main__':
    
    
    from zoneinfo import ZoneInfo
    from datetime import datetime
    
    # download today news only
    dt = datetime.today().strftime("%Y%m%d")
    fname = f'{dt}_CCTV.txt'
    
    if news_sum := pull_news_cctv(dt):
        import os
        if not os.path.exists(fname):
            save_file(fname, TPL, fname=fname, content=news_sum)
        
    else:
        print('no news is good news')
    
    