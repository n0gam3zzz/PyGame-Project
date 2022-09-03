# coding=utf-8
# Python 3.10.5
# written by zyf in 2022/08/12 22:10
# v0.1
import pygame
import sys
import time
import random
import os
# 以下为自建库
import rgb_color  # RGB颜色元组

# 1 初始化
os.chdir(os.path.dirname(__file__))  # 将本文件所在目录作为工作目录
pygame.init()  # 初始化PyGame
SCREEN_SIZE = (288, 512)  # 画面大小
screen_img = pygame.display.set_mode(SCREEN_SIZE)  # 显示画面
screen_rect = screen_img.get_rect()  # 获取画面的矩形
# pygame.key.set_repeat(50, 5)  # (灵敏度, 间隔)，单位为ms使得按键能被持续按下
pygame.display.set_caption("Flappy Bird by zyf written in Python")  # 更改PyGame程序标题
game_clk = pygame.time.Clock()  # 创建PyGame的时钟对象
# game_clk.tick(60)  # 刷新率为60fps


def render_text(txt: str, size: int, coor=(0, 0), fg_color=rgb_color.black,
                bg_color=rgb_color.white, font="Times New Roman") -> None:
    """渲染文字
    :param txt: 为要渲染的文字
    :param size: 文字大小，单位为像素
    :param coor: 文本框左上角的位置(x, y)
    :param fg_color: 前景色(R, G, B)三值，默认为黑色
    :param bg_color: 背景色(R, G, B)三值，默认为白色
    :param font: 文字字体，默认为\"Times New Roman\""""
    txt_font = pygame.font.SysFont(font, size)  # 字体配置
    txt_img = txt_font.render(txt, True, fg_color, bg_color)  # 将文字渲染为图像
    txt_rect = txt_img.get_rect()  # 获得文字图像的矩形
    txt_rect.x, txt_rect.y = coor
    screen_img.blit(txt_img, txt_rect)  # 在画面中应用文字图像与其矩形


# 2 背景
BG_IMGS = [pygame.image.load("../Content/Images/bg_day.png"),
           pygame.image.load("../Content/Images/bg_night.png")]  # 导入背景图片
bg_img = BG_IMGS[random.randint(0, 1)]  # 随机背景为白天/黑夜
bg_rect = [[0, 0], [SCREEN_SIZE[0], 0]]  # 两张背景图的坐标
BG_SPEED = -0.05  # 背景移动速度(px/frame)，向右为正


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


# 3 鸟
class Bird:
    """鸟类"""
    def __init__(self):
        """初始化鸟类"""
        self.index = random.randint(0, 2)  # 随机一只小鸟
        # self.index = 0  # test 小鸟编号为0
        self.img = BIRDS_IMGS[self.index][1]  # 鸟图
        self.rect = self.img.get_rect()  # 鸟图矩形
        self.speed = -0.5  # 鸟的速度(px/frame)，向下为正
        self.rect.center = screen_rect.center  # 先放到屏幕中间
        self.rect.x = SCREEN_SIZE[0] / 5
        self.x, self.y = self.rect.center  # 鸟图矩形中心坐标

    def show(self):
        """更新并显示鸟"""
        self.speed += ACCELERATION
        if self.speed >= 0.8:  # 限制最大速度
            self.speed = 0.8
        self.update_img()
        self.y += self.speed
        if self.y >= SCREEN_SIZE[1]:  # 超出屏幕下方
            self.y = SCREEN_SIZE[1]  # test 边缘保护
            # gameover
        elif self.y <= 0:  # 超出屏幕上方
            self.y = 0  # 边缘保护
        self.rect.center = (self.x, self.y)
        screen_img.blit(self.img, self.rect)

    def up(self):
        """按下空格鸟往上飞"""
        self.speed = -0.5

    def update_img(self):
        """根据速度更新图片"""
        if self.speed > 0.2:
            self.img = BIRDS_IMGS[self.index][0]
        elif self.speed < -0.2:
            self.img = BIRDS_IMGS[self.index][2]
        else:
            self.img = BIRDS_IMGS[self.index][1]


BIRD0_IMGS = [pygame.image.load("../Content/Images/bird0_0.png"), pygame.image.load("../Content/Images/bird0_1.png"),
              pygame.image.load("../Content/Images/bird0_2.png")]  # 导入鸟0图片素材
BIRD1_IMGS = [pygame.image.load("../Content/Images/bird1_0.png"), pygame.image.load("../Content/Images/bird1_1.png"),
              pygame.image.load("../Content/Images/bird1_2.png")]  # 导入鸟1图片素材
BIRD2_IMGS = [pygame.image.load("../Content/Images/bird2_0.png"), pygame.image.load("../Content/Images/bird2_1.png"),
              pygame.image.load("../Content/Images/bird2_2.png")]  # 导入鸟2图片素材
BIRDS_IMGS = [BIRD0_IMGS, BIRD1_IMGS, BIRD2_IMGS]
ACCELERATION = 0.002  # 向下加速度(px/frame^2)
bird = Bird()  # 初始化鸟


# 4 柱子
def pipe_show() -> None:
    for j in range(PIPE_NUM):
        pipes_up[j].show()
        pipes_down[j].show()


class PipeUp:
    """上方柱子类"""
    def __init__(self, index):
        self.index = index  # 序号
        self.rect = PIPE_IMGS[1].get_rect()  # 获取矩形
        if self.index == 0:
            self.x = SCREEN_SIZE[0]  # 生成在屏幕外
        else:
            self.x = pipes_up[self.index - 1].x + PIPE_HORIZONTAL  # 距离上个柱子一定距离
        self.y = random.randint(100, int(SCREEN_SIZE[1]/2) + 50)  # 随机生成y坐标
        self.rect.midbottom = (self.x, self.y)  # 应用矩形

    def show(self):
        """更新并显示"""
        self.x += PIPE_SPEED
        if self.x < -PIPE_IMG_SIZE[0] / 2:
            self.x = SCREEN_SIZE[0] + PIPE_IMG_SIZE[0] / 2  # 生成在屏幕外
            self.y = random.randint(100, int(SCREEN_SIZE[1] / 2) + 50)  # 随机生成y坐标
        self.rect.midbottom = (self.x, self.y)
        screen_img.blit(PIPE_IMGS[1], self.rect)


class PipeDown:
    """下方柱子类"""
    def __init__(self, index):
        self.index = index  # 序号
        self.rect = PIPE_IMGS[0].get_rect()  # 获取矩形
        if self.index == 0:
            self.x = SCREEN_SIZE[0]  # 生成在屏幕外
        else:
            self.x = pipes_down[self.index - 1].x + PIPE_HORIZONTAL  # 距离上个柱子一定距离
        self.y = pipes_up[self.index].y + PIPE_VERTICAL  # 根据上方柱子生成y坐标
        self.rect.midtop = (self.x, self.y)  # 应用矩形

    def show(self):
        """更新并显示"""
        self.x += PIPE_SPEED
        if self.x < -PIPE_IMG_SIZE[0] / 2:
            self.x = SCREEN_SIZE[0] + PIPE_IMG_SIZE[0] / 2  # 生成在屏幕外
            self.y = pipes_up[self.index].y + PIPE_VERTICAL  # 根据上方柱子生成y坐标
        self.rect.midtop = (self.x, self.y)
        screen_img.blit(PIPE_IMGS[0], self.rect)


PIPE_IMGS = [pygame.image.load("../Content/Images/pipe_up.png"),
             pygame.image.load("../Content/Images/pipe_down.png")]  # 导入柱子图片
PIPE_IMG_SIZE = PIPE_IMGS[0].get_size()  # 柱子图片的尺寸
PIPE_SPEED = -0.15  # 柱子速度
PIPE_HORIZONTAL = 150  # 柱子的横向距离
PIPE_VERTICAL = 120  # 柱子的纵向距离
pipes_up = []  # 一堆上方柱子
pipes_down = []  # 一堆下方柱子
PIPE_NUM = 2  # 柱子对数
for i in range(PIPE_NUM):  # 生成柱子
    pipes_up.append(PipeUp(i))
    pipes_down.append(PipeDown(i))

# 5 游戏相关
score = 0


def render_screen() -> None:
    """刷新渲染主要游戏画面"""
    bg_show()  # 图层1: 背景
    pipe_show()  # 图层2: 管道
    bird.show()  # 图层3: 鸟
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
# frame = 0  # test 刷新次数
while 1:
    game_clk.tick(480)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 系统事件-关闭
            pygame.quit()  # 退出PyGame程序
            sys.exit()  # 退出Python程序
        if event.type == pygame.KEYDOWN:  # 系统事件-按下按键
            # print(event, event.key)  # 控制台输出键盘按下事件
            # print(pygame.key.get_pressed())  # 控制台输出按下的按键
            if event.key == pygame.K_SPACE:  # 按下"SPACE"
                bird.up()
    #         if key_pressed[pygame.K_SPACE]:  # 按下"SPACE"
    #             bird_rect.y -= bird_upspeed
    #             render_screen()
    #             bird_rect.y -= bird_upspeed
    #             render_screen()
    #             pass
    # bird_rect.y += bird_downspeed  # 鸟下降
    # frame += 1  # test 刷新次数+1
    render_screen()
