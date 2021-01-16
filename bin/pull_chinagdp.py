
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
fig, ax1 = plt.subplots(figsize=(25,8))
# 设置xaxis的刻度
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


for ax in [ax1]:
        ax.xaxis_date()
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.grid(True)

#################3

df1 = ak.macro_china_gdp_yearly().map(float)

ax1.plot(df1, label="GDP")
# 标注最大、最低、当前gold_volume
latest_bond = df1.iloc[-1]
latest_date = df1.index[-1]
ax1.annotate('最新{:.2f}'.format(latest_bond), xy=(latest_date, latest_bond), xytext=(+10, -10),
             textcoords='offset points', fontsize=12,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"),
            fontproperties=fontprop)
ax1.legend(loc="upper left")
fig.legend(loc="upper left", prop=fontprop, bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)


from datetime import datetime
updated_at = datetime.now().strftime('%Y-%m-%d')
fig.suptitle('中国GDP年率\n公众号：结丹记事本儿,更新于{}'.format(updated_at), fontproperties=fontprop, fontsize=16)
#fig.tight_layout()
#plt.show()
import os
fname = os.path.abspath(os.path.join(dest+'chinamacro.png'))
fig.savefig(fname=fname, dpi=100, quality=50)
