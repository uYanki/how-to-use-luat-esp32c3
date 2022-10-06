# 合宙 Air10x 系列屏幕扩展板 + 合宙 Esp32-C3 直插
# 功能: 雷霆战机低低低配版

import _thread
import random
import time
import math

from machine import Pin, SPI
from st7735 import ST7735, color
import ufont

spi = SPI(1, 30_000_000, sck=Pin(2), mosi=Pin(3))
display = ST7735(spi, cs=7, dc=6, rst=10, bl=11,
                 width=160, height=80, rotate=1)
f = ufont.BMFont("DIGITAL-Dreamfat-95-16.v3.bmf")

# 按钮
up_key = Pin(8, Pin.IN, pull=Pin.PULL_UP)
down_key = Pin(13, Pin.IN, pull=Pin.PULL_UP)
left_key = Pin(5, Pin.IN, pull=Pin.PULL_UP)
right_key = Pin(9, Pin.IN, pull=Pin.PULL_UP)
center_key = Pin(4, Pin.IN, pull=Pin.PULL_UP)

# 血量
hp = 100
# 玩家位置
player_pos = [10, 40]
# 玩家移动速度
player_speed = 3
# 子弹移动速度
bullet_speed = 1
# 敌人移动速度
enemy_speed = 1
# 子弹位置
bullet_pos = []
# 敌人位置
enemy_pos = []
# 奖励
reward_pos = []
# 防止发射过快
key_status = True
max_bullet = 8
key_interval = 0.5

# 游戏状态
game_status = True
# 消灭敌人数量
enemies_killed = 0
# 游戏分数
score = 0
# 游戏时间
play_time = 0
# 游戏难度 1 ~ 5.0
difficulty = 3.0
# 游戏最高帧数
fps = 30


def update_screen(_fps):
    """
    更新屏幕
    :param _fps: 帧数
    :return:
    """
    while True:
        if hp > 0 and game_status:
            display.fill(0)
            # 显示分数
            display.text("SCORE:" + str(score), (13 - len(str(score))) * 8, 0, color(255, 255, 255))
            display.text("KILL:" + str(enemies_killed), 8, 0, color(255, 255, 255))

            # 绘制子弹位置
            for b in bullet_pos:
                display.fill_rect(b[0] - 2, b[1] - 2, 5, 5, color(0, random.randint(1, 2) * 127, 255))

            # 绘制敌人位置
            for e in enemy_pos:
                display.fill_rect(e[0] - 4, e[1] - 4, 9, 9, e[1] * 819)

            # 绘制奖励
            for r in reward_pos:
                display.circle(r, 5, color(255, 0, 0), 4)

            # 绘制血量
            display.fill_rect(0, 80 - int(0.8 * hp), 4, 80, color(155 + hp, 0, 0))

            # 绘制玩家位置
            display.fill_rect(player_pos[0] - 3, player_pos[1] - 3, 7, 7, color(255, 255, 255))
        elif hp <= 0:
            display.fill(0)
            game_over(score)
        display.show()
        time.sleep_ms(1000 // _fps)


def update_pos():
    """
    更新位置
    :return:
    """
    global hp, score
    while True:
        if hp <= 0:
            # 如果没有血了
            pass
        elif not game_status:
            # 如果暂停了
            pass
        else:
            # 子弹的移动
            for b in bullet_pos:
                if b[0] > 180:
                    bullet_pos.remove(b)
                else:
                    b[0] += bullet_speed

            # 敌人的移动
            for e in enemy_pos:
                # 如果撞向基地
                if e[0] < 4:
                    hp -= 10
                    enemy_pos.remove(e)
                # 如果撞向玩家
                elif abs(e[0] - player_pos[0]) < 7 and abs(e[1] - player_pos[1]) < 7:
                    hp -= 20
                    enemy_pos.remove(e)
                else:
                    e[0] -= 1

            # 奖励的获取
            for r in reward_pos:
                if abs(r[0] - player_pos[0]) < 7 and abs(r[1] - player_pos[1]) < 7:
                    hp = 100
                    score += 20
                    reward_pos.remove(r)
        time.sleep(0.03)


def add_enemy():
    """
    添加敌人
    :return:
    """
    while True:
        # 根据时间的变换难度不断上升
        _delay = int(15 - math.log2(enemies_killed + 2))
        time.sleep(random.randint(_delay - 2, _delay) // difficulty)
        if len(enemy_pos) < 10 and game_status and hp > 0:
            enemy_pos.append([160, random.randint(14, 76)])
        if play_time % 30 == 0 and random.choice([True, False]):
            reward_pos.append([random.randint(7, 100), random.randint(14, 76)])
        elif play_time % 35 == 0:
            reward_pos.clear()


def _check():
    """
    判定子弹击中
    :return:
    """
    global enemies_killed, play_time, score
    while True:
        break_status = False
        for b in bullet_pos:
            for e in enemy_pos:
                if abs(e[0] - b[0]) < 7 and abs(e[1] - b[1]) < 7:
                    bullet_pos.remove(b)
                    enemy_pos.remove(e)
                    enemies_killed += 1
                    score += int(math.log2(enemies_killed + 2))
                    break_status = True
                    break
            if break_status:
                break
        time.sleep(0.03)


def add_bullet():
    """
    发射子弹
    :return:
    """
    global key_status
    if key_status and game_status and hp > 0 and len(bullet_pos) < max_bullet:
        bullet_pos.append(player_pos.copy())
        _thread.start_new_thread(bullet_interval, ())


def bullet_interval():
    """
    子弹发射间隔
    :return:
    """
    global key_status
    key_status = False
    time.sleep(key_interval)
    key_status = True


def time_update():
    global play_time, reward_pos
    while True:
        if game_status and hp > 0:
            play_time += 1

        time.sleep(1)


def game_over(_score):
    """
    游戏结束显示分数
    :param _score:
    :return:
    """
    display.back_light(128)
    display.fill_rect(10, 10, 140, 60, color(26, 184, 157))
    display.fill_rect(13, 13, 134, 54, 0)

    f.text(display, "GAME", 15, 15, color=color(255, 255, 255), half_char=False)
    f.text(display, "OVER", 83, 15, color=color(184, 26, 53), half_char=False)

    f.text(display, "SCORE:", 20, 40, color=color(255, 255, 255), font_size=8, half_char=False)
    f.text(display, str(_score), 70, 40, color=color(255, 255, 255), font_size=8, half_char=False)
    f.text(display, "KILL :", 20, 50, color=color(255, 255, 255), font_size=8, half_char=False)
    f.text(display, str(enemies_killed), 70, 50, color=color(255, 255, 255), font_size=8, half_char=False)


# 更新
_thread.start_new_thread(update_screen, (fps,))
_thread.start_new_thread(update_pos, ())
_thread.start_new_thread(add_enemy, ())
_thread.start_new_thread(_check, ())
_thread.start_new_thread(time_update, ())

display.back_light(255)
while True:
    if key_status and center_key.value() == 0:
        add_bullet()
    # 上移
    elif player_pos[1] > 10 and up_key.value() == 0:
        player_pos[1] -= player_speed
    # 下移
    elif player_pos[1] < 78 and down_key.value() == 0:
        player_pos[1] += player_speed
    # 左移
    elif player_pos[0] > 7 and left_key.value() == 0:
        player_pos[0] -= player_speed
    # 右移
    elif player_pos[0] < 100 and right_key.value() == 0:
        player_pos[0] += player_speed
    elif hp < 0:
        break
    time.sleep_ms(30)
