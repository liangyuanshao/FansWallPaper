最近csdn偶尔就又有几个同学关注我，觉得很有动力！于是我想能在任何时候的桌面壁纸，都能看到csdn粉丝数以及显示他们的昵称，我觉得会很有意义！


视频展示地址：[http://www.liangyuanshao.top/s/MZdzk7ojY7TmfeA](http://www.liangyuanshao.top/s/MZdzk7ojY7TmfeA)


分为如下几步

### 一，爬取csdn粉丝数和粉丝昵称

#### 爬粉丝数

首先和粉丝数目有关的请求，**qq_45722494是csdn的用户名**

```python
https://blog.csdn.net/qq_45722494/article/list/
```

![image-20221216205000585](http://1.12.68.28/s/4bNJASqkJNywWe7/preview)

发现了粉丝数目是直接镶嵌到html里面的，直接用get方式拿到

```python
# 请求头，只需要User-Agent就行
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400'
}
# 获取粉丝数的函数
def get_fans_number():
    # 发起请求
    resp=requests.get("https://blog.csdn.net/qq_45722494/article/list/",headers=headers)
    # resp=requests.get("https://liangyuanshao.blog.csdn.net/article/list/",headers=headers)
    # 通过正则表达式匹配粉丝数，比较简洁
    fans_num=re.search('<span class="count" id="fan">(.*?)</span></dt>',resp.text).group(1)
    # 输出正确
    print("粉丝数",fans_num)
    return fans_num
```

输出正确

#### 爬粉丝昵称（最新前五个）

粉丝信息通过这个接口来获取，pageSize我只弄了5个，按照自己的需求来

```python
https://blog.csdn.net/community/home-api/v2/get-fans-list?page=1&pageSize=5&id=0&noMore=false&blogUsername=qq_45722494
```

需要从下面的json里面提取信息

```json
{'code': 200, 'message': 'success', 'traceId': '24c12f9b-3075-4d68-adad-b39d8d87763b', 'data': {'list': [{'username': 'Bzmer', 'nickname': 'BBenjaminn', 'userAvatar': 'https://profile.csdnimg.cn/D/F/1/3_bzmer', 'blogUrl': 'https://blog.csdn.net/Bzmer', 'loginUserNameIsFollow': False, 'blogExpert': False, 'briefIntroduction': '个人网站：sigmod.coms.hk', 'id': 146750018}, {'username': 'm0_62902789', 'nickname': 'm0_62902789', 'userAvatar': 'https://profile.csdnimg.cn/2/F/F/3_m0_62902789', 'blogUrl': 'https://blog.csdn.net/m0_62902789', 'loginUserNameIsFollow': False, 'blogExpert': False, 'briefIntroduction': None, 'id': 146749679}, {'username': 'xujham', 'nickname': 'kkk@ynu', 'userAvatar': 'https://profile.csdnimg.cn/F/5/8/3_xujham', 'blogUrl': 'https://blog.csdn.net/xujham', 'loginUserNameIsFollow': False, 'blogExpert': False, 'briefIntroduction': None, 'id': 146711649}, {'username': 'huitaiter123', 'nickname': 'huitaiter123', 'userAvatar': 'https://profile.csdnimg.cn/4/1/3/3_huitaiter123', 'blogUrl': 'https://blog.csdn.net/huitaiter123', 'loginUserNameIsFollow': False, 'blogExpert': False, 'briefIntroduction': None, 'id': 146646263}, {'username': 'qq_56005252', 'nickname': '朝朝暮暮635', 'userAvatar': 'https://profile.csdnimg.cn/2/E/7/3_qq_56005252', 'blogUrl': 'https://blog.csdn.net/qq_56005252', 'loginUserNameIsFollow': False, 'blogExpert': False, 'briefIntroduction': None, 'id': 146625839}]}
```

下面是获取的函数，**我采用了jsonpath来从json里面提取信息，非常的方便**，或者直接for循环提取出nickname也是可以的。最后返回一个列表就行

```python
import jsonpath
def get_fans_name():
    resp=requests.get("https://blog.csdn.net/community/home-api/v2/get-fans-list?page=1&pageSize=5&id=0&noMore=false&blogUsername=qq_45722494",headers=headers)
    checkurl = "$.data.list[*].nickname"
    # print(resp.json())
    nickname_list=jsonpath.jsonpath(resp.json(),checkurl)
    return nickname_list
    # print(nickname_list) ['BBenjaminn', 'm0_62902789', 'kkk@ynu', 'huitaiter123', '朝朝暮暮635']
get_fans_name()
```

### 二，生成自定义壁纸

#### python生成自定义图片，并保存

![image-20221216222541154](http://1.12.68.28/s/sibADY8wKkK7iGe/preview)

如何生成自定义图片，参考的是[**何三笔记**](http://www.h3blog.com/)源码，我是在其基础上改了一下，==**生成了图片，并把其保存到了本地（同目录下）**==



先用python生成图片，并保存到本地，不做过多解释了，自己该参数，就能改成想要的效果。

```python
import re
from io import BytesIO
import requests
from PIL import Image,ImageDraw,ImageFont

class H3blogDrow:
    '''自定义图片样式'''
    def __init__(self) -> None:
        self.width = 1920
        self.heigth = 1080
        self.background_img = ''
        self.background_color = (42, 41, 55)
        self.layers = []
        self.convas = None

    def parse_config(self, config: dict) -> None:
        c = config
        self.convas = None
        self.width = c.get('width', 1920)
        self.heigth = c.get('height', 1080)
        self.background_color = tuple([int(i) for i in c.get('background_color', '').split(',')])
        self.background_img = c.get('background_img', (42, 41, 55))

        layers = c.get('layers', None)
        if not layers:
            return
        self.layers.extend(layers)

    def _create_canvas(self) -> None:
        self.convas = Image.new('RGB', (self.width, self.heigth), self.background_color)


    def draw(self) -> Image:
        '''画图'''
        # 创建背景设置画布
        self._create_canvas()

        if self.background_img and len(self.background_img) > 0:
            regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            m = re.match(regex, self.background_img)
            bg_img = None
            if m :
                resp = requests.get(self.background_img)
                _img_bytes = BytesIO()
                _img_bytes.write(resp.content)
                bg_img = Image.open(_img_bytes)
            else:
                #创建背景图片
                bg_img = Image.open(self.background_img)
            #将背景图片写入画布
            self.convas.paste(bg_img, (0,0))

        for layer in self.layers:
            if layer.get('layer_type') == 'text':
                self._draw_text(layer)
            if layer.get('layer_type') == 'image':
                self._draw_image()

        return self.convas

    def _darw_image(self, layer: dict) -> None:
        pass

    def _draw_text(self, layer: dict) -> None:
        draw = ImageDraw.Draw(self.convas)
        _font = layer.get('font')
        font = ImageFont.truetype(_font.get('font'), _font.get('size', 36))
        align = layer.get('align')
        p = tuple()
        if align and align == 'center':
            f_w, f_h = font.getsize(layer.get('text')) #获取字体大小
            p = ((self.convas.width - f_w)/2, (self.convas.height - f_h)/2)
        elif align and align == 'top-left':
            p = (0,0)
        elif align and align == 'top-right':
            f_w, f_h = font.getsize(layer.get('text')) #获取字体大小
            p = (self.convas.width - f_w, 0)
        elif align and align == 'bottom-left':
            f_w, f_h = font.getsize(layer.get('text')) #获取字体大小
            p = (0, self.convas.height - 4*f_h)
        elif align and align == 'bottom-right':
            f_w, f_h = font.getsize(layer.get('text')) #获取字体大小
            p = (self.convas.width - f_w, self.convas.height - f_h)
        else:
            p = tuple([int(i) for i in layer.get('position','0,0').split(',')])
        color = tuple([int(i) for i in layer.get('color','0,0,0').split(',')])
        draw.text(p, layer.get('text',''), fill = color, font = font)


config = {
    'width': 1920,
    'height': 1080,
    'background_img': '',
    'background_color':'42,41,55',

    'layers': [
        {
            'layer_type': 'text',
            'color': '255,0,0',
            'font': {
                'font': './上首疾风书法体.ttf',
                'size': 140,
            },
            'position': '0,0',
            'align': 'center',
            'text': 'csdn粉丝数：1220'
        },
        {
            'layer_type': 'text',
            'color': '0,255,0',
            'font': {
                'font':'./上首疾风书法体.ttf',
                'size': 40,
            },
            'position': '',
            'align': 'bottom-left',
            'text': 'kkk@ynu关注了你\nhuitaiter123关注了你\n朝朝暮暮635关注了你\nzfy2763428175关注了你\nzxy20030123关注了你'
        },
        {
            'layer_type': 'text',
            'color': '155,0,255',
            'font': {
                'font': './上首疾风书法体.ttf',
                'size': 70,
            },
            'position': '',
            'align': 'bottom-right',
            'text': '小梁说代码'
        },
    ],
}
d = H3blogDrow()
d.parse_config(config)
img = d.draw()
# 展示出来
img.show()
# 保存到本地
# img.save('./wallpaper.png')
```

#### 再将图片设置成壁纸

五行代码就能把图片变成壁纸，注意imagepath必须是**绝对路径！绝对路径！绝对路径**！**需要改成自己的路径**windows系统才能找到

```python
import ctypes
import os
# imagepath是要将被设置成壁纸图片的绝对路径，自己改
#获取当前目录绝对路径
path=os.getcwd()
# print(path)   D:\Software\PyCharm\Projects\FansWallPaper
imagepath=path+r"\wallpaper.png"
# imagepath ='D:\Software\PyCharm\Projects\FansWallPaper\wallpaper.png'
ctypes.windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)
```

### 三，完成实时更新（动态展示）

最后把它们连在一起来就行啦！我设置的时间是3秒进行来刷新，你们也可以设置时间短一点

```python
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
```

最后我把它打包成了一个exe文件，关于python如何打包可以参考我这个文档，还是比较新的：[https://liangyuanshao.blog.csdn.net/article/details/123022418](https://liangyuanshao.blog.csdn.net/article/details/123022418)

**最后我把这个exe文件设置为开机自动运行，每天就能实时自动展示csdn粉丝数了**

![image-20221217094756826](http://1.12.68.28/s/S3TrLFCpNoLf9Xy/preview)

### 四，相关代码地址

完整代码可以参考

**github仓库地址：[https://github.com/liangyuanshao/FansWallPaper](https://github.com/liangyuanshao/FansWallPaper)**

或者通过我的微信公众号获取：**小梁代码**





>参考链接
>
>https://blog.csdn.net/Ikaros_521/article/details/121906468
>
>http://www.h3blog.com/article/python-autobuild-image/
