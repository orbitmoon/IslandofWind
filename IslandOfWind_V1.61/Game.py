# -*- coding: UTF-8 -*-

# Author: CJT
# Date: 2016/6/16

# A simple skybox.

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'window-title Island of Wind')
loadPrcFileData('', 'win-size 1280 720')
loadPrcFileData('', 'sync-video true')
loadPrcFileData('', 'show-frame-rate-meter true')
loadPrcFileData('', 'texture-minfilter linear-mipmap-linear')
# loadPrcFileData('', 'cursor-hidden true')

from pandac.PandaModules import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.BufferViewer import BufferViewer
from direct.showbase.InputStateGlobal import inputState
from direct.interval.IntervalGlobal import Sequence
from direct.showbase import Audio3DManager
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import *
import sys
import os
from math import *

from panda3d.bullet import *

from direct.gui.DirectGui import *


MouseSensitivity = 100
CameraSpeed = 25
zoomRate = 5
blockerWidth = 0.9
blockerheight = 1.6
blockerSpacing = 0.06
count = 0
playSpeed = 0.5

class Skybox(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        # base.setBackgroundColor(0.0, 0.0, 0.0, 1)
        # base.setFrameRateMeter(True)
        
        self.base = self
        self.font = loader.loadFont('material/1.ttf')
        self.buttonget= base.loader.loadSfx("sounds/buttonget.mp3")
        self.buttondown= base.loader.loadSfx("sounds/buttondown.mp3")
        self.victorymusic= base.loader.loadSfx("sounds/victory.mp3")
        self.falsemusic= base.loader.loadSfx("sounds/false.mp3")
        self.jiechu1 = 0
        self.jiechu2 = 0
        self.down = 0
        self.menuon = 0

        ######初始界面的加载（By Hll）######
        # 背景
        self.beijing = OnscreenImage(
            image='material/1.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1.02))
        # 开始游戏碰之前图片
        self.a1 = OnscreenImage(image='material/buttontemp2.png',
                                pos=(0.8, 0, -0.5), scale=(0.2, 0.1, 0.065))
        self.a1.setTransparency(TransparencyAttrib.MAlpha)
        # 碰到开始游戏后显示的按钮
        self.zjmkaishi = DirectButton(text=('', '', '', 'disabled'), image='material/button2.png', frameColor=(255, 255, 255, 0),
                                      image_scale=(1.8, 1, 0.6), pos=(0.8, 0, -0.5), scale=0.1,
                                      rolloverSound=self.buttonget,clickSound=self.buttondown,
                                      command=self.putdown)
                                      #(2, 1, 0.7)
        self.zjmkaishi.hide()
        self.b1 = OnscreenImage(image='material/buttontemp1.png',
                                pos=(0.8, 0, -0.5), scale=(0.25, 0.1, 0.13))
        self.b1.setTransparency(TransparencyAttrib.MAlpha)
        self.b1.hide()
        # 点击开始游戏后图片
        self.c1 = OnscreenImage(image='material/buttontemp3.png',
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
        self.a2 = OnscreenImage(image='material/buttontemp2.png',
                                pos=(0.8, 0, -0.7), scale=(0.2, 0.1, 0.065))
        self.a2.setTransparency(TransparencyAttrib.MAlpha)
        # 碰到退出游戏后显示的按钮
        self.zjmkaishi2 = DirectButton(text=('', '', '', 'disabled'), image='material/button2.png', frameColor=(255, 255, 255, 0),
                                       image_scale=(1.8, 1, 0.6), pos=(0.8, 0, -0.7), scale=0.1, command=self.quit,
                                       rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.zjmkaishi2.hide()
        self.b2 = OnscreenImage(image='material/buttontemp1.png',
                                pos=(0.8, 0, -0.7), scale=(0.25, 0.1, 0.13))
        self.b2.setTransparency(TransparencyAttrib.MAlpha)
        self.b2.hide()
        # 点击退出游戏后图片
        self.c2 = OnscreenImage(image='material/buttontemp3.png',
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
            image='material/caidan.jpg', pos=(0, 0, 0), scale=(0.5, 0.1, 0.41))
        self.caidanjiemian.hide()

        self.bangzhu1button = DirectButton(text=('', '', '', 'disabled'), image='material/button1.png', frameColor=(255, 255, 255, 0),
                                           image_scale=(2.2, 1, 0.7), pos=(0, 0, 0.23), scale=0.1, command=self.putdown1,
                                           rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhu1button.hide()
        self.bangzhu1 = OnscreenText(text='游戏帮助', pos=(
            0, 0.21, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhu1.setFont(self.font)
        self.bangzhu1.hide()

        self.bangzhu2button = DirectButton(text=('', '', '', 'disabled'), image='material/button1.png', frameColor=(255, 255, 255, 0),
                                           image_scale=(2.2, 1, 0.7), pos=(0, 0, 0.03), scale=0.1, command=self.putdown2,
                                           rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhu2button.hide()
        self.bangzhu2 = OnscreenText(text='继续游戏', pos=(
            0, 0.01, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhu2.setFont(self.font)
        self.bangzhu2.hide()

        self.bangzhu3button = DirectButton(text=('', '', '', 'disabled'), image='material/button1.png', frameColor=(255, 255, 255, 0),
                                           image_scale=(2.2, 1, 0.7), pos=(0, 0, -0.18), scale=0.1, command=self.putdown3,
                                           rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhu3button.hide()
        self.bangzhu3 = OnscreenText(text='退出游戏', pos=(
            0, -0.2, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhu3.setFont(self.font)
        self.bangzhu3.hide()

        self.bangzhujiemian = OnscreenImage(
            image='material/caidan.jpg', pos=(-0, 0, 0), scale=(1, 0.1, 0.81))
        self.bangzhujiemian.hide()

        ####写游戏说明####
        self.bangzhuxinxi = OnscreenText(
            text='coooooooooooooooool', pos=(0, 0, 0), scale=0.1)
        self.bangzhuxinxi.hide()
        self.bangzhuxinxibutton = DirectButton(text=('', '', '', 'disabled'), image='material/button1.png', frameColor=(255, 255, 255, 0),
                                               image_scale=(2.2, 1, 0.7), pos=(0.55, 0, -0.55), scale=0.1, command=self.help1,
                                               rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.bangzhuxinxibutton.hide()
        self.bangzhuxinxi1 = OnscreenText(
            text='返回', pos=(0.55, -0.56, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.bangzhuxinxi1.setFont(self.font)
        self.bangzhuxinxi1.hide()

        # 游戏胜利
        self.victorypic = OnscreenImage(
            image='material/victory.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1.02))
        self.victorypic.hide()
        # 游戏失败
        self.falsepic = OnscreenImage(
            image='material/false.jpg', pos=(0, 0, 0.02), scale=(1.4, 1, 1.02))
        self.falsepic.hide()
        self.rebornbutton = DirectButton(text=('', '', '', 'disabled'), image='material/button1.png', frameColor=(255, 255, 255, 0),
                                         image_scale=(2.2, 1, 0.7), pos=(0.75, 0, -0.75), scale=0.1, command=self.reborn,
                                         rolloverSound=self.buttonget,clickSound=self.buttondown)
        self.rebornbutton.hide()
        self.reborntext = OnscreenText(
            text='返回主菜单', pos=(0.75, -0.76, 0), scale=0.05, fg=(255, 255, 255, 1))
        self.reborntext.setFont(self.font)
        self.reborntext.hide()

        # 主界面事件队列
        taskMgr.add(self.example, 'Welcome')

    #### 初始界面函数 ####
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

        # 渲染天空盒，添加光照
        self.nowX = 0.00
        self.nowY = 0.00
        sha = Shader.load(
            Shader.SLGLSL, "shaders/skybox_vert.glsl", "shaders/skybox_frag.glsl")

        self.skyTex = loader.loadCubeMap("textures/skybox/Highnoon_#.jpg")

        self.ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
        self.ambientLight.node().setColor((0.2, 0.2, 0.2, 1.0))

        self.sun = render.attachNewNode(DirectionalLight("sun"))
        self.sun.node().setColor((0.8, 0.8, 1.0, 1.0))
        self.sun.node().setDirection(LVector3(1, -1, -3))

        render.setLight(self.ambientLight)
        render.setLight(self.sun)

        self.skybox = self.loader.loadModel("models/skybox")
        self.skybox.reparentTo(self.render)
        self.skybox.setShader(sha)
        self.skybox.setShaderInput("skybox", self.skyTex)
        self.skybox.setAttrib(DepthTestAttrib.make(RenderAttrib.MLessEqual))

        # 处理输入
        self.accept('escape', self.doExit)
        self.accept('r', self.doReset)
        self.accept('f1', self.toggleWireframe)
        self.accept('f2', self.toggleTexture)
        self.accept('f3', self.toggleDebug)

        self.tagOfForward = 0
        self.tagOfReverse = 0
        self.tagOfLeft = 0
        self.tagOfRight = 0
        self.count = 0
        self.flyto = 0

        #### 各种tag参数 ####

        # 是否在零摩擦区域内
        self.tagOfZeroRub = 0
        # 用来判断零摩擦运动是否结束
        self.posXBefore = 0
        self.posYBefore = 0
        self.posXNow = 0
        self.posYNow = 0
        #
        self.tagOfSlabStone = 1
        self.isMoving = False
        #### 各种tag参数 ####

        # 开启粒子效果
        base.enableParticles()

        # 接受输入
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('transfer', 'e')
        inputState.watchWithModifiers('slabstone', 'z')

        self.taskMgr.remove("Welcome")
        # Task
        taskMgr.add(self.update, 'updateWorld')

        # 初始化
        self.setup()

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

    #### 主程序函数 ####
    # 退出
    def doExit(self):
        self.cleanup()
        sys.exit(1)

    # 重置
    def doReset(self):
        #### 各种tag参数 ####

        # 是否在零摩擦区域内
        self.tagOfZeroRub = 0
        # 用来判断零摩擦运动是否结束
        self.posXBefore = 0
        self.posYBefore = 0
        self.posXNow = 0
        self.posYNow = 0
        #
        self.tagOfSlabStone = 1
        #### 各种tag参数 ####

        self.cleanup()
        self.setup()

    # 暂时不可用，会出错，希望谁能够实现这两个函数
    # def toggleWireframe(self):
    #     base.toggleWireframe()

    # def toggleTexture(self):
    #     base.toggleTexture()
    # def goZ(self):
    #     for i in range(100):
    #         speed = Vec3(0, 0, 0)
    #         speed.setY(1.0)
    #         speed *= 6.0
    #         self.characterNP.node().setLinearMovement(speed, True)

    # 显示框框
    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    # 处理输入(在零摩擦区域之外)
    def processInputOutZero(self, dt):
        speed = Vec3(0, 0, 0)
        # torque = Vec3(0, 0, 0)

        if inputState.isSet('forward'):
            self.visualNP.setH(-45)
            speed.setX(1.0)
        if inputState.isSet('reverse'):
            self.visualNP.setH(135)
            speed.setX(-1.0)
        if inputState.isSet('left'):
            self.visualNP.setH(45)
            speed.setY(1.0)
        if inputState.isSet('right'):
            self.visualNP.setH(-135)
            speed.setY(-1.0)

        if inputState.isSet('forward') or inputState.isSet('reverse') or inputState.isSet('left') or inputState.isSet('right'):
            if self.isMoving is False:
                self.visualNP.loop('run')
                self.isMoving = True

        else:
            if self.isMoving:
                self.visualNP.stop()
                self.visualNP.loop("breath")
                self.isMoving = False

        speed *= 2.5
        # torque *= 10.0

        # speed = render.getRelativeVector(self.boxNP, speed)
        # torque = render.getRelativeVector(self.boxNP, torque)

        self.characterNP.node().setLinearMovement(speed, True)

        # self.boxNP.node().setActive(True)
        # self.boxNP.node().applyCentralspeed(speed)
        # self.boxNP.node().applyTorque(torque)

    # 处理输入(在零摩擦区域之内)
    def processInputInZero(self, dt):
        if self.tagOfForward == 0 and self.tagOfReverse == 0 and self.tagOfLeft == 0 and self.tagOfRight == 0:
            if inputState.isSet('forward'):
                self.tagOfForward = 1
            if inputState.isSet('reverse'):
                self.tagOfReverse = 1
            if inputState.isSet('left'):
                self.tagOfLeft = 1
            if inputState.isSet('right'):
                self.tagOfRight = 1

    # 在零摩擦区域内的移动
    def MoveInZero(self):
        self.posXBefore = self.characterNP.getX()
        self.posYBefore = self.characterNP.getY()
        self.speed = Vec3(0, 0, 0)
        if self.tagOfForward == 1:
            if self.world.contactTest(self.characterNP.node()).getNumContacts() != 0:
                speed = Vec3(0, 0, 0)
                speed.setX(1.0)
                speed *= 6.0
                self.speed = speed
            if self.world.contactTest(self.characterNP.node()).getNumContacts() == 0:
                self.speed = Vec3(0, 0, 0)
            self.characterNP.node().setLinearMovement(self.speed, True)
        if self.tagOfReverse == 1:
            if self.world.contactTest(self.characterNP.node()).getNumContacts() != 0:
                speed = Vec3(0, 0, 0)
                speed.setX(-1.0)
                speed *= 6.0
                self.speed = speed
            if self.world.contactTest(self.characterNP.node()).getNumContacts() == 0:
                self.speed = Vec3(0, 0, 0)
            self.characterNP.node().setLinearMovement(self.speed, True)
        if self.tagOfLeft == 1:
            if self.world.contactTest(self.characterNP.node()).getNumContacts() != 0:
                speed = Vec3(0, 0, 0)
                speed.setY(1.0)
                speed *= 6.0
                self.speed = speed
            if self.world.contactTest(self.characterNP.node()).getNumContacts() == 0:
                self.speed = Vec3(0, 0, 0)
            self.characterNP.node().setLinearMovement(self.speed, True)
        if self.tagOfRight == 1:
            if self.world.contactTest(self.characterNP.node()).getNumContacts() != 0:
                speed = Vec3(0, 0, 0)
                speed.setY(-1.0)
                speed *= 6.0
                self.speed = speed
            if self.world.contactTest(self.characterNP.node()).getNumContacts() == 0:
                self.speed = Vec3(0, 0, 0)
            self.characterNP.node().setLinearMovement(self.speed, True)


    def check(self):
        self.posXNow = self.characterNP.getX()
        self.posYNow = self.characterNP.getY()

        if self.posXBefore == self.posXNow and self.posYBefore == self.posYNow:
            self.tagOfForward = 0
            self.tagOfReverse = 0
            self.tagOfLeft = 0
            self.tagOfRight = 0

        # #print self.characterNP.getPos()
        # if self.characterNP.getPos() == Vec3(15, 31, 0.96):
        #     if self.tagOfOut == 1:
        #         self.tagOfZeroRub = 1
        #     self.tagOfSlabStone -= 1
        #     self.tagOfOut -= 1

        # # #print self.tagOfOut
        # print "now",self.characterNP.getPos()
        # # #print self.tagOfOut
        # if self.characterNP.getX() > 16 and self.characterNP.getY() < 4:
        #     # print self.tagOfOut
        #     if self.tagOfOut < 0:
        #         # #print "yes"
        #         self.tagOfOut += 1
        #         self.tagOfZeroRub = 0
        #         characterPosInterval = self.characterNP.posInterval(
        #             2, Point3(20, 19, 2), startPos=Point3(16, 2, 1))
        #         characterPosInterval.start()

        # if self.characterNP.getPos() == Vec3(20, 19, 0.96):
        #     # #print "yesA"
        #     # print self.tagOfOut
        #     if self.tagOfOut == 0:
        #         # #print "yesB"
        #         self.characterNP.node().removeChild(self.visualNPOfCharacter.node())
        #         self.visualNPOfSlabstone.reparentTo(self.slabstoneNP)
        #         self.tagOfOut += 1

    # 碰撞事件
    def contact(self):
        result = self.world.contactTest(self.characterNP.node())
        for contact in result.getContacts():
            # #print contact.getNode0()
            # #print contact.getNode1()
            if self.characterNP.getX() > 40:
                for i in range(len(self.alarms)):
                    for j in range(len(self.alarms[i])):
                        for k in range(len(self.alarms[i][j])): 
                            if contact.getNode1() == self.alarms[i][j][k].node():
                                if i == 0:
                                    if j == 1 and k == 1 and self.blockerStates[i] == 1:#逆时针
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(270,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX(), self.characterNP.getY() - 1.5, 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 0
                                        return
                                    elif j == 1 and k == 2 and self.blockerStates[i] == 1:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(270,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX() + 1.5, self.characterNP.getY(), 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 0
                                        return
                                    elif j == 0 and k == 0 and self.blockerStates[i] == 0:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(180,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX(), self.characterNP.getY() + 1.5, 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 1
                                        return
                                    elif j == 0 and k == 1 and self.blockerStates[i] == 0:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(180,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed* 1.5,
                                            (self.characterNP.getX() - 1.5, self.characterNP.getY(), 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 1
                                        return
                                elif i == 1:
                                    if j == 1 and k == 1 and self.blockerStates[i] == 1:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(180,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX() - 1.5, self.characterNP.getY(), 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 0
                                        return
                                    elif j == 1 and k == 2 and self.blockerStates[i] == 1:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(180,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX(), self.characterNP.getY() - 1.5, 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 0
                                        return
                                    elif j == 0 and k == 0 and self.blockerStates[i] == 0:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(90,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX() + 1.5, self.characterNP.getY(), 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 1
                                        return
                                    elif j == 0 and k == 1 and self.blockerStates[i] == 0:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed,(90,0,0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor3(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX(), self.characterNP.getY() + 1.5, 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 1
                                        return
                                elif i == 2:
                                    if j == 0 and self.blockerStates[i] == 0:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed, (90, 0, 0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor2(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX() + 2, self.characterNP.getY(), 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 1
                                        return
                                    elif j == 1 and self.blockerStates[i] == 1:
                                        hprInterval = self.blockers[i].hprInterval(playSpeed, (180, 0, 0))
                                        hprInterval.start()
                                        self.blockerReframeIntervalFor2(i)
                                        posInterval = self.characterNP.posInterval(playSpeed * 1.5, 
                                            (self.characterNP.getX() - 2, self.characterNP.getY(), 1))
                                        posInterval.start()
                                        self.blockerStates[i] = 0
                                        return
            if self.characterNP.getX() > 20 and self.characterNP.getX() < 40:
                for i in range(len(self.throwers)):
                    if contact.getNode1() == self.throwers[i].thrower.node() and self.throwers[i].canDamage == 1:
                        self.HP = self.HP - 1
                        self.throwers[i].canDamage = 0
                        self.HPtext.setText(bytes(self.HP))
            for i in range(2):
                if self.tagOfSlabStone == 0:
                    if contact.getNode1() == self.outZeroNP.node():
                        self.Gear.getChild(0).hide()
                        self.world.removeRigidBody(self.Gear.node())
                        self.tagOfForward = 0
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.tagOfSlabStone = 1
                        self.takeoff(-1)
                if inputState.isSet('slabstone'):
                    if self.tagOfSlabStone == 1:
                        if contact.getNode1() == self.slabstoneNP.node():
                            # self.characterNP.node().setGravity(0)
                            # characterPosInterval = self.characterNP.posInterval(
                            # 2, Point3(15, 31, 2), startPos=Point3(20, 19, 1))
                            self.visualNPOfCharacter = loader.loadModel(
                                'models/Slabstone.egg')
                            self.visualNPOfCharacter.clearModelNodes()
                            self.visualNPOfCharacter.setScale(0.5)
                            self.visualNPOfCharacter.reparentTo(
                                self.characterNP)
                            self.visualNPOfCharacter.setPos(0, 0, -1)
                            # self.characterNP.node().setGravity(0)
                            # characterPosInterval.start()
                            self.takeoff(-2)
                            self.tagOfSlabStone = 0
                            # #print self.characterNP.getPos()
                            self.slabstoneNP.node().removeChild(self.visualNPOfSlabstone.node())
                            # if self.characterNP.getPos == Point3(15,31,0):
                            # self.characterNP.node().setGravity(9.81)

                if inputState.isSet('transfer'):
                    if contact.getNode1() == self.transList[1].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 0
                        # # self.characterNP.setPos(
                        # #     self.transList[4].getPos() + (0, 0, 0.1))
                        self.takeoff(0)

                        # self.nowX = 6.00
                        # self.nowY = 36.00
                        # self.nowZ = 40.96

                        # self.flyto = 3
                        # self.takeoff(3)

                    if contact.getNode1() == self.transList[5].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 7
                        # self.characterNP.setPos(
                        #     self.transList[7].getPos() + (0, 0, 0.1))
                        self.takeoff(7)

                    if contact.getNode1() == self.transList[6].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 3
                        self.takeoff(3)
                        # self.characterNP.setPos(
                        #     self.transList[3].getPos() + (0, 0, 3))

                    if contact.getNode1() == self.transList[2].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 0
                        # self.characterNP.setPos(
                        #     self.transList[0].getPos() + (0, 0, 0.1))
                        self.takeoff(0)

                    if contact.getNode1() == self.transList[12].node()\
                    or contact.getNode1() == self.transList[15].node()\
                    or contact.getNode1() == self.transList[18].node()\
                    or contact.getNode1() == self.transList[19].node()\
                    or contact.getNode1() == self.transList[21].node()\
                    or contact.getNode1() == self.transList[22].node()\
                    or contact.getNode1() == self.transList[24].node():
                    	self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 9
                        self.takeoff(9)

                    if contact.getNode1() == self.transList[11].node()\
                    or contact.getNode1() == self.transList[14].node()\
                    or contact.getNode1() == self.transList[17].node()\
                    or contact.getNode1() == self.transList[23].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 8
                        # self.characterNP.setPos(
                        #     self.transList[0].getPos() + (0, 0, 0.1))
                        self.takeoff(8)

                    if contact.getNode1() == self.transList[10].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 11
                        # self.characterNP.setPos(
                        #     self.transList[0].getPos() + (0, 0, 0.1))
                        self.takeoff(11)

                    if contact.getNode1() == self.transList[13].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 14
                        # self.characterNP.setPos(
                        #     self.transList[0].getPos() + (0, 0, 0.1))
                        self.takeoff(14)

                    if contact.getNode1() == self.transList[16].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 17
                        # self.characterNP.setPos(
                        #     self.transList[0].getPos() + (0, 0, 0.1))
                        self.takeoff(17)

                    if contact.getNode1() == self.transList[20].node():
                        self.speed = Vec3(0, 0, 0)
                        self.characterNP.node().setLinearMovement(self.speed, True)
                        self.flyto = 23
                        # self.characterNP.setPos(
                        #     self.transList[0].getPos() + (0, 0, 0.1))
                        self.takeoff(23)

    def takeoff(self, tag):
        self.taskMgr.remove("updateWorld")

        if tag < 0:
            self.taskMgr.add(self.fly, "Fly")

        if tag >= 0:
            self.speedX = float(
                self.transList[tag].getX(render) - self.characterNP.getX()) / float(200)
            self.speedY = float(
                self.transList[tag].getY(render) - self.characterNP.getY()) / float(200)
            self.speedZ = float(
                self.transList[tag].getZ(render) - self.characterNP.getZ()) / float(200)
            # print self.transList[tag].getPos(),self.characterNP.getPos(),self.nowX,self.nowY,self.nowZ
            # print self.speedX,self.speedY,self.speedZ
            self.taskMgr.add(self.flycam, "Flycam")

    def fly(self, task):
        if self.tagOfZeroRub == 0:
            self.characterNP.setPos(self.characterNP.getX(
                 ) - 0.025, self.characterNP.getY() + 0.06, self.characterNP.getZ())
            self.updatecam()
            self.count += 1

            if self.count == 199:
                self.count = 0
                self.land(-2)

        if self.tagOfZeroRub == 1:
            self.characterNP.setPos(self.characterNP.getX(
            ) + 0.025, self.characterNP.getY() + 0.09, self.characterNP.getZ())
            self.updatecam()
            self.count += 1

            if self.count == 199:
                self.count = 0
                self.land(-1)

        return Task.cont

    def flycam(self, task):
        self.transto()
        # print "x",self.cam.getX()
        self.cam.setPos(self.cam.getX() + self.speedX, self.cam.getY() +
                        self.speedY, self.cam.getZ() + self.speedZ)

        # print "flying",self.cam.getPos()
        self.skybox.setPos(self.cam.getPos())
        self.count += 1

        if self.count == 199:
            self.count = 0
            self.land(1)
        return Task.cont

    def transto(self):
        #print self.transList[self.flyto].getPos(),self.characterNP.getPos(),self.cam.getPos()
        self.characterNP.setPos(
            self.transList[self.flyto].getPos(render) + Vec3(0, 0, 1))

    def land(self, tag):
        # self.characterNP.setPos(15, 31, 0.97)
        if tag == -1:
            self.tagOfZeroRub = 0
            self.taskMgr.remove("Fly")
            self.visualNPOfSlabstone.reparentTo(self.slabstoneNP)
            self.characterNP.node().removeChild(self.visualNPOfCharacter.node())
            x = self.characterNP.getX()
            y = self.characterNP.getY()
            self.worldNP.node().removeChild(self.characterNP.node())
            self.world.removeCharacter(self.characterNP.node())
            self.characterNP = None
            self.initCharacter(x, y, 2)
        if tag == -2:
            self.tagOfZeroRub = 1
            self.taskMgr.remove("Fly")
        if tag >= 0:
            if self.flyto > 7:
                self.tagOfZeroRub = 0
                self.taskMgr.remove("Flycam")
            else :
                self.tagOfZeroRub = 1
                self.taskMgr.remove("Flycam")
            # print self.transList[tag].getPos(),self.characterNP.getPos()

        self.taskMgr.add(self.update, "updateWorld")

    # Task函数
    def update(self, task):

        countForCheck =float(globalClock.getLongTime()*100)
        dt = globalClock.getDt()

        if self.tagOfZeroRub == 0:
            self.processInputOutZero(dt)
        if self.tagOfZeroRub == 1:
            self.processInputInZero(dt)

        if self.characterNP.getX()<22:
            self.checkZero(countForCheck,dt)
        else:
            self.world.doPhysics(dt,10,1.0/90.0)

        self.contact()
        # #print "out"
        self.updatecam()
        self.fireSwitch((int)(countForCheck/100))

        return task.cont

    def checkZero(self,countForCheck,dt):
        if (int)(countForCheck) % 3 != 0:
            self.MoveInZero()
        # self.world.doPhysics(dt)
        self.world.doPhysics(dt,5,1.0/45.0)
        if (int)(countForCheck) % 3 == 0:
            self.check()
    # 重置
    def cleanup(self):
        self.world.removeCharacter(self.characterNP.node())
        self.world.removeRigidBody(self.groundNP.node())
        self.world.removeRigidBody(self.wallNP.node())

        self.world = None

        self.boxNP = None
        self.debugNP = None
        self.groundNP = None
        self.wallNP = None

        self.HPtext.destroy()
        self.worldNP.removeNode()

    # 设置地面方块
    def initGroundBoxes(self, posx, posy, posz):
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        # #print 'GroundBox_(%d,%d)_' % (posx, posy)
        groundBoxNP = self.worldNP.attachNewNode(
            BulletRigidBodyNode('GroundBox_(%d,%d,%d)_' % (posx, posy, posz)))
        groundBoxNP.node().addShape(shape)
        groundBoxNP.setPos(posx, posy, posz)
        groundBoxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(groundBoxNP.node())
        # visualNP = loader.loadModel('models/cube.egg')
        # visualNP.clearModelNodes()
        # visualNP.setScale(0.5)
        # visualNP.reparentTo(groundBoxNP)

        self.groundNP = groundBoxNP

    # 设置墙面方块
    def initWallBoxes(self, posx, posy, posz):
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        # #print 'WallBox_(%d,%d)_' % (posx, posy)
        wallBoxNP = self.worldNP.attachNewNode(
            BulletRigidBodyNode('WallBox_(%d,%d,%d)_' % (posx, posy, posz)))
        wallBoxNP.node().addShape(shape)
        wallBoxNP.setPos(posx, posy, posz + 1)
        wallBoxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(wallBoxNP.node())
        visualNP = loader.loadModel('models/Stair.egg')
        visualNP.clearModelNodes()
        visualNP.setScale(0.5)
        visualNP.reparentTo(wallBoxNP)

        self.wallNP = wallBoxNP

    # 设置传送方块
    def initTransBoxes(self, posx, posy, posz, fatherNP, scale):
        shape = BulletBoxShape(Vec3(scale, scale, scale))
        # #print 'TransBox_(%d,%d)_' % (posx, posy)
        transBoxNP = fatherNP.attachNewNode(
            BulletRigidBodyNode('TransBox_(%d,%d,%d)_' % (posx, posy, posz)))
        transBoxNP.node().addShape(shape)
        transBoxNP.setPos(posx, posy, posz)
        transBoxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(transBoxNP.node())
        visualNP = loader.loadModel('models/tp.egg')
        visualNP.clearModelNodes()
        visualNP.setScale(scale)
        visualNP.reparentTo(transBoxNP)

        return transBoxNP
    
    # 传送阵迷宫初始化
    def initTMaze(self):
    	#8 游戏开始位置
        self.transList.append(self.initTransBoxes(40, 18, -0.45, self.worldNP, 1))
        #9 浮台位置
        self.transList.append(self.initTransBoxes(24, 24.5, -0.45, self.worldNP, 1))
        #10 挡板迷宫结束位置
        self.transList.append(self.initTransBoxes(63, 17, -0.45, self.worldNP, 1))

        #11,12,13
        tIsland1 = self.worldNP.attachNewNode('tIsland1')
        tIsland1.setPos(40, 20, 5)
        self.createNewISland(tIsland1,'假如你是一个香港司机，你上下车的车门在哪边？')

        #14,15,16
        tIsland2 = self.worldNP.attachNewNode('tIsland2')
        tIsland2.setPos(35, 30, 15)
        self.createNewISland(tIsland2,'通常来说，肝在体内的哪边？')

        #17,18,19
        tIsland3 = self.worldNP.attachNewNode('tIsland3')
        tIsland3.setPos(50, 10, 30)
        self.createNewISland(tIsland3,'人的左右脑哪边更加聪明？')

        #20,21,22
        tIsland4 = self.worldNP.attachNewNode('tIsland4')
        tIsland4.setPos(41, 10, 15)
        self.createNewISland(tIsland4,'你知道吗，我已经不是原来的我了！')

        #23,24,25
        tIsland4 = self.worldNP.attachNewNode('tIsland4')
        tIsland4.setPos(50, 5, 3)
        self.createNewISland(tIsland4,'Which side can get out from here?')

    def createNewISland(self, tIsland, qStr):
        shape = BulletBoxShape(Vec3(0.5, 3, 0.5))
        island = tIsland.attachNewNode(BulletRigidBodyNode('island'))
        island.node().addShape(shape)
        island.setCollideMask(BitMask32.allOn())
        island.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(island.node())
        for j in xrange(0, 1):
            for i in xrange(0, 3):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(0.5, 1, 0.5)
                visualNP.setPos(0 + j * 2, -2 + i * 2, 0)
                visualNP.reparentTo(island)
        self.transList.append(self.initTransBoxes(-1, 0, 0, tIsland, 0.5))
        self.transList.append(self.initTransBoxes(0, 3.5, 0, tIsland, 0.5))
        self.transList.append(self.initTransBoxes(0, -3.5, 0, tIsland, 0.5))

        text = TextNode('nodename')
        text.setText(qStr)
        text.setTextColor(0,0,0,1)
        text.setAlign(TextNode.ACenter)
        textNodePath = render2d.attachNewNode(text)
        textNodePath.reparentTo(island)
        textNodePath.setScale(0.4)
        textNodePath.setPos(-0.2,0,2)
        textNodePath.setHpr(-45,-30,0)
        font = loader.loadFont('1.ttf')
        text.setFont(font)
        text.setCardColor(1, 1, 1, 0.2)
        text.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
        text.setCardDecal(True)

    #********* 火焰机关 *********
    def initFMaze(self):
        self.fMazeNP = self.worldNP.attachNewNode('FMazeNode')
        self.fMazeNP.setPos(30,25,0)
        shape = BulletBoxShape(Vec3(1,3,0.5))
        groundBox = self.fMazeNP.attachNewNode(BulletRigidBodyNode('groundBox'))
        groundBox.node().addShape(shape)
        groundBox.setPos(0.5, -4.5, 0)
        groundBox.setCollideMask(BitMask32.allOn())
        groundBox.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(groundBox.node())
        for i in xrange(0, 3):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(0, -2 + i * 2, 0)
                visualNP.reparentTo(groundBox)
        self.initFire()

    def initFire(self):
        thrower1 = FireNode(self.fMazeNP, self.world)
        thrower1.thrower.setPos(5.5, 0, 0)

        thrower2 = FireNode(self.fMazeNP, self.world)
        thrower2.thrower.setPos(3, 0, 0)

        thrower3 = FireNode(self.fMazeNP, self.world)
        thrower3.thrower.setPos(0.5, 0, 0)

        thrower4 = FireNode(self.fMazeNP, self.world)
        thrower4.thrower.setPos(0.5, -9, 0)

        thrower5 = FireNode(self.fMazeNP, self.world)
        thrower5.thrower.setPos(-2, -9, 0)

        thrower6 = FireNode(self.fMazeNP, self.world)
        thrower6.thrower.setPos(-4.5, -9, 0)

        self.throwers = [thrower1,thrower2,thrower3,thrower4,thrower5,thrower6]

    def fireSwitch(self,tag):
        #开喷
        if tag % 2 == 0:
            if self.throwers[0].lastTag != 0:
                self.fireON(0)
        #停喷
        else :
            if self.throwers[0].lastTag != 1 :
                self.fireOFF(0)

        #开喷
        if tag % 3 == 0:
            if self.throwers[1].lastTag != 0:
                self.fireON(1)
        #停喷
        else :
            if self.throwers[1].lastTag != 1 :
                self.fireOFF(1)

        #开喷
        if tag % 4 == 0:
            if self.throwers[2].lastTag != 0:
                self.fireON(2)
        #停喷
        else :
            if self.throwers[2].lastTag != 1 :
                self.fireOFF(2)

        #开喷
        if tag % 3 == 0:
            if self.throwers[3].lastTag != 0:
                self.fireON(3)
        #停喷
        else :
            if self.throwers[3].lastTag != 1 :
                self.fireOFF(3)

        #开喷
        if tag % 2 == 0:
            if self.throwers[4].lastTag != 0:
                self.fireON(4)
        #停喷
        else :
            if self.throwers[4].lastTag != 1 :
                self.fireOFF(4)

        #开喷
        if tag % 4 == 0:
            if self.throwers[5].lastTag != 0:
                self.fireON(5)
        #停喷
        else :
            if self.throwers[5].lastTag != 1 :
                self.fireOFF(5)

    def fireON(self, index):
        self.throwers[index].particle.softStart()
        self.throwers[index].canDamage = 1
        self.throwers[index].lastTag = 0

    def fireOFF(self, index):
        self.throwers[index].particle.softStop()
        self.throwers[index].canDamage = 0
        self.throwers[index].lastTag = 1

    # 游戏角色
    def initCharacter(self, x, y, type):
        characterMaterial = Material()
        characterMaterial.setShininess(4.0)
        characterMaterial.setSpecular(VBase4(1, 1, 1, 1))

        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        if type == 2:
            shape = BulletSphereShape(0.5)

        characterBoxNP = self.worldNP.attachNewNode(
            BulletCharacterControllerNode(shape, 0.5, 'character'))
        # characterBoxNP.node().setGravity(0)
        # characterBoxNP.node().setMass(1.0)
        # characterBoxNP.node().addShape(shape)
        # characterBoxNP.setPos(15, 32, 4) #落在零摩擦初始地点
        #characterBoxNP.setPos(20, 20, 4)
        characterBoxNP.setPos(x, y, 1)
        characterBoxNP.setCollideMask(BitMask32.allOn())

        self.world.attachCharacter(characterBoxNP.node())

        self.characterNP = characterBoxNP

        # 角色模型
        self.visualNP = Actor(
            "models/robot", {"run": "models/robot-run", "breath": "models/robot-breath"})
        self.visualNP.setPlayRate(2,'breath')
        # self.visualNP.setPlayRate(0.9,'run')
        self.visualNP.setPos(0, 0, -0.4)
        self.visualNP.clearModelNodes()
        self.visualNP.setHpr(-45, 0, 0)
        self.visualNP.setScale(0.6)
        self.visualNP.reparentTo(self.characterNP)

        self.characterNP.setAntialias(AntialiasAttrib.MMultisample)   

    def initHP(self):
        self.HP = 10
        HPimage = OnscreenImage(image = 'textures/HP.png', pos = (1.3, 0, 0.9))
        HPimage.setScale(0.05)
        HPimage.setTransparency(TransparencyAttrib.MAlpha)
        HPX = OnscreenText(text = 'X', pos = (1.4, 0.88), scale = 0.07)
        self.HPtext = OnscreenText(text = bytes(self.HP), pos = (1.55, 0.86), scale = 0.2)

    def initMainGround(self):
        #一开始的主干道
        shape = BulletBoxShape(Vec3(3, 10, 0.5))
        groundboxNP1 = self.worldNP.attachNewNode(BulletRigidBodyNode('GroundBox0'))
        groundboxNP1.node().addShape(shape)
        groundboxNP1.setPos(40, 25, 0)
        groundboxNP1.setCollideMask(BitMask32.allOn())
        groundboxNP1.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(groundboxNP1.node())
        for j in xrange(0,3):
            for i in xrange(0,10):
                if i == 1 and j == 1:
                    continue
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-2 + j * 2,-9 + i * 2,0)
                visualNP.reparentTo(groundboxNP1)

        #第一关前的浮台
        shape = BulletBoxShape(Vec3(3, 5, 0.5))
        groundboxNP2 = self.worldNP.attachNewNode(BulletRigidBodyNode('GroundBox0'))
        groundboxNP2.node().addShape(shape)
        groundboxNP2.setPos(24, 22.5, 0)
        groundboxNP2.setCollideMask(BitMask32.allOn())
        groundboxNP2.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(groundboxNP2.node())
        for j in xrange(0,3):
            for i in xrange(0,5):
                if j == 1 and i == 3:
                    continue
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-2 + j * 2,-4 + i * 2,0)
                visualNP.reparentTo(groundboxNP2)

    # 机关门
    def initGear(self):
        #机关门
        shape = BulletBoxShape(Vec3(1, 1, 1))

        self.Gear = self.worldNP.attachNewNode(
            BulletRigidBodyNode('Gear'))
        self.Gear.node().addShape(shape)
        self.Gear.setPos(47, 30, 1)
        self.Gear.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(self.Gear.node())
        visualNP = loader.loadModel('models/Gearcube.egg')
        visualNP.clearModelNodes()
        visualNP.setScale(1)
        visualNP.reparentTo(self.Gear)
        self.Gear.setAntialias(AntialiasAttrib.MMultisample)

    # 浮板
    def initSlabstone(self):
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        slabstoneBoxNP = self.worldNP.attachNewNode(
            BulletRigidBodyNode('SlabstoneBox'))
        slabstoneBoxNP.node().addShape(shape)
        slabstoneBoxNP.setPos(20, 19, 0)
        slabstoneBoxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(slabstoneBoxNP.node())
        self.visualNPOfSlabstone = loader.loadModel('models/Slabstone.egg')
        self.visualNPOfSlabstone.clearModelNodes()
        self.visualNPOfSlabstone.setScale(0.5)
        self.visualNPOfSlabstone.reparentTo(slabstoneBoxNP)

        self.slabstoneNP = slabstoneBoxNP

    def initOutZero(self):
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        outZeroBoxNP = self.worldNP.attachNewNode(
            BulletRigidBodyNode('OutZeroBox'))
        outZeroBoxNP.node().addShape(shape)
        outZeroBoxNP.setPos(16, 1, 0)
        outZeroBoxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(outZeroBoxNP.node())
        # self.visualNPOfOutZero = loader.loadModel('models/Cloudcube.egg')
        # self.visualNPOfOutZero.clearModelNodes()
        # self.visualNPOfOutZero.setScale(0.5)
        # self.visualNPOfOutZero.reparentTo(outZeroBoxNP)

        self.outZeroNP = outZeroBoxNP

    # 零摩擦地图
    def initZero(self):
        # 零摩擦第一层（2个传送）
        L1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2,
               1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 3, 1, 0, 0, 0],
              [0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2,
               2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 0, 0, 0],
              [0, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0],
              [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1,
               2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
              [1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
               2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0],
              [1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1,
               1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 0, 0, 0],
              [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1,
               1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0],
              [1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2,
               2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1, 0, 0],
              [1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 3, 2, 1, 1, 2, 2, 2, 2,
               2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0],
              [1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0]]

        L1CountX = 0
        for i in L1:
            L1CountY = -1
            for j in i:
                if j == 0:
                    L1CountY += 1
                    # continue
                if j == 1:
                    L1CountY += 1
                    self.initWallBoxes(L1CountX, L1CountY, 0)
                    # continue
                if j == 2:
                    L1CountY += 1
                    self.initGroundBoxes(L1CountX, L1CountY, 0)
                    # continue
                if j == 3:
                    self.countTransTag += 1
                    L1CountY += 1
                    self.transList.append(self.initTransBoxes(L1CountX, L1CountY, 0, self.worldNP, 0.5))
                    # continue
            L1CountX += 1

        # 零摩擦第二层（4个传送）
        L2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 2,
               1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 2, 2, 2,
               1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 3, 2, 1, 3, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2,
               1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2,
               2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2,
               2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2,
               1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2,
               2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1,
               2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1,
               2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 2, 2, 2, 2, 1, 1,
               1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]

        L2CountX = 0
        for i in L2:
            L2CountY = 0
            for j in i:
                if j == 0:
                    L2CountY += 1
                    # continue
                if j == 1:
                    L2CountY += 1
                    self.initWallBoxes(L2CountX, L2CountY, 20)
                    # continue
                if j == 2:
                    L2CountY += 1
                    self.initGroundBoxes(L2CountX, L2CountY, 20)
                    # continue
                if j == 3:
                    self.countTransTag += 1
                    L2CountY += 1
                    self.transList.append(self.initTransBoxes(L2CountX, L2CountY, 20, self.worldNP, 0.5))
                    # continue
            L2CountX += 1

        # 零摩擦第三层（2个传送）
        L3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                  2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1,
               1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2,
               2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1,
               2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1,
               2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 2, 2, 2, 1,
               2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 3, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]]

        L3CountX = 0
        for i in L3:
            L3CountY = 0
            for j in i:
                if j == 0:
                    L3CountY += 1
                    # continue
                if j == 1:
                    L3CountY += 1
                    self.initWallBoxes(L3CountX, L3CountY, 40)
                    # continue
                if j == 2:
                    L3CountY += 1
                    self.initGroundBoxes(L3CountX, L3CountY, 40)
                    # continue
                if j == 3:
                    self.countTransTag += 1
                    L3CountY += 1
                    self.transList.append(self.initTransBoxes(L3CountX, L3CountY, 40, self.worldNP, 0.5))
                    # continue
            L3CountX += 1

    #*************制作挡板旋转的动画的一部分**************
    def blockerReframeIntervalFor2(self, index):
        interval = self.alarms[index][0][0].posInterval(playSpeed * 1.5,(blockerSpacing , -blockerWidth * 2.1, blockerheight * 1.5),
            startPos = (0, -blockerWidth * 2.1, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][1][0].posInterval(playSpeed * 1.5,(-blockerSpacing , -blockerWidth * 2.1, blockerheight * 1.5),
            startPos = (0, -blockerWidth * 2.1, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][0][1].posInterval(playSpeed * 1.5,(blockerWidth * 2.1, blockerSpacing, blockerheight * 1.5),
            startPos = (blockerWidth * 2.1, 0, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][1][1].posInterval(playSpeed * 1.5,(blockerWidth * 2.1, -blockerSpacing, blockerheight * 1.5),
            startPos = (blockerWidth * 2.1, 0, blockerheight * 10))
        interval.start()

    def blockerReframeIntervalFor3(self, index):
        interval = self.alarms[index][0][0].posInterval(playSpeed * 1.5,(blockerSpacing, -blockerWidth, blockerheight),
            startPos = (0, -blockerWidth, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][1][0].posInterval(playSpeed * 1.5,(-blockerSpacing, -blockerWidth, blockerheight),
            startPos = (0, -blockerWidth, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][0][1].posInterval(playSpeed * 1.5,(blockerWidth, blockerSpacing, blockerheight),
            startPos = (blockerWidth, 0, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][1][1].posInterval(playSpeed * 1.5,(blockerWidth, -blockerSpacing, blockerheight),
            startPos = (blockerWidth, 0, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][0][2].posInterval(playSpeed * 1.5,(-blockerSpacing, blockerWidth, blockerheight),
            startPos = (0, blockerWidth, blockerheight * 10))
        interval.start()
        interval = self.alarms[index][1][2].posInterval(playSpeed * 1.5,(blockerSpacing, blockerWidth, blockerheight),
            startPos = (0, blockerWidth, blockerheight * 10))
        interval.start()

    #*************** 初始化BMaze地面和墙体box *****************
    def initMaze(self):
        # 放置路面
        shape = BulletBoxShape(Vec3(9, 7, 0.5))
        groundboxNP1 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('GroundBox1'))
        groundboxNP1.node().addShape(shape)
        groundboxNP1.setCollideMask(BitMask32.allOn())
        groundboxNP1.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(groundboxNP1.node())
        for j in xrange(0,9):
            for i in xrange(0,7):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-8 + j * 2,-6 + i * 2,0)
                visualNP.reparentTo(groundboxNP1)

        # 放置路面
        shape = BulletBoxShape(Vec3(4, 1, 0.5))
        groundboxNP2 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('GroundBox2'))
        groundboxNP2.node().addShape(shape)
        groundboxNP2.setPos(-13, 5, 0)
        groundboxNP2.setCollideMask(BitMask32.allOn())
        groundboxNP2.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(groundboxNP2.node())
        for j in xrange(0,4):
            for i in xrange(0,1):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-3 + j * 2,0 + i * 2,0)
                visualNP.reparentTo(groundboxNP2)

        #中间偏左
        shape1 = BulletBoxShape(Vec3(6, 1, 0.5))
        wall1 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('wall1'))
        wall1.node().addShape(shape1)
        wall1.setPos(0, 2, 1)
        wall1.setCollideMask(BitMask32.allOn())
        wall1.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(wall1.node())
        for j in xrange(0,6):
            for i in xrange(0,1):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-5 + j * 2,0 + i * 2,0)
                visualNP.reparentTo(wall1)

        #中间偏右
        shape2 = BulletBoxShape(Vec3(2, 1, 0.5))
        wall2 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('wall2'))
        wall2.node().addShape(shape2)
        wall2.setPos(-4, 0, 1)
        wall2.setCollideMask(BitMask32.allOn())
        wall2.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(wall2.node())
        for j in xrange(0,2):
            for i in xrange(0,1):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-1 + j * 2,0 + i * 2,0)
                visualNP.reparentTo(wall2)

        #左上角
        shape3 = BulletBoxShape(Vec3(5, 1, 0.5))
        wall3 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('wall3'))
        wall3.node().addShape(shape3)
        wall3.setPos(3, 6, 1)
        wall3.setCollideMask(BitMask32.allOn())
        wall3.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(wall3.node())
        for j in xrange(0,5):
            for i in xrange(0,1):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-4 + j * 2, 0 + i * 2, 0)
                visualNP.reparentTo(wall3)

        #右下角
        shape4 = BulletBoxShape(Vec3(2, 2, 0.5))
        wall4 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('wall4'))
        wall4.node().addShape(shape4)
        wall4.setPos(-1, -5, 1)
        wall4.setCollideMask(BitMask32.allOn())
        wall4.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(wall4.node())
        for j in xrange(0, 2):
            for i in xrange(0, 2):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-1 + j * 2, -1 + i * 2, 0)
                visualNP.reparentTo(wall4)

        #右上角
        wall5 = self.BMazeNP.attachNewNode(BulletRigidBodyNode('wall5'))
        wall5.node().addShape(shape4)
        wall5.setPos(6, -5, 1)
        wall5.setCollideMask(BitMask32.allOn())
        wall5.setAntialias(AntialiasAttrib.MMultisample)
        self.world.attachRigidBody(wall5.node())
        for j in xrange(0, 2):
            for i in xrange(0, 2):
                visualNP = loader.loadModel('models/cube')
                visualNP.clearModelNodes()
                visualNP.setScale(1, 1, 0.5)
                visualNP.setPos(-1 + j * 2, -1 + i * 2, 0)
                visualNP.reparentTo(wall5)

    #************* 初始化挡板blocker ****************   
    def initBlocker(self):
        self.BMazeNP = self.worldNP.attachNewNode('BMazeNode')
        self.BMazeNP.setPos(60,25,0)
        self.alarms = []
        self.blockerStates = []
        
        blocker1 = self.setBlocker(1)
        blocker1.setHpr(180, 0, 0)
        blocker1.setPos(-2,5,0)

        blocker2 = self.setBlocker(1)
        blocker2.setHpr(180, 0, 0)
        blocker2.setPos(-3, -3, 0)

        blocker3 = self.setBlocker(2)
        blocker3.setHpr(180, 0, 0)
        blocker3.setPos(5, -3, 0)
        self.blockers = [blocker1, blocker2, blocker3]
        self.blockerStates.append(1)
        self.blockerStates.append(0)
        self.blockerStates.append(0)

    #制作挡板类框架，方便编程
    def setBlocker(self,Btype):
        blockerRoot = self.BMazeNP.attachNewNode('BlockerRoot')
        #短3个
        if Btype == 1:
            shape1 = BulletBoxShape(Vec3(0.001, blockerWidth, blockerWidth))
            #clockwise顺时针警报器
            cwAlarm1 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm1'))
            cwAlarm1.node().addShape(shape1)
            cwAlarm1.setPos(blockerSpacing, -blockerWidth, blockerheight)
            cwAlarm1.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(cwAlarm1.node())
            interval = cwAlarm1.posInterval(0.1,(blockerSpacing, -blockerWidth, blockerheight),
                startPos = (0, -blockerWidth, blockerheight))
            interval.start()
            #anticlockwise逆时针警报器
            acwAlarm1 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm2'))
            acwAlarm1.node().addShape(shape1)
            acwAlarm1.setPos(-blockerSpacing, -blockerWidth, blockerheight)
            acwAlarm1.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(acwAlarm1.node())
            interval = acwAlarm1.posInterval(0.1,(-blockerSpacing, -blockerWidth, blockerheight),
                startPos = (0, -blockerWidth, blockerheight))
            interval.start()
            #载入模型
            visualNP1 = loader.loadModel('models/blocker-both.egg')
            visualNP1.clearModelNodes
            visualNP1.setScale(0.19)
            visualNP1.setPos(0,-0.08,0.5)
            visualNP1.reparentTo(blockerRoot)

            shape2 = BulletBoxShape(Vec3(blockerWidth - 0.1, 0.001, blockerWidth))
            #clockwise顺时针警报器
            cwAlarm2 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm3'))
            cwAlarm2.node().addShape(shape2)
            cwAlarm2.setPos(blockerWidth,blockerSpacing, blockerheight)
            cwAlarm2.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(cwAlarm2.node())
            interval = cwAlarm2.posInterval(0.1,(blockerWidth, blockerSpacing, blockerheight),
                startPos = (blockerWidth, 0, blockerheight))
            interval.start()
            #anticlockwise逆时针警报器
            acwAlarm2 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm4'))
            acwAlarm2.node().addShape(shape2)
            acwAlarm2.setPos(blockerWidth,-blockerSpacing, blockerheight)
            acwAlarm2.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(acwAlarm2.node())
            interval = acwAlarm2.posInterval(0.1,(blockerWidth,-blockerSpacing, blockerheight),
                startPos = (blockerWidth,0, blockerheight))
            interval.start()
            #载入模型
            visualNP2 = loader.loadModel('models/blocker-both.egg')
            visualNP2.clearModelNodes
            visualNP2.setScale(0.19)
            visualNP2.setHpr(90,0,0)
            visualNP2.setPos(0.08,0,0.5)
            visualNP2.reparentTo(blockerRoot)

            #clockwise顺时针警报器
            cwAlarm3 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm5'))
            cwAlarm3.node().addShape(shape1)
            cwAlarm3.setPos(-blockerSpacing, blockerWidth, blockerheight)
            cwAlarm3.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(cwAlarm3.node())
            interval = cwAlarm3.posInterval(0.1,(-blockerSpacing, blockerWidth, blockerheight),
                startPos = (0, blockerWidth, blockerheight))
            interval.start()
            #anticlockwise逆时针警报器
            acwAlarm3 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm6'))
            acwAlarm3.node().addShape(shape1)
            acwAlarm3.setPos(blockerSpacing, blockerWidth, blockerheight)
            acwAlarm3.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(acwAlarm3.node())
            interval = acwAlarm3.posInterval(0.1,(blockerSpacing, blockerWidth, blockerheight),
                startPos = (0, blockerWidth, blockerheight))
            interval.start()
            #载入模型
            visualNP3 = loader.loadModel('models/blocker-both.egg')
            visualNP3.clearModelNodes
            visualNP3.setScale(0.19)
            visualNP3.setHpr(180,0,0)
            visualNP3.setPos(0,0.1,0.5)
            visualNP3.reparentTo(blockerRoot)

            cwAlarms = [cwAlarm1, cwAlarm2, cwAlarm3]
            acwAlarms = [acwAlarm1, acwAlarm2, acwAlarm3]
            tempAlarms = [cwAlarms, acwAlarms]
            self.alarms.append(tempAlarms)
        elif Btype == 2:
            shape1 = BulletBoxShape(Vec3(0.001, blockerWidth * 2, blockerWidth * 2))
            #clockwise顺时针警报器
            cwAlarm1 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm1'))
            cwAlarm1.node().addShape(shape1)
            cwAlarm1.setPos(blockerSpacing, -blockerWidth * 2, blockerheight * 1.5)
            cwAlarm1.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(cwAlarm1.node())
            interval = cwAlarm1.posInterval(0.01,(blockerSpacing, -blockerWidth * 2.1, blockerheight * 1.5),
                startPos = (0, -blockerWidth * 2, blockerheight * 1.5))
            interval.start()
            #anticlockwise逆时针警报器
            acwAlarm1 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm2'))
            acwAlarm1.node().addShape(shape1)
            acwAlarm1.setPos(-blockerSpacing, -blockerWidth * 2, blockerheight * 1.5)
            acwAlarm1.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(acwAlarm1.node())
            interval = acwAlarm1.posInterval(0.01,(-blockerSpacing, -blockerWidth * 2.1, blockerheight * 1.5),
                startPos = (0, -blockerWidth * 2, blockerheight * 1.5))
            interval.start()
            #载入模型
            visualNP1 = loader.loadModel('models/blocker-both.egg')
            visualNP1.clearModelNodes
            visualNP1.setScale(0.35)
            visualNP1.setPos(0,-0.2,0.5)
            visualNP1.reparentTo(blockerRoot)

            shape2 = BulletBoxShape(Vec3(blockerWidth * 2, 0.001, blockerWidth * 2))
            #clockwise顺时针警报器
            cwAlarm2 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm3'))
            cwAlarm2.node().addShape(shape2)
            cwAlarm2.setPos(blockerWidth * 2.1,blockerSpacing * 2, blockerheight * 1.5)
            cwAlarm2.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(cwAlarm2.node())
            interval = cwAlarm2.posInterval(0.01,(blockerWidth * 2.1, blockerSpacing * 2, blockerheight * 1.5),
                startPos = (blockerWidth * 2.1, 0, blockerheight * 1.5))
            interval.start()
            #anticlockwise逆时针警报器
            acwAlarm2 = blockerRoot.attachNewNode(BulletRigidBodyNode('alarm4'))
            acwAlarm2.node().addShape(shape2)
            acwAlarm2.setPos(blockerWidth * 2.1, -blockerSpacing * 2, blockerheight * 1.5)
            acwAlarm2.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(acwAlarm2.node())
            interval = acwAlarm2.posInterval(0.1,(blockerWidth * 2.1, -blockerSpacing * 2, blockerheight * 1.5),
                startPos = (blockerWidth * 2.1, 0, blockerheight * 1.5))
            interval.start()
            #载入模型
            visualNP2 = loader.loadModel('models/blocker-both.egg')
            visualNP2.clearModelNodes
            visualNP2.setScale(0.35)
            visualNP2.setHpr(90,0,0)
            visualNP2.setPos(0.25,0,0.5)
            visualNP2.reparentTo(blockerRoot)

            cwAlarms = [cwAlarm1, cwAlarm2]
            acwAlarms = [acwAlarm1, acwAlarm2]
            tempAlarms = [cwAlarms, acwAlarms]
            self.alarms.append(tempAlarms)  
        return blockerRoot

    def initBMaze(self):
        self.initBlocker()
        self.initMaze()

    # 初始化
    def setup(self):
        self.worldNP = render.attachNewNode('World')

        # World
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()
        self.debugNP.node().showWireframe(True)
        self.debugNP.node().showConstraints(True)
        self.debugNP.node().showBoundingBoxes(False)
        self.debugNP.node().showNormals(True)

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        # 传送阵标识
        self.countTransTag = -1
        self.transList = []

        self.initZero()
        self.initSlabstone()
        self.initOutZero()
        self.initCharacter(40, 20, 1)
        self.initHP()
        self.initFMaze()
        self.initBMaze()
        self.initTMaze()
        self.initMainGround()
        self.initGear()

    # 摄像机更新函数
    def updatecam(self):
        self.cam.setPos(self.characterNP.getX(
        ) - 8, self.characterNP.getY() - 9.5, self.characterNP.getZ() + 8.5)
        self.skybox.setPos(self.cam.getPos())
        self.cam.lookAt(self.characterNP)
        # print self.cam.getPos()

class FireNode():
    """docstring for fire"""
    def __init__(self, fatherNode, world):
        self.canDamage = 1
        self.lastTag = 0
        shape = BulletBoxShape(Vec3(1,1,0.5))
        self.thrower = fatherNode.attachNewNode(BulletRigidBodyNode('firenode'))
        self.thrower.setCollideMask(BitMask32.allOn())
        self.thrower.node().addShape(shape)
        throwerModel = loader.loadModel('models/ph')
        throwerModel.setPos(0,0,0.6)
        throwerModel.setScale(0.6)
        throwerModel.reparentTo(self.thrower)
        cubeModel = loader.loadModel('models/cube')
        cubeModel.setScale(1,1,0.5)
        cubeModel.reparentTo(self.thrower)
        world.attachRigidBody(self.thrower.node())
        self.particle = ParticleEffect()
        self.particle.loadConfig(Filename('models/fireish.ptf'))
        self.particle.start(self.thrower)
        self.particle.setPos(0.000, 0.000, 1.250)

game = Skybox()
game.run()
