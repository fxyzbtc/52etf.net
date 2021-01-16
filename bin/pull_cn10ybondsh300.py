import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import akshare as ak
import urllib

import sys
dest = sys.argv[1]

# 设置字体
import matplotlib.font_manager as fm
path = '/usr/share/fonts/truetype/SimHei.ttf'
github_url = 'https://github.com/adobe-fonts/source-han-sans/blob/release/OTF/SimplifiedChinese/SourceHanSansSC-Normal.otf'
url = github_url + '?raw=true'  # You want the actual file, not some html
from tempfile import NamedTemporaryFile
response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()
fontprop = fm.FontProperties(fname=f.name, size=13)

# 设置xaxis的刻度
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')

# 国债数据
df = ak.bond_investing_global(country="中国", index_name="中国10年期国债", period="每月", start_date="1990-01-01", end_date="2020-06-13")
df = df[['收盘']]
df.reset_index(inplace=True)
import matplotlib.dates as mdates
df['日期'] = df['日期'].map(mdates.date2num)

# 初始化fig, axes
fig, ax = plt.subplots(figsize=(25,8))
ax.plot(df['日期'], df['收盘'], label='十年期国债收益率')
ax.xaxis_date()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(months)
ax.xaxis.set_major_formatter(years_fmt)

ax.set_ylabel(ylabel='到期收益率', fontproperties=fontprop)
ax.grid(True)



# 沪深300数据
stock_df = ak.stock_zh_index_daily(symbol="sh000300")
stock_df.reset_index(inplace=True)
stock_df['date'] = stock_df['date'].map(mdates.date2num)
# 初始化fig, axes
ax2 = ax.twinx()
ax2.plot(stock_df['date'], stock_df['close'],
         color='red', alpha=0.8, label='沪深300')
ax2.set_ylabel(ylabel='沪深300', fontproperties=fontprop)


from datetime import datetime
updated_at = datetime.now().strftime('%Y-%m-%d')
fig.suptitle('中国十年期国债收益率 v.s. 沪深300\n公众号：结丹记事本儿,更新于{}'.format(updated_at), fontproperties=fontprop, fontsize=16)
fig.legend(loc="upper left", prop=fontprop, bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)

#fig.tight_layout()
import os
fname = os.path.abspath(dest+'cn10ybondsh300.png')
fig.savefig(fname=fname, dpi=100, quality=50)
