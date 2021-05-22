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

    def CreatePrixyNode(self, name, mScale=None, mMvoe=None, lScale=None, mRotate=None, PC=None, isConnect=False,
                        isParent=False):

        if mScale is None:
            mScale = [1, 1, 1]

        if mMvoe is None:
            mMvoe = [0, 0, 0]

        if mRotate is None:
            mRotate = [0, 0, 0]

        self.ProxyBase(name)
        if PC is not None:
            PCons = cmds.pointConstraint(PC, name)
            cmds.delete(PCons)
        cmds.scale(mScale[0], mScale[1], mScale[2], name, r=True)
        cmds.move(mMvoe[0], mMvoe[1], mMvoe[2], name, r=True, os=True, wd=True)
        cmds.rotate(mRotate[0], mRotate[1], mRotate[2], name)
        cmds.makeIdentity(name, apply=True, t=1, r=1, s=1)
        if lScale is not None:
            cmds.setAttr("%sSnapShape.localScaleX" % name, lScale[0])
            cmds.setAttr("%sSnapShape.localScaleY" % name, lScale[1])
            cmds.setAttr("%sSnapShape.localScaleZ" % name, lScale[2])
        if isConnect and PC is not None:
            self.ProxyConnectors(PC, name)
        if isParent and PC is not None:
            cmds.parent(name, PC)
        pass

    def CreateProxies(self):
        thumbsOn = True
        fingersNum = 5
        toesNum = 1
        spineNum = 4
        neckNum = 2
        self.Main = "Proxies_Main"
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
        Main = cmds.circle(n=self.Main, c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=8, d=3, ut=0, tol=0.01, s=8, ch=0)

        # Root
        self.CreatePrixyNode(name=self.Proxies_Root,
                             mScale=[1.6, 1.6, 1.6],
                             mMvoe=[0, 15.25, 0],
                             lScale=[0.4, 0.4, 0.4])

        # Top
        self.CreatePrixyNode(name=self.Proxies_SpineTop,
                             PC=self.Proxies_Root,
                             mScale=[1.6, 1.6, 1.6],
                             mMvoe=[0, 6.6, 0],
                             lScale=[0.4, 0.4, 0.4])

        # Aim Locator
        loc = cmds.spaceLocator(n=self.Proxies_SpineOrientLocator)
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

        # Head
        self.CreatePrixyNode(name=self.Proxies_Head,
                             PC=self.Proxies_SpineTop,
                             mMvoe=[0, 2, 0],
                             mScale=[1.25, 1.25, 1.25])

        # CREATE AIM LOCATOR TO ORIENT NECK PROXIES
        cmds.spaceLocator(n=self.Proxies_NeckOrientLocator)
        cmds.parent(self.Proxies_NeckOrientLocator, self.Main)
        cmds.pointConstraint(self.Proxies_SpineTop, self.Proxies_NeckOrientLocator)
        cmds.aimConstraint(self.Proxies_Head, self.Proxies_NeckOrientLocator, aimVector=[0, 1, 0],
                           upVector=[1, 0, 0], worldUpType="vector", worldUpVector=[1, 0, 0])
        cmds.setAttr("%s.visibility" % self.Proxies_NeckOrientLocator, 0)

        # Neck
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
        self.CreatePrixyNode(self.Proxies_Jaw,
                             PC=self.Proxies_Head,
                             mMvoe=[0, 0.83, 0.38],
                             isConnect=True)

        self.CreatePrixyNode(self.Proxies_JawTip,
                             PC=self.Proxies_Jaw,
                             mMvoe=[0, -0.83, 1.52],
                             isConnect=True)

        self.CreatePrixyNode(self.Proxies_HeadTip,
                             PC=self.Proxies_Head,
                             mMvoe=[0, 3.38, 0],
                             isConnect=True)
        # Eye
        self.CreatePrixyNode(self.Proxies_LeftEye,
                             PC=self.Proxies_Head,
                             mMvoe=[0.57, 1.53, 1.64],
                             isConnect=True)

        self.CreatePrixyNode(self.Proxies_RightEye,
                             PC=self.Proxies_Head,
                             mMvoe=[-0.57, 1.53, 1.64],
                             isConnect=True)

        # Arms
        armLoop = 1
        armPrefx = "_L"
        armMultiplier = 1.0
        while armLoop <= 2:

            Clavicle = "Proxies" + armPrefx + "_Clavicle"
            self.CreatePrixyNode(Clavicle,
                                 PC=self.Proxies_SpineTop,
                                 mMvoe=[armMultiplier * 1.25, 0.5, 0],
                                 isConnect=True,
                                 isParent=True)

            Shoulder = "Proxies" + armPrefx + "_Shoulder"
            self.CreatePrixyNode(Shoulder,
                                 PC=Clavicle,
                                 mMvoe=[armMultiplier * 1.7, 0, 0],
                                 isConnect=True,
                                 isParent=True)

            Elbow = "Proxies" + armPrefx + "_Elbow"
            self.CreatePrixyNode(Elbow,
                                 PC=Shoulder,
                                 mMvoe=[armMultiplier * 3.5, 0, 0],
                                 isConnect=True)

            Wrist = "Proxies" + armPrefx + "_Wrist"
            self.CreatePrixyNode(Wrist,
                                 PC=Elbow,
                                 mMvoe=[armMultiplier * 3.5, 0, 0],
                                 isConnect=True)

            ElbowG = "Proxies" + armPrefx + "_Elbow_GRP"
            cmds.group(n=ElbowG, em=True)
            PCons = cmds.pointConstraint(Elbow, ElbowG)
            cmds.delete(PCons)
            cmds.parent(Elbow, ElbowG)
            cmds.makeIdentity(ElbowG, apply=True, t=1, r=1, s=1)
            cmds.move(0, 0, 0.001, "%s.scalePivot" % ElbowG, "%s.rotatePivot" % ElbowG, r=True)
            cmds.pointConstraint(Shoulder, Wrist, ElbowG, mo=True)
            cmds.parent(ElbowG, Wrist, self.Main)

            Palm = "Proxies" + armPrefx + "_Palm"
            self.CreatePrixyNode(Palm,
                                 PC=Wrist,
                                 mMvoe=[armMultiplier * 0.7, 0, 0],
                                 mScale=[0.7, 0.7, 0.7],
                                 lScale=[0.175, 0.175, 0.175],
                                 isConnect=True,
                                 isParent=True)

            if thumbsOn:
                ThumbJ1 = "Proxies" + armPrefx + "_ThumbJ1"
                self.CreatePrixyNode(ThumbJ1,
                                     PC=Wrist,
                                     mMvoe=[armMultiplier * 0.45, 0, 0.51],
                                     mScale=[0.75, 0.75, 0.75],
                                     lScale=[0.1875, 0.1875, 0.1875],
                                     isConnect=True,
                                     isParent=True)

                ThumbJ2 = "Proxies" + armPrefx + "_ThumbJ2"
                self.CreatePrixyNode(ThumbJ2,
                                     PC=ThumbJ1,
                                     mMvoe=[armMultiplier * 0, 0, 0.75],
                                     mScale=[0.75, 0.75, 0.75],
                                     lScale=[0.1875, 0.1875, 0.1875],
                                     isConnect=True,
                                     isParent=True)

                ThumbJ3 = "Proxies" + armPrefx + "_ThumbJ3"
                self.CreatePrixyNode(ThumbJ3,
                                     PC=ThumbJ2,
                                     mMvoe=[armMultiplier * 0, 0, 0.75],
                                     mScale=[0.75, 0.75, 0.75],
                                     lScale=[0.1875, 0.1875, 0.1875],
                                     isConnect=True,
                                     isParent=True)

                ThumbJTip = "Proxies" + armPrefx + "_ThumbJTip"
                self.CreatePrixyNode(ThumbJTip,
                                     PC=ThumbJ3,
                                     mMvoe=[armMultiplier * 0, 0, 0.75],
                                     mScale=[0.75, 0.75, 0.75],
                                     lScale=[0.1875, 0.1875, 0.1875],
                                     isConnect=True,
                                     isParent=True)

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
                cmds.parent(FingerJ1, Palm)
                self.ProxyConnectors(Palm, FingerJ1)

                FingerJ2 = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_J2"
                self.CreatePrixyNode(FingerJ2,
                                     PC=FingerJ1,
                                     mMvoe=[armMultiplier * 0.61, 0, 0],
                                     mScale=[0.62, 0.62, 0.62],
                                     lScale=[0.155, 0.155, 0.155],
                                     isConnect=True,
                                     isParent=True)

                FingerJ3 = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_J3"
                self.CreatePrixyNode(FingerJ3,
                                     PC=FingerJ2,
                                     mMvoe=[armMultiplier * 0.61, 0, 0],
                                     mScale=[0.62, 0.62, 0.62],
                                     lScale=[0.155, 0.155, 0.155],
                                     isConnect=True,
                                     isParent=True)

                FingerJTip = "Proxies" + armPrefx + "_Finger_" + str(fingerIndex) + "_JTip"
                self.CreatePrixyNode(FingerJTip,
                                     PC=FingerJ3,
                                     mMvoe=[armMultiplier * 0.61, 0, 0],
                                     mScale=[0.62, 0.62, 0.62],
                                     lScale=[0.155, 0.155, 0.155],
                                     isConnect=True,
                                     isParent=True)

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
            self.CreatePrixyNode(Hip,
                                 PC=self.Proxies_Root,
                                 mMvoe=[legMultiplier * 1.72, -0.8, 0],
                                 isConnect=True,
                                 isParent=True)

            Knee = "Proxies" + legPrefx + "_Knee"
            self.CreatePrixyNode(Knee,
                                 PC=Hip,
                                 mMvoe=[0, -6.4, 0],
                                 mRotate=[0, 180, 90],
                                 isConnect=True,
                                 isParent=True)

            Ankle = "Proxies" + legPrefx + "_Ankle"
            self.CreatePrixyNode(Ankle,
                                 PC=Knee,
                                 mMvoe=[0, -6.4, 0],
                                 isConnect=True,
                                 isParent=True)

            KneeG = "Proxies" + legPrefx + "_Knee_GRP"
            cmds.group(n=KneeG, em=True)
            PCons = cmds.pointConstraint(Knee, KneeG)
            cmds.delete(PCons)
            cmds.parent(Knee, KneeG)
            cmds.makeIdentity(KneeG, apply=True, t=1, r=1, s=1)
            # cmds.move(0,0,0.001,"%s.scalePivot" % KneeG,"%s.rotatePivot"  % KneeG ,r=True)
            cmds.pointConstraint(Hip, Ankle, KneeG, mo=True)
            cmds.parent(KneeG, Ankle, self.Main)

            Ball = "Proxies" + legPrefx + "_Ball"
            self.CreatePrixyNode(Ball,
                                 PC=Ankle,
                                 mMvoe=[0, -1.65, 2.26],
                                 isConnect=True,
                                 isParent=True)

            Toe = "Proxies" + legPrefx + "_Toe"
            self.CreatePrixyNode(Toe,
                                 PC=Ball,
                                 mMvoe=[0, 0, 1.7])

            if toesNum == 1:
                self.ProxyConnectors(Ball, Toe)

            BallG = "Proxies" + legPrefx + "_Ball_GRP"
            cmds.group(n=BallG, em=True)
            cmds.parent(BallG, Ball)
            cmds.parent(Toe, BallG)

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
        cmds.parent(self.Proxies_Root, spineProxiesG, self.Proxies_SpineTop, neckProxiesG, self.Proxies_Head, self.Main)
        cmds.parent(self.Proxies_Jaw, self.Proxies_HeadTip, self.Proxies_LeftEye, self.Proxies_RightEye,
                    self.Proxies_Head)
        cmds.parent(self.Proxies_JawTip, self.Proxies_Jaw)

        # INDICATOR
        self.ElbowIndicator("L")
        self.ElbowIndicator("R")
        self.KneeIndicator("L")
        self.KneeIndicator("R")

        # LOCATORS FOR FOOT TILT
        self.FootTilt("L")
        self.FootTilt("R")

        self.LimitAndLock()

        # CREATE LAYER
        cmds.select(self.Main)
        layer = cmds.objExists("ProxiesLayer")
        if layer is not None:
            cmds.createDisplayLayer(n="ProxiesLayer", number=1, nr=True)
        else:
            cmds.editDisplayLayerMembers("ProxiesLayer", self.Main, noRecurse=True)

        cmds.select(clear=True)
        pass

    def ElbowIndicator(self, side):
        sign = 1
        if side == "L":
            sign = 1
        else:
            sign = -1

        # fetch
        Proxies_Elbow = "Proxies_" + side + "_Elbow"
        Proxies_Shoulder = "Proxies_" + side + "_Shoulder"
        Proxies_Wrist = "Proxies_" + side + "_Wrist"
        Proxies_Elbow_GRP = "Proxies_" + side + "_Elbow_GRP"
        Proxies_ElbowParent = "Proxies_" + side + "_ElbowParent"
        Proxies_ElbowAim = "Proxies_" + side + "_ElbowAim"
        Proxies_ElbowParentUp = "Proxies_" + side + "_ElbowParentUp"
        Proxies_ElbowParentUp_GRP = "Proxies_" + side + "_ElbowParentUp_GRP"

        # Locator
        cmds.spaceLocator(n=Proxies_ElbowParent)
        cmds.parent(Proxies_ElbowParent, self.Main)
        cmds.spaceLocator(n=Proxies_ElbowAim)
        cmds.move(2 * sign, 0, 0, Proxies_ElbowAim, r=True)
        cmds.parent(Proxies_ElbowAim, Proxies_ElbowParent)
        cmds.spaceLocator(n=Proxies_ElbowParentUp, p=(0, 0, 0))
        cmds.group(n=Proxies_ElbowParentUp_GRP)
        cmds.pointConstraint(Proxies_Shoulder, Proxies_ElbowParentUp_GRP, skip=['x', 'z'])
        cmds.parent(Proxies_ElbowParentUp_GRP, self.Main)

        # connect
        Proxies_ElbowParentUp_MD = "%s_MD" % Proxies_ElbowParentUp
        cmds.shadingNode("multiplyDivide", asUtility=True, n=Proxies_ElbowParentUp_MD)
        cmds.setAttr("%s.operation" % Proxies_ElbowParentUp_MD, 2)
        cmds.setAttr("%s.input2X" % Proxies_ElbowParentUp_MD, -2)
        cmds.connectAttr("%s.translateY" % Proxies_Wrist, "%s.input1X" % Proxies_ElbowParentUp_MD)
        cmds.connectAttr("%s.outputX" % Proxies_ElbowParentUp_MD, "%s.translateY" % Proxies_ElbowParentUp)
        cmds.pointConstraint(Proxies_Shoulder, Proxies_ElbowParent)
        cmds.pointConstraint(Proxies_Shoulder, Proxies_Wrist, Proxies_ElbowAim)
        cmds.connectAttr("%s.rotate" % Proxies_ElbowParent, "%s.rotate" % Proxies_Elbow_GRP)
        cmds.aimConstraint(Proxies_Wrist, Proxies_ElbowParent,
                           aimVector=[1 * sign, 0, 0], upVector=[-1 * sign, 0, 0], worldUpType="object",
                           worldUpObject=Proxies_ElbowParentUp)
        cmds.aimConstraint(Proxies_ElbowAim, Proxies_Elbow,
                           aimVector=[0, 0, 1], upVector=[0, 1, 0], worldUpType="none",
                           skip=['y', 'z'])
        pass

    def KneeIndicator(self, side):
        sign = 1
        if side == "L":
            sign = 1
        else:
            sign = -1

        # fetch & name
        Hip = "Proxies_" + side + "_Hip"
        Ankle = "Proxies_" + side + "_Ankle"
        Knee = "Proxies_" + side + "_Knee"
        KneeG = "Proxies_" + side + "_Knee_GRP"
        Proxies_KneeParent = "Proxies_" + side + "_KneeParent"
        Proxies_KneeAim = "Proxies_" + side + "_KneeAim"
        Proxies_KneeParentUp = "Proxies_" + side + "_KneeParentUp"
        Proxies_KneeParentUp_GRP = "Proxies_" + side + "_KneeParentUp_GRP"

        # Locator
        cmds.spaceLocator(n=Proxies_KneeParent)
        cmds.parent(Proxies_KneeParent, self.Main)
        cmds.spaceLocator(n=Proxies_KneeAim)
        cmds.move(0, -2, 0, Proxies_KneeAim, r=True)
        cmds.parent(Proxies_KneeAim, Proxies_KneeParent)
        cmds.spaceLocator(n=Proxies_KneeParentUp, p=(0, 0, 0))
        cmds.group(n=Proxies_KneeParentUp_GRP)
        cmds.pointConstraint(Hip, Proxies_KneeParentUp_GRP, offset=(0, 2, 0))
        cmds.parent(Proxies_KneeParentUp_GRP, self.Main)

        # connect
        Proxies_KneeParentUp_MD = "%s_MD" % Proxies_KneeParentUp
        cmds.shadingNode("multiplyDivide", asUtility=True, n=Proxies_KneeParentUp_MD)
        cmds.setAttr("%s.operation" % Proxies_KneeParentUp_MD, 2)
        cmds.setAttr("%s.input2X" % Proxies_KneeParentUp_MD, -2)
        cmds.connectAttr("%s.translateX" % Ankle, "%s.input1X" % Proxies_KneeParentUp_MD)
        cmds.connectAttr("%s.outputX" % Proxies_KneeParentUp_MD, "%s.translateX" % Proxies_KneeParentUp)
        cmds.pointConstraint(Hip, Proxies_KneeParent)
        cmds.pointConstraint(Hip, Ankle, Proxies_KneeAim)

        cmds.connectAttr("%s.rotate" % Proxies_KneeParent, "%s.rotate" % KneeG)

        cmds.aimConstraint(Ankle, Proxies_KneeParent,
                           aimVector=[0, -1, 0], upVector=[0, 1, 0], worldUpType="object",
                           worldUpObject=Proxies_KneeParentUp)

        cmds.aimConstraint(Proxies_KneeAim, Knee,
                           aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType="objectrotation",
                           worldUpVector=[0, 1, 0], worldUpObject=Proxies_KneeAim, skip=['x', 'z'])
        pass

    def FootTilt(self, side):

        sign = 1
        if side == "L":
            sign = 1
        else:
            sign = -1
        Ankle = "Proxies_" + side + "_Ankle"
        Ball = "Proxies_" + side + "_Ball"
        BallG = "Proxies_" + side + "_Ball_GRP"
        FootG = "Proxies_" + side + "_Foot_GRP"
        FootInTilt = "Proxies_" + side + "_FootInTilt"
        FootInTiltShape = "%sShape" % FootInTilt

        FootOutTilt = "Proxies_" + side + "_FootOutTilt"
        FootOutTiltShape = "%sShape" % FootInTilt

        FootHeelPivot = "Proxies_" + side + "_FootHeelPivot"
        FootHeelPivotShape = "%sShape" % FootHeelPivot

        mel.eval(
            "curve -n " + FootInTilt + " -d 1 -p 0 0 -1 -p 0 0 1 -p 0 0 0 -p 1 0 0 -p -1 0 0 -p 0 0 0 -p 0 1 0 -p 0 -1 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;")
        cmds.pickWalk(d="down")
        cmds.rename(FootInTiltShape)
        cmds.move(0.5 * sign, 0, 2.26, FootInTilt)
        cmds.makeIdentity(FootInTilt, apply=True, t=1, r=1, s=1)

        mel.eval(
            "curve -n " + FootOutTilt + " -d 1 -p 0 0 -1 -p 0 0 1 -p 0 0 0 -p 1 0 0 -p -1 0 0 -p 0 0 0 -p 0 1 0 -p 0 -1 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;")
        cmds.pickWalk(d="down")
        cmds.rename(FootOutTiltShape)
        cmds.move(3 * sign, 0, 2.26, FootOutTilt)
        cmds.makeIdentity(FootOutTilt, apply=True, t=1, r=1, s=1)
        cmds.parent(FootOutTilt, FootInTilt, BallG)

        mel.eval(
            "curve -n " + FootHeelPivot + " -d 1 -p 0 0 -1 -p 0 0 1 -p 0 0 0 -p 1 0 0 -p -1 0 0 -p 0 0 0 -p 0 1 0 -p 0 -1 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;")
        cmds.pickWalk(d="down")
        cmds.rename(FootHeelPivotShape)
        cmds.move(1.72 * sign, 0, -1.079, FootHeelPivot)
        cmds.makeIdentity(FootHeelPivot, apply=True, t=1, r=1, s=1)

        cmds.group(Ball, FootHeelPivot, n=FootG)
        cmds.parent(FootG, self.Main)
        AnklePosition = cmds.xform(Ankle, q=True, ws=True, rp=True)
        cmds.move(AnklePosition[0], 0, AnklePosition[2], "%s.scalePivot" % FootG, "%s.rotatePivot" % FootG)
        cmds.pointConstraint(Ankle, FootG, mo=True, skip="y")
        cmds.orientConstraint(Ankle, FootG, mo=True, skip=['x', 'z'])
        cmds.scaleConstraint(Ankle, FootG, offset=[1, 1, 1], skip='y')
        pass

    def LimitAndLock(self):
        cmds.select(self.Main, hi=True)
        nurbsCurvesShapes = cmds.ls(sl=True, type="nurbsCurve")
        cmds.select(nurbsCurvesShapes)
        cmds.pickWalk(d="up")
        nurbsCurvesOnly = cmds.ls(sl=True)
        for selectedProxy in nurbsCurvesOnly:
            cmds.transformLimits(selectedProxy, sx=(0.01, 1), esx=(1, 0))
            cmds.transformLimits(selectedProxy, sy=(0.01, 1), esy=(1, 0))
            cmds.transformLimits(selectedProxy, sz=(0.01, 1), esz=(1, 0))

        self.FingerLimit("L")
        self.FingerLimit("R")

        # CONSTRAIN FOOT CONTROLS TO GROUND PLANE
        LBallG = "Proxies_" + "L" + "_Ball_GRP"
        RBallG = "Proxies_" + "R" + "_Ball_GRP"

        cmds.pointConstraint(self.Main, LBallG)
        cmds.pointConstraint(self.Main, RBallG)

        cmds.transformLimits(self.Proxies_Root, ty=(-12, 1), ety=(1, 0))
        cmds.transformLimits(self.Proxies_SpineTop, ty=(-17.5, 1), ety=(1, 0))
        cmds.transformLimits(self.Proxies_HeadTip, ty=(-3, 1), ety=(1, 0))
        cmds.transformLimits(self.Proxies_LeftEye, ty=(-0.5, 1), ety=(1, 0))
        cmds.transformLimits(self.Proxies_RightEye, ty=(-1, 0.5), ety=(0, 1))
        self.LimitSide("L")
        self.LimitSide("R")

        self.setLock(self.Main, "tx")
        self.setLock(self.Main, "ty")
        self.setLock(self.Main, "tz")
        self.setLock(self.Main, "rx")
        self.setLock(self.Main, "ry")
        self.setLock(self.Main, "rz")

        pass

    def FingerLimit(self, side):
        sign = 1
        if side == "L":
            sign = 1
        else:
            sign = -1

        FingerList = "Proxies_" + side + "_Finger***J1"
        FingerJ2 = "Proxies_" + side + "_Finger***J2"
        FingerJ3 = "Proxies_" + side + "_Finger***J3"
        FingerJTip = "Proxies_" + side + "_Finger***JTip"

        cmds.select(FingerList)
        currentSelection = len(cmds.ls(sl=True))
        if currentSelection > 0:
            cmds.select(FingerList)
            finger_J1 = cmds.ls(sl=True)
            for selectedProxy in finger_J1:
                if sign > 0:
                    cmds.transformLimits(selectedProxy, tx=(-0.75, 1), etx=(1, 0))
                else:
                    cmds.transformLimits(selectedProxy, tx=(0, 0.75), etx=(0, 1))

            cmds.select(FingerJ2, FingerJ3, FingerJTip)
            finger_J1 = cmds.ls(sl=True)
            for selectedProxy in finger_J1:
                if sign > 0:
                    cmds.transformLimits(selectedProxy, tx=(-0.5, 1), etx=(1, 0))
                else:
                    cmds.transformLimits(selectedProxy, tx=(0, 0.5), etx=(0, 1))

        pass

    def LimitSide(self, side):
        Clavicle = "Proxies_" + side + "_Clavicle"
        Shoulder = "Proxies_" + side + "_Shoulder"
        Wrist = "Proxies_" + side + "_Wrist"
        Palm = "Proxies_" + side + "_Palm"
        Hip = "Proxies_" + side + "_Hip"
        Ankle = "Proxies_" + side + "_Ankle"
        Elbow = "Proxies_" + side + "_Elbow"
        Knee = "Proxies_" + side + "_Knee"
        if side == "L":
            cmds.transformLimits(Clavicle, tx=(-1, 1), etx=(1, 0))
            cmds.transformLimits(Shoulder, tx=(-1.5, 1), etx=(1, 0))
            cmds.transformLimits(Wrist, tx=(-6.75, 1), etx=(1, 0))
            cmds.transformLimits(Palm, tx=(-0.6, 1), etx=(1, 0))
            cmds.transformLimits(Hip, tx=(-1.5, 1), etx=(1, 0))
            cmds.transformLimits(Ankle, tx=(-1.5, 1), etx=(1, 0))
            cmds.transformLimits(Elbow, tz=(-1, -0.001), etz=(0, 1))
            cmds.transformLimits(Knee, tz=(0.001, 1), etz=(1, 0))
        else:
            cmds.transformLimits(Clavicle, tx=(1, 1), etx=(0, 1))
            cmds.transformLimits(Shoulder, tx=(1, 1.5), etx=(0, 1))
            cmds.transformLimits(Wrist, tx=(1, 6.75), etx=(0, 1))
            cmds.transformLimits(Palm, tx=(0, 0.6), etx=(0, 1))
            cmds.transformLimits(Hip, tx=(1, 1.5), etx=(0, 1))
            cmds.transformLimits(Ankle, tx=(1, 1.5), etx=(0, 1))
            cmds.transformLimits(Elbow, tz=(-1, -0.001), etz=(0, 1))
            cmds.transformLimits(Knee, tz=(0.001, 1), etz=(1, 0))
        cmds.transformLimits(Ankle, ry=(-80, 80), ery=(1, 1))
        self.setLock(Ankle, "rx")
        self.setLock(Ankle, "rz")
        pass

    def setLock(self, name, attr):
        cmds.setAttr("%s.%s" % (name, attr), l=1, k=0, channelBox=0)
        pass
