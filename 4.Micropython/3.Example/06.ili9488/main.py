# 功能：在驱动芯片为 ili9341 的屏幕上显示图片和文字
from machine import Pin, SPI
import ili9341
from zhFont2tft import Font16
from bmpdecoder import bmpFileData
import time
spi = SPI(1, 60000000, sck=Pin(2), mosi=Pin(3), miso=Pin(10))
display = ili9341.Display(spi, cs=Pin(5), dc=Pin(7), rst=Pin(11),
                          width=240, height=320)
display.clear(0xffff)
display.block(0, 0, 20, 20, bytearray([0xff, 0xff, 0xff]*400))
time.sleep(1)
# 解码成 rgb565 格式（慢）
# p = bmpFileData.decode('majo.bmp',screenSize = (240,320))
# 读取 rgb565 格式（快）
average = 0
count = 0
p = bmpFileData.load('majo')
font = Font16('font1616.ebin')
for i in range(20):
    t0 = time.ticks_ms()
    p.render(display, (0, 0))
    font.text2x(0, 280, '循环第%d' % (count+1), display, linecount=12, color=[255, 0, 0], backgroundcolor=[255, 255, 0])
    font.text(0, 200, '中文123测试', display, linecount=12, color=[31, 255, 215], backgroundcolor=[64, 1, 0])
    if count:
        font.text2x(0, 0, 'fps:'+str(average/count)[0:3], display, linecount=12, color=[0, 255, 0], backgroundcolor=[255, 255, 255])
    fps = 1000/(time.ticks_ms()-t0)
    average += fps
    count += 1
