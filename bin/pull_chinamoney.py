
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


# 初始化fig, axes
fig, [ax1, ax2] = plt.subplots(2,1, figsize=(25,16))
# 设置xaxis的刻度
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


for ax in [ax1, ax2]:
        ax.xaxis_date()
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.grid(True)


def fmtdate(date):
        from datetime import datetime
        import matplotlib.dates as mdates
        dt = datetime.strptime(date, '%Y年%m月份')
        return mdates.date2num(dt)

#################
df1 = ak.macro_china_money_supply()
df1['M2-数量'] = df1['M2-数量'].map(float)
df1['M1-数量'] = df1['M1-数量'].map(float)
df1['M0-数量'] = df1['M0-数量'].map(float)
df1['月份'] = df1['月份'].apply(fmtdate)

ax1.plot(df1['月份'], df1['M2-数量'], label = "M2 亿元")
ax1.plot(df1['月份'], df1['M1-数量'], label = "M1 亿元")
ax1.plot(df1['月份'], df1['M0-数量'], label = "M0 亿元")
ax1.legend(loc="upper left")

df2 = ak.macro_china_m2_yearly()
ax2.plot(df2, label="M2年率")
ax2.legend(loc="upper left")

fig.legend(loc="upper left", prop=fontprop, bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)

from datetime import datetime
updated_at = datetime.now().strftime('%Y-%m-%d')
fig.suptitle('中国宏观货币\n公众号：结丹记事本儿,更新于{}'.format(updated_at), fontproperties=fontprop, fontsize=16)
#fig.tight_layout()
#plt.show()
import os
fname = os.path.abspath(os.path.join(dest+'chinamoney.png'))
fig.savefig(fname=fname, dpi=100, quality=50)
