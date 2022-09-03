# coding=utf-8
# Python 3.10.5
# written by zyf in 2022/08/12 22:10
# v1.0 in 2022/08/14 11:15
# v1.1 in 2022/09/03 00:00 Add sound effects.
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
BG_IMGS = [pygame.image.load("Content/Images/bg_day.png"),
           pygame.image.load("Content/Images/bg_night.png")]  # 导入背景图片
bg_img = BG_IMGS[random.randint(0, 1)]  # 随机背景为白天/黑夜
bg_rect = [[0, 0], [SCREEN_SIZE[0], 0]]  # 两张背景图的坐标
BG_SPEED = -0.2  # 背景移动速度(px/frame)，向右为正


def bg_show(option=True) -> None:
    """显示背景：两张图接连显示
    :param option -> bool 为True则有速度，为False则静止"""
    if option:
        bg_rect[0][0] += BG_SPEED
        if bg_rect[0][0] <= -SCREEN_SIZE[0]:  # 超出左边则移到右边
            bg_rect[0][0] = SCREEN_SIZE[0]
        bg_rect[1][0] += BG_SPEED
        if bg_rect[1][0] <= -SCREEN_SIZE[0]:  # 超出左边则移到右边
            bg_rect[1][0] = SCREEN_SIZE[0]
    screen_img.blit(bg_img, bg_rect[0])  # 在画面中应用背景图像与其矩形
    screen_img.blit(bg_img, bg_rect[1])  # 在画面中应用背景图像与其矩形


# 2.1 地板
LAND_IMG = pygame.image.load("Content/Images/land.png")  # 地板的图片
LAND_IMG_SIZE = LAND_IMG.get_size()  # 地板图片的尺寸
land_rect = [[0, SCREEN_SIZE[1] - LAND_IMG_SIZE[1]], [SCREEN_SIZE[0], SCREEN_SIZE[1] - LAND_IMG_SIZE[1]]]  # 两张地板图片的矩形
LAND_SPEED = -1  # 地板移动速度


def land_show(option=True) -> None:
    """显示地板：两张图接连显示
    :param option -> bool 为True则有速度，为False则静止"""
    if option:
        land_rect[0][0] += LAND_SPEED
        if land_rect[0][0] <= -LAND_IMG_SIZE[0]:  # 超出左边则移到右边
            land_rect[0][0] = SCREEN_SIZE[0]
        land_rect[1][0] += LAND_SPEED
        if land_rect[1][0] <= -LAND_IMG_SIZE[0]:  # 超出左边则移到右边
            land_rect[1][0] = SCREEN_SIZE[0]
    screen_img.blit(LAND_IMG, land_rect[0])  # 在画面中应用地板图像与其矩形
    screen_img.blit(LAND_IMG, land_rect[1])  # 在画面中应用地板图像与其矩形


# 3 鸟
class Bird:
    """鸟类"""
    def __init__(self):
        """初始化鸟类"""
        self.index = random.randint(0, 2)  # 随机一只小鸟
        # self.index = 0  # test 小鸟编号为0
        self.img = BIRDS_IMGS[self.index][1]  # 鸟图
        self.rect = self.img.get_rect()  # 鸟图矩形
        self.speed = -1  # 鸟的速度(px/frame)，向下为正
        self.rect.y = SCREEN_SIZE[1] / 3  # 鸟的位置y坐标
        self.rect.x = SCREEN_SIZE[0] / 5  # 鸟的位置x坐标
        self.x, self.y = self.rect.center  # 鸟图矩形中心坐标

        self.mask = pygame.mask.from_surface(self.img)  # 鸟图的遮罩

    def show(self, option=True):
        """更新并显示鸟
        :param option 为True则有速度，为False则静止"""
        global is_over
        if option:
            self.speed += ACCELERATION
            if self.speed >= 3:  # 限制最大速度
                self.speed = 3
            self.update_img()
            self.y += self.speed
            if self.y >= SCREEN_SIZE[1] - LAND_IMG_SIZE[1]:  # 落到地板
                self.y = SCREEN_SIZE[1] - LAND_IMG_SIZE[1]  # test 边缘保护
                BIRD_HIT_SE.play()
                is_over = True
                # print("HIT: GROUND")  # test
            elif self.y <= 0:  # 超出屏幕上方
                self.y = 0  # 边缘保护
            self.rect.center = (self.x, self.y)
        screen_img.blit(self.img, self.rect)

    def up(self):
        """按下空格鸟往上飞"""
        BIRD_UP_SE.play()
        self.speed = -2

    def update_img(self):
        """根据速度更新鸟图"""
        if self.speed > 0.5:
            self.img = BIRDS_IMGS[self.index][0]
        elif self.speed < -0.5:
            self.img = BIRDS_IMGS[self.index][2]
        else:
            self.img = BIRDS_IMGS[self.index][1]


BIRD0_IMGS = [pygame.image.load("Content/Images/bird0_0.png").convert_alpha(),
              pygame.image.load("Content/Images/bird0_1.png").convert_alpha(),
              pygame.image.load("Content/Images/bird0_2.png").convert_alpha()]  # 导入鸟0图片素材
BIRD1_IMGS = [pygame.image.load("Content/Images/bird1_0.png").convert_alpha(),
              pygame.image.load("Content/Images/bird1_1.png").convert_alpha(),
              pygame.image.load("Content/Images/bird1_2.png").convert_alpha()]  # 导入鸟1图片素材
BIRD2_IMGS = [pygame.image.load("Content/Images/bird2_0.png").convert_alpha(),
              pygame.image.load("Content/Images/bird2_1.png").convert_alpha(),
              pygame.image.load("Content/Images/bird2_2.png").convert_alpha()]  # 导入鸟2图片素材
BIRDS_IMGS = [BIRD0_IMGS, BIRD1_IMGS, BIRD2_IMGS]
BIRD_IMG_SIZE = BIRD0_IMGS[0].get_size()
ACCELERATION = 0.04  # 向下加速度(px/frame^2)
bird = Bird()  # 初始化鸟
BIRD_UP_SE = pygame.mixer.Sound("Content/Audio/wing.wav")  # 飞的音效
BIRD_UP_SE.set_volume(0.2)
BIRD_HIT_SE = pygame.mixer.Sound("Content/Audio/hit.wav")  # 撞到的音效
BIRD_HIT_SE.set_volume(0.2)
BIRD_POINT_SE = pygame.mixer.Sound("Content/Audio/point.wav")  # 得分音效
BIRD_POINT_SE.set_volume(0.2)


# 4 柱子
def pipe_show(option=True) -> None:
    """显示柱子
    :param option -> bool 为True则有速度，为False则静止"""
    for j in range(PIPE_NUM):
        pipes_up[j].show(option)
        pipes_down[j].show(option)


class PipeUp:
    """上方柱子类"""
    def __init__(self, index):
        self.index = index  # 序号
        self.rect = PIPE_IMGS[1].get_rect()  # 获取矩形
        if self.index:
            self.x = pipes_up[self.index - 1].x + PIPE_HORIZONTAL  # 距离上个柱子一定距离
        else:
            self.x = SCREEN_SIZE[0]  # 序号为0，生成在屏幕外
        self.y = random.randint(25, SCREEN_SIZE[1] // 2 - LAND_IMG_SIZE[1] + PIPE_VERTICAL)  # 随机生成y坐标
        self.rect.midbottom = (self.x, self.y)  # 应用矩形
        self.mask = pygame.mask.from_surface(PIPE_IMGS[1])  # 上方柱子图的遮罩

    def show(self, option=True):
        """更新并显示
        :param option -> bool 为True则有速度，为False则静止"""
        if option:
            self.x += PIPE_SPEED
        self.update()
        self.rect.midbottom = (self.x, self.y)
        screen_img.blit(PIPE_IMGS[1], self.rect)

    def update(self):
        """已走出屏幕外更新位置"""
        if self.x < -PIPE_IMG_SIZE[0] / 2:  # 已走出屏幕外
            if self.index:
                self.x = pipes_up[self.index - 1].x + PIPE_HORIZONTAL  # 距离前个柱子一定距离
            else:
                self.x = pipes_up[PIPE_NUM - 1].x + PIPE_HORIZONTAL  # 距离前个柱子一定距离
            self.y = random.randint(25, SCREEN_SIZE[1] // 2 - LAND_IMG_SIZE[1] + PIPE_VERTICAL)  # 随机生成y坐标


class PipeDown:
    """下方柱子类"""
    def __init__(self, index):
        self.index = index  # 序号
        self.rect = PIPE_IMGS[0].get_rect()  # 获取矩形
        if self.index:
            self.x = pipes_down[self.index - 1].x + PIPE_HORIZONTAL  # 距离上个柱子一定距离
        else:
            self.x = SCREEN_SIZE[0]  # 序号为0，生成在屏幕外
        self.y = pipes_up[self.index].y + PIPE_VERTICAL  # 根据上方柱子生成y坐标
        self.rect.midtop = (self.x, self.y)  # 应用矩形
        self.mask = pygame.mask.from_surface(PIPE_IMGS[0])  # 下方柱子图的遮罩

    def show(self, option=True):
        """更新并显示
        :param option -> bool 为True则有速度，为False则静止"""
        if option:
            self.x += PIPE_SPEED
        self.update()
        self.rect.midtop = (self.x, self.y)
        screen_img.blit(PIPE_IMGS[0], self.rect)

    def update(self):
        """已走出屏幕外更新位置"""
        if self.x < -PIPE_IMG_SIZE[0] / 2:  # 已走出屏幕外
            if self.index:
                self.x = pipes_down[self.index - 1].x + PIPE_HORIZONTAL  # 距离前个柱子一定距离
            else:
                self.x = pipes_down[PIPE_NUM - 1].x + PIPE_HORIZONTAL  # 距离前个柱子一定距离
            self.y = pipes_up[self.index].y + PIPE_VERTICAL  # 根据上方柱子生成y坐标


PIPE_IMGS = [pygame.image.load("Content/Images/pipe_up.png").convert_alpha(),
             pygame.image.load("Content/Images/pipe_down.png").convert_alpha()]  # 导入柱子图片
PIPE_IMG_SIZE = PIPE_IMGS[0].get_size()  # 柱子图片的尺寸
PIPE_SPEED = LAND_SPEED  # 柱子速度
PIPE_HORIZONTAL = 150  # 左右两对柱子间的横向距离
PIPE_VERTICAL = 120  # 上下两个柱子的纵向距离
pipes_up = []  # 一堆上方柱子
pipes_down = []  # 一堆下方柱子
PIPE_NUM = 3  # 柱子对数，三个够用了
for i in range(PIPE_NUM):  # 生成柱子
    pipes_up.append(PipeUp(i))
    pipes_down.append(PipeDown(i))


# 5 游戏相关
SCORE_IMGS = [pygame.image.load("Content/Images/number_0.png"), pygame.image.load("Content/Images/number_1.png"),
              pygame.image.load("Content/Images/number_2.png"), pygame.image.load("Content/Images/number_3.png"),
              pygame.image.load("Content/Images/number_4.png"), pygame.image.load("Content/Images/number_5.png"),
              pygame.image.load("Content/Images/number_6.png"), pygame.image.load("Content/Images/number_7.png"),
              pygame.image.load("Content/Images/number_8.png"), pygame.image.load("Content/Images/number_9.png")]
SCORE_IMG_SIZE = SCORE_IMGS[0].get_size()  # 分数的数字图片的大小
SCORE_CENTER = (int(SCREEN_SIZE[0] / 2 - SCORE_IMG_SIZE[0] / 2), int(SCREEN_SIZE[1] / 10))  # 分数的中心位置
score = 0  # 分数记录
is_over = False  # 判断是否撞柱子或在地板上
GAME_OVER_IMG = pygame.image.load("Content/Images/text_game_over.png")  # 游戏结束图片
game_over_rect = GAME_OVER_IMG.get_rect()  # 游戏结束图片的矩形
is_start = False  # 是否开始游戏
TITLE_IMG = pygame.image.load("Content/Images/title.png")  # 标题图片
title_rect = TITLE_IMG.get_rect()  # 标题图片的矩形
title_rect.center = screen_rect.center
title_rect.y = 1 / 5 * SCREEN_SIZE[1]
PLAY_IMG = pygame.image.load("Content/Images/button_play.png")  # 开始按钮图片
play_rect = PLAY_IMG.get_rect()  # 开始按钮图片的矩形
play_rect.center = screen_rect.center
play_rect.y = 2 / 3 * SCREEN_SIZE[1] - 10


def score_show() -> None:
    """显示分数"""
    score_update()
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


def score_update() -> None:
    """更新分数"""
    global score
    for pipe_up in pipes_up:  # 鸟图中心x坐标=柱子中心x坐标时 即加分
        if bird.rect.center[0] == pipe_up.x:
            BIRD_POINT_SE.play()
            score += 1


def check_hit() -> None:
    """判断是否撞墙"""
    global is_over
    for pipe_up in pipes_up:
        if pipe_up.mask.overlap(bird.mask, (bird.rect.x - pipe_up.rect.x, bird.rect.y - pipe_up.rect.y)):
            # overlap(mask, (x差, y差))
            BIRD_HIT_SE.play()
            is_over = True
            print("HIT: PIPE_UP")
            break
    for pipe_down in pipes_down:
        if is_over:
            break
        if pipe_down.mask.overlap(bird.mask, (bird.rect.x - pipe_down.rect.x, bird.rect.y - pipe_down.rect.y)):
            BIRD_HIT_SE.play()
            is_over = True
            print("HIT: PIPE_DOWN")
            break
    # for pipe_up in pipes_up:
    #     if (pipe_up.rect.x - BIRD_IMG_SIZE[0] / 2) <= bird.rect.x \
    #             <= (pipe_up.rect.x + PIPE_IMG_SIZE[0] + BIRD_IMG_SIZE[0] / 2):
    #         if (bird.rect.y >= pipe_up.rect.midbottom[1] + PIPE_VERTICAL - BIRD_IMG_SIZE[1] / 2) or \
    #                 (bird.rect.y <= pipe_up.rect.midbottom[1] + BIRD_IMG_SIZE[1] / 2):
    #             is_over = True  # 上管道下边缘 和 下管道上边缘
    #             print("HIT: PIPE")  # test


def start_show() -> None:
    """开始界面"""
    screen_img.blit(TITLE_IMG, title_rect)
    screen_img.blit(PLAY_IMG, play_rect)
    pass


def check_over() -> None:
    """游戏结束"""
    if is_over:
        game_over_rect.midtop = screen_rect.midbottom
        while True:  # 游戏结束界面
            game_clk.tick(120)  # 刷新率为120fps
            for __event in pygame.event.get():
                if __event.type == pygame.QUIT:  # 系统事件-关闭
                    print("退出游戏...")
                    pygame.quit()  # 退出PyGame程序
                    sys.exit()  # 退出Python程序
                if __event.type == pygame.KEYDOWN:  # 系统事件-按下按键
                    if __event.key == pygame.K_q:  # 按下"Q"
                        print("退出游戏...")
                        pygame.quit()  # 退出PyGame程序
                        sys.exit()  # 退出Python程序
            render_screen("over")


def over_show() -> None:
    """游戏结束画面"""
    if game_over_rect.centery >= screen_rect.centery:
        game_over_rect[1] -= 0.5
    screen_img.blit(GAME_OVER_IMG, game_over_rect)


def restart() -> None:
    """重置游戏"""
    pass


def render_screen(option="game") -> None:
    """刷新渲染画面
    :param option -> str 渲染的场景"""
    if option == "game":  # 主要游戏画面
        bg_show()  # 图层1: 背景
        pipe_show()  # 图层2: 管道
        land_show()  # 图层3: 地板
        score_show()  # 图层4: 分数
        bird.show()  # 图层5: 鸟
        # render_text("Time:" + str(int(time.perf_counter() - time_start)).rjust(3, '0') + "s", 16,
        #             fg_color=rgb_color.green)  # 图层6: 时间
        # render_text("Time:" + str(int(time.perf_counter() - time_start)).rjust(3, '0') + "s" + str(frame) + "frames",
        #             12, (100, 0), fg_color=rgb_color.green, bg_color=rgb_color.black)  # test
        # print(frame/(time.perf_counter() - time_start))  # test 输出刷新率
        # render_text("FPS " + str(int(frame/(time.perf_counter() - time_start))),
        #             10, fg_color=rgb_color.green)  # test 在左上角显示帧率
        pygame.display.update()  # 刷新画面
    elif option == "over":  # 游戏结束画面
        bg_show(False)  # 图层1: 背景
        pipe_show(False)  # 图层2: 管道
        land_show(False)  # 图层3: 地板
        score_show()  # 图层4: 分数
        bird.show(False)  # 图层5: 鸟
        over_show()  # 图层6: 结束
        pygame.display.update()  # 刷新画面
    elif option == "start":  # 游戏开始画面
        bg_show()  # 图层1: 背景
        land_show()  # 图层2: 地板
        if bird.speed > 2:
            bird.speed = -2
        bird.show()  # 图层3: 鸟
        start_show()  # 图层4: 标题与开始按钮
        pygame.display.update()  # 刷新画面


# 主程序循环
time_start = time.perf_counter()  # 开始计时
# frame = 0  # test 刷新次数
while True:  # 开始界面
    game_clk.tick(120)  # 刷新率为120fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 系统事件-关闭
            print("退出游戏...")
            pygame.quit()  # 退出PyGame程序
            sys.exit()  # 退出Python程序
        if event.type == pygame.KEYDOWN:  # 系统事件-按下按键
            # print(event, event.key)  # 控制台输出键盘按下事件
            # print(pygame.key.get_pressed())  # 控制台输出按下的按键
            if event.key == pygame.K_SPACE:  # 按下"SPACE"
                is_start = True
                break
            if event.key == pygame.K_q:  # 按下"Q"
                print("退出游戏...")
                pygame.quit()  # 退出PyGame程序
                sys.exit()  # 退出Python程序
    render_screen("start")  # 刷新渲染画面
    if is_start:
        break
while True:  # 游戏时界面
    game_clk.tick(120)  # 刷新率为120fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 系统事件-关闭
            print("退出游戏...")
            pygame.quit()  # 退出PyGame程序
            sys.exit()  # 退出Python程序
        if event.type == pygame.KEYDOWN:  # 系统事件-按下按键
            # print(event, event.key)  # 控制台输出键盘按下事件
            # print(pygame.key.get_pressed())  # 控制台输出按下的按键
            if event.key == pygame.K_SPACE:  # 按下"SPACE"
                bird.up()
            if event.key == pygame.K_q:  # 按下"Q"
                print("退出游戏...")
                pygame.quit()  # 退出PyGame程序
                sys.exit()  # 退出Python程序
    # frame += 1  # test 刷新次数+1
    # print("pipes_up[0].rect.midbottom: " + str(pipes_up[0].rect.midbottom))
    # print("pipes_up[0].rect.x, .y: " + str(pipes_up[0].rect.x) + " " + str(pipes_up[0].rect.y))
    check_hit()
    check_over()
    render_screen()  # 刷新渲染画面
