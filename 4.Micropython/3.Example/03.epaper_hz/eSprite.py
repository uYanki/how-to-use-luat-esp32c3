
import framebuf
import math
import os


def getbin(inta: int, x: int) -> int:
    return (inta & (1 << x)) >> x


def clamp(a, min, max):
    global aa, bb, cc
    if max < min:
        return min
    if a > max:
        return min
    elif a < min:
        return max
    else:
        return a


def getPageLen2(num: int) -> int:
    temp = num >> 3
    if (num == temp << 3):
        return temp
    else:
        return temp + 1


def getPageLen(num: int) -> int:
    temp = num >> 3
    if (num & 7):
        return temp + 1
    else:
        return temp


def DataScale(data, scale):
    re = []
    inv = False
    if scale == 0:
        return re
    if scale < 0:
        scale = - scale
        inv = True
    scale = len(data)/(scale*len(data))
    i = 0
    while math.ceil(i) < len(data):
        re.append(data[math.ceil(i)])
        i += scale
    if inv:
        re.reverse()
    return re


def bmpdecode(filename, newname=None, biasY=0, limit=128, log=True, InvertColor=False, delAfterDecode=False):
    f = open(filename, 'rb')
    if f.read(2) == b'BM':  # header
        dummy = f.read(8)  # file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1:  # planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:  # compress method == uncompressed
                print("Image size:", width, "x", height)
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                #display._setwindowloc((posX,posY),(posX+w - 1,posY+h - 1))
                row = 0
                if newname == None:
                    newname = filename[:-4]
                buff = open(newname+'.ebin', 'wb+')
                buff.write(b'\x00\x01')
                buff.write((getPageLen(width)*8).to_bytes(2, 'little'))
                buff.write(height.to_bytes(2, 'little'))

                temp = [0]*(getPageLen(width))
                temp2 = height - 1 + biasY
                dataCounter = 0
                dataPointer = 0
                if (InvertColor):
                    while row < height:
                        if row != 0:
                            buff.write(bytearray(temp))
                        temp = [0]*getPageLen(width)
                        dataCounter = 0
                        dataPointer = 0
                        if flip:
                            pos = offset + (temp2 - row) * rowsize
                        else:
                            pos = offset + (row + biasY) * rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            gray = (bgr[2]*77 + bgr[1]*151+bgr[0]*28) >> 8
                            # (R*77+G*151+B*28)>>8
                            if (gray <= limit):
                                data = 128  # 1<<7
                            else:
                                data = 0
                            # print(dataPointer,dataCounter)
                            temp[dataPointer] = temp[dataPointer]+(data >> dataCounter)
                            dataCounter = dataCounter + 1
                            if dataCounter >= 8:
                                dataCounter = 0
                                dataPointer += 1
                            #temp[col] = (temp[col]>>1)+data
                            col = col + 1
                        row = row+1
                        if log:
                            print("decoding :%d%%" % (row*100//height))
                else:  # 空间换时间 本质一个if
                    while row < height:
                        # 写入
                        buff.write(bytearray(temp))
                        temp = [0]*getPageLen(width)
                        dataCounter = 0
                        dataPointer = 0
                        if flip:
                            pos = offset + (temp2 - row) * rowsize
                        else:
                            pos = offset + (row + biasY) * rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            gray = (bgr[2]*77 + bgr[1]*151+bgr[0]*28) >> 8
                            # (R*77+G*151+B*28)>>8
                            if (gray > limit):
                                data = 128  # 1<<7
                            else:
                                data = 0
                            # print(dataPointer,dataCounter)
                            temp[dataPointer] = temp[dataPointer]+(data >> dataCounter)
                            dataCounter = dataCounter + 1
                            if dataCounter >= 8:
                                dataCounter = 0
                                dataPointer += 1
                            #temp[col] = (temp[col]>>1)+data
                            col = col + 1
                        row = row+1
                        if log:
                            print("decoding :%d%%" % (row*100//height))
    else:
        raise TypeError("Type not support")
    f.close()
    buff.close()
    if (delAfterDecode):
        os.remove(filename)
    print('Encode Finish save to: '+newname+'.ebin')
    return BinloaderFile(newname+'.ebin')


class BinloaderFile:
    def __init__(self, filename, x=0, y=0):
        self.x, self.y = x, y
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4] + (temp[5] << 8)

    def draw(self, display, x=0, y=0):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        width = getPageLen(self.w)
        displayW = display.width // 8
        drawWidth = min(width, displayW - x)
        displayW = min(displayW, displayW + self.w - x)
        start = x + y * displayW
        y = 0
        while y < self.h:
            self.f.seek(6+y*width)
            #print(start + y * displayW + drawWidth)
            if start + y * displayW + drawWidth > len(display.buffer):
                return
            display.buffer[start + y * displayW:start + y * displayW + drawWidth] = self.f.read(drawWidth)
            y += 1

    def __del__(self):
        self.f.close()


def chsC2enc(d):
    if 0x4e00 <= d <= 0x9fa5 or d < 128:
        return d
    if (d == 0xff0c):
        return 0x2c
    elif (d == 0x3002):
        return 0x2e
    elif (d == 0xff1a):
        return 0x3b
    elif (d == 0x201c or d == 0x201d):
        return 0x22
    elif (d == 0x2019 or d == 0x2018):
        return 0x27
    elif (d == 0x3010):
        return 0x5b
    elif (d == 0x3011):
        return 0x5d
    elif (d == 0xff08):
        return 0x28
    elif (d == 0xff09):
        return 0x29
    elif (d == 0xff1b):
        return 0x3b
    elif (d == 0x3001):
        return 0xb7
    elif (d == 0xff01):
        return 0x21
    print(d, chr(d))


class Font16:
    def __init__(self, filename) -> None:
        self.bias = 0x4e00
        #self.end = 0x9fa5
        self.f = open(filename, 'rb')
        if (self.f.read(3) != b'f16'):
            raise TypeError("!!!Font not support!!!")

    def text(self, x, y, data, display, width=2):
        i = 0  # 换字
        p = y  # 换行
        for d in data:
            # print(d)
            d = ord(d)
            d = chsC2enc(d)
            if 0 < d < 128:
                self.f.seek((d)*32 + 3)
            elif d >= 0x4e00:
                self.f.seek((d-self.bias+128)*32 + 3)
            fromD = x+p*25+i*width
            if (p > 184):
                break

            for charData in range(16):
                display.buffer[fromD+charData*25:fromD+2+charData*25] = self.f.read(2)

            i = i+1
            if i >= 12:
                # print(i)
                p += 16
                i = 0
