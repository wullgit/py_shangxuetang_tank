'''
v1.06
    新增功能：
    加载我方坦克

'''
import pygame
#设置一个全局变量，对pygame.display重命名
_display = pygame.display
#设置颜色变量，全局变量
COLOR_BLACK = pygame.Color(0,0,0)
COLOR_RED = pygame.Color(255,0,0)
version = 'v1.06'

class MainGame():
    #游戏主窗口对象
    window = None
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    #创建我方坦克
    TANK_P1 = None

    def __init__(self):
        pass
    #开始游戏方法
    def startGame(self):
        _display.init()
        #创建窗口加载游戏（借鉴官方文档）
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        #创建我方坦克
        MainGame.TANK_P1 = Tank(400,300)
        #设置一下游戏标题
        _display.set_caption('坦克大战'+version)
        #让窗口持续刷新操作：解决窗口一闪就关闭，而是持续打开
        while True:
            #给窗口完成一个填充颜色
            MainGame.window.fill(COLOR_BLACK)
            #在循环中持续完成事件的获取
            self.getEvent()
            #将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.getTextSurface('剩余敌方坦克%d辆'%5),(5,5))
            #将我方坦克加入到窗口中
            MainGame.TANK_P1.displayTank()
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

    #左上角问题绘制的功能
    def getTextSurface(self,text):
        #初始化字体模块
        pygame.font.init()
        #查看系统支持的所有字体
        # fontList = pygame.font.get_fonts()
        # print(fontList)
        #选中一个合适的字体，如果最后弹窗中字体显示不出来或者为乱码，则是对字体不识别，需要更换
        font = pygame.font.SysFont('microsoftyaheiui',18)
        #使用对应的字符完成相关内容的绘制
        textSurface = font.render(text,True,COLOR_RED)
        return textSurface
    #结束游戏方法
    def endGame(self):
        print('谢谢使用')
        #结束python解释器
        exit()

class Tank():
    def __init__(self,left,top):
        self.images = {
            'U':pygame.image.load('img/P1_U.png'),
            'D':pygame.image.load('img/P1_D.png'),
            'L':pygame.image.load('img/P1_L.png'),
            'R':pygame.image.load('img/P1_R.png')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        #坦克所在的区域
        self.rect = self.image.get_rect()
        #手动指定坦克的初始化位置，分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top

    #坦克的移动方法
    def move(self):
        pass

    #射击方法
    def shot(self):
        pass

    #展示坦克（将坦克这个surface绘制到窗口中，blit()）
    def displayTank(self):
        #1、重新设置坦克的图片
        self.image = self.images[self.direction]
        #2、将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)

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