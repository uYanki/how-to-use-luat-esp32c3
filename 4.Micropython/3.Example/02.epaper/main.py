# 合宙 200x200 墨水屏, 显示 阿尼亚 和 2233娘

from machine import SPI, Pin
from e1in54 import EPD
from eSprite import BinloaderFile, bmpdecode

spi = SPI(1, 60000000, sck=Pin(2), mosi=Pin(3))
display = EPD(spi, rst=10, dc=6, cs=7, busy=5)

p = BinloaderFile('aniya.ebin')
# p = bmpdecode('2233_2.bmp',InvertColor=False,  limit=220, log=False)
# 是否翻转颜色 InvertColor, 灰度值限制 limit

p.draw(display, 0, 0)  # ebin,x,y

display.line(0, 0, 200, 200, 0)  # x1,y1,x2,y2,isWhite
display.text('aniya', 0, 0, 0)  # str,x,y,isWhite

display.show()
