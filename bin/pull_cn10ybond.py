
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


# 标注最大、最低、当前值
max_bond = df['收盘'].max()
min_bond = df['收盘'].min()
latest_bond = df['收盘'].iloc[0]
latest_date = df['日期'].iloc[0]
ax.annotate('最新{:.2f}'.format(latest_bond), xy=(latest_date, latest_bond), xytext=(+10, -10),
             textcoords='offset points', fontsize=12,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"),
            fontproperties=fontprop)
ax.annotate('最高{:.2f}'.format(max_bond), xy=(df['日期'][df['收盘'].idxmax()], max_bond),xytext=(+10, -10),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->'), color='g',fontsize=12,
            fontproperties=fontprop)
ax.annotate('最低{:.2f}'.format(min_bond), xy=(df['日期'][df['收盘'].idxmin()], min_bond),xytext=(+10, -10),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->'), color='r', fontsize=12,
            fontproperties=fontprop)


# 添加20-650-80分位线
mean = df['收盘'].quantile(0.5)
chance = df['收盘'].quantile(0.8)
risk = df['收盘'].quantile(0.2)
ax.axhline(y=mean, color='grey', linestyle='--', label='中位线')
ax.axhline(y=risk, color='red', linestyle='--', label='80分位价值线')
ax.axhline(y=chance, color='green', linestyle='--', label='20分位风险线')
ax.annotate('中位线{:.2f}'.format(mean), xy=(df['日期'].iloc[-1], mean), xytext=(-20, +10),
             textcoords='offset points',
        color='grey', fontsize=12,
        fontproperties=fontprop)
ax.annotate('80分位价值线{:.2f}'.format(chance), xy=(df['日期'].iloc[-1], chance),xytext=(-20, +10),
             textcoords='offset points',
        color='green', fontsize=12,
        fontproperties=fontprop)
ax.annotate('20分位风险线{:.2f}'.format(risk), xy=(df['日期'].iloc[-1], risk),xytext=(-20, +10),
             textcoords='offset points',
        color='r', fontsize=12,
        fontproperties=fontprop)

# 根据分位值来填充图红色（卖出）、绿色（持有）、灰色（中性）
ax.fill_between(df['日期'],0,df['收盘'],facecolor='g', where=df['收盘']>=chance, alpha=0.5, interpolate=True)
ax.fill_between(df['日期'],0,df['收盘'],facecolor='r', where=df['收盘']<=risk, alpha=0.5, interpolate=True)

fig.legend(loc="upper left", prop=fontprop, bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)

ax.set_ylim([2,5.5])
from datetime import datetime
updated_at = datetime.now().strftime('%Y-%m-%d')
fig.suptitle('中国十年期国债收益率\n公众号：结丹记事本儿,更新于{}'.format(updated_at), fontproperties=fontprop, fontsize=16)
#fig.tight_layout()
#plt.show()
import os
fname = os.path.abspath(dest+'cn10ybond.png')
fig.savefig(fname=fname, dpi=100, quality=50)
