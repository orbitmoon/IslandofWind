#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *
from panda3d.core import *
from threading import Timer
import time

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.font = loader.loadFont('1.ttf')
        self.buttonget= base.loader.loadSfx("buttonget.mp3")
        self.buttondown= base.loader.loadSfx("buttondown.mp3")
        self.victorymusic= base.loader.loadSfx("victory.mp3")
        self.falsemusic= base.loader.loadSfx("false.mp3")
        self.jiechu1 = 0
        self.jiechu2 = 0
        self.down = 0
        self.menuon = 0
        # ESC退出
        self.accept("escape", self.caidan)
        self.accept("q", self.victory)
        self.accept("w", self.false)
        # 背景
        self.beijing = OnscreenImage(
            image='1.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1.02))
        # 开始游戏碰之前图片
        self.a1 = OnscreenImage(image='buttontemp2.png',
                                pos=(0.8, 0, -0.5), scale=(0.2, 0.1, 0.065))
        self.a1.setTransparency(TransparencyAttrib.MAlpha)
        # 碰到开始游戏后显示的按钮
        self.zjmkaishi = DirectButton(text=('', '', '', 'disabled'), image='button2.png', frameColor=(255, 255, 255, 0),
                                      image_scale=(1.8, 1, 0.6), pos=(0.8, 0, -0.5), scale=0.1,
                                      rolloverSound=self.buttonget,clickSound=self.buttondown,
                                      command=self.putdown)
                                      #(2, 1, 0.7)
        self.zjmkaishi.hide()
        self.b1 = OnscreenImage(image='buttontemp1.png',
                                pos=(0.8, 0, -0.5), scale=(0.25, 0.1, 0.13))
        self.b1.setTransparency(TransparencyAttrib.MAlpha)
        self.b1.hide()
        # 点击开始游戏后图片
        self.c1 = OnscreenImage(image='buttontemp3.png',
                                pos=(0.8, 0, -0.5), scale=(0.2, 0.1, 0.065))
        self.c1.setTransparency(TransparencyAttrib.MAlpha)
        self.c1.hide()
        # 开始游戏显示的文字
        self.textObjectstart1 = OnscreenText(
            text='开始游戏', pos=(0.8, -0.51, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.textObjectstart2 = OnscreenText(
            text='开始游戏', pos=(0.8, -0.51, 0), scale=0.055, fg=(255, 255, 255, 1))
        self.textObjectstart2.hide()
        self.textObjectstart3 = OnscreenText(
            text='开始游戏', pos=(0.8, -0.51, 0), scale=0.06, fg=(255, 255, 255, 1))
        self.textObjectstart3.hide()
        self.textObjectstart1.setFont(self.font)
        self.textObjectstart2.setFont(self.font)
        self.textObjectstart3.setFont(self.font)

        # 退出游戏碰之前图片
        self.a2 = OnscreenImage(image='buttontemp2.png',
                                pos=(0.8, 0, -0.7), scale=(0.2, 0.1, 0.065))
        self.a2.setTransparency(TransparencyAttrib.MAlpha)
        # 碰到退出游戏后显示的按钮
        self.zjmkaishi2 = DirectButton(text=('', '', '', 'disabled'), image='button2.png', frameColor=(255, 255, 255, 0),
                                       image_scale=(1.8, 1, 0.6), pos=(0.8, 0, -0.7), scale=0.1, command=self.quit,
                                       rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.zjmkaishi2.hide()
        self.b2 = OnscreenImage(image='buttontemp1.png',
                                pos=(0.8, 0, -0.7), scale=(0.25, 0.1, 0.13))
        self.b2.setTransparency(TransparencyAttrib.MAlpha)
        self.b2.hide()
        # 点击退出游戏后图片
        self.c2 = OnscreenImage(image='buttontemp3.png',
                                pos=(0.8, 0, -0.7), scale=(0.2, 0.1, 0.071))
        self.c2.setTransparency(TransparencyAttrib.MAlpha)
        self.c2.hide()
        # 退出游戏显示的文字
        self.textObjectstart4 = OnscreenText(
            text='退出', pos=(0.8, -0.71, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.textObjectstart5 = OnscreenText(
            text='退出', pos=(0.8, -0.71, 0), scale=0.055, fg=(255, 255, 255, 1))
        self.textObjectstart5.hide()
        self.textObjectstart6 = OnscreenText(
            text='退出', pos=(0.8, -0.71, 0), scale=0.06, fg=(255, 255, 255, 1))
        self.textObjectstart6.hide()
        self.textObjectstart4.setFont(self.font)
        self.textObjectstart5.setFont(self.font)
        self.textObjectstart6.setFont(self.font)

        # ESC菜单
        self.caidanjiemian = OnscreenImage(
            image='caidan.jpg', pos=(0, 0, 0), scale=(0.5, 0.1, 0.41))
        self.caidanjiemian.hide()

        self.bangzhu1button = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                                           image_scale=(2.2, 1, 0.7), pos=(0, 0, 0.23), scale=0.1, command=self.putdown1,
                                           rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhu1button.hide()
        self.bangzhu1 = OnscreenText(text='游戏帮助', pos=(
            0, 0.21, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhu1.setFont(self.font)
        self.bangzhu1.hide()

        self.bangzhu2button = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                                           image_scale=(2.2, 1, 0.7), pos=(0, 0, 0.03), scale=0.1, command=self.putdown2,
                                           rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhu2button.hide()
        self.bangzhu2 = OnscreenText(text='继续游戏', pos=(
            0, 0.01, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhu2.setFont(self.font)
        self.bangzhu2.hide()

        self.bangzhu3button = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                                           image_scale=(2.2, 1, 0.7), pos=(0, 0, -0.18), scale=0.1, command=self.putdown3,
                                           rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhu3button.hide()
        self.bangzhu3 = OnscreenText(text='退出游戏', pos=(
            0, -0.2, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhu3.setFont(self.font)
        self.bangzhu3.hide()

        self.bangzhujiemian = OnscreenImage(
            image='caidan.jpg', pos=(-0, 0, 0), scale=(1, 0.1, 0.81))
        self.bangzhujiemian.hide()
        self.bangzhuxinxi = OnscreenText(
            text='coooooooooooooooool', pos=(0, 0, 0), scale=0.1)
        self.bangzhuxinxi.hide()
        self.bangzhuxinxibutton = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                                               image_scale=(2.2, 1, 0.7), pos=(0.55, 0, -0.55), scale=0.1, command=self.help1,
                                               rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhuxinxibutton.hide()
        self.bangzhuxinxi1 = OnscreenText(
            text='返回', pos=(0.55, -0.56, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhuxinxi1.setFont(self.font)
        self.bangzhuxinxi1.hide()

        # 游戏胜利
        self.victorypic = OnscreenImage(
            image='victory.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1.02))
        self.victorypic.hide()
        # 游戏失败
        self.falsepic = OnscreenImage(
            image='false.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1.02))
        self.falsepic.hide()
        self.rebornbutton = DirectButton(text=('', '', '', 'disabled'), image='button1.png', frameColor=(255, 255, 255, 0),
                                         image_scale=(2.2, 1, 0.7), pos=(0.75, 0, -0.75), scale=0.1, command=self.reborn,
                                         rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.rebornbutton.hide()
        self.reborntext = OnscreenText(
            text='返回主菜单', pos=(0.75, -0.76, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.reborntext.setFont(self.font)
        self.reborntext.hide()

        #事件队列
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
        if mpos.getY() < -0.42 and mpos.getY() > -0.55 and mpos.getX() > 0.45 and mpos.getX() < 0.75:
            #print(mpos.getY())
            self.jiechu1 = 1
        elif mpos.getY() < -0.62 and mpos.getY() > -0.75 and mpos.getX() > 0.45 and mpos.getX() < 0.75:
            # print(mpos.getY())
            self.jiechu2 = 1
        else:
            self.jiechu1 = 0
            self.jiechu2 = 0
        if(self.jiechu1 == 1 and self.down == 0):
            self.zjmkaishi.show()
            # self.textObjectstart1.hide()
            self.textObjectstart2.show()
            self.b1.show()
        elif(self.jiechu2 == 1 and self.down == 0):
            self.zjmkaishi2.show()
            # self.textObjectstart4.hide()
            self.textObjectstart5.show()
            self.b2.show()
        elif(self.down == 0):
            self.c1.hide()
            self.c2.hide()
            self.b1.hide()
            self.b2.hide()
            self.a1.show()
            self.a2.show()
            self.zjmkaishi.hide()
            self.textObjectstart3.hide()
            self.textObjectstart2.hide()
            self.textObjectstart1.show()
            self.zjmkaishi2.hide()
            self.textObjectstart6.hide()
            self.textObjectstart5.hide()
            self.textObjectstart4.show()
        else:
            self.b1.hide()
            self.b2.hide()
            self.zjmkaishi.hide()
            self.textObjectstart2.hide()
            self.zjmkaishi2.hide()
            self.textObjectstart5.hide()
        return task.cont
        # return task.done
# 按下开始游戏触发

    def putdown(self):
        print('start')
        self.down = 1
        self.a1.hide()
        self.b1.hide()
        self.zjmkaishi.hide()
        self.c1.show()
        self.textObjectstart1.hide()
        self.textObjectstart2.hide()
        self.textObjectstart3.show()

        self.beijing.hide()
        self.textObjectstart1.hide()
        self.textObjectstart2.hide()
        self.textObjectstart3.hide()
        self.textObjectstart4.hide()
        self.textObjectstart5.hide()
        self.textObjectstart6.hide()
        self.a1.hide()
        self.a2.hide()
        self.b1.hide()
        self.b2.hide()
        self.c1.hide()
        self.c2.hide()

# 按下退出游戏触发

    def quit(self):
        print('exit')
        self.down = 1
        self.a2.hide()
        self.zjmkaishi2.hide()
        self.c2.show()
        self.textObjectstart4.hide()
        self.textObjectstart5.hide()
        self.textObjectstart6.show()
        sys.exit()
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


    def putdown3(self):
        sys.exit()
        # self.b.show()
# 按下帮助界面的返回触发

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
        self.bangzhuxinxi1.hide()
# 胜利和失败触发

    def victory(self):
        self.victorypic.show()
        self.rebornbutton.show()
        self.reborntext.show()
        self.victorymusic.play()

    def false(self):
        self.falsepic.show()
        self.rebornbutton.show()
        self.reborntext.show()
        self.falsemusic.play()
    def reborn(self):
        print("reborn")
        self.rebornbutton.hide()
        self.reborntext.hide()
        self.victorypic.hide()
        self.falsepic.hide()
        self.down=0
        self.beijing.show()
app = MyApp()
app.run()
