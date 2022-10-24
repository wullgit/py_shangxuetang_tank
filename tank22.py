'''
v1.22
    新增功能：
        1、实现子弹不可以穿墙
        2、实现子弹可以打掉墙壁生命值

'''
import pygame,time,random
#设置一个全局变量，对pygame.display重命名
_display = pygame.display
#设置颜色变量，全局变量
COLOR_BLACK = pygame.Color(0,0,0)
COLOR_RED = pygame.Color(255,0,0)
version = 'v1.22'

class MainGame():
    #游戏主窗口对象
    window = None
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    #创建我方坦克
    TANK_P1 = None
    #存储所有敌方坦克
    EnemyTank_list = []
    #要创建的敌方坦克的数量
    EnemyTank_count = 5
    #存储我方子弹的列表
    Bullet_list = []
    #存储敌方子弹的列表
    Enemy_bullet_list = []
    #爆炸效果列表
    Explode_list = []
    #墙壁列表
    Wall_list = []

    def __init__(self):
        pass
    #开始游戏方法
    def startGame(self):
        _display.init()
        #创建窗口加载游戏（借鉴官方文档）
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        #调用创建我方坦克的方法
        self.createMyTank()
        #创建敌方坦克
        self.createEnemyTank()
        #调用创建墙壁的方法
        self.createWalls()

        #设置一下游戏标题
        _display.set_caption('坦克大战'+version)
        #让窗口持续刷新操作：解决窗口一闪就关闭，而是持续打开
        while True:
            #给窗口完成一个填充颜色
            MainGame.window.fill(COLOR_BLACK)
            #在循环中持续完成事件的获取
            self.getEvent()
            #将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.getTextSurface('剩余敌方坦克%d辆'%len(MainGame.EnemyTank_list)),(5,5))
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                # 将我方坦克加入到窗口中
                MainGame.TANK_P1.displayTank()
            else:
                del MainGame.TANK_P1
                #设置我方坦克为None，同时需要在地方子弹显示在窗口中
                # 对敌方子弹与我方坦克碰撞的调用方法进行判断我方坦克不为None
                MainGame.TANK_P1 = None
            #循环展示敌方坦克
            self.blitEnemyTank()
            #根据坦克的开关状态调用坦克的移动方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                #调用碰撞墙壁的方法
                # MainGame.TANK_P1.hitWalls()

            #调用渲染子弹列表的一个方法
            self.blitBullet()
            #调用渲染敌方子弹列表的一个方法
            self.blitEnemyBullet()
            #调用展示爆炸效果的方法
            self.displayExplodes()
            #调用展示墙壁的方法
            self.blitWalls()
            #设置休眠时间，用于控制刷新频率，来达到移动速度减慢
            time.sleep(0.02)
            #窗口的刷新
            _display.update()

    #创建我方坦克
    def createMyTank(self):
        MainGame.TANK_P1 = Tank(400, 300)

    #创建敌方坦克
    def createEnemyTank(self):
        top = 100
        for i in range(MainGame.EnemyTank_count):
            #每次都随机生成一个left值，速度值
            left = random.randint(1, 7)
            speed = random.randint(1, 6)
            eTank = EnemyTank(left*100,top,speed)
            MainGame.EnemyTank_list.append(eTank)

    #创建墙壁的方法
    def createWalls(self):
        for i in range(6):
            wall = Wall(130*i,240)
            MainGame.Wall_list.append(wall)
    #将墙壁加入到窗口中
    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)
    #将敌方坦克加入到窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                # 敌方坦克随机移动的方法
                eTank.randMove()
                #调用敌方坦克与墙壁的碰撞方法
                # eTank.hitWalls()
                # 调用敌方坦克的射击
                eBullet = eTank.shot()
                # 如果子弹为None，不加入到列表
                if eBullet:
                    # 将子弹存储敌方坦克列表，
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    #将子弹加入到窗口中
    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            #如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if bullet.live:
                bullet.displayBullet()
                #让子弹移动
                bullet.bulletMove()
                #调用我方子弹与敌方坦克的碰撞方法
                bullet.hitEnemyTank()
                #调用判断我方子弹是否碰撞到墙壁的方法
                bullet.hitWalls()
            else:
                MainGame.Bullet_list.remove(bullet)

    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            #如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if eBullet.live:
                eBullet.displayBullet()
                #让子弹移动
                eBullet.bulletMove()
                #调用敌方子弹与我方坦克的碰撞方法
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()
                # 调用判断敌方子弹是否碰撞到墙壁的方法
                eBullet.hitWalls()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)
    #新增方法：展示效果列表
    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_list.remove(explode)
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
                #点击ESC按键让我方坦克重生
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:
                    #调用创建我方坦克的方法
                    self.createMyTank()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    #具体是哪一个按键的处理
                    if event.key == pygame.K_LEFT:
                        print('坦克向左调头，移动')
                        #修改坦克方向
                        MainGame.TANK_P1.direction = 'L'
                        #关闭坦克的开关
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print('坦克向右调头，移动')
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'R'
                        # 关闭坦克的开关
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print('坦克向上调头，移动')
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'U'
                        #关闭坦克的开关
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print('坦克向下调头，移动')
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'D'
                        #关闭坦克的开关
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        print('发射子弹')
                        if len(MainGame.Bullet_list)<3:
                            # 产生一颗子弹
                            m = Bullet(MainGame.TANK_P1)
                            # 将子弹加入到子弹列表
                            MainGame.Bullet_list.append(m)
                        else:
                            print('子弹数量不足')
                        print('当前屏幕中的子弹数量为：%d'%len(MainGame.Bullet_list))
            #按键松开判断
            if event.type == pygame.KEYUP:
                #松开的如果是方向键，才更改移动开关状态
                # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                #     or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                #     #修改坦克的移动状态
                #     MainGame.TANK_P1.stop = True

                if event.key in [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN]:
                    #在我方坦克存在，且活着，才可修改移动状态
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        #修改坦克的移动状态
                        MainGame.TANK_P1.stop = True


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

class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Tank(BaseItem):
    def __init__(self,left,top):
        self.images = {
            'U':pygame.image.load('img/WU.gif'),
            'D':pygame.image.load('img/WD.gif'),
            'L':pygame.image.load('img/WL.gif'),
            'R':pygame.image.load('img/WL.gif')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        #坦克所在的区域
        self.rect = self.image.get_rect()
        #手动指定坦克的初始化位置，分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        #新增速度属性
        self.speed = 5
        #新增属性：坦克的移动开关
        self.stop = True
        # 新增属性，用来记录坦克是否活着
        self.live = True


    #坦克的移动方法
    def move(self):

        if self.direction == 'L':
            if self.rect.left >0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top >0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    # #还原坦克的位置
    # def stay(self):
    #     self.rect.left = self.oldLeft
    #     self.rect.top = self.oldTop
    #
    # #新增碰撞墙壁的方法
    # def hitWalls(self):
    #     for wall in MainGame.Wall_list:
    #         if pygame.sprite.collide_rect(self,wall):
    #             self.stay()

    #射击方法
    def shot(self):
        return Bullet(self)

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
    def __init__(self,left,top,speed):
        # 因为要用到父类Tank中的live属性，必须先继承父类的初始化方法
        # super(EnemyTank,self).__init__(left,top)
        #Python 3 可以使用直接使用 super().xxx 代替 super(Class, self).xxx
        super().__init__(left,top)
        self.images = {
            'U': pygame.image.load('img/EU.gif'),
            'D': pygame.image.load('img/ED.gif'),
            'L': pygame.image.load('img/EL.gif'),
            'R': pygame.image.load('img/ER.gif')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        # 坦克所在的区域
        self.rect = self.image.get_rect()
        # 手动指定坦克的初始化位置，分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        # 新增属性：坦克的移动开关
        self.stop = True
        #新增步数属性，用来控制敌方坦克随机移动
        self.step = 30


    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    # def displayEnemtTank(self):
    #     super().displayTank()
    #随机移动
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 20
        else:
            self.move()
            self.step -= 1

    def shot(self):
        num = random.randint(1,1000)
        if num <= 20: #注意：如果小于等于20，则返回一个子弹，否则返回None
            return Bullet(self)
class Bullet(BaseItem):
    def __init__(self,tank):
        #图片
        self.images = {
            'U': pygame.image.load('img/MU.gif'),
            'D': pygame.image.load('img/MD.gif'),
            'L': pygame.image.load('img/ML.gif'),
            'R': pygame.image.load('img/MR.gif')
        }
        #方向（坦克方向）
        self.direction = tank.direction
        self.image = self.images[self.direction]
        #位置
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height/2 - self.rect.height/2 #可能是图片的原因，所以使用的1.4
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height/2 - self.rect.height/2

        #速度
        self.speed = 7
        #用来记录子弹是否碰撞
        self.live = True

    #子弹的移动方法
    def bulletMove(self):
        if self.direction == 'L':
            if self.rect.left >0:
                self.rect.left -= self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改状态值
                self.live = False
        elif self.direction == 'U':
            if self.rect.top >0:
                self.rect.top -= self.speed
            else:
                # 修改状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                # 修改状态值
                self.live = False

    #展示子弹
    def displayBullet(self):
        # 1、重新设置子弹的图片
        self.image = self.images[self.direction]
        # 2、将子弹加入到窗口中
        MainGame.window.blit(self.image, self.rect)

    #新增我方子弹碰撞敌方坦克的方法
    def hitEnemyTank(self):
        for eTank in  MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                #产生一个爆炸效果
                explode = Explode(eTank)
                #将爆炸效果加入到爆炸效果列表
                MainGame.Explode_list.append(explode)
                #子弹消失
                self.live = False
                #敌方坦克消失
                eTank.live = False

    #新增敌方子弹与我方坦克的碰撞方法
    def hitMyTank(self):
        if pygame.sprite.collide_rect(self,MainGame.TANK_P1):
            #产生爆炸效果，并加入到爆炸效果列表中
            explode = Explode(MainGame.TANK_P1)
            MainGame.Explode_list.append(explode)
            #修改子弹状态
            self.live = False
            #修改我方坦克状态
            MainGame.TANK_P1.live = False

    #新增子弹与墙壁的碰撞
    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self,wall):
                #修改子弹的live属性
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False

class Explode():
    def __init__(self,tank): #在敌方坦克处爆炸
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/0.gif'),
            pygame.image.load('img/1.gif'),
            pygame.image.load('img/2.gif'),
            pygame.image.load('img/3.gif'),
            pygame.image.load('img/4.gif'),
            pygame.image.load('img/5.gif'),
            pygame.image.load('img/6.gif'),
            pygame.image.load('img/7.gif')
        ]
        self.image = self.images[self.step]
        #通过live判断爆炸效果是否还要在窗口显示
        self.live = True
    #展示爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0
class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('img/iron.png')

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        #用来判断墙壁是否应该在窗口中展示
        self.live = True
        #用来记录墙壁的生命值
        self.hp = 3
    #展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)

class Music():
    def __init__(self):
        pass
    #开始播放音乐
    def play(self):
        pass

MainGame().startGame()