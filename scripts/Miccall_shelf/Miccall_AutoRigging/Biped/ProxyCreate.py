# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


class BipedProxyCreator:
    def __init__(self):
        self.thumbsOn = True
        self.fingersNum = 4
        toesNum = 1
        self.spineNum = 4
        self.neckNum = 2
        self.Main = "Proxies_Main"
        self.Proxies_Root = "Proxies_Root"
        self.Proxies_SpineList = []
        self.Proxies_SpineTop = "Proxies_SpineTop"
        self.Proxies_NeckList = []
        self.Proxies_Head = "Proxies_Head"
        self.Proxies_HeadTip = "Proxies_HeadTip"
        self.Proxies_Jaw = "Proxies_Jaw"
        self.Proxies_JawTip = "Proxies_JawTip"
        self.Proxies_Eyes = []
        self.Proxies_Clavicles = []
        self.Proxies_Shoulders = []
        self.Proxies_Elbows = []
        self.Proxies_Wrists = []
        self.Proxies_ThumbList = []
        self.Proxies_FingerLists = []
        self.Proxies_Hips = []
        self.Proxies_Knees = []
        self.Proxies_Ankles = []
        self.Proxies_Balls = []
        self.Proxies_Toes = []

        for i in range(1, self.spineNum):
            spineName = "Proxies_Spine_0" + str(i)
            self.Proxies_SpineList.append(spineName)

        for i in range(1, self.neckNum):
            neckName = "Proxies_Neck_0" + str(i)
            self.Proxies_NeckList.append(neckName)

        self.InitData("L")
        self.InitData("R")
        pass

    def InitData(self, side):
        if self.thumbsOn:
            for i in range(1, 4):
                ThumbName = "Proxies_" + side + "_ThumbJ" + str(i)
                self.Proxies_ThumbList.append(ThumbName)
            ThumbTipName = "Proxies_" + side + "_ThumbJTip"
            self.Proxies_ThumbList.append(ThumbTipName)

        for i in range(1, self.fingersNum + 1):
            FingerChain = []
            for j in range(1, 4):
                FingerName = "Proxies_" + side + "_Finger_" + str(i) + "_J" + str(j)
                FingerChain.append(FingerName)
            FingerTip = "Proxies_" + side + "_Finger_" + str(i) + "_JTip"
            FingerChain.append(FingerTip)
            self.Proxies_FingerLists.append(FingerChain)

        EyeName = "Proxies_" + side + "_Eye"
        self.Proxies_Eyes.append(EyeName)

        ClavicleName = "Proxies_" + side + "_Clavicle"
        self.Proxies_Clavicles.append(ClavicleName)

        ShoulderName = "Proxies_" + side + "_Shoulder"
        self.Proxies_Shoulders.append(ShoulderName)

        ElbowName = "Proxies_" + side + "_Elbow"
        self.Proxies_Elbows.append(ElbowName)

        WristName = "Proxies_" + side + "_Wrist"
        self.Proxies_Wrists.append(WristName)

        ToeName = "Proxies_" + side + "_Toe"
        self.Proxies_Toes.append(ToeName)

        BallName = "Proxies_" + side + "_Ball"
        self.Proxies_Balls.append(BallName)

        AnkleName = "Proxies_" + side + "_Ankle"
        self.Proxies_Ankles.append(AnkleName)

        KneeName = "Proxies_" + side + "_Knee"
        self.Proxies_Knees.append(KneeName)

        HipName = "Proxies_" + side + "_Hip"
        self.Proxies_Hips.append(HipName)
        pass

    def MainProcessing(self):
        cmds.circle(n=self.Main, c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=8, d=3, ut=0, tol=0.01, s=8, ch=0)
        # Root
        self.CreatePrixyNode(name=self.Proxies_Root,
                             mScale=[1.6, 1.6, 1.6],
                             mMvoe=[0, 15.25, 0],
                             lScale=[0.4, 0.4, 0.4])

        # Spine Top
        self.CreatePrixyNode(name=self.Proxies_SpineTop,
                             PC=self.Proxies_Root,
                             mScale=[1.6, 1.6, 1.6],
                             mMvoe=[0, 6.6, 0],
                             lScale=[0.4, 0.4, 0.4])

        self.Proxies_SpineOrientLocator = "Proxies_SpineOrientLocator"
        self.Proxies_NeckOrientLocator = "Proxies_NeckOrientLocator"

        # Aim
        cmds.spaceLocator(n=self.Proxies_SpineOrientLocator)
        cmds.parent(self.Proxies_SpineOrientLocator, self.Main)
        cmds.pointConstraint(self.Proxies_Root, self.Proxies_SpineOrientLocator)
        cmds.aimConstraint(self.Proxies_SpineTop, self.Proxies_SpineOrientLocator, aimVector=[0, 1, 0],
                           upVector=[1, 0, 0], worldUpType="vector", worldUpVector=[1, 0, 0])
        cmds.setAttr("%s.visibility" % self.Proxies_SpineOrientLocator, 0)

        # Spline
        i2 = self.spineNum - 1
        for i, Spine in enumerate(self.Proxies_SpineList):
            self.ProxyBase(Spine)
            SpineGRP = Spine + "_GRP"
            cmds.group(Spine, n=SpineGRP)
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.makeIdentity(SpineGRP, apply=True, t=1, r=1, s=1)
            cmds.pointConstraint(self.Proxies_Root, self.Proxies_SpineTop, SpineGRP)
            cmds.orientConstraint(self.Proxies_SpineOrientLocator, SpineGRP)
            cmds.setAttr("%s_pointConstraint1.Proxies_RootW0" % SpineGRP, i2)
            cmds.setAttr("%s_pointConstraint1.Proxies_SpineTopW1" % SpineGRP, i+1)
            # CONNECTORS
            if i+1 == 1:
                self.ProxyConnectors(self.Proxies_Root, SpineGRP)
            else:
                self.ProxyConnectors(SpineGRP, self.Proxies_SpineList[i-1])
            i2 = i2 - 1
        self.ProxyConnectors(self.Proxies_SpineList[self.spineNum - 2], self.Proxies_SpineTop)
        cmds.select(self.Proxies_SpineList)
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

        i2 = self.neckNum - 1
        for i, Neck in enumerate(self.Proxies_NeckList):
            self.ProxyBase(Neck)
            cmds.scale(0.8, 0.8, 0.8, Neck, r=True)
            cmds.makeIdentity(Neck, apply=True, t=1, r=1, s=1)
            NeckGRP = Neck + "_GRP"
            cmds.group(Neck, n=NeckGRP)
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.makeIdentity(NeckGRP, apply=True, t=1, r=1, s=1)
            cmds.pointConstraint(self.Proxies_SpineTop, self.Proxies_Head, NeckGRP)
            cmds.orientConstraint(self.Proxies_NeckOrientLocator, NeckGRP)
            cmds.setAttr("%s_pointConstraint1.Proxies_SpineTopW0" % NeckGRP, i2)
            cmds.setAttr("%s_pointConstraint1.Proxies_HeadW1" % NeckGRP, i+1)
            # CONNECTORS
            if i+1 == 1:
                self.ProxyConnectors(self.Proxies_SpineTop, NeckGRP)
            else:
                self.ProxyConnectors(NeckGRP, self.Proxies_NeckList[i-1])
            i2 = i2 - 1
        self.ProxyConnectors(self.Proxies_NeckList[self.neckNum - 2], self.Proxies_SpineTop)
        cmds.select(self.Proxies_NeckList)
        cmds.pickWalk(d="up")
        neckProxiesG = cmds.ls(sl=True)

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
