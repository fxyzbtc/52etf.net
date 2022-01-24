---
title:  "用Python实现折价溢价基金提醒"
date: 2020-03-19T22:18:10+08:00
tags: [python,套利]
---
欢迎转载，转载时请注明公众号：结丹记事本儿
# 摘要
场内外基金套利前，我们需要筛选折溢价率，同时查看交易量、申购赎回状态来确定标的。本文设计了自动化工具，可以每天下午2点提醒折溢价基金，给套利节约大量时间。

# 需求分析
1. 拉取折溢价数据
1. 筛选过滤
1. 邮件提醒

# 实现方式
1. 数据源主要使用集思录和基智网
1. 邮件提醒
1. 基础设施：亚马逊云EC2, SimpleMailService
1. 软件配套：FASTAPI 提供json接口和github pages呈现页面

# 找出第三方数据的接口
访问集思录[实时数据页面](https://www.jisilu.cn/data/etf/#index)，通过Chrome开发者模式，找到列表数据的接口地址 https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___ 

查看接口返回的数据，找到有用的溢价和代码信息![溢价和代码](..\\_static\\images\\Snipaste_2020-03-12_15-43-38.png)。因为集思录数据不包括申购和赎回状态，还要以来另一个数据源fundsmart，数据非常强大，墙裂推荐。

以同样的方法找到接口地址和数据结构如下![基金详情](..\\_static\\images\\Snipaste_2020-03-12_17-44-40.png)

# 筛选有用的信息
我们设计的功能较为单一，只提取必要的信息，另外对应一下中文翻译。

```Python
TICKER_TAGS = ['ticker','name','navPriceRatioFcst', 'navPriceRatio','amplitudes','tradingAmount','application', 'redemption','dependentFundBeans']
TICKER_TAGS_CN = ['代码','名称','折溢价', '昨日折溢价','价差','交易量','申购', '赎回','依赖的基金']
HEADERS = dict(zip(TICKER_TAGS, TICKER_TAGS_CN))
```

在集思录返回数据中，我们只提取折溢价超过6%的标的。

```Python
    resp = s.get(URLS[name])
    j = resp.json()
    arbitrage_list = j['rows']
    arbitrage_list = [item['id'] for item in arbitrage_list if float(item['cell']['discount_rt'].replace('%','')) >=6 or float(item['cell']['discount_rt'].replace('%','')) <=-6]
```

在提取fundsmart数据后，检查是否可赎回，如果溢价（场内价格高），只筛选出可场内申购（按场外净值购入）的品种；如果折价（场外价格高），只筛选出可场内赎回（按场外价格卖出）的品种。![申购赎回状态查询](..\\_static\images\Snipaste_2020-03-12_17-49-39.png)

```Python
        for item in arbitrage_list:
            j = s.get(TICKER_URL.format(id=item)).json()
            if (float(j['navPriceRatioFcst'].replace('%',''))>=6 and j['application'] == "1") or (float(j['navPriceRatioFcst'].replace('%',''))<=-6 and j['redemption'] == "1"):
                rows['list'].append({HEADERS[x]:j[x] for x in HEADERS})
```

# 合并后的代码
```
# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
import requests
import simplejson as json
from requests.adapters import HTTPAdapter
from json2table import convert
from fastapi.responses import HTMLResponse


URLS = {'ETF':'https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___',
        'QDII-T0':'https://www.jisilu.cn/data/qdii/qdii_list/?___jsl=LST___',
        'STOCK':'https://www.jisilu.cn/data/lof/stock_lof_list/?___jsl=LST___',
        'LOF':'https://www.jisilu.cn/data/lof/index_lof_list/?___jsl=LST___',
}

TICKER_URL = 'https://www.fundsmart.com.cn/api/fund.detail.categroy.php?type=basic&ticker={id}'
TICKER_TAGS = ['ticker','name','navPriceRatioFcst', 'navPriceRatio','amplitudes','tradingAmount','application', 'redemption','dependentFundBeans']
TICKER_TAGS_CN = ['代码','名称','折溢价', '昨日折溢价','振幅价差','交易量','申购', '赎回','依赖的基金']
HEADERS = dict(zip(TICKER_TAGS, TICKER_TAGS_CN))

app = FastAPI()
s = requests.Session()
s.verify = False
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

@app.get("/taoli/")
async def root():
    rows={'records':[]}
    for name in URLS:
        
        resp = s.get(URLS[name])
        j = resp.json()
        arbitrage_list = j['rows']
        arbitrage_list = [item['id'] for item in arbitrage_list if float(item['cell']['discount_rt'].replace('%','')) >=6 or float(item['cell']['discount_rt'].replace('%','')) <=-6]
        
        for item in arbitrage_list:
            j = s.get(TICKER_URL.format(id=item)).json()
            if (float(j['navPriceRatioFcst'].replace('%',''))>=6 and j['application'] == "1") or (float(j['navPriceRatioFcst'].replace('%',''))<=-6 and j['redemption'] == "1"):
                rows['records'].append({HEADERS[x]:j[x] for x in HEADERS})

    return rows

```

简单格式化输出页面，![查询结果](..\\_static\images\Snipaste_2020-03-12_18-36-50.png)我们可以很清晰的看到今天共有5个品种有套利机会且开放了申购，下午两点如果折溢价仍然很大，那么就可以执行内外场套利的操作。

# 下一步
我们将使用亚马逊邮件功能实现定时在中午12点和下午2点发送提醒邮件，并部署在亚马逊服务器上。

欢迎点击**阅读原文**试用或者浏览器访问 [http://invest.btcz.im/taoli/](http://invest.btcz.im/taoli/) 页面。

![index](..\static\images\Snipaste_2020-03-18_23-47-23.png)


接上文，我们实现了一个基础页面用于筛选可套利基金，本篇继续介绍如何将服务搬上了亚马逊云，且提供了邮件注册提醒服务，速度和稳定性基本达到商用效果。下一篇介绍如何使用该套利页面。

# 迭代目标
经过一天的试用反馈，结合之前规划，我们共要做以下改进。

1. 将服务部署到亚马逊云可以访问
1. 优化访问速度
1. 添加邮件提醒功能
1. 美化下页面显示

# 如何在亚马逊部署web服务
亚马逊提供一年免费云服务，可以体验使用大多数的计算、存储、数据等资源，作为自己学习和搭建小型站点非常方便。这里只给出大致思路，具体配置方法可以参考官方文档，非常详细和及时。

## 计算资源
想搭建web服务器，亚马逊提供两种方式Elastic Beanstalk(EBS)和Elastic Computing(EC)，前者对平台环境进行了打包，开发者只需要关注自己的web服务程序，适用AWS CLI上传发布即可，开发迅速，版本管理方便。EC则是常见的裸服务器模式，可以自己安装和搭建任意程序，非常灵活（同义词是很坑）。

我们选择EC方式从头搭建
1. 选择Ubuntu镜像
1. 安装配置Nginx服务器
1. 安装配置uwsgi Python进程

## 申请亚马逊RDS关系数据库Postgres
参考提示创建数据库，记录密钥信息，注意权限设置为外网访问，否则会联结不上。Postgres的客户端可以用pgAdmin或者Vscode中的Postgres插件。


## Nginx配置陷阱
Nginx是强大但同样对新手不够友好，其中的路由配置和server进程配置非常的奇葩。下次我会直接用EBS服务器，不需要关注nginx代理，只需要上传web服务程序即可。

1. 不要使用一个server，在location中尝试用rewrite来达到两个测试服务器，配置路由路径规则太过复杂耗时。直接改用两个服务端口对应到不同的测试socket
1. 不要在/etc/nginx/nginx.conf中以引用方式配置server，容易出错且找不到原因（比如一直拉不起8080端口）。
1. 如果设置location的子目录，使用alias不用使用root，否则会在root基础上叠加子目录嵌套
 
```
server {
        listen 80;
        server_name  _;
        # Load configuration files for the default server block.

        location /books/ {
            alias /home/ubuntu/www/books/;
            autoindex on;
        }

        location / {
            include uwsgi_params;
            uwsgi_pass unix:///tmp/invest.sock;
            uwsgi_read_timeout 120s;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            proxy_send_timeout 120s;
            proxy_read_timeout 120s;
        }
        }

server {
        listen 8080;
        server_name  _x;
        # Load configuration files for the default server block.

        location / {
            include uwsgi_params;
            uwsgi_pass unix:///tmp/invest_test.sock;
            uwsgi_read_timeout 120s;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            proxy_send_timeout 120s;
            proxy_read_timeout 120s;
        }

        }


```
## uwsgi配置陷阱

如果遇到no module "encoding"等报错，需要重建venv环境即可解决，或者检查home参数设置错误。
```
rm -r venv
pip3 freeze > requirements.txt
Python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

出现nginx-uwsgi-unavailable-modifier-requested错误，是因为uwsgi依赖Python插件
```
sudo apt-get install uwsgi-plugin-Python3
```

然后再uwsgi.ini配置文件中添加
```
plugins=Python3
```
>注意：引入plugins参数也可能在某些平台导致./uwsgi_plugin_Python3.so找不到的错误。注释掉可以解决。


阅读uwsgi.log看启动日志，能发现Python路径等错误。

尽量使用变量和相对路径配置uwsgi.ini文件，可以在WSL/不同服务器之间迁移，好的配置样例如下，

```
[uwsgi]
#配合nginx使用
project = arbitrage
#http-socket = 127.0.0.1:8080
socket = /tmp/invest.sock
#plugins = Python3
chdir = %d
home = .env/
module = runner:application
#指定工作进程
processes       = 5
#每个工作进程有2个线程
threads = 10
#指的后台启动 日志输出的地方
daemonize       = uwsgi.log
#保存主进程的进程号
pidfile = uwsgi.pid
#虚拟环境环境路径

harakiri = 240 
http-timeout = 240 
socket-timeout = 240 
worker-reload-mercy = 240 
reload-mercy = 240 
mule-reload-mercy = 240

master = 1
```

通过以上配置我们的web服务就上线云端了，可以通过移动端手机和电脑随时访问。



欢迎点击**阅读原文**试用或者浏览器访问 [http://invest.btcz.im/taoli/](http://invest.btcz.im/taoli/) 页面。

![index](..\static\images\Snipaste_2020-03-18_23-47-23.png)


接上文，我们将服务搬上了亚马逊云，然后继续对代码做一些增补和优化。

1. 优化访问速度
1. 添加邮件提醒功能
1. 美化下页面显示


# flask app目录结构优化
后面我们要引入表单来登记邮件提醒功能，同时在写完第一个版本后，我们的flask目录并不够优化，views/models/forms混杂在一起，会给将来代码扩容带来麻烦，所以提早对目录做一些优化。

## app打包
主要是出于import清晰的引用目的，还有将来方便生成pypi包，这是优化后的目录包。
```
.env:虚拟环境目录
app/:主程序目录
    __init__.py:初始化flask和映射views路径
    static/:静态文件
    templates/:模板文件
    app.py:主程序
    views.py:视图路径
    forms.py:表单
    models.py:数据库模型
    utils.py:附加函数
config.py:主程序配置文件
runner.py:web服务调用入口文件
uwsgi.ini:web服务配置文件
```
![目录优化](..\static\images\Snipaste_2020-03-18_23-04-02.png)

主要的调用路径是
```
runner.py -> app.__init__.py -> Flask -> views -> forms+models
```

当app.__init__.py初始化后，app成为一个package，可以被其他文件直接import app，同时views/forms/models互相引用时，相当于引用package内部的module.

如果将来该程序规模进一步扩大，可以将views/forms/models再次分包到blueprint中分prefix各自管理。


## class view来替代def view
通常我们写flask view是类似这样的，
```
@app.route('/taoli/')
def index():
    return 'hi index'

@app.route('/xxx')
def xxx():
    pass

...

```

替代成class会简洁一些，同时在app.__init__中集中注册管理url，非常方便做到plugin形式。（写到这里越看越像Django）
```
# import views
from . import views
app.add_url_rule('/taoli/', view_func=views.TaoLi.as_view('show_taoli'))
app.add_url_rule('/subscribe/', methods=['POST'], view_func=views.Subscribe.as_view('subscribe'))
app.add_url_rule('/api/taoli/', view_func=views.ApiTaoLi.as_view('api_taoli'))
app.add_url_rule('/api/notifyall/', view_func=views.NotifyAll.as_view('api_notifyall'))
```

# 优化访问速度
在之前的/taoli/页面，flask的view页面中需要遍历集思录几个基金列表页面，筛选出及今后再次访问fundsmart接口，耗时非常久，同时由于web服务器性能限制，非常容易导致500 bad gateway错误，服务器挂死。

我们可以尝试将这个接口隐藏起来，只内部访问，获取数据后写入本地文件，其他用户访问这个代理文件接口即可。

只需将原有的/taoli/映射为/xxx/yyy/隐藏起来，并将数据写入本地文件，每分钟刷新一次，因为只有服务器一个访问所以性能瓶颈得以解决。
```
class ApiTaoLi(View):
    def dispatch_request(self):

        result={'records':[]}
        # 过滤集思录数据
        def _fs_filter(j):
            if ('万手' in j['tradingAmount']):
                if (float(j['navPriceRatioFcst'].replace('%',''))>=6 and j['application'] == "1") or \
                (float(j['navPriceRatioFcst'].replace('%',''))<=-6 and j['redemption'] == "1"): # 可申购赎回
                    return True

        def _jsl_filter(item):
            if float(item['cell']['discount_rt'].replace('%','')) >=6 \
            or float(item['cell']['discount_rt'].replace('%','')) <=-6:
                return True

        for name in app.config['URLS']: # 按板块
            jsl = s.get(app.config['URLS'][name]).json()['rows']
            jsl = [item['id'] for item in jsl if _jsl_filter(item)]

            # 提取fundsmart数据
            for item in jsl: # 提取符合集思录溢价条件的标的
                fs = s.get(app.config['TICKER_URL'].format(id=item)).json()

                if _fs_filter(fs):
                    fs = {app.config['HEADERS'][x]:fs[x] for x in app.config['HEADERS']}
                    #dt_string = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    #fs['更新时间'] = dt_string
                    result['records'].append(fs)

        #如果有依赖基金，格式化下
        for index,record in enumerate(result['records']):
            if type(record['关联基金']) == list:
                dep_fund = '<br>'.join([','.join(v.values()) for v in record['关联基金']])
                result['records'][index]['关联基金'] = dep_fund

        #open(url_for('static', filename='taoli.json'),'w').write(json.dumps(result))
        open('taoli.json','w').write(json.dumps(result))
        return result
```        

同时对原油/taoli/简单改写，每次只读取本地缓存的文件。

```
class TaoLi(View):
    def dispatch_request(self):
        result = json.load(open('taoli.json')) or {'records':[]}
        _time = datetime.strptime('14:00', '%H:%M')
        subform = SubscriptionForm(time=_time)
        return render_template('taoli.html', result=result, subform=subform)
```

# 添加邮件提醒
这部分使用flask-mail模块实现，封装了smtplib模块，可以发送text和html类型邮件。

## 配置亚马逊SimpleMailService(SES)
在服务中选择SES菜单，切换到Ire数据中心，配置几个步骤，

1. 开通SES，下载鉴权信息
1. 认证发件人域名，添加一个自己的邮箱验证，验证通过后所有邮件都以此邮箱名义发出
1. 配置时注意使用465+SSL组合，因为TLS组合会有超时和报错现象

Flask config.py典型配置如下，
```
MAIL_SERVER = 'email-smtp.eu-west-1.amazonaws.com'
MAIL_PORT = 465
#MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_DEBUG = DEBUG
MAIL_USERNAME = 'xxx'
MAIL_PASSWORD = 'yyyy'
MAIL_DEFAULT_SENDER = 'foobar@gmail.com'
```

## 表单视图
我们使用flask-wtform模块来管理表单信息，可以方便的管理类型检测和映射到sqlalchemy ORM模型中。主要使用的字段有，

```
from flask_wtf import FlaskForm

from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField
from wtforms.fields import HiddenField
from wtforms.fields import DateTimeField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
from wtforms.validators import Email

class SubscriptionForm(FlaskForm):
    url = HiddenField('数据地址', validators=[DataRequired()])
    email = EmailField('接收邮箱', validators=[Email(), DataRequired()])
    time = TimeField('提醒时间', validators=[DataRequired])
    

```

需要注意的是TimeField，我们的提醒功能只在乎时间，不在乎日期，所以不用DateTime字段。

表单中我们加入添加和删除按钮，为了区分两次post，将他们设置不同的name，post到相同的地址，server这里做一个判断来进行添加还是删除操作。

当然也可以多做一个form+hiddenField隐藏，只暴漏一个提交按钮，然后用DELETE方法来删除，这样做的api会清晰一些。

另外在对model做json序列化输出时，DateTime等类型需要特别处理，可以使用json中的encoder选项来格式化，
```
def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.time):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
flash(json.dumps([r.as_dict() for r in _all], default = alchemyencoder))
```

如果想model直接使用form的表单数据，需要form主动对model进行赋值
```
subform = SubscriptionForm(request.form)
subscription = Subscription()
subform.populate_obj(subscription)
```

## 创建model保存邮箱等信息
为了简化对数据库访问，我们使用flask-sqlalchemy库，提供的ORM映射可以很方便的读写postgres数据库。

```
from app import db
    
class Subscription(db.Model):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.Time(), unique=False, nullable=False)
```

>同样注意time列我们使用Time类型，和wtform表单保持一致，当model改变时，需要重新创建数据库，否则后续sqlalchemy写入会类型不匹配报错。

>这里Time会被sqlalemy映射为postgres的Time without timezone类型，所以wtform表单获取数据后我们要存储的只是一个当地时间值（已经假设是北京时间），比如14:00，服务器实际时间需要转化成北京时间比较。

## 数据读写删除
1. 读:model(request.form).filter(x).filter(y)...按条件筛选
1. 写入:我们允许url+email唯一
1. 删除:按照url+email条件删除

```
                if Subscription.query.filter(Subscription.email == request.form['email']). \
                                        filter(Subscription.url == request.form['url']).all():
                    _all = Subscription.query.filter(Subscription.email == request.form['email']).all()   
                    db.session.add(subscription)
                    db.session.commit()                    
```

```
                record = Subscription.query.filter(Subscription.email == request.form['email']). \
                                            filter(Subscription.url == request.form['url']). \
                                            filter(Subscription.time == request.form['time']).delete()
                db.session.commit()
```

# 邮件提醒
提醒的初衷是避免过度看盘，只在必要时才给予提醒，经过梳理，我们发现只有LOF基金开放、ETF存在联接基金时才给与韭菜足够的空间来操作。否则，其他时候要么资金量需求太大、要么关闭申购无法交易，同时过度盯盘大量消耗时间，且跟套利本身收益严格不成比例。

所以我们设计只有在折溢价超过6个百分点时，基金开放或者有替代ETF联结，发送邮件提醒（如果时QQ邮箱绑定微信后可以收到提醒消息）。

同时我们只需要给出提醒和链接，不需要格式化页面数据，用户只要在终端打开/taoli/网页浏览就可以做下一步判断。
```
class NotifyAll(View):
    def dispatch_request(self):
        '''LOF in name or etfFeeders not --此时可以套利或者降成本操作'''
        
        tz_china = timezone('Asia/Shanghai')
        tz_utc = timezone('UTC')
        utc = datetime.utcnow().replace(tzinfo=tz_utc)
        time_china = utc.astimezone(tz_china)
        time_china = datetime.time(time_china)
        
        
        subscriptions = Subscription.query.filter(Subscription.time <= time_china). \
                                            filter(Subscription.sent_flag != day_today).all()
        subscriptions = Subscription.query.all()
        for sub in subscriptions:
            print(time_china, sub.time)
            addr = sub.email
            subject = 'LOF和联接ETF套利提醒@公众号：结丹记事本儿'
            recipients=[addr]
            sender = 'molartech2020@gmail.com'
            msg = Message(subject,recipients=recipients)
            msg.html = "<b>监控到LOF和ETF联结基金折溢价套利机会，请 <a href={}taoli/>点击这里查看</a>或者浏览器打开 {}taoli/ 查看</b>".format(request.host_url, request.host_url)
            mail.send(msg)
        
        return {'message': 'mails sent'}
```

>需要注意的是这里的时间处理，记得前面postgres设计的是time without timezone格式，而且假定是北京时间，所以当程序运行时需要转为北京时间，而后跟保存的记录比较，如果运行时间大于>提醒时间，则发送邮件。

```
subscriptions = Subscription.query.filter(Subscription.time <= time_china).all()
```

同时设置发送标志位，填入当天日期，发送前检查如果不相等则发送。

# 页面美化
使用boostrap4来格式化前端页面,将其放置到table表和card样式中，由于bs4自带美化的css，所以只要是标准化的标签，显示效果基本能保证。

在提醒时间那里，为了实现默认下午两点提醒，我们对SubscriptionForm实例创建时置值
```
        _time = datetime.strptime('14:00', '%H:%M')
        subform = SubscriptionForm(time=_time)
```
![index](..\static\images\Snipaste_2020-03-18_23-47-23.png)

总结：到目前为止，我们的折溢价提醒服务就基本开发完毕，通过该页面我们能清晰的看到折溢价可套利基金列表，且能随意注册和使用邮件提醒服务。下次我们说明下如何参考这个页面来实现不盯盘省心套利。



# 摘要
本文主要讲解套利原理，操作步骤，还有如何使用我们开发的邮件提醒功能来监控可能的套利机会。

# 结论
场内外套利操作机会少，管理费用成本高，存在价格风险，对小散不友好等不利因素。不值当花费大量精力来去套利。但如果你自己的策略（比如长赢或者网格）中存在LOF品种时，可以通过套利来达到降低成本的目的。广告-> 点击**阅读原文**注册邮件提醒。

# 原理和操作
基本的套利操作可以用下面这一张脑图来说明。风险等在途中用红色图标、炸*丹图标标识了出来。

![套利脑图](..\static\images\基金折溢价套利.png)

如果嫌内容多，可以只看结论部分。绿色高亮部分就是小散比较适合的机会。

![套利脑图结论](..\static\images\套利结论.png)

下面介绍如何订阅邮件自动提醒功能。
# 如何注册自动提醒
## 访问invest.btcz.im/taoli/
![invest home](../static/images/invest-home.png)
## 输入个人信息
![personal mail](../static/images/reg-email1.png)
## 注册
![personal mail reg](../static/images/reg-email2.png)
## 接收邮件
![mail notify sample](../static/images/mailnotify.png)
## 注销邮件
![personal mail unreg](../static/images/reg-email3.png)

>注:由于微信公众号限制，目前无法做到对关注人进行消息提醒。可以在微信内绑定QQ邮箱，这样在收到邮件时微信会提醒，简介达到提醒的目的。

# 下一步
套利第一步是有底仓，如果想提前知道哪些品种可能有较大机会，我们该怎么去找数据？下篇分析。
