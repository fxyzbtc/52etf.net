---
title:  最爱的Python量化库：AkShare
date: 2020-06-14
tags: [量化]
---

先来看介绍,

>[AkShare](https://www.akshare.xyz/zh_CN/latest/introduction.html) 是基于 Python 的财经数据接口库, 目的是实现对股票、期货、期权、基金、外汇、债券、指数、数字货币等金融产品的基本面数据、实时和历史行情数据、衍生数据从数据采集、数据清洗到数据落地的一套工具, 主要用于学术研究目的.

>AkShare 的特点是获取的是相对权威的财经数据网站公布的原始数据, 通过利用原始数据进行各数据源之间的交叉验证, 进而再加工, 从而得出科学的结论.

AkShare是一个非常平民化的财经数据接口库，实时性和准确度没有保证，不能用作量化炒股，但用作延迟研究和大周期决策是没有任何问题的。我们的资产配置、目标市值或者网格可以取其价格来做回测也非常合适。

最重要的，相比tushare或者商业数据源，AkShare完全开源免费，数据采用的是公开网站内容，不存在将来封闭或者不能用的问题。

Akshare支持的接口非常广，文档丰富，完美符合我的预期，

![功能图](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/mindmap/AkShare.svg)


对我们有用的接口主要有

1. 货币汇率，折算QDII价格和摩擦成本
2. 市场波动率
3. 市场利率（货币充裕度）
4. 中美欧经济GPD/CPI/失业率/M2
5. 沪深融资融券（市场热度）
6. 黄金白银ETF持仓监控（市场信心）
7. 中国宏观杠杆率
8. 恐慌指数（极限情况）
9. 基金管理人信息
10. 公募基金数据
11. 债券行情
12. 沪深可转债
13. 中美股票
14. 新增股票账户（市场热度）
15. 指数成分
16. 南北向资金
17. 资金流向
18. 机构持股池

还有大量期货指标数据，对我没什么用就不再列举。

通过以上数据接口，可以搭建所有我们需要的指标，再搭配回测框架（例如vnpy和聚宽）则可以测试策略的有效性。

## 全球债券行情
![20200614112350](https://cdn.jsdelivr.net/gh/leeleilei/leeleilei.github.io/assets/images/20200614112350.png)

除了线图外，使用ax.twinx添加一个副坐标沪深300作为对比图。


```
#%matplotlib inline
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import akshare as ak
import urllib

import matplotlib.font_manager as fm
# 设置字体路径
path = '/usr/share/fonts/truetype/SimHei.ttf'
github_url = 'https://github.com/adobe-fonts/source-han-sans/blob/release/OTF/SimplifiedChinese/SourceHanSansSC-Normal.otf'
url = github_url + '?raw=true'  # You want the actual file, not some html

from tempfile import NamedTemporaryFile

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()
fontprop = fm.FontProperties(fname=f.name, size=13)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


df = ak.bond_investing_global(country="中国", index_name="中国10年期国债", period="每月", start_date="1990-01-01", end_date="2020-06-13")
df = df[['收盘']]
df.reset_index(inplace=True)
import matplotlib.dates as mdates
df['日期'] = df['日期'].map(mdates.date2num)

fig, ax = plt.subplots(figsize=(20,5))

ax.plot(df['日期'], df['收盘'])

ax.xaxis_date()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(months)
ax.xaxis.set_major_formatter(years_fmt)

ax.set_xlabel(xlabel='时间', fontproperties=fontprop)
ax.set_ylabel(ylabel='到期收益率', fontproperties=fontprop)
ax.legend(loc=0)
ax.grid(True)


stock_df = ak.stock_zh_index_daily(symbol="sh000300")
stock_df.reset_index(inplace=True)
stock_df['date'] = stock_df['date'].map(mdates.date2num)

ax2 = ax.twinx()
ax2.plot(stock_df['date'], stock_df['close'],
         color='red')
ax2.set_ylabel(ylabel='沪深300', fontproperties=fontprop)
ax2.legend(loc=0)

fig.suptitle('中国十年期国债收益率 v.s. 沪深300', fontproperties=fontprop, fontsize=16)
plt.show()

```

## 尾声

Akshare能提供资产配置所需的各类非实时数据（历史PEPB除外），接口清晰简单，数据源稳定无需维护和付费。我们再未来将会主要依靠Akshare来搭建我们的指标系统。

