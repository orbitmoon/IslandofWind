#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.font = loader.loadFont('1.ttf')
        self.jiechu1 = 0
        self.jiechu2 = 0
        self.down = 0
        self.menuon = 0
        # ESC退出
        self.accept("escape", self.caidan)
        # 背景
        self.beijing = OnscreenImage(
            image='1.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1))
        # 开始游戏碰之前图片
        self.a1 = OnscreenImage(image='button3.png',
                               pos=(-0.8, 0, 0.7), scale=(0.2, 0.1, 0.071))
        # 碰到开始游戏后显示的按钮
        self.zjmkaishi = DirectButton(text=('', '', '', 'disabled'), image='button2.png', frameColor=(255, 255, 255, 0),
                              image_scale=(2, 1, 0.7), pos=(-0.8, 0, 0.7), scale=0.1, command=self.putdown)
        self.zjmkaishi.hide()
        # 点击开始游戏后图片
        self.c1 = OnscreenImage(image='button1.png',
                               pos=(-0.8, 0, 0.7), scale=(0.2, 0.1, 0.071))
        self.c1.hide()
        # 开始游戏显示的文字
        self.textObjectstart1 = OnscreenText(
            text='开始游戏', pos=(-0.8, 0.68, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.textObjectstart2 = OnscreenText(
            text='开始游戏', pos=(-0.8, 0.68, 0), scale=0.055, fg=(255, 255, 255, 1))
        self.textObjectstart2.hide()
        self.textObjectstart3 = OnscreenText(
            text='开始游戏', pos=(-0.8, 0.68, 0), scale=0.06, fg=(255, 255, 255, 1))
        self.textObjectstart3.hide()
        self.textObjectstart1.setFont(self.font)
        self.textObjectstart2.setFont(self.font)
        self.textObjectstart3.setFont(self.font)

        # 退出游戏碰之前图片
        self.a2 = OnscreenImage(image='button3.png',
                               pos=(-0.8, 0, 0.5), scale=(0.2, 0.1, 0.071))
        # 碰到退出游戏后显示的按钮
        self.zjmkaishi2 = DirectButton(text=('', '', '', 'disabled'), image='button2.png', frameColor=(255, 255, 255, 0),
                              image_scale=(2, 1, 0.7), pos=(-0.8, 0, 0.5), scale=0.1, command=self.quit)
        self.zjmkaishi2.hide()
        # 点击退出游戏后图片
        self.c2 = OnscreenImage(image='button1.png',
                               pos=(-0.8, 0, 0.5), scale=(0.2, 0.1, 0.071))
        self.c2.hide()
        # 退出游戏显示的文字
        self.textObjectstart4 = OnscreenText(
            text='退出', pos=(-0.8, 0.48, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.textObjectstart5 = OnscreenText(
            text='退出', pos=(-0.8, 0.48, 0), scale=0.055, fg=(255, 255, 255, 1))
        self.textObjectstart5.hide()
        self.textObjectstart6 = OnscreenText(
            text='退出', pos=(-0.8, 0.48, 0), scale=0.06, fg=(255, 255, 255, 1))
        self.textObjectstart6.hide()
        self.textObjectstart4.setFont(self.font)
        self.textObjectstart5.setFont(self.font)
        self.textObjectstart6.setFont(self.font)

        # ESC菜单
        self.caidanjiemian = OnscreenImage(
            image='caidan.jpg', pos=(0, 0, 0), scale=(0.5, 0.1, 0.41))
        self.caidanjiemian.hide()

        self.bangzhu1button = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                              image_scale=(2.2, 1, 0.7), pos=(0, 0, 0.23), scale=0.1, command=self.putdown1)
        self.bangzhu1button.hide()
        self.bangzhu1 = OnscreenText(text='游戏帮助', pos=(0, 0.21, 0), scale=0.05,fg=(255, 255, 255, 1))
        self.bangzhu1.setFont(self.font)
        self.bangzhu1.hide()

        self.bangzhu2button = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                              image_scale=(2.2, 1, 0.7), pos=(0, 0, 0.03), scale=0.1, command=self.putdown2)
        self.bangzhu2button.hide()
        self.bangzhu2 = OnscreenText(text='继续游戏', pos=(0, 0.01, 0), scale=0.05,fg=(255, 255, 255, 1))
        self.bangzhu2.setFont(self.font)
        self.bangzhu2.hide()

        self.bangzhu3button = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                              image_scale=(2.2, 1, 0.7), pos=(0, 0, -0.18), scale=0.1, command=self.putdown3)
        self.bangzhu3button.hide()
        self.bangzhu3 = OnscreenText(text='退出游戏', pos=(0, -0.2, 0), scale=0.05,fg=(255, 255, 255, 1))
        self.bangzhu3.setFont(self.font)
        self.bangzhu3.hide()

        self.bangzhujiemian = OnscreenImage(
            image='caidan.jpg', pos=(-0, 0, 0), scale=(1, 0.1, 0.81))
        self.bangzhujiemian.hide()
        self.bangzhuxinxi = OnscreenText(
            text='coooooooooooooooool', pos=(0, 0, 0), scale=0.1)
        self.bangzhuxinxi.hide()
        self.bangzhuxinxibutton = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                              image_scale=(2.2, 1, 0.7), pos=(0.55, 0, -0.55), scale=0.1, command=self.help1)
        self.bangzhuxinxibutton.hide()
        self.bangzhuxinxi1 = OnscreenText(
            text='返回', pos=(0.55, -0.56, 0), scale=0.05,fg=(255, 255, 255, 1))
        self.bangzhuxinxi1.setFont(self.font)
        self.bangzhuxinxi1.hide()

        taskMgr.add(self.example, 'MyTaskName')

# 按下ESC触发
    def caidan(self):
        if(self.menuon == 0):
            self.menuon = 1
            self.caidanjiemian.show()
            self.bangzhu1button.show()
            self.bangzhu2button.show()
            self.bangzhu3button.show()
            self.bangzhu1.show()
            self.bangzhu2.show()
            self.bangzhu3.show()
        else:
            self.menuon = 0
            self.caidanjiemian.hide()
            self.bangzhu1button.hide()
            self.bangzhu2button.hide()
            self.bangzhu3button.hide()
            self.bangzhu1.hide()
            self.bangzhu2.hide()
            self.bangzhu3.hide()
            self.bangzhujiemian.hide()
            self.bangzhuxinxi.hide()
            self.bangzhuxinxi1.hide()
            self.bangzhuxinxibutton.hide()

# 无限循环
    def example(self, task):
        mpos = base.mouseWatcherNode.getMouse()
        if mpos.getY() < 0.77 and mpos.getY() > 0.63 and mpos.getX() > -0.75 and mpos.getX() < -0.45:
        	# print(mpos.getX())
        	self.jiechu1 = 1
        elif mpos.getY() < 0.57 and mpos.getY() > 0.43 and mpos.getX() > -0.75 and mpos.getX() < -0.45:
            self.jiechu2 = 1
        else:
            self.jiechu1=0
            self.jiechu2=0
       	if(self.jiechu1 == 1 and self.down == 0):
       	    self.zjmkaishi.show()
            #self.textObjectstart1.hide()
            self.textObjectstart2.show()
        elif(self.jiechu2 == 1 and self.down == 0): 
            self.zjmkaishi2.show()
            #self.textObjectstart4.hide()
            self.textObjectstart5.show()
       	else:
            self.zjmkaishi.hide()
            self.textObjectstart2.hide()
            self.textObjectstart1.show()
            self.zjmkaishi2.hide()
            self.textObjectstart5.hide()
            self.textObjectstart4.show()
        return task.cont
        # return task.done
# 按下开始游戏触发
    def putdown(self):
        print('start')
        self.down=1
        self.a1.hide()
        self.zjmkaishi.hide()
        self.c1.show()
        self.textObjectstart1.hide()
        self.textObjectstart2.hide()
        self.textObjectstart3.show()
# 按下退出游戏触发
    def quit(self):
        print('exit')
        self.down=1
        self.a2.hide()
        self.zjmkaishi2.hide()
        self.c2.show()
        self.textObjectstart4.hide()
        self.textObjectstart5.hide()
        self.textObjectstart6.show()
# 按下菜单界面按钮触发
    def putdown1(self):
            self.caidanjiemian.hide()
            self.bangzhu1button.hide()
            self.bangzhu2button.hide()
            self.bangzhu3button.hide()
            self.bangzhu1.hide()
            self.bangzhu2.hide()
            self.bangzhu3.hide()
            self.bangzhujiemian.show()
            self.bangzhuxinxi.show()
            self.bangzhuxinxibutton.show()
            self.bangzhuxinxi1.show()
    def putdown2(self):
        print(2)
    def putdown3(self):
        print(3)
        # self.b.show()
#按下帮助界面的返回触发
    def help1(self):
            self.caidanjiemian.show()
            self.bangzhu1button.show()
            self.bangzhu2button.show()
            self.bangzhu3button.show()
            self.bangzhu1.show()
            self.bangzhu2.show()
            self.bangzhu3.show()
            self.bangzhujiemian.hide()
            self.bangzhuxinxi.hide()
            self.bangzhuxinxibutton.hide()
app = MyApp()
app.run()
