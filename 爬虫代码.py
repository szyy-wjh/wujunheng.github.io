# import requests
#
# url = "https://www.w3schools.com/html/horse.mp3"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
# }
# resp = requests.get(url, headers=headers, timeout=15)


# import requests
# szyyurl=''#里面输入网址
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }#伪装成浏览器
# response = requests.get(url=szyyurl,headers=szyyheaders)


# 爬取图片
# import requests
# # from lxml import etree
# szyyurl=''#里面输入网址
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }#伪装成浏览器
# response = requests.get(url=szyyurl,headers=szyyheaders)#里面自定义名称
# with open("","wb") as f:
#     f.write(response.content)


# 爬取小说章节
# import requests
# from lxml import etree
#
# szyyurl=''
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
# date =etree.HTML(response.text)
# biaoti = date.xpath('//h1/text()')
# zw = date.xpath('//div[@id="contrnt"}/text()')
# for hang in zw:
#     print(hang)
#     with open(f'{biaoti[0]}.txt','a',encoding='utf-8') as f:
#         f.write(hang+'\n')


# 批量爬取小说章节
# import requests
# from lxml import etree
# from itertools import count
# import time
#
# szyyurl='https://www.diandingnnn.cc/ddk32515650/'
# szyyheaders = {
#      "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
# date =etree.HTML(response.text)
# urls = date.xpath('//div[@class="listmain"]//dd/a/@href')
# count = 0
# for url in urls [12:22]:
#     new_url = 'https://www.diandingnnn.cc' + url
#     new_response = requests.get(url=new_url,headers=szyyheaders)
#     new_date = etree.HTML(new_response.text)
#     new_biaoti = new_date.xpath('//h1/text()')[0]
#     new_zw = new_date.xpath('//div[@id="content"]/text()')
#
#     with open(f'歌曲/{new_biaoti}.txt', 'a', encoding='utf-8') as f:
#         for hang in new_zw:
#             hang = hang.strip()
#             if hang :
#                 f.write(hang+'\n')
#     count = count + 1
#     print(f'第{count}章下载完毕')
#     time.sleep(2)


#爬取歌曲
# import requests
# import json
# from lxml import etree
#
#
# szyyurl='https://music.taihe.com/v1/song/tracklink?sign=483b2bea7f2d005390e6f9a8ec724f81&appid=16073360&TSID=T10062480746&timestamp=1793016495'
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
#
# qqyy = json.loads(response.text)
# # print(qqyy)
# yymz = (qqyy['data']['title'])  #歌曲名称
# yygq = (qqyy['data']['path'])   #歌曲
# yygc = (qqyy['data']['lyric'])  #歌词
# yytp = (qqyy['data']['pic'])    #歌曲图片
# #----------保存歌曲----------
# response1 = requests.get(yygq)
# with open(f'{yymz}.mp3','wb') as f:
#     f.write(response1.content)
# #----------保存歌词----------
# response2 = requests.get(yygc)
# with open(f'{yymz}.lrc','w',encoding='utf-8') as f:
#     f.write(response2.text)
# #----------保存图片----------
# response3 = requests.get(yygc)
# with open(f'{yymz}.png','wb') as f:
#     f.write(response3.content)


#批量爬取歌曲
# import time
# import requests, json
# from lxml import etree
#
#
# szyyurl='https://www.gequbao.com/s/周杰伦'
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
# tree = etree.HTML(response.text)
# a_tags = tree.xpath("//a[@class='hover-zoom d-block text-decoration-none']")
# for a in a_tags[:2]:
#     detail_url = a.xpath('./@href')[0]
#     detail_url = 'https://www.gequbao.com' + detail_url
#     print(detail_url)
#     music_name = a.xpath('./@title')[0]
#     print(f'开始下载{music_name}...')
#     response1 = requests.get(url=detail_url, headers=szyyheaders)
#     detail_result = response1.text
#     str1 = detail_result.split('\\u0022play_id\\u0022:\\u0022')[1]
#     play_id = str1.split('\\u0022')[0]
#     play_data = {
#         'id': play_id,
#         "purpose": "play"
#     }
#     play_url = 'https://www.gequbao.com/member/common-play-url'
#     play_resp = requests.post(url=play_url, data=play_data, headers=szyyheaders)
#     result = json.loads(play_resp.text)
#     music_url = result['data']['url']
#     print(music_url)
#     dx = requests.get(url=szyyurl, headers=szyyheaders)
#     with open(f'歌曲/{music_name}.mp3', 'wb') as f:
#         f.write(response1.content)
#     print(f'{music_name}下载完成')
#     time.sleep(3)


#另一个爬取歌曲
# import requests
# import json
#
#
# szyyurl='https://music.taihe.com/v1/song/tracklink?sign=483b2bea7f2d005390e6f9a8ec724f81&appid=16073360&TSID=T10062480746&timestamp=1793016495'
# szyyheaders = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 QQBrowser/22.0.7003.400"
# }
# response = requests.get(url=szyyurl,headers=szyyheaders)
#
# qqyy = json.loads(response.text)
# yymz = (qqyy['data']['title'])  #歌曲名称
# yygq = (qqyy['data']['path'])   #歌曲
# yygc = (qqyy['data']['lyric'])  #歌词
# yytp = (qqyy['data']['pic'])    #歌曲图片
# if response.status_code == 200:
#     #----------保存歌曲----------
#     response1 = requests.get(yygq)
#     with open(f'{yymz}.mp3','wb') as f:
#         f.write(response1.content)
#     #----------保存歌词----------
#     response2 = requests.get(yygc)
#     with open(f'{yymz}.lrc','w',encoding='utf-8') as f:
#         f.write(response2.text)
#     #----------保存图片----------
#     response3 = requests.get(yygc)
#     with open(f'{yymz}.png','wb') as f:
#         f.write(response3.content)
#         print(f"{yymz}.mp3,保存成功（{len(response.content)} 字节）")
# else:
#     print(f"请求失败：状态码 {response.status_code}")


# 直接且批量下载图片
# from DrissionPage import ChromiumPage
# from lxml import etree
# import time
#
# page = ChromiumPage()
# page.get("https://www.baidu.com")
# textarea = page.ele("#chat-textarea")
# textarea.input('')
# button = page.ele("#chat-submit-button")
# button.click()
# time.sleep(2)
# inner = page.ele('xpath://div[@id="s_tab_inner"/a[2]').click()
# # for i in range(5):
# #     time.sleep(2)
# #     page.scroll.to_bottom()
# imgs = page.eles('xpath://div[@class="image-m9T9I img-hFPj_"//img')
# for img in imgs:
#     img.save('')


# from DrissionPage import ChromiumPage
# import time
# import b站单视频下载
#
#
# page = ChromiumPage()
# page.get("https://www.bilibili.com")
# time.sleep(2)
# page.ele('xpath://input[@class"‘nav-search-input"]').input('')
# page.ele('xpath://div[@class="nav-search-btn"]').click()
# newPath = page.latest_tab
# time.sleep(2)
# newPath.eles('xpath://div[@class="search-condition-row"]/button')[1].click()
# time.sleep(2)
# videourls = newPath.eles('xpath://div[@class="bili-video-card__wrap"]/a')
# for video in videourls[0,3]:
#     videourl = video.attr('href')
#     print(videourl)
#     videotab = page.new_tab(videourl)
#     time.sleep(2)
#     b站单视频下载.downloadVideo(videotab.html)
#     time.sleep(1)
#     videotab.close()

# 小红书数据爬取
# from DrissionPage import ChromiumPage
# import os,time,csv
#
#
# filename = '大蓝书数据'
# if os.path.exists(filename):
#     pass
# else:
#     os.makedirs(filename)
# sj = input('输入要搜索的数据：')
# page = ChromiumPage()
# page.listen.start("https://so.xiaohongshu.com/api/sns/web/v2/search/notes",method='POST')
# page.get(f"https://www.xiaohongshu.com/search_result?keyword={sj}&source=web_explore_feed")
# time.sleep(3)
# allData = []
# for i in range(20):
#     print(f'滚动的第{i+1}次')
#     page.scroll.to_bottom()
#     time.sleep(1)
#     res = page.listen.wait()
#     result = res.response.body
#     items = result['data']['items']
#     for item in items:
#         try:
#             id = item['id']
#             token = item['xsec_token']
#             title = item['note_card']['display_title']
#             name = item['note_card']['user']['nickname']
#             avatar = item['note_card']['user']['avatar']
#             comment_count = item['note_card']['interact_info']['comment_count']
#             shared_count = item['note_card']['interact_info']['shared_count']
#             liked_count = item['note_card']['interact_info']['liked_count']
#             collected_count = item['note_card']['interact_info']['collected_count']
#             # print(comment_count,shared_count,liked_count,collected_count)
#             allData.append([id, token, title, name, avatar, liked_count,collected_count,comment_count, shared_count])
#         except Exception as e:
#             print('程序报错了，错误的原因是',e)
# # print(allData)
# with open(f'{filename}/大蓝书数据.csv', 'w',newline="", encoding='utf-8-sig') as f:
#     cf = csv.writer(f)
#     cf.writerow(['id','token','标题','名字','头像','喜欢','收藏','评论','分享'])
#     cf.writerows(allData)


# from DrissionPage import ChromiumPage
# import os,time,csv
#
# all_data = []
# szyyword ='爬虫'#szyyword = ['爬虫'，'python开发']
# page = ChromiumPage()
# page.get('https://www.zbj.com/')
# page.ele('.j-header-kw').input(szyyword)
# # page.ele('xpath://input[@class="j-header-kw"]').input('爬虫')
# page.ele('.btn-search').click()
# # page.ele('xpath://input[@class="btn-search"]').click()
# time.sleep(5)
# new_page = page.latest_tab
# new_page.ele('xpath://div[@class="tabs"]/a[3]').click()
# for p in range(1,3):#(1,page_-1)
#     new_page.wait(5)
#     items = new_page.eles('.card-item-single')
#     for item in items:
#         title = item.ele('.task-names').text
#         price = item.ele('.total-money').text
#         classify = item.ele('.depict-refer').text
#         content = item.ele('.contents-text').text
#         try:
#             status = item.ele('xpath:.//span[@class="status-box"]').text
#         except:
#             status = item.ele('xpath:.//span[@class="status-box orange"]').text
#             url = item.ele('xpath:./a/@href')
#             all_data.append([title,status,price,classify,content,url])
#         time.sleep(1)
# page.quit()
# print(all_data)
# with open('猪八戒.csv', 'w',newline="", encoding='utf-8-sig') as f:
#     cf = csv.writer(f)
#     cf.writerow(['标题','状态','价格','需求分类','任务描述','详情链接'])
#     cf.writerows(all_data)
#[ SCT468355Tnp6oBFzapt8ZTNNtujGCk3w1
# sendkey：在 https://sct.ftqq.com/ 登录后获取]