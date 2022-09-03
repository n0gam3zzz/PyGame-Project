# coding=utf-8
# Python 3.10.5
# written by zyf in 2022/08/12 22:10
import pygame
import sys
import time
import random
import os

# 1 初始化
os.chdir(os.path.dirname(__file__))  # 将本文件所在目录作为工作目录
pygame.init()  # 初始化PyGame
SCREEN_SIZE = (288, 512)  # 画面大小
screen_img = pygame.display.set_mode(SCREEN_SIZE)  # 显示画面
screen_rect = screen_img.get_rect()  # 获取画面的矩形
# pygame.key.set_repeat(50, 5)  # (灵敏度, 间隔)，单位为ms使得按键能被持续按下
pygame.display.set_caption("Flappy Bird by zyf written in Python")  # 更改PyGame程序标题
game_clk = pygame.time.Clock()  # 创建PyGame的时钟对象

# 2 背景
BG_IMGS = [pygame.image.load("Content/Images/bg_day.png"),
           pygame.image.load("Content/Images/bg_night.png")]  # 导入背景图片
bg_img = BG_IMGS[random.randint(0, 1)]  # 随机背景为白天/黑夜
bg_rect = [[0, 0], [SCREEN_SIZE[0], 0]]  # 两张背景图的坐标
BG_SPEED = -0.2  # 背景移动速度(px/frame)，向右为正

# 5 游戏相关
SCORE_IMGS = [pygame.image.load("Content/Images/number_0.png"), pygame.image.load("Content/Images/number_1.png"),
              pygame.image.load("Content/Images/number_2.png"), pygame.image.load("Content/Images/number_3.png"),
              pygame.image.load("Content/Images/number_4.png"), pygame.image.load("Content/Images/number_5.png"),
              pygame.image.load("Content/Images/number_6.png"), pygame.image.load("Content/Images/number_7.png"),
              pygame.image.load("Content/Images/number_8.png"), pygame.image.load("Content/Images/number_9.png")]
SCORE_IMG_SIZE = SCORE_IMGS[0].get_size()  # 分数的数字图片的大小
SCORE_CENTER = (int(SCREEN_SIZE[0] / 2 - SCORE_IMG_SIZE[0] / 2), int(SCREEN_SIZE[1] / 10))  # 分数的中心位置
score = 666


def score_show() -> None:
    if 0 <= score <= 9:  # 一位数
        screen_img.blit(SCORE_IMGS[score], SCORE_CENTER)
    elif 10 <= score <= 99:  # 二位数
        screen_img.blit(SCORE_IMGS[score % 10], (SCORE_CENTER[0] + SCORE_IMG_SIZE[0] / 2, SCORE_CENTER[1]))  # 个位
        screen_img.blit(SCORE_IMGS[score // 10], (SCORE_CENTER[0] - SCORE_IMG_SIZE[0] / 2, SCORE_CENTER[1]))  # 十位
    elif 100 <= score < 999:  # 三位数，我不信你能玩到上千分
        screen_img.blit(SCORE_IMGS[score % 10], (SCORE_CENTER[0] + SCORE_IMG_SIZE[0], SCORE_CENTER[1]))  # 个位
        screen_img.blit(SCORE_IMGS[score // 10 % 10], SCORE_CENTER)  # 十位
        screen_img.blit(SCORE_IMGS[score // 100], (SCORE_CENTER[0] - SCORE_IMG_SIZE[0], SCORE_CENTER[1]))  # 百位
    else:  # 999
        screen_img.blit(SCORE_IMGS[9], (SCORE_CENTER[0] + SCORE_IMG_SIZE[0], SCORE_CENTER[1]))  # 个位
        screen_img.blit(SCORE_IMGS[9], SCORE_CENTER)  # 十位
        screen_img.blit(SCORE_IMGS[9], (SCORE_CENTER[0] - SCORE_IMG_SIZE[0], SCORE_CENTER[1]))  # 百位


def bg_show() -> None:
    """显示背景：两张图接连显示"""
    bg_rect[0][0] += BG_SPEED
    if bg_rect[0][0] <= -SCREEN_SIZE[0]:  # 超出左边则移到右边
        bg_rect[0][0] = SCREEN_SIZE[0]
    bg_rect[1][0] += BG_SPEED
    if bg_rect[1][0] <= -SCREEN_SIZE[0]:  # 超出左边则移到右边
        bg_rect[1][0] = SCREEN_SIZE[0]
    screen_img.blit(bg_img, bg_rect[0])  # 在画面中应用背景图像与其矩形
    screen_img.blit(bg_img, bg_rect[1])


def render_screen() -> None:
    """刷新渲染主要游戏画面"""
    bg_show()  # 图层1: 背景
    score_show()
    # pipe_show()  # 图层2: 管道
    # bird.show()  # 图层3: 鸟
    # render_text("Time:" + str(int(time.perf_counter() - time_start)).rjust(3, '0') + "s", 16,
    #             fg_color=rgb_color.green)  # 图层6: 时间
    # render_text("Time:" + str(int(time.perf_counter() - time_start)).rjust(3, '0') + "s" + str(frame) + "frames",
    #             12, (100, 0), fg_color=rgb_color.green, bg_color=rgb_color.black)  # test
    # print(frame/(time.perf_counter() - time_start))  # test 输出刷新率
    # render_text("FPS " + str(int(frame/(time.perf_counter() - time_start))),
    #             10, fg_color=rgb_color.green)  # test 在左上角显示帧率
    pygame.display.update()  # 刷新画面


# 主程序循环
time_start = time.perf_counter()  # 开始计时
frame = 0  # test 刷新次数
while 1:
    game_clk.tick(120)  # 刷新率为60fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 系统事件-关闭
            pygame.quit()  # 退出PyGame程序
            sys.exit()  # 退出Python程序
        if event.type == pygame.KEYDOWN:  # 系统事件-按下按键
            # print(event, event.key)  # 控制台输出键盘按下事件
            # print(pygame.key.get_pressed())  # 控制台输出按下的按键
            if event.key == pygame.K_SPACE:  # 按下"SPACE"
                pass
    frame += 1  # test 刷新次数+1
    render_screen()
