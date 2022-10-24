'''
v1.04
    新增功能：
    事件处理：
        点击关闭按钮，退出程序的事件
        方向控制，子弹发射

'''
import pygame
#设置一个全局变量，对pygame.display重命名
_display = pygame.display
#设置颜色变量，全局变量
COLOR_BLACK = pygame.Color(0,0,0)
version = 'v1.04'

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
        _display.set_caption('坦克大战'+version)
        #让窗口持续刷新操作：解决窗口一闪就关闭，而是持续打开
        while True:
            #给窗口完成一个填充颜色
            MainGame.window.fill(COLOR_BLACK)
            #在循环中持续完成事件的获取
            self.getEvent()
            #窗口的刷新
            _display.update()

    #获取程序期间所有事件（鼠标事件、键盘事件）
    def getEvent(self):
        #1:获取所有事件
        eventList = pygame.event.get()
        #2:对事件进行判断处理（1、点击关闭按钮2、按下键盘上的某个按键）
        for event in eventList:
            #判断event.type是否为QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            #判断事件类型是否为按键按下，如果是，继续判断按键是哪一个按键，来进行对应的处理
            if event.type == pygame.KEYDOWN:
                #具体是哪一个按键的处理
                if event.key == pygame.K_LEFT:
                    print('坦克向左调头，移动')
                elif event.key == pygame.K_RIGHT:
                    print('坦克向右调头，移动')
                elif event.key == pygame.K_UP:
                    print('坦克向上调头，移动')
                elif event.key == pygame.K_DOWN:
                    print('坦克向下调头，移动')
                elif event.key == pygame.K_SPACE:
                    print('发射子弹')
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