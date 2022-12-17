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
# img.show()
# 保存到本地
img.save('./wallpaper.png')
