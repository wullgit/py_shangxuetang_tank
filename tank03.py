'''
v1.03
    新增功能：
    创建游戏窗口
    用到游戏引擎中的功能模块
    官方开发文档

'''
import pygame
#设置一个全局变量，对pygame.display重命名
_display = pygame.display
#设置颜色变量，全局变量
COLOR_BLACK = pygame.Color(0,0,0)

class MainGame():
    #游戏主窗口对象
    window = None
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500


    def __init__(self):
        pass
    #开始游戏方法
    def startGame(self):
        _display.init()
        #创建窗口加载游戏（借鉴官方文档）
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        #设置一下游戏标题
        _display.set_caption('坦克大战v1.03')
        #让窗口持续刷新操作：解决窗口一闪就关闭，而是持续打开
        while True:
            #给窗口完成一个填充颜色
            MainGame.window.fill(COLOR_BLACK)
            _display.update()
    #结束游戏方法
    def endGame(self):
        print('谢谢使用')
        #结束python解释器
        exit()

class Tank():
    def __init__(self):
        pass

    #坦克的移动方法
    def move(self):
        pass

    #射击方法
    def shot(self):
        pass

    #展示坦克
    def displayTank(self):
        pass

class MyTank(Tank):
    def __init__(self):
        pass

class EnemyTank(Tank):
    def __init__(self):
        pass

class Bullet():
    def __init__(self):
        pass
    #子弹的移动方法
    def move(self):
        pass
    #展示子弹
    def displayBullet(self):
        pass

class Explode():
    def __init__(self):
        pass
    #展示爆炸效果
    def displayExplode(self):
        pass

class Wall():
    def __init__(self):
        pass
    #展示墙壁的方法
    def displayWall(self):
        pass

class Music():
    def __init__(self):
        pass
    #开始播放音乐
    def play(self):
        pass

MainGame().startGame()