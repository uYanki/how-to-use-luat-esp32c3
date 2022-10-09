# 功能：滑动均值滤波
from machine import Pin, ADC
import time
from filter import AverageFliter
a = ADC(Pin(0), atten=ADC.ATTN_11DB)
p = Pin(2, Pin.OUT, value=1)

N = 3000
i = 0
f = open('data.csv', 'w+')
f.write('k,zk,xH\n'.encode())
fiter = AverageFliter(lenth=10)
t0 = time.ticks_us()
while i < N:
    zk = a.read_uv()
    fiter.update(zk)
    f.write(('%d,%d,%d\n' % (i, zk, fiter.value())).encode())
    i += 1
    if (i < 1000 or i > 2000):
        p.value(1)
    else:
        p.value(0)
f.close()
print((time.ticks_us() - t0)/1e6)
