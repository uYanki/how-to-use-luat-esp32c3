# 功能：通过寄存器使能并获取 gpio0 的输入

from machine import Pin, mem16, mem8, mem32
from micropython import const
import time
GPIO = const(0x6000_4000)
# GPIO_OUT_REG = const(0x0004)
# GPIO_ENABLE_REG = const(0x0020)
GPIO_IN_REG = const(0x003C)
# GPIO12 = const(1<<12)
# GPIO_PIN0_REG = const(0x0074)
# GPIO_FUNC0_IN_SEL_CFG_REG = const(0x0154)

IO_MUX = const(0x6000_9000)
IO_MUX_GPIO0_REG = const(0x0004)
# print(bin(mem32[GPIO+GPIO_PIN0_REG]))
# p0 = Pin(0,Pin.IN,pull=Pin.PULL_UP)
# print(bin(mem32[GPIO+GPIO_PIN0_REG]))
# p0 = Pin(0,Pin.IN,pull=Pin.PULL_DOWN)
print(bin(mem32[IO_MUX+IO_MUX_GPIO0_REG]))
mem32[IO_MUX+IO_MUX_GPIO0_REG] ^= 1 << 7  # 下拉电阻
mem32[IO_MUX+IO_MUX_GPIO0_REG] ^= 1 << 9  # 输入模式

# print(bin(mem32[GPIO+GPIO_PIN0_REG]))
print(bin(mem32[IO_MUX+IO_MUX_GPIO0_REG]))
print((mem32[GPIO+GPIO_IN_REG]) & 1)  # 输出
