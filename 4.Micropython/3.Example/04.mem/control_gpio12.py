# 功能：通过寄存器使能并控制 gpio12

from machine import Pin, mem16, mem8, mem32
import time
GPIO = 0x6000_4000
GPIO_OUT_REG = 0x0004
GPIO_ENABLE_REG = 0x0020
print(mem32[GPIO+GPIO_OUT_REG])
print(mem32[GPIO+GPIO_ENABLE_REG])
mem32[GPIO+GPIO_ENABLE_REG] ^= 1 << 12
while True:
    mem32[GPIO+GPIO_OUT_REG] ^= 1 << 12
    time.sleep(1)
