# 功能：函数与寄存器速度对比

from machine import Pin, mem16, mem8, mem32
from micropython import const
import time
GPIO = const(0x6000_4000)
GPIO_OUT_REG = const(0x0004)
GPIO_ENABLE_REG = const(0x0020)
GPIO12 = const(1 << 12)

if not ((mem16[GPIO+GPIO_ENABLE_REG] >> 16) & 1):
    mem16[GPIO+GPIO_ENABLE_REG] ^= GPIO12
p12 = Pin(13, Pin.OUT)


print('1次')

t0 = time.ticks_us()
mem16[GPIO+GPIO_OUT_REG] ^= GPIO12
print('mem', time.ticks_us()-t0)


t0 = time.ticks_us()
p12.value(not p12.value())
print('gpio', time.ticks_us()-t0)


print('100k次')
t0 = time.ticks_us()

i = 0
while i < 100000:
    mem16[GPIO+GPIO_OUT_REG] ^= GPIO12
    i += 1
print('mem', time.ticks_us()-t0)


t0 = time.ticks_us()

i = 0
while i < 100000:
    p12.value(not p12.value())
    i += 1
print('gpio', time.ticks_us()-t0)

# 输出:
# 1次
# mem 25
# gpio 65
# 100k次
# mem 1045798
# gpio 1478547
