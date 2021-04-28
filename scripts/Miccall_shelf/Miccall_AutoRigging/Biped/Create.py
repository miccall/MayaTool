# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


class CreateBipedJoints:
    def __init__(self):
        self.TorsoChainNames = ['Hip_JNT']
        self.LegChainNames = ['Thigh_L_JNT', 'Shin_L_JNT', 'Foot_L_JNT', 'Ball_L_JNT', 'Toe_L_JNT']
        self.SplineCount = 3
        self.splineLength = 30
        self.HipSize = 15
        self.CharacterHeight = 170
        self.LegLenght = self.CharacterHeight / 1.618
        self.ThighLenght = self.LegLenght * 3 / 8
        self.CalfLenght = self.LegLenght * 5 / 8
        self.FootHeight = 8
        self.Hip = None

        # self.CreatTorso()
        self.CreatLeg()
        pass

    def CreatLeg(self):
        # print("create Leg ")
        self.Thigh = cmds.joint(p=(self.HipSize, self.LegLenght, 0))
        self.Shin = cmds.joint(p=(self.HipSize, self.CalfLenght, 5))
        cmds.joint(self.Thigh, e=True, zso=True, oj='xyz', sao='xup', ch=True)
        self.Foot = cmds.joint(p=(self.HipSize, self.FootHeight, 0))
        cmds.joint(self.Shin, e=True, zso=True, oj='xyz', sao='xup', ch=True)
        self.Ball = cmds.joint(p=(self.HipSize, 0, 15))
        cmds.joint(self.Foot, e=True, zso=True, oj='xyz', sao='xup', ch=True)
        self.Toe = cmds.joint(p=(self.HipSize, 0, 23))
        cmds.joint(self.Ball, e=True, zso=True, oj='xyz', sao='xup', ch=True)
        # Rename
        cmds.rename(self.Thigh, self.LegChainNames[0])
        self.Thigh = self.LegChainNames[0]
        cmds.rename(self.Shin, self.LegChainNames[1])
        self.Shin = self.LegChainNames[1]
        cmds.rename(self.Foot, self.LegChainNames[2])
        self.Foot = self.LegChainNames[2]
        cmds.rename(self.Ball, self.LegChainNames[3])
        self.Ball = self.LegChainNames[3]
        cmds.rename(self.Toe, self.LegChainNames[4])
        self.Toe = self.LegChainNames[4]
        # hirechy
        if self.Hip is not None:
            cmds.parent(self.Thigh, self.Hip)
        # Clear
        cmds.select(clear=True)
        pass

    def CreatTorso(self):
        self.Hip = cmds.joint(p=(0, self.LegLenght + 10, 0))
        cmds.rename(self.Hip, self.TorsoChainNames[0])
        self.Hip = self.TorsoChainNames[0]
        for i in range(0, self.SplineCount):
            Spline = cmds.joint(p=(0, self.LegLenght + (i + 1) * self.splineLength + 10, 0))
            cmds.joint(Spline, e=True, zso=True, oj='xyz', sao='yup')
            cmds.rename(Spline, "Spline%s_JNT" % str(i))
            self.TorsoChainNames.append("Spline%s_JNT" % str(i))
        cmds.select(clear=True)
        pass

    def CreatArm(self):
        pass

    def CreateHead(self):
        pass

    def CreateHand(self):
        pass
