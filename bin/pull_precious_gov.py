
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import akshare as ak
import urllib
import requests
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
fig, ax1 = plt.subplots(figsize=(16,8))

#####################
# 世界央行黄金持仓数据
url = 'https://fsapi.gold.org/api/v11/charts/reservestats/37?countries[]=WW&from=0&to=0'
y = requests.get(url).json()['chartData']['Series']['Tonnage'][0]['data']
x = requests.get(url).json()['chartData']['selectedCategories']

ax1.plot(x, y, label="全球央行黄金实物持仓")
ax1.set_ylabel(ylabel='持仓量(吨)', fontproperties=fontprop)

for tick in ax1.get_xticklabels():
        tick.set_rotation(90)
        tick.set_visible(False)
for tick in ax1.get_xticklabels()[::10]:
         tick.set_visible(True)


latest_bond = y[-1]
latest_date = x[-1]
ax1.annotate('最新{:.2f}'.format(latest_bond), xy=(latest_date, latest_bond), xytext=(+10, -10),
             textcoords='offset points', fontsize=12,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"),
            fontproperties=fontprop)
ax1.legend(loc="upper left")

fig.legend(loc="upper left", prop=fontprop, bbox_to_anchor=(0,1))

from datetime import datetime
updated_at = datetime.now().strftime('%Y-%m-%d')
fig.suptitle('全球央行黄金持仓报告\n公众号：结丹记事本儿,更新于{}'.format(updated_at), fontproperties=fontprop, fontsize=16)
fig.tight_layout()
#plt.show()
import os
fname = os.path.abspath(os.path.join(dest+'globalgovgold.png'))
fig.savefig(fname=fname, dpi=100, quality=50)
