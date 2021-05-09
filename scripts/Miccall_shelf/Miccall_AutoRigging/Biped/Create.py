# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


class CreateBipedJoints:
    def __init__(self):
        self.root = "Hip_JNT"
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
        self.CreateProxies()
        # self.CreatTorso()
        # self.CreatLeg()
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
            cmds.rename(Spline, "Spline%s_JNT" % str(i))
            self.TorsoChainNames.append("Spline%s_JNT" % str(i))
        cmds.select(clear=True)
        cmds.joint(self.TorsoChainNames[0], e=True, zso=True, oj='xzy', sao='xup', ch=True)
        pass

    def CreatArm(self):
        pass

    def CreateHead(self):
        pass

    def CreateHand(self):
        pass

    def ProxyBase(self, name):
        first = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=0.25, d=3, ut=0, tol=0.01, s=8, ch=1)
        cmds.rename(first[0], name)
        scend = cmds.duplicate(rr=True)
        cmds.rename(scend[0], "%sB" % name)
        cmds.setAttr("%sB.rx" % name, 90)
        cmds.makeIdentity("%sB" % name, apply=True, t=1, r=1, s=1)
        third = cmds.duplicate(rr=True)
        cmds.rename(third[0], "%sC" % name)
        cmds.setAttr("%sC.ry" % name, 90)
        cmds.makeIdentity("%sC" % name, apply=True, t=1, r=1, s=1)
        Loc = cmds.spaceLocator()
        cmds.rename(Loc[0], "%sSnap" % name)
        cmds.setAttr("%sSnapShape.localScaleZ" % name, 0.25)
        cmds.setAttr("%sSnapShape.localScaleX" % name, 0.25)
        cmds.setAttr("%sSnapShape.localScaleY" % name, 0.25)
        cmds.parent("%sBShape" % name, "%sCShape" % name, "%sSnapShape" % name, name, r=True, s=True)
        cmds.delete("%sB" % name, "%sC" % name, "%sSnap" % name)
        cmds.select(name)
        cmds.makeIdentity(name, apply=True, t=1, r=1, s=1)
        cmds.delete(name, ch=True)

    def ProxyAim(self, name):
        self.ProxyBase(name)
        cmds.curve(n="%s_Aim" % name, d=1,
                   p=[(-0.25, 0, 0), (-0.25, 0, -1), (-0.5, 0, -1), (0, 0, -1.5), (0.5, 0, -1), (0.25, 0, -1),
                      (0.25, 0, 0)], k=[0, 1, 2, 3, 4, 5, 6])
        pw = cmds.pickWalk(d="down")
        cmds.rename(pw[0], "%s_AimShape" % name)
        PCons = cmds.pointConstraint(name, "%s_Aim" % name)
        cmds.delete(PCons)
        cmds.makeIdentity("%s_Aim" % name, apply=True, t=1, r=1, s=1)
        cmds.parent("%s_AimShape" % name, name)
        cmds.delete("%s_Aim" % name)

    def ProxyUp(self, name):
        self.ProxyBase(name)

    def ProxyConnectors(self, node1, node2):

        cmds.curve(n="%s_%s_Connector" % (node1, node2), d=1, p=[(0, 0, 0), (1, 0, 0)], k=[0, 1])
        pw = cmds.pickWalk(d="down")
        cmds.rename(pw[0], "%s_%s_CShape" % (node1, node2))
        cmds.spaceLocator(n=(node1 + "_" + node2 + "_AimLctr"))
        cmds.spaceLocator(n=(node1 + "_" + node2 + "_TargetLctr"))
        cmds.parent((node1 + "_" + node2 + "_TargetLctr"), (node1 + "_" + node2 + "_AimLctr"))
        cmds.pointConstraint(node1, (node1 + "_" + node2 + "_AimLctr"))
        cmds.aimConstraint(node2, (node1 + "_" + node2 + "_AimLctr"), aimVector=[1, 0, 0], upVector=[0, 1, 0],
                           worldUpType="none")
        cmds.pointConstraint(node2, (node1 + "_" + node2 + "_TargetLctr"))

        cmds.connectAttr((node1 + "_" + node2 + "_AimLctr.translate"), (node1 + "_" + node2 + "_Connector.translate"))
        cmds.connectAttr((node1 + "_" + node2 + "_AimLctr.rotate"), (node1 + "_" + node2 + "_Connector.rotate"))
        cmds.connectAttr((node1 + "_" + node2 + "_TargetLctr.tx"), (node1 + "_" + node2 + "_Connector.sx"))
        cmds.setAttr(node1 + "_" + node2 + "_AimLctr.v", 0)
        cmds.setAttr(node1 + "_" + node2 + "_Connector.template", 1)

        if not cmds.objExists("Proxies_ConnectorG"):
            cmds.group(em=True, n="Proxies_ConnectorG")
            cmds.xform(os=True, piv=(0, 0, 0))
            cmds.setAttr("Proxies_ConnectorG.inheritsTransform", 0)
            cmds.parent("Proxies_ConnectorG", self.Main)

        cmds.parent((node1 + "_" + node2 + "_Connector"), (node1 + "_" + node2 + "_AimLctr"), "Proxies_ConnectorG")
        cmds.setAttr(node1 + "_" + node2 + "_AimLctr.scale", 1, 1, 1)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.tx"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.ty"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.tz"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.rx"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.ry"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.rz"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.sx"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.sy"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.sz"), lock=True, keyable=False, channelBox=False)
        cmds.setAttr((node1 + "_" + node2 + "_Connector.v"), lock=True, keyable=False, channelBox=False)

    def CreateProxies(self):
        thumbsOn = True
        fingersNum = 5
        toesNum = 1
        spineNum = 4
        neckNum = 3
        self.Main = "Main"
        self.Proxies_Root = "Proxies_Root"
        self.Proxies_SpineTop = "Proxies_SpineTop"
        self.Proxies_Head = "Proxies_Head"
        self.Proxies_Jaw = "Proxies_Jaw"
        self.Proxies_JawTip = "Proxies_JawTip"
        self.Proxies_HeadTip = "Proxies_HeadTip"
        self.Proxies_LeftEye = "Proxies_LeftEye"
        self.Proxies_RightEye = "Proxies_RightEye"
        self.Proxies_SpineOrientLocator = "Proxies_SpineOrientLocator"
        self.Proxies_NeckOrientLocator = "Proxies_NeckOrientLocator"
        # todo : SET UNITS TO CENTIMETERS
        # todo :  Close NODE EDITOR
        # Joint Base
        Main = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=8, d=3, ut=0, tol=0.01, s=8, ch=0)
        cmds.rename(Main[0], self.Main)

        # Root
        self.ProxyBase(self.Proxies_Root)
        cmds.scale(1.6, 1.6, 1.6, self.Proxies_Root, r=True)
        cmds.move(0, 15.25, 0, self.Proxies_Root, r=True, os=True, wd=True)
        cmds.makeIdentity("%s" % self.Proxies_Root, apply=True, t=1, r=1, s=1)
        cmds.setAttr("%sSnapShape.localScaleX" % self.Proxies_Root, 0.4)
        cmds.setAttr("%sSnapShape.localScaleY" % self.Proxies_Root, 0.4)
        cmds.setAttr("%sSnapShape.localScaleZ" % self.Proxies_Root, 0.4)

        # Top
        self.ProxyBase(self.Proxies_SpineTop)
        PCons = cmds.pointConstraint(self.Proxies_Root, self.Proxies_SpineTop)
        cmds.delete(PCons)
        cmds.move(0, 6.6, 0, self.Proxies_SpineTop, r=True, os=True, wd=True)
        cmds.scale(1.6, 1.6, 1.6, self.Proxies_SpineTop, r=True)
        cmds.makeIdentity("%s" % self.Proxies_SpineTop, apply=True, t=1, r=1, s=1)
        cmds.setAttr("%sSnapShape.localScaleX" % self.Proxies_SpineTop, 0.4)
        cmds.setAttr("%sSnapShape.localScaleY" % self.Proxies_SpineTop, 0.4)
        cmds.setAttr("%sSnapShape.localScaleZ" % self.Proxies_SpineTop, 0.4)

        # Aim Locator
        loc = cmds.spaceLocator()
        cmds.rename(loc[0], self.Proxies_SpineOrientLocator)
        cmds.parent(self.Proxies_SpineOrientLocator, self.Main)
        cmds.pointConstraint(self.Proxies_Root, self.Proxies_SpineOrientLocator)
        cmds.aimConstraint(self.Proxies_SpineTop, self.Proxies_SpineOrientLocator, aimVector=[0, 1, 0],
                           upVector=[1, 0, 0], worldUpType="vector", worldUpVector=[1, 0, 0])
        cmds.setAttr("%s.visibility" % self.Proxies_SpineOrientLocator, 0)

        # Spline
        self.spineProxies = []
        i2 = spineNum - 1
        nPad = "0"
        for i in range(1, spineNum):
            self.ProxyBase("Proxies_Spine_%s%s" % (nPad, i))
            cmds.group("Proxies_Spine_%s%s" % (nPad, i), n="Proxies_Spine_%s%s_GRP" % (nPad, i))
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.makeIdentity("Proxies_Spine_%s%s_GRP" % (nPad, i), apply=True, t=1, r=1, s=1)
            cmds.pointConstraint(self.Proxies_Root, self.Proxies_SpineTop, "Proxies_Spine_%s%s_GRP" % (nPad, i))
            cmds.orientConstraint(self.Proxies_SpineOrientLocator, "Proxies_Spine_%s%s_GRP" % (nPad, i))
            cmds.setAttr("Proxies_Spine_%s%s_GRP_pointConstraint1.Proxies_RootW0" % (nPad, i), i2)
            cmds.setAttr("Proxies_Spine_%s%s_GRP_pointConstraint1.Proxies_SpineTopW1" % (nPad, i), i)
            self.spineProxies.append("Proxies_Spine_%s%s" % (nPad, i))
            # CONNECTORS
            if i == 1:
                self.ProxyConnectors(self.Proxies_Root, "Proxies_Spine_%s%s" % (nPad, i))
            else:
                self.ProxyConnectors("Proxies_Spine_%s%s" % (nPad, i), "Proxies_Spine_%s%s" % (nPad, i - 1))
            i2 = i2 - 1

        self.ProxyConnectors("Proxies_Spine_%s%s" % (nPad, spineNum - 1), self.Proxies_SpineTop)

        cmds.select(self.spineProxies)
        cmds.pickWalk(d="up")
        spineProxiesG = cmds.ls(sl=True)

        # Neck
        self.ProxyBase(self.Proxies_Head)
        PCons = cmds.pointConstraint(self.Proxies_SpineTop, self.Proxies_Head)
        cmds.delete(PCons)
        cmds.move(0, 2, 0, self.Proxies_Head, r=True, os=True, wd=True)
        cmds.scale(1.25, 1.25, 1.25, self.Proxies_Head, r=True)
        cmds.makeIdentity("%s" % self.Proxies_Head, apply=True, t=1, r=1, s=1)
        # CREATE AIM LOCATOR TO ORIENT NECK PROXIES
        cmds.spaceLocator(n=self.Proxies_NeckOrientLocator)
        cmds.parent(self.Proxies_NeckOrientLocator, self.Main)
        cmds.pointConstraint(self.Proxies_SpineTop, self.Proxies_NeckOrientLocator)
        cmds.aimConstraint(self.Proxies_Head, self.Proxies_NeckOrientLocator, aimVector=[0, 1, 0],
                           upVector=[1, 0, 0], worldUpType="vector", worldUpVector=[1, 0, 0])
        cmds.setAttr("%s.visibility" % self.Proxies_NeckOrientLocator, 0)

        self.neckProxies = []
        i2 = neckNum - 1
        nPad = "0"
        for i in range(1, neckNum):
            self.ProxyBase("Proxies_Neck_%s%s" % (nPad, i))
            cmds.scale(0.8, 0.8, 0.8, "Proxies_Neck_%s%s" % (nPad, i), r=True)
            cmds.makeIdentity("Proxies_Neck_%s%s" % (nPad, i), apply=True, t=1, r=1, s=1)
            cmds.group("Proxies_Neck_%s%s" % (nPad, i), n="Proxies_Neck_%s%s_GRP" % (nPad, i))
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.makeIdentity("Proxies_Neck_%s%s_GRP" % (nPad, i), apply=True, t=1, r=1, s=1)
            cmds.pointConstraint(self.Proxies_SpineTop, self.Proxies_Head, "Proxies_Neck_%s%s_GRP" % (nPad, i))
            cmds.orientConstraint(self.Proxies_NeckOrientLocator, "Proxies_Neck_%s%s_GRP" % (nPad, i))
            cmds.setAttr("Proxies_Neck_%s%s_GRP_pointConstraint1.Proxies_SpineTopW0" % (nPad, i), i2)
            cmds.setAttr("Proxies_Neck_%s%s_GRP_pointConstraint1.Proxies_HeadW1" % (nPad, i), i)
            self.neckProxies.append("Proxies_Neck_%s%s" % (nPad, i))
            if i == 1:
                self.ProxyConnectors(self.Proxies_SpineTop, "Proxies_Neck_%s%s" % (nPad, i))
            else:
                self.ProxyConnectors("Proxies_Neck_%s%s" % (nPad, i), "Proxies_Neck_%s%s" % (nPad, i - 1))
            i2 = i2 - 1

        cmds.select(self.neckProxies)
        cmds.pickWalk(d="up")
        neckProxiesG = cmds.ls(sl=True)

        self.ProxyConnectors("Proxies_Neck_%s%s" % (nPad, neckNum - 1), self.Proxies_Head)

        # Jaw
        self.ProxyBase(self.Proxies_Jaw)
        PCons = cmds.pointConstraint(self.Proxies_Head, self.Proxies_Jaw)
        cmds.delete(PCons)
        cmds.move(0, 0.83, 0.38, self.Proxies_Jaw, r=True, os=True, wd=True)
        cmds.makeIdentity(self.Proxies_Jaw, apply=True, t=1, r=1, s=1)
        self.ProxyConnectors(self.Proxies_Head, self.Proxies_Jaw)

        self.ProxyBase(self.Proxies_JawTip)
        PCons = cmds.pointConstraint(self.Proxies_Jaw, self.Proxies_JawTip)
        cmds.delete(PCons)
        cmds.move(0, -0.83, 1.52, self.Proxies_JawTip, r=True, os=True, wd=True)
        cmds.makeIdentity(self.Proxies_JawTip, apply=True, t=1, r=1, s=1)
        self.ProxyConnectors(self.Proxies_Jaw, self.Proxies_JawTip)

        self.ProxyBase(self.Proxies_HeadTip)
        PCons = cmds.pointConstraint(self.Proxies_Head, self.Proxies_HeadTip)
        cmds.delete(PCons)
        cmds.move(0, 3.38, 0, self.Proxies_HeadTip, r=True, os=True, wd=True)
        cmds.makeIdentity(self.Proxies_HeadTip, apply=True, t=1, r=1, s=1)
        self.ProxyConnectors(self.Proxies_Head, self.Proxies_HeadTip)

        # Eye
        self.ProxyBase(self.Proxies_LeftEye)
        PCons = cmds.pointConstraint(self.Proxies_Head, self.Proxies_LeftEye)
        cmds.delete(PCons)
        cmds.move(0.57, 1.53, 1.64, self.Proxies_LeftEye, r=True, os=True, wd=True)
        cmds.makeIdentity(self.Proxies_LeftEye, apply=True, t=1, r=1, s=1)
        self.ProxyConnectors(self.Proxies_Head, self.Proxies_LeftEye)

        self.ProxyBase(self.Proxies_RightEye)
        PCons = cmds.pointConstraint(self.Proxies_Head, self.Proxies_RightEye)
        cmds.delete(PCons)
        cmds.move(-0.57, 1.53, 1.64, self.Proxies_RightEye, r=True, os=True, wd=True)
        cmds.makeIdentity(self.Proxies_RightEye, apply=True, t=1, r=1, s=1)
        self.ProxyConnectors(self.Proxies_Head, self.Proxies_RightEye)
        # Arms
        armLoop = 1
        armPrefx = "_L"
        armMultiplier = 1.0
        while armLoop <= 2:
            Clavicle = "Proxies" + armPrefx + "_Clavicle"
            self.ProxyBase(Clavicle)
            PCons = cmds.pointConstraint(self.Proxies_SpineTop, Clavicle)
            cmds.delete(PCons)
            cmds.move(armMultiplier * 1.25, 0.5, 0, Clavicle, r=True, os=True, wd=True)
            cmds.makeIdentity(Clavicle, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(self.Proxies_SpineTop, Clavicle)
            cmds.parent(Clavicle,self.Proxies_SpineTop)

            Shoulder = "Proxies" + armPrefx + "_Shoulder"
            self.ProxyBase(Shoulder)
            PCons = cmds.pointConstraint(Clavicle, Shoulder)
            cmds.delete(PCons)
            cmds.move(armMultiplier * 1.7, 0, 0, Shoulder, r=True, os=True, wd=True)
            cmds.makeIdentity(Shoulder, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Clavicle, Shoulder)
            cmds.parent(Shoulder,Clavicle)

            Elbow = "Proxies" + armPrefx + "_Elbow"
            self.ProxyBase(Elbow)
            PCons = cmds.pointConstraint(Shoulder, Elbow)
            cmds.delete(PCons)
            cmds.move(armMultiplier * 3.5, 0, 0, Elbow, r=True, os=True, wd=True)
            cmds.makeIdentity(Elbow, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Shoulder, Elbow)

            Wrist = "Proxies" + armPrefx + "_Wrist"
            self.ProxyBase(Wrist)
            PCons = cmds.pointConstraint(Elbow, Wrist)
            cmds.delete(PCons)
            cmds.move(armMultiplier * 3.5, 0, 0, Wrist, r=True, os=True, wd=True)
            cmds.makeIdentity(Wrist, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Elbow, Wrist)

            ElbowG = "Proxies"+ armPrefx + "_Elbow_GRP"
            cmds.group(n=ElbowG,em=True)
            PCons = cmds.pointConstraint(Elbow, ElbowG)
            cmds.delete(PCons)
            cmds.parent(Elbow,ElbowG)
            cmds.makeIdentity(ElbowG, apply=True, t=1, r=1, s=1)
            cmds.move(0,0,0.001,"%s.scalePivot" % ElbowG,"%s.rotatePivot"  % ElbowG ,r=True)
            cmds.pointConstraint(Shoulder,Wrist,ElbowG,mo=True)
            cmds.parent(ElbowG,Wrist,self.Main)

            Palm = "Proxies" + armPrefx + "_Palm"
            self.ProxyBase(Palm)
            cmds.makeIdentity(Palm, apply=True, t=1, r=1, s=1)
            PCons = cmds.pointConstraint(Wrist, Palm)
            cmds.delete(PCons)
            cmds.move(armMultiplier * 0.7, 0, 0, Palm, r=True, os=True, wd=True)
            cmds.scale(0.7, 0.7, 0.7, Palm)
            cmds.setAttr("%sSnapShape.localScaleX" % Palm, 0.175)
            cmds.setAttr("%sSnapShape.localScaleY" % Palm, 0.175)
            cmds.setAttr("%sSnapShape.localScaleZ" % Palm, 0.175)
            cmds.makeIdentity(Palm, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Wrist, Palm)
            cmds.parent(Palm, Wrist)

            if thumbsOn:
                ThumbJ1 = "Proxies" + armPrefx + "_ThumbJ1"
                self.ProxyBase(ThumbJ1)
                PCons = cmds.pointConstraint(Wrist, ThumbJ1)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0.45, 0, 0.51, ThumbJ1, r=True, os=True, wd=True)
                cmds.scale(0.75, 0.75, 0.75, ThumbJ1)
                cmds.makeIdentity(ThumbJ1, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % ThumbJ1, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleY" % ThumbJ1, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleZ" % ThumbJ1, 0.1875)

                ThumbJ2 = "Proxies" + armPrefx + "_ThumbJ2"
                self.ProxyBase(ThumbJ2)
                PCons = cmds.pointConstraint(ThumbJ1, ThumbJ2)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0, 0, 0.75, ThumbJ2, r=True, os=True, wd=True)
                cmds.scale(0.75, 0.75, 0.75, ThumbJ2)
                cmds.makeIdentity(ThumbJ2, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % ThumbJ2, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleY" % ThumbJ2, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleZ" % ThumbJ2, 0.1875)

                ThumbJ3 = "Proxies" + armPrefx + "_ThumbJ3"
                self.ProxyBase(ThumbJ3)
                PCons = cmds.pointConstraint(ThumbJ2, ThumbJ3)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0, 0, 0.75, ThumbJ3, r=True, os=True, wd=True)
                cmds.scale(0.75, 0.75, 0.75, ThumbJ3)
                cmds.makeIdentity(ThumbJ3, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % ThumbJ3, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleY" % ThumbJ3, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleZ" % ThumbJ3, 0.1875)

                ThumbJTip = "Proxies" + armPrefx + "_ThumbJTip"
                self.ProxyBase(ThumbJTip)
                PCons = cmds.pointConstraint(ThumbJ3, ThumbJTip)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0, 0, 0.75, ThumbJTip, r=True, os=True, wd=True)
                cmds.scale(0.75, 0.75, 0.75, ThumbJTip)
                cmds.makeIdentity(ThumbJTip, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % ThumbJTip, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleY" % ThumbJTip, 0.1875)
                cmds.setAttr("%sSnapShape.localScaleZ" % ThumbJTip, 0.1875)

                cmds.parent(ThumbJ1, Wrist)
                cmds.parent(ThumbJ2, ThumbJ2)
                cmds.parent(ThumbJ2, ThumbJ3)
                cmds.parent(ThumbJ3, ThumbJTip)

                self.ProxyConnectors(Wrist, ThumbJ1)
                self.ProxyConnectors(ThumbJ1, ThumbJ2)
                self.ProxyConnectors(ThumbJ2, ThumbJ3)
                self.ProxyConnectors(ThumbJ3, ThumbJTip)

            fingerIndex = 1
            while fingerIndex <= fingersNum:
                FingerJ1 = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_J1"
                if fingerIndex == 1:
                    self.ProxyBase(FingerJ1)
                    PCons = cmds.pointConstraint(Wrist, FingerJ1)
                    cmds.delete(PCons)
                    cmds.move(armMultiplier * 1.47, 0, 0, FingerJ1, r=True, os=True, wd=True)
                    if fingersNum == 2:
                        cmds.move(0, 0, 0.25, FingerJ1, r=True)
                        cmds.makeIdentity(FingerJ1, apply=True, t=1, r=1, s=1)
                    elif fingersNum >= 3:
                        cmds.move(0, 0, 0.5, FingerJ1, r=True)
                        cmds.makeIdentity(FingerJ1, apply=True, t=1, r=1, s=1)
                else:
                    FingerJ0 = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex - 1) + "_J1"
                    self.ProxyBase(FingerJ1)
                    PCons = cmds.pointConstraint(FingerJ0, FingerJ1)
                    cmds.delete(PCons)
                    cmds.move(0, 0, -0.4, FingerJ1, r=True, os=True, wd=True)

                cmds.scale(0.62, 0.62, 0.62, FingerJ1)
                cmds.makeIdentity(FingerJ1, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % FingerJ1, 0.155)
                cmds.setAttr("%sSnapShape.localScaleY" % FingerJ1, 0.155)
                cmds.setAttr("%sSnapShape.localScaleZ" % FingerJ1, 0.155)

                FingerJ2 = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_J2"
                self.ProxyBase(FingerJ2)
                PCons = cmds.pointConstraint(FingerJ1, FingerJ2)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0.61, 0, 0, FingerJ2, r=True, os=True, wd=True)
                cmds.scale(0.62, 0.62, 0.62, FingerJ2)
                cmds.makeIdentity(FingerJ2, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % FingerJ2, 0.155)
                cmds.setAttr("%sSnapShape.localScaleY" % FingerJ2, 0.155)
                cmds.setAttr("%sSnapShape.localScaleZ" % FingerJ2, 0.155)

                FingerJ3 = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_J3"
                self.ProxyBase(FingerJ3)
                PCons = cmds.pointConstraint(FingerJ2, FingerJ3)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0.61, 0, 0, FingerJ3, r=True, os=True, wd=True)
                cmds.scale(0.62, 0.62, 0.62, FingerJ3)
                cmds.makeIdentity(FingerJ3, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % FingerJ3, 0.155)
                cmds.setAttr("%sSnapShape.localScaleY" % FingerJ3, 0.155)
                cmds.setAttr("%sSnapShape.localScaleZ" % FingerJ3, 0.155)

                FingerJTip = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_JTip"
                self.ProxyBase(FingerJTip)
                PCons = cmds.pointConstraint(FingerJ3, FingerJTip)
                cmds.delete(PCons)
                cmds.move(armMultiplier * 0.61, 0, 0, FingerJTip, r=True, os=True, wd=True)
                cmds.scale(0.62, 0.62, 0.62, FingerJTip)
                cmds.makeIdentity(FingerJTip, apply=True, t=1, r=1, s=1)
                cmds.setAttr("%sSnapShape.localScaleX" % FingerJTip, 0.155)
                cmds.setAttr("%sSnapShape.localScaleY" % FingerJTip, 0.155)
                cmds.setAttr("%sSnapShape.localScaleZ" % FingerJTip, 0.155)

                cmds.parent(FingerJ1, Palm)
                cmds.parent(FingerJ2, FingerJ1)
                cmds.parent(FingerJ3, FingerJ2)
                cmds.parent(FingerJTip, FingerJ3)

                self.ProxyConnectors(Palm, FingerJ1)
                self.ProxyConnectors(FingerJ1, FingerJ2)
                self.ProxyConnectors(FingerJ2, FingerJ3)
                self.ProxyConnectors(FingerJ3, FingerJTip)
                fingerIndex += 1

            cmds.makeIdentity(Wrist, apply=True, t=1, r=1, s=1)
            armPrefx = "_R"
            armMultiplier = -1.0
            armLoop += 1

        # Legs
        legLoop = 1
        legPrefx = "_L"
        legMultiplier = 1.0
        while legLoop <= 2:
            Hip = "Proxies" + legPrefx + "_Hip"
            self.ProxyBase(Hip)
            PCons = cmds.pointConstraint(self.Proxies_Root, Hip)
            cmds.delete(PCons)
            cmds.move(legMultiplier * 1.72, -0.8, 0, Hip, r=True, os=True, wd=True)
            cmds.makeIdentity(Hip, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(self.Proxies_Root, Hip)
            cmds.parent(Hip,self.Proxies_Root)

            Knee = "Proxies" + legPrefx + "_Knee"
            self.ProxyBase(Knee)
            PCons = cmds.pointConstraint(Hip, Knee)
            cmds.delete(PCons)
            cmds.move(0, -6.4, 0, Knee, r=True, os=True, wd=True)
            cmds.rotate(0, 180, 90, Knee)
            cmds.makeIdentity(Knee, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Hip, Knee)

            Ankle = "Proxies" + legPrefx + "_Ankle"
            self.ProxyBase(Ankle)
            PCons = cmds.pointConstraint(Knee, Ankle)
            cmds.delete(PCons)
            cmds.move(0, -6.4, 0, Ankle, r=True, os=True, wd=True)
            cmds.makeIdentity(Ankle, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Knee, Ankle)

            KneeG = "Proxies"+ legPrefx + "_Knee_GRP"
            cmds.group(n=KneeG,em=True)
            PCons = cmds.pointConstraint(Knee, KneeG)
            cmds.delete(PCons)
            cmds.parent(Knee,KneeG)
            cmds.makeIdentity(KneeG, apply=True, t=1, r=1, s=1)
            # cmds.move(0,0,0.001,"%s.scalePivot" % KneeG,"%s.rotatePivot"  % KneeG ,r=True)
            cmds.pointConstraint(Hip,Ankle,KneeG,mo=True)
            cmds.parent(KneeG,Ankle,self.Main)

            Ball = "Proxies" + legPrefx + "_Ball"
            self.ProxyBase(Ball)
            PCons = cmds.pointConstraint(Ankle, Ball)
            cmds.delete(PCons)
            cmds.move(0, -1.65, 2.26, Ball, r=True, os=True, wd=True)
            cmds.makeIdentity(Ball, apply=True, t=1, r=1, s=1)
            self.ProxyConnectors(Ankle, Ball)

            Toe = "Proxies" + legPrefx + "_Toe"
            self.ProxyBase(Toe)
            PCons = cmds.pointConstraint(Ball, Toe)
            cmds.delete(PCons)
            cmds.move(0, 0, 1.7, Toe, r=True, os=True, wd=True)
            cmds.makeIdentity(Toe, apply=True, t=1, r=1, s=1)

            if toesNum == 1:
                self.ProxyConnectors(Ball, Toe)
            cmds.group(n="%s_GRP" % Ball, em=True)
            cmds.parent("%s_GRP" % Ball, Ball)
            cmds.parent(Toe, "%s_GRP" % Ball)

            KneeLocator = "Proxies" + legPrefx + "_KneeLocator"
            cmds.spaceLocator(n=KneeLocator)
            PCons = cmds.pointConstraint(Knee, KneeLocator)
            cmds.delete(PCons)
            cmds.parent(KneeLocator, Knee)
            cmds.move(0, 0, 1.5, KneeLocator, r=True)
            cmds.setAttr("%s.v" % KneeLocator, 0)

            # toe num
            cmds.makeIdentity(Ball, apply=True, t=1, r=1, s=1)
            legLoop += 1
            legPrefx = "_R"
            legMultiplier = -1.0

        # PARENT CONTROLS
        cmds.parent(self.Proxies_Root,spineProxiesG,self.Proxies_SpineTop,neckProxiesG,self.Proxies_Head,self.Main)
        cmds.parent(self.Proxies_Jaw,self.Proxies_HeadTip,self.Proxies_LeftEye,self.Proxies_RightEye,self.Proxies_Head)
        cmds.parent(self.Proxies_JawTip,self.Proxies_Jaw)


