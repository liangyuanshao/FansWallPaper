import time

import requests
import re
import os
# 请求头，只需要User-Agent就行

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400'
}
# 获取粉丝数的函数
def get_fans_number():
    # 发起请求
    resp = requests.get("https://blog.csdn.net/qq_45722494/article/list/", headers=headers)
    # resp=requests.get("https://liangyuanshao.blog.csdn.net/article/list/",headers=headers)
    # 通过正则表达式匹配粉丝数，比较简洁
    fans_num=re.search('<span class="count" id="fan">(.*?)</span></dt>',resp.text).group(1)
    return fans_num
    # 输出正确
    # print("粉丝数",fans_num)
import jsonpath
def get_fans_name():
    resp=requests.get("https://blog.csdn.net/community/home-api/v2/get-fans-list?page=1&pageSize=5&id=0&noMore=false&blogUsername=qq_45722494",headers=headers)
    checkurl = "$.data.list[*].nickname"
    # print(resp.json())
    nickname_list=jsonpath.jsonpath(resp.json(),checkurl)
    return nickname_list
    # print(nickname_list) ['BBenjaminn', 'm0_62902789', 'kkk@ynu', 'huitaiter123', '朝朝暮暮635']
import ctypes
def change_wallpaper():
    #获取当前目录绝对路径
    path=os.getcwd()
    # print(path)   D:\Software\PyCharm\Projects\FansWallPaper
    #再加上wallpaper.png就行啦
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path+r"\wallpaper.png", 0)


# get_fans_name()
import H3blogDrow
d = H3blogDrow.H3blogDrow()
config= H3blogDrow.config

last_fans_num=get_fans_number()

while True:
    fans_num=get_fans_number()
    # 如何粉丝数没有变的话，就不进行下面的命令了，直接休息跳过
    if last_fans_num==fans_num:
        time.sleep(10)
        continue
    last_fans_num=fans_num
    nickname_list=get_fans_name()
    config['layers'][0]['text']=f'csdn粉丝数：{fans_num}'
    config['layers'][1]['text']="关注了你\n".join(nickname_list)
    # print(config)
    d.parse_config(config=config)
    img = d.draw()
    img.save('./wallpaper.png')
    change_wallpaper()
    #刷新时间3秒
    time.sleep(3)


