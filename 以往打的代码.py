#安装库 pip install 后面输入要安装的库如requests
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 后面输入要安装的库
# pyecharts是python绘制图表的库
# 需要先安装 pip install pyecharts -i https://mirrors.aliyun.com/pypi/simple/
#200为请求成功 403禁止访问 404网页不存在 500服务器内部错误
# import random
# import time
# ns1=input('请输入男生姓名:')
# ns2=input('请输入女生姓名:')
# yf=random.randint(0,100)
# print(f'{ns1}和{ns2}的缘分指数为{yf}')
# if yf == 100:
#     print('满分缘分')


# name =input('请输入你的名字:')
# name = input('请输入你的名字:')
# if name == '关关':
#     print('检测成功：你是有缘人')


# 写注释
# name = '时之月语'
# age=20
# sj=2
# print('='*20)
# print('     hello world\n')
# print('='*20)
# print(f'     我叫{name}')
# time.sleep(sj)


# for i in range(3):
#     print(f'第{i}次点击提现')


# import  random
#
# count=1
# while True:
#     count += 1
#     result = random.randint(0, 1)
#     print(f'第{count}次查看，结果{result}')
#
#     if  result==1:
#         print(f'提现成功,第{count}次查看时成功')
#         break


# import random
#
# cards=["SSR","SR","R","N"]
# role = random.choice(cards)
#
# print(f'你抽到了：{role}卡')


# import random
#
# name = ['木头','石头','金属','木制品','石器','金属制品','合金制品']
# level={'木头':'R','石头':'S','金属':'SS','木制品':'S','石器':'SS','金属制品':'SSS','合金制品':'SSR'}
# point={'R':'1','S':'2','SS':'3','SSS':'4','SSR':"5"}
#
# role = random.choice(name)
# card = {
#     'name':role,
#     'level':level[role],
#     'point':point[level[role]],
# }
# print(f'名称’：{card["name"]}')
# print(f'卡片稀有度:{card["level"]}')
# print(f'卡片积分：{card["point"]}')


# import random
#
# cards = ['木头','石头','金属','木制品','石器','金属制品','合金制品']
# level={'木头':'这只是一根木头',
#        '石头':'如你所见这是一块石头',
#        '金属':'这是冶炼之后的金属',
#        '木制品':'你已经学会制造木制品',
#        '石器':'石器时代',
#        '金属制品':'金属革命',
#        '合金制品':'工业革命之后的科技爆炸'}
# role = random.choice(cards)
# card = {
#     'name':role,
#     'level':level[role],
# }
# print(f"名称:{card['name']}")
# print(f"描述:{card['level']}")
# result = f"本次抽到的卡片是：{role}\n描述：{level[role]}"
#
# with open('result.txt','w',encoding='utf-8') as f:
#     f.write(result)


# def say_welcome():
#     print('欢迎来到 Python 语法闯关挑战')
# say_welcome()


# def cheer(name):
#     print(f'{name}同学，继续加油闯关！')
# cheer('李雷')


# import random
#
# name=''
# name=input('输入你的姓名:')
# age=''
# age=input('输入你的年龄:')
# xyz= random.randint(1, 100)
# print(f'角色姓名{name}')
# print(f'角色年龄{age}')
# print(f'幸运值{xyz}')
# print(f'幸运值的数据类型{type(xyz)}')


# name=''
# name=input('输入你的姓名:')
# if name=='勇者':
#     print('隐藏身份已解锁')
# else:
#     print(name)


# import random
# events=['体力耗尽','你不知道你在干什么所以你发了一下午的呆','努力学习']
#
# for day in range(1,4):
#
#     event = random.choice(events)
#     print(f'第{day}天：{event}')
#     if event==('体力耗尽'):
#         print('体力耗尽,模拟提前结束，')
#         break


# import requests
#
# szyyurl='https://www.baidu.com'
# response = requests.get(url=szyyurl,)
# print(response.status_code)


# import requests
#
# szyyurl='https://www.baidu.com'
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
# print(response.status_code)


# with open('test.txt','w',encoding='utf-8') as f:
#     f.write('Hello World,你好，世界')


# urls = ['链接1','链接2','链接3']
# print(urls)


# urls = ['链接1','链接2','链接3']
# for url in urls:
#     print(url)


# urls = [' 链接 1',' 链接 2',' 链接 3']
# with open ('链接.txt','a',encoding='utf-8') as f:
#     for url in urls:
#         f.write (url+'\n')


# fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜", "芒果"]
# print(fruits[:3])
# print(fruits[2:5])
# print(fruits[4:6])


# import random
# mbje = 100
# ljq = 0
# jsq = 0
# zdcjs = 50
# while jsq < zdcjs:
#     jsq += 1
#     sjje = round(random.uniform(0.1,10),1)
#     ljq += sjje
#     print(f'第{jsq}次增加{sjje}元，累计金额{ljq:.1f}元')
#
#
#     if ljq >= mbje:
#         print(f"提现成功！共抽了 {jsq} 次，累计金额 {ljq:.1f} 元")
#         break
# else:
#     print(f"未成功：抽满 {zdcjs} 次仍未达到 {mbje} 元，当前累计 {ljq:.1f} 元")


# import json
#
#
# data= '{"name": "张三", "age": 18}'
# zh = json.loads(data)
# print(zh["name"])


# import requests
#
# urls = ["http://music1.mp3", "http://music2.mp3"]
# for url in urls:
#     response = requests.get(url)
#     wjm= url.split('/')[-1]
#     with open(wjm, 'wb') as f:
#         f.write(response.content)
#     print(f'{wjm}下载完成')


# music_list = [
#    {"name": "歌曲1", "url": "http://1.mp3"},
#    {"name": "歌曲2", "url": "http://2.mp3"}
# ]
# for music in music_list:
#     print(music["name"])


# import requests
#
#
# szyyurl=' http://video.com/movie.mp4'
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
# with open('movie.mp4','wb') as f:
#     f.write(response.content)


# import os
#
#
# names = ["流行音乐", "古典音乐", "摇滚音乐"]
# os.makedirs('music')
# for name in names:
#     os.makedirs(f'music/ {name}')


# import os                                           import os
# import requests                                     import requests
#
#
# videos = [                                          videos = [
#     {"name": "流行音乐", "url": "https://1.mp4"},     {"name": "video1", "url": "http://1.mp4"},
#     {"name": "古典音乐", "url": "https://2.mp4"},     {"name": "video2", "url": "http://2.mp4"}
#     {"name": "摇滚音乐", "url": "https://3.mp4"}      ]
# ]
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# if not os.path.exists("videos"):                     if not os.path.exists("videos"):
#     os.mkdir("videos")                                   os.makedirs("videos")
# for video in videos:                                 for v in videos:
#     name = video["name"]                                 resp = requests.get(v["url"])
#     url = video["url"]                                   with open(f"videos/{v['name']}.mp4", "wb") as f:
#     resp = requests.get(url, headers=szyyheaders)        f.write(resp.content)
#     path = os.path.join("videos", f"{name}.mp4")         print(f"下载完成: {v['name']}")
#     with open(path,'wb') as f:
#         f.write(resp.content)


# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get("https://www.baidu.com")
# textarea = page.ele("#chat-textarea")
# textarea.input('张杰')
# button = page.ele("#chat-submit-button")
# button.click()
# first = page.ele("css:.result-op h3 a", timeout=10)
# print("第一个结果的标题:", first.text)
# print("第一个结果的链接:", first.link)
# page.quit()


# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get("https://www.baidu.com")
# textarea = page.ele("#chat-textarea")
# textarea.input('张杰')
# button = page.ele("#chat-submit-button")
# button.click()
# first = page.ele("css:.result-op h3 a", timeout=10)
# first.click()
# new_tab = page.latest_tab


# data = {
#     "note_id": "xxxxxxxxxx",
#     "note_card": {
#         "title": "xxxxxxxxxxxxxx",
#         "user": {
#             "nickname": "xxx"
#         }
#     }
# }
# note_id = data.get("note_id", "未知")
# title = data.get("note_card", {}).get("title", "未知")
# nickname = data.get("note_card", {}).get("user", {}).get("nickname", "未知")
# print(f"帖子ID：{note_id} | 标题：{title} | 作者：{nickname}")


# import csv
#
# data = ['帖子ID','标题','作者昵称'],['id','标题','不知道']
# with open('test.csv', 'w',newline="", encoding='utf-8-sig') as f:
#     cf = csv.writer(f)
#     cf.writerows(data)


# collect_data = []
# for i in range(5):
#     post_id = input(f"输入第 {i + 1} 条帖子ID（直接回车跳过）：").strip()
#     if post_id != "" and post_id not in collect_data:
#         collect_data.append(post_id)
# print(f"\n有效帖子ID数量：{len(collect_data)}")
# print(f"完整列表：{collect_data}")


# products = [
#    {"name": "商品A", "price": 800},
#    {"name": "商品B", "price": 1500}
# ]
# result = []
# for product in products:
#     if product["price"] > 1000:
#         result.append(product)
# print(result)


# numbers = [1, 2, 3, 4, 5, 6]
# evens = []
# for number in numbers:
#     if number % 2 == 0:
#         evens.append(number)
# print(evens)


# numbers = [10, 60, 30, 80, 20]
# result = []
# for number in numbers:
#     if number > 50:
#         result.append(number)
# print(result)

#
# from DrissionPage import ChromiumPage
# from serverchan_sdk import sc_send
# import time
#
# page = ChromiumPage()
# qwjg = 4500
# url ='https://item.jd.com/100359969926.html'
# sj = 60
# page.get(url)
# rounds = 0
# try:
#     while True:
#         rounds += 1
#         page.wait(3)
#         try:
#             if 'item.jd.com' not in page.url:
#                 page.get(url)
#             title = page.ele('.sku-title-name').text
#             title = title[:15]
#             price = page.ele('.product-price--value').text
#             print(f'你关注的{title}的价格是{price}')
#             if price is None:
#                 print(f'第 {rounds} 轮：这次没取到价格，跳过')
#             else:
#                 print(f'第 {rounds} 轮：{title} 当前价 {price} 元')
#             if float(price) < qwjg:
#                 print("价格低于理想价格，立即购买")
#                 sc_send(
#                         "SCT382432TAFggbULHnql1ToaCuqAaoWab",
#                         f"你关注的{title}已降价",
#                         f"点击立即购买{url}"
#                 )
#             else:
#                 print("价格高于理想价格，暂不购买")
#         except Exception as e:
#             print(f'第 {rounds} 轮程序报错，错误的原因是',e)
#         time.sleep(sj)
# except KeyboardInterrupt:
#     print('\n收到 Ctrl+C，停止监听')
# finally:
#     page.quit()


# import requests
# from lxml import etree
#
# url='https://book.douban.com/top250?start=0'
# szyyheaders = {
#      "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# page  = requests.get(url,headers=szyyheaders)
# html = etree.HTML(page.text)
# title = html.xpath('//div[@class="pl2"]/a')
# dysm = title[0].text.strip()
# print(dysm)


# url_list = []
# for i in range(5):
#     sz = i * 25
#     url = f'https://book.douban.com/top250?start={sz}'
#     url_list.append(url)
# for page_num, u in enumerate(url_list, start=1):
#     print(f'第{page_num}页：{u}')


# import requests,time
# from lxml import etree
#
# szyyheaders = {
#      "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# url_list = []
# for i in range(10):
#     url_list.append(f'https://book.douban.com/top250?start={i * 25}')
# print(f'共生成 {len(url_list)} 页 URL')
# start_time = time.time()
# for ys, url in enumerate(url_list, start=1):
#     try:
#         page  = requests.get(url,headers=szyyheaders)
#         html = etree.HTML(page.text)
#         title = html.xpath('//div[@class="pl2"]/a')
#         zzxq = html.xpath('//p[@class="pl"]')
#         sjxq = html.xpath('//span[@class="inq"]')
#         sm = title[0].text.strip()
#         parts = [x.strip() for x in zzxq[0].text.strip().split('/')]
#         zz = parts[0] if parts else '未知'
#         jg = parts[-1] if parts else '未知'
#         smxx = sjxq[0].text.strip() if sjxq and sjxq[0].text else '无短评'
#         print(f'第{ys}页 第一本：{sm} | 作者：{zz} | 价格：{jg} | 书籍信息:{sjxq}')
#     except Exception as e:
#         print(f'第{ys}页出错：{type(e).__name__} {e}')
#         time.sleep(1)
# elapsed = time.time() - start_time
# print(f'\n总耗时：{elapsed:.2f} 秒')


# import jsonpath
#
# data = {
#    "products": [
#        {"name": "手机", "price": 1000},
#        {"name": "电脑", "price": 5000}
#    ]
# }
# print(jsonpath.jsonpath(data,'$..name'))

# import requests
#
# params = {'keyword':'手机'
# ,'page':1
# ,'size':10
# }
# url = ' https://api.example.com/search'
# josni =  requests.get(url, params=params)
# print(josni.josn())

# import requests,time
#
# params = {'keyword':'手机','page':1,'size':10}
# url = ' https://api.example.com/search'
#
#
#
# def fetch_data(url,params,max_retry=3):
#     for i in range(1,max_retry+1):
#         try:
#             resp = requests.get(url, params=params)
#             if resp.status_code == 200:
#                 print(f'第 {i} 次请求成功')
#                 return resp.json()
#             else:
#                 print(f'第 {i} 次失败：状态码 {resp.status_code}')
#         except requests.exceptions.RequestException as e:
#             print(f'第 {i} 次异常：{type(e).__name__} {e}')
#         if i < max_retry:
#             print('等待 2 秒后重试...')
#             time.sleep(2)
#     return None
# data = fetch_data(url, params, max_retry=3)
# if data is not None:
#     print('采集成功，返回数据：')
#     print(data)
# else:
#     print('采集失败：重试 3 次仍未成功'


# import requests
# import time
#
# def fetch_data(url, max_retry=3):
#    for i in range(max_retry):
#        try:
#            resp = requests.get(url, timeout=10)
#            if resp.status_code == 200:
#                return resp.json()
#        except Exception as e:
#            print(f"第{i+1}次尝试失败: {e}")
#            time.sleep(2)
#    return None
#
# data = fetch_data("https://api.example.com/data")
# if data:
#    print("采集成功")
# else:
#    print("采集失败")


# import pandas as pd
#
# df = pd.read_csv('scores.csv')
# print(df.head())


# import pandas as pd
#
# data = {
#     '姓名': ['一', '二', '三', '四', '五'],
#     '学习时长': [2.5, None, 1.8, None, 3.2],
#     '打卡次数': [3, 2, None, 4, 5],
# }
# df = pd.DataFrame(data)
# print(df)
# print(df.isnull().sum())
# df_drop = df.dropna()
# print('\n dropna()')
# print(df_drop)


# from pyecharts.charts import Line
#
# line = Line()
# x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# y_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# line.add_xaxis(xaxis_data=x_data)
# line.add_yaxis('折线图',y_data ,is_smooth=True)
# line.render('折线图.html')


# from pyecharts.charts import WordCloud
# from pyecharts import options as opts
# import pandas
#
# pd = pandas.read_excel('各院校历年数据采集.xlsx')
# word = WordCloud()
# yxmc =pd['学校']
# jhzsrs =pd['招生人数']
# data_pair = [(name, int(num)) for name, num in zip(yxmc, jhzsrs)]
# word.add(
#     series_name='招生人数',
#     data_pair=data_pair,
#     word_size_range=[20, 80],
#     textstyle_opts=opts.TextStyleOpts(font_family='Microsoft YaHei'),
# )
# word.render('词云图.html')
# print('已生成 词云图.html，共', len(data_pair), '所学校')


# from pyecharts.charts import Line
#
# city_names = ['北京','上海','广州','深圳','杭州']
# population = [2189,2487,1868,1756,1193]
# list = Line
# list.add_xaxis(city_names)
# list.add_yaxis('人口',population)
# list.render('城市人口数据折线图.html')


# from pyecharts.charts import Bar
# from pyecharts import options
#
# city_names = ['北京','上海','广州','深圳','杭州']
# population = [2189,2487,1868,1756,1193]
# bar = Bar
# bar.add_xaxis(city_names)
# bar.add_yaxis('常住人口',population)
# bar.render('城市人口柱状图.html'


# from pyecharts.charts import Line,Pie
# from pyecharts import options as opts
#
# city_names = ['北京','上海','广州','深圳','杭州']
# population = [2189,2487,1868,1756,1193]
# date = list(zip(city_names, population))
# pie = Pie()
#
# pie.add( series_name='人口占比',
#     data_pair=date,
#     radius=['35%', '65%'],
# )
# pie.set_series_opts(
#     label_opts=opts.LabelOpts(
#         formatter='{b}: {c}万人 ({d}%)',
#         position='outside',
#     )
# )
# pie.set_global_opts(
#     title_opts=opts.TitleOpts(title='五大城市人口占比', subtitle='单位：万人'),
#     legend_opts=opts.LegendOpts(orient='vertical', pos_left='left', pos_top='middle'),
# )
# pie.render('城市人口饼图.html')


