# coding=utf-8
# Python 3.10
# written by zyf in 2022/07/23 00:46
# finished in 2022/07/25 13:20
# Update: Changed identifiers of some invariants to all caps and underscores. 2022/08/03 16:54
import pygame
import time
import sys
import random
import os
# 以下为自建库
import rgb_color


# 报错libpng，将图片均使用ImageMagick Display打开保存即可
# 下载地址: https://www.imagemagick.org/script/download.php


def render_text(txt: str, size: int, coor=(0, 0), fg_color=rgb_color.black, bg_color=rgb_color.white,
                font="Times New Roman") -> None:
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
    screen_image.blit(txt_img, txt_rect)  # 在画面中应用文字图像与其矩形


# 1 初始化画面
os.chdir(os.path.dirname(__file__))  # 将本文件所在目录作为工作目录
pygame.init()  # 初始化PyGame
SCREEN_SIZE = (960, 852)  # 画面大小
screen_image = pygame.display.set_mode(SCREEN_SIZE)  # 显示画面
screen_rect = screen_image.get_rect()  # 获取画面的矩形
# pygame.key.set_repeat(50, 5)  # (灵敏度, 间隔)，单位为ms 使得按键能被持续按下
pygame.display.set_caption("打飞机都 by zyf written in Python")  # 更改PyGame程序标题
pygame.display.set_icon(pygame.image.load("images/icon.jpg"))  # 更改PyGame程序图标

# 2 添加背景与音乐
BG_IMG = pygame.image.load("images/background.png")  # 导入背景图片
BG_RECT = BG_IMG.get_rect()  # 得到背景图片的矩形
BG_RECT.topleft = (0, 0)  # 使得背景铺满整个游戏画面
screen_image.blit(BG_IMG, BG_RECT)  # 在画面中应用背景图片与其矩形
# 添加背景音乐
pygame.mixer.music.load("se/Souleye - Pressure cooker.mp3")  # 导入背景音乐
pygame.mixer.music.play(-1)  # 设置为单曲循环
pygame.mixer.music.set_volume(0.1)  # 设置音量
# 添加爆炸音效
BOOM_SE = pygame.mixer.Sound("se/exp.wav")  # 导入音效
BOOM_SE.set_volume(0.1)  # 设置音量


# 3 玩家
class Speed:
    """初始化速度"""

    def __init__(self, x=0, y=0) -> None:
        self.x = x  # 横向速度
        self.y = y  # 纵向速度


PLAYER_IMGS = [pygame.image.load("images/hero1.png"), pygame.image.load("images/hero2.png"),
               pygame.image.load("images/hero_blowup_n1.png"), pygame.image.load("images/hero_blowup_n2.png"),
               pygame.image.load("images/hero_blowup_n3.png"), pygame.image.load("images/hero_blowup_n4.png")]
player_img = pygame.image.load("images/hero1.png")  # 导入玩家图片
player_img_size = player_img.get_size()  # 获得玩家图片的大小
player_rect = player_img.get_rect()  # 得到玩家图片的矩形
player_rect.midbottom = screen_rect.midbottom  # 将玩家图片的底部与画面底部对齐
player_rect.y -= 50  # 向上50px
player_speed = Speed()  # 玩家速度初始化
PLAYER_FLY_SPEED = 5  # 玩家飞行速度的固定值


class Player:
    """玩家类"""

    @staticmethod
    def shoot() -> None:
        """发射子弹"""
        global bullets
        bullets.append(Bullet())

    @staticmethod
    def show() -> None:
        """显示玩家"""
        player_rect.x += player_speed.x
        player_rect.y += player_speed.y
        # 边缘保护
        if player_rect.x < 0:  # 横向边缘保护
            player_rect.x = 0
        elif player_rect.x > SCREEN_SIZE[0] - player_img_size[0]:
            player_rect.x = SCREEN_SIZE[0] - player_img_size[0]
        if player_rect.y < 0:  # 纵向边缘保护
            player_rect.y = 0
        elif player_rect.y > SCREEN_SIZE[1] - player_img_size[1]:
            player_rect.y = SCREEN_SIZE[1] - player_img_size[1]
        screen_image.blit(player_img, player_rect)


# 4 子弹
BULLET_IMG = pygame.image.load("images/bullet1.png")  # 导入子弹图片
BULLET_IMG_SIZE = BULLET_IMG.get_size()  # 得到子弹图片的大小信息
bullet_rect = BULLET_IMG.get_rect()  # 得到子弹图片的矩形
bullets = []  # 初始化子弹


class Bullet:
    """子弹"""

    def __init__(self, speed=None) -> None:
        """初始化子弹

        :param speed: -> float 子弹速度，默认为5.0
        """
        if speed is None:
            speed = 5.0
        self.rect = BULLET_IMG.get_rect()  # 获得子弹图片的矩形
        self.rect.midbottom = player_rect.midtop  # 子弹矩形的中下与玩家矩形的中上重合
        self.speed = speed  # 子弹速度

    def show(self, mode=True) -> None:
        """更新子弹位置和图像

        :param mode: -> boolean 默认为True即更新位置，为False则不更新位置
        """
        if mode:
            self.rect.y -= self.speed  # 往上飞
            if self.rect.y < BULLET_IMG_SIZE[1]:  # 飞出屏幕则删除
                bullets.remove(self)
        screen_image.blit(BULLET_IMG, self.rect)  # 应用子弹图片与其矩形

    def hit_check(self) -> None:
        """检测与敌人的碰撞"""
        global score
        if enemies:
            for enemy in enemies:
                if distance(enemy.coor, self.rect) < 50:  # 与敌人碰撞
                    print(f"射中啦... {enemies.index(enemy)}")
                    score += 1  # 增加分数
                    try:
                        bullets.remove(self)  # 删除子弹
                    except ValueError:
                        pass
                    enemy.reset()  # 重置敌人


def distance(coor1=(0, 0), coor2=(0, 0), mode=0) -> float:
    """计算两点的距离

    :param coor1: 第一个点的二维坐标
    :param coor2: 第二个点的二维坐标
    :param mode: 计算方式，默认为0即曼哈顿距离，为1即欧几里得距离的平方
    """
    if mode:
        return (coor1[0] - coor2[0]) ** 2 + (coor1[1] - coor2[1]) ** 2
    else:
        return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])


def bullet_show() -> None:
    """更新子弹位置和图像"""
    for bullet in bullets:
        bullet.show()
        bullet.hit_check()


# 5 敌人
ENEMY_IMG = pygame.image.load("images/enemy1.png")  # 导入敌人图片
enemy_rect = ENEMY_IMG.get_rect()  # 获得敌人图片的矩形
ENEMY_IMG_SIZE = ENEMY_IMG.get_size()  # 获得敌人图片的大小
ENEMY_NUM = 5  # 敌人数量
enemies = []  # 初始化敌人


class Enemy:
    """敌人"""

    def __init__(self, coor=None, speed=None) -> None:
        """初始化敌人

        :param coor: -> list = [int, int] 起始坐标
        :param speed: -> list = [float, float] 横向与纵向速度，默认为[2.0, 15.0]"""
        if speed is None:
            speed = [2.0, 15.0]
        if coor is None:
            coor = [random.randint(100, 800), random.randint(-20, 20)]
        self.img = ENEMY_IMG  # 导入敌人的图片
        self.rect = enemy_rect  # 获得敌人的矩形
        self.coor = coor  # 起始坐标
        self.rect.center = self.coor  # 将坐标应用到矩形中
        # 设置敌人横向移动范围
        self.range = [self.coor[0] - random.randint(0, 600), self.coor[0] + random.randint(0, 600)]
        if self.range[0] < 0:  # 如果横向移动的范围超出画面左侧，则将范围左侧设为画面左侧
            self.range[0] = 0
        if self.range[1] > SCREEN_SIZE[0] - ENEMY_IMG_SIZE[0]:  # 如果横向移动的范围超出画面右侧，则将范围左侧设为画面右侧
            self.range[1] = SCREEN_SIZE[0] - ENEMY_IMG_SIZE[0]
        self.fly_speed = speed  # 速度
        self.isdead = False

    def show_update(self) -> None:
        """更新enemy位置和图像"""
        self.coor[0] += self.fly_speed[0]  # 横坐标
        if self.coor[0] < self.range[0] or self.coor[0] > self.range[1]:
            self.fly_speed[0] *= -1  # 达到范围边界则横向反向飞行
            self.coor[1] += self.fly_speed[1]  # 达到范围边界则下降
        self.rect.center = self.coor  # 将坐标应用到矩形中
        screen_image.blit(self.img, self.rect)

    def reset(self) -> None:
        """敌人死亡后重新生成"""
        BOOM_SE.play()  # 播放爆炸音效
        self.fly_speed[0] = abs(self.fly_speed[0])
        self.fly_speed[0] += 1.0  # 增加飞行速度
        self.fly_speed[1] += 1.0  # 增加飞行速度
        # 以下是常规生成敌人的项目
        coor = [random.randint(100, 800), random.randint(-20, 20)]
        self.coor = coor  # 起始坐标
        self.rect.center = self.coor  # 将坐标应用到矩形中
        self.range = [self.coor[0] - random.randint(0, 600), self.coor[0] + random.randint(0, 600)]
        if self.range[0] < 0:  # 如果横向移动的范围超出画面左侧，则将范围左侧设为画面左侧
            self.range[0] = 0
        if self.range[1] > SCREEN_SIZE[0] - ENEMY_IMG_SIZE[0]:  # 如果横向移动的范围超出画面右侧，则将范围左侧设为画面右侧
            self.range[1] = SCREEN_SIZE[0] - ENEMY_IMG_SIZE[0]
        pass

    def dead(self) -> None:
        """敌人死亡"""
        # 这里想实现一个死亡动画来着。。。
        pass


def enemy_show() -> None:
    """更新敌人位置与图像"""
    global game_over
    for e in enemies:
        e.show_update()
        screen_image.blit(e.img, e.rect)
        if e.rect.y > SCREEN_SIZE[1] or e.rect.colliderect(player_rect):
            game_over = True  # 如果超出底边或碰到玩家则游戏结束
            print(f"游戏结束... {enemies.index(e)}")
            enemies.clear()


for _ in range(ENEMY_NUM):  # 生成敌人
    enemies.append(Enemy())

# 6 游戏相关
score = 0
game_over = False
OVER_IMG = pygame.image.load("images/game_over_.png")
OVER_IMG_RECT = OVER_IMG.get_rect()
OVER_IMG_RECT.center = screen_rect.center


# 游戏主循环
class Check:
    """按键检测"""

    @staticmethod
    def game() -> None:
        """判断游戏中按键"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 系统事件-关闭
                print("游戏已退出...")
                pygame.quit()  # 退出PyGame程序
                sys.exit()  # 退出程序
            Check.movement()
            # 控制射击
            if event.type == pygame.KEYDOWN:  # 系统事件-按下按键
                if event.key == pygame.K_SPACE:  # 按下"SPACE"
                    Player.shoot()
                if event.key == pygame.K_q:  # 按下"q"
                    print("游戏已退出...")
                    pygame.quit()  # 退出PyGame程序
                    sys.exit()  # 退出程序

    @staticmethod
    def movement() -> None:
        """判断移动相关按键"""
        global player_img
        key_pressed = pygame.key.get_pressed()  # 获取按下的按键
        if key_pressed[pygame.K_a] and key_pressed[pygame.K_d]:  # 按下了"a"和"d"
            player_speed.x = 0  # 横向速度=0
        elif key_pressed[pygame.K_a]:  # 只按下了"a"
            player_speed.x = -PLAYER_FLY_SPEED  # 给予向左的速度
        elif key_pressed[pygame.K_d]:  # 只按下了"d"
            player_speed.x = PLAYER_FLY_SPEED  # 给予向右的速度
        else:
            player_speed.x = 0  # 横向速度=0
        # 控制纵向速度
        if key_pressed[pygame.K_w] and key_pressed[pygame.K_s]:  # 按下了"w"和"s"
            player_speed.y = 0  # 纵向速度=0
        elif key_pressed[pygame.K_w]:  # 只按下了"w"
            player_speed.y = -PLAYER_FLY_SPEED  # 给予向上的速度
        elif key_pressed[pygame.K_s]:  # 只按下了"s"
            player_speed.y = PLAYER_FLY_SPEED  # 给予向下的速度
        else:
            player_speed.y = 0  # 纵向速度=0
        # # 边缘保护
        # if player_rect.x < 0 or player_rect.x > screen_size[0] - player_img_size[0]:  # 横向边缘保护
        #     player_speed.x = 0
        # if player_rect.y < 0 or player_rect.y > screen_size[1] - player_img_size[1]:  # 纵向边缘保护
        #     player_speed.y = 0
        # 移动与静止时的图片
        if player_speed.x == 0 and player_speed.y == 0:
            player_img = PLAYER_IMGS[1]
        else:
            player_img = PLAYER_IMGS[0]


def over_show():
    """游戏结束的显示"""
    while 1:
        check_quit()
        screen_image.blit(OVER_IMG, OVER_IMG_RECT)  # 应用游戏结束的图片
        pygame.display.update()


def check_quit():
    """判断程序退出"""
    for event_ in pygame.event.get():
        if event_.type == pygame.QUIT:  # 系统事件-关闭
            print("游戏已退出...")
            pygame.quit()  # 退出PyGame程序
            sys.exit()  # 退出程序
        if event_.type == pygame.KEYDOWN:  # 系统事件-按下按键
            if event_.key == pygame.K_q:  # 按下"q"
                print("游戏已退出...")
                pygame.quit()  # 退出PyGame程序
                sys.exit()  # 退出程序


time_start = time.perf_counter()  # 开始计时
while 1:
    screen_image.blit(BG_IMG, BG_RECT)  # 画面图层1: 背景
    Check.game()  # 游戏中的按键检测
    enemy_show()  # 画面图层2: 敌人
    bullet_show()  # 画面图层3: 子弹
    Player.show()  # 画面图层4: 玩家
    render_text(f"Score:{score}", 32, (SCREEN_SIZE[0] / 2 - 50, 0))  # 画面图层5: 分数
    render_text("Time:" + str(int(time.perf_counter() - time_start)).rjust(3, '0') + "s", 25,
                fg_color=rgb_color.green, bg_color=rgb_color.black)  # 画面图层6: 时间
    if game_over:  # 检测是否游戏结束
        over_show()
    pygame.display.update()
