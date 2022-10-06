import ili9488
from machine import Pin,SPI
spi = SPI(1,baudrate=60000000,sck=Pin(0),mosi=Pin(1))
rst = Pin(12)
dc = Pin(18)
cs = Pin(19)
display = ili9488.Display(spi,cs,dc,rst)
display.clear(0xff0000)
display.block(0,0,20,20,bytearray([0xff,0xff,0xff]*400))