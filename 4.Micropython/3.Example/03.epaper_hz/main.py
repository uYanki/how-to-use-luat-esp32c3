from machine import SPI, Pin
from e1in54 import EPD
from eSprite import BinloaderFile, bmpdecode, Font16
spi = SPI(1, 60000000, sck=Pin(2), mosi=Pin(3))
display = EPD(spi, rst=10, dc=6, cs=7, busy=5)
fontWhite = Font16('font1616.ebin')  # font1616w.ebin 白底, font1616.ebin 黑底
text = '豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰。台隍枕夷夏之交，宾主尽东南之美。都督阎公之雅望，棨戟遥临；宇文新州之懿范，襜帷暂驻。十旬休假，胜友如云；千里逢迎，高朋满座。腾蛟起凤，孟学士之词宗；紫电青霜，王将军之武库。家君作宰，路出名区；童子何知，躬逢胜饯。'
fontWhite.text(0, 0, text, display, width=2)
display.show()
