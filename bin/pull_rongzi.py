
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
years_fmt = mdates.DateFormatter('%Y%m')


#################
import pandas as pd
fig, [ax1, ax2] = plt.subplots(2,1, figsize=(25,16))
for ax in [ax1, ax2]:
        ax.xaxis_date()
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.grid(True)


df1 = ak.macro_china_market_margin_sz()
df1.index = pd.to_datetime(df1.index)
ax1.plot(df1.index, df1['融资融券余额'].apply(lambda x: float(x)), label="深圳余额(元)")
ax1.legend(loc="upper left")

df2 = ak.macro_china_market_margin_sh()
df2.index = pd.to_datetime(df2.index)
ax2.plot(df2.index, df2['融资融券余额(元)'].apply(lambda x: float(x)), label="上海余额(元)")
ax2.legend(loc="upper left")

fig.legend(loc="upper left", prop=fontprop, bbox_to_anchor=(0,1))

from datetime import datetime
updated_at = datetime.now().strftime('%Y-%m-%d')
fig.suptitle('沪深两市融资融券余额报告\n公众号：结丹记事本儿,更新于{}'.format(updated_at), fontproperties=fontprop, fontsize=16)
#fig.tight_layout()
#plt.show()
import os
fname = os.path.abspath(os.path.join(dest+'rongzi.png'))
fig.savefig(fname=fname, dpi=100, quality=50)
