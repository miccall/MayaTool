# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


class BipedProxyCreator:
    def __init__(self):
        self.thumbsOn = True
        self.fingersNum = 4
        self.toesNum = 1
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
        self.Proxies_Palms = []
        self.Proxies_Thumbs = []
        self.Proxies_Fingers = []
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
            Proxies_ThumbList = []
            for i in range(1, 4):
                ThumbName = "Proxies_" + side + "_ThumbJ" + str(i)
                Proxies_ThumbList.append(ThumbName)
            ThumbTipName = "Proxies_" + side + "_ThumbJTip"
            Proxies_ThumbList.append(ThumbTipName)
            self.Proxies_Thumbs.append(Proxies_ThumbList)

        Proxies_FingerLists = []
        for i in range(1, self.fingersNum + 1):
            FingerChain = []
            for j in range(1, 4):
                FingerName = "Proxies_" + side + "_Finger_" + str(i) + "_J" + str(j)
                FingerChain.append(FingerName)
            FingerTip = "Proxies_" + side + "_Finger_" + str(i) + "_JTip"
            FingerChain.append(FingerTip)
            Proxies_FingerLists.append(FingerChain)
        self.Proxies_Fingers.append(Proxies_FingerLists)

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

        Palm = "Proxies_" + side + "_Palm"
        self.Proxies_Palms.append(Palm)

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
            cmds.setAttr("%s_pointConstraint1.Proxies_SpineTopW1" % SpineGRP, i + 1)
            # CONNECTORS
            if i + 1 == 1:
                self.ProxyConnectors(self.Proxies_Root, SpineGRP)
            else:
                self.ProxyConnectors(SpineGRP, self.Proxies_SpineList[i - 1])
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
            cmds.setAttr("%s_pointConstraint1.Proxies_HeadW1" % NeckGRP, i + 1)
            # CONNECTORS
            if i + 1 == 1:
                self.ProxyConnectors(self.Proxies_SpineTop, NeckGRP)
            else:
                self.ProxyConnectors(NeckGRP, self.Proxies_NeckList[i - 1])
            i2 = i2 - 1
        self.ProxyConnectors(self.Proxies_NeckList[self.neckNum - 2], self.Proxies_Head)
        cmds.select(self.Proxies_NeckList)
        cmds.pickWalk(d="up")
        neckProxiesG = cmds.ls(sl=True)

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
        self.Main_Side("L")
        self.Main_Side("R")

        # PARENT CONTROLS
        cmds.parent(self.Proxies_Root, spineProxiesG, self.Proxies_SpineTop, neckProxiesG, self.Proxies_Head, self.Main)
        cmds.parent(self.Proxies_Jaw, self.Proxies_HeadTip, self.Proxies_Eyes, self.Proxies_Head)
        cmds.parent(self.Proxies_JawTip, self.Proxies_Jaw)

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

    def Main_Side(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        # Eye
        self.CreatePrixyNode(self.Proxies_Eyes[sideindex],
                             PC=self.Proxies_Head,
                             mMvoe=[0.57 * sign, 1.53, 1.64],
                             isConnect=True)

        # Arm
        Clavicle = self.Proxies_Clavicles[sideindex]
        self.CreatePrixyNode(Clavicle,
                             PC=self.Proxies_SpineTop,
                             mMvoe=[sign * 1.25, 0.5, 0],
                             isConnect=True,
                             isParent=True)

        Shoulder = self.Proxies_Shoulders[sideindex]
        self.CreatePrixyNode(Shoulder,
                             PC=Clavicle,
                             mMvoe=[sign * 1.7, 0, 0],
                             isConnect=True,
                             isParent=True)

        Elbow = self.Proxies_Elbows[sideindex]
        self.CreatePrixyNode(Elbow,
                             PC=Shoulder,
                             mMvoe=[sign * 3.5, 0, 0],
                             isConnect=True)

        Wrist = self.Proxies_Wrists[sideindex]
        self.CreatePrixyNode(Wrist,
                             PC=Elbow,
                             mMvoe=[sign * 3.5, 0, 0],
                             isConnect=True)

        ElbowG = Elbow + "_GRP"
        cmds.group(n=ElbowG, em=True)
        PCons = cmds.pointConstraint(Elbow, ElbowG)
        cmds.delete(PCons)
        cmds.parent(Elbow, ElbowG)
        cmds.makeIdentity(ElbowG, apply=True, t=1, r=1, s=1)
        cmds.move(0, 0, 0.001, "%s.scalePivot" % ElbowG, "%s.rotatePivot" % ElbowG, r=True)
        cmds.pointConstraint(Shoulder, Wrist, ElbowG, mo=True)
        cmds.parent(ElbowG, Wrist, self.Main)

        Palm = self.Proxies_Palms[sideindex]
        self.CreatePrixyNode(Palm,
                             PC=Wrist,
                             mMvoe=[sign * 0.7, 0, 0],
                             mScale=[0.7, 0.7, 0.7],
                             lScale=[0.175, 0.175, 0.175],
                             isConnect=True,
                             isParent=True)

        # Hand
        if self.thumbsOn:
            ThumbJ1 = self.Proxies_Thumbs[sideindex][0]
            self.CreatePrixyNode(ThumbJ1,
                                 PC=Wrist,
                                 mMvoe=[sign * 0.45, 0, 0.51],
                                 mScale=[0.75, 0.75, 0.75],
                                 lScale=[0.1875, 0.1875, 0.1875],
                                 isConnect=True,
                                 isParent=True)

            ThumbJ2 = self.Proxies_Thumbs[sideindex][1]
            self.CreatePrixyNode(ThumbJ2,
                                 PC=ThumbJ1,
                                 mMvoe=[sign * 0, 0, 0.75],
                                 mScale=[0.75, 0.75, 0.75],
                                 lScale=[0.1875, 0.1875, 0.1875],
                                 isConnect=True,
                                 isParent=True)

            ThumbJ3 = self.Proxies_Thumbs[sideindex][2]
            self.CreatePrixyNode(ThumbJ3,
                                 PC=ThumbJ2,
                                 mMvoe=[sign * 0, 0, 0.75],
                                 mScale=[0.75, 0.75, 0.75],
                                 lScale=[0.1875, 0.1875, 0.1875],
                                 isConnect=True,
                                 isParent=True)

            ThumbJTip = self.Proxies_Thumbs[sideindex][3]
            self.CreatePrixyNode(ThumbJTip,
                                 PC=ThumbJ3,
                                 mMvoe=[sign * 0, 0, 0.75],
                                 mScale=[0.75, 0.75, 0.75],
                                 lScale=[0.1875, 0.1875, 0.1875],
                                 isConnect=True,
                                 isParent=True)

            FingerList = self.Proxies_Fingers[sideindex]
            jointindex = 0
            for i, Finger in enumerate(FingerList):
                FingerJ1 = Finger[jointindex]
                if i == 0:
                    self.ProxyBase(FingerJ1)
                    PCons = cmds.pointConstraint(Wrist, FingerJ1)
                    cmds.delete(PCons)
                    cmds.move(sign * 1.47, 0, 0, FingerJ1, r=True, os=True, wd=True)
                    if self.fingersNum == 2:
                        cmds.move(0, 0, 0.25, FingerJ1, r=True)
                        cmds.makeIdentity(FingerJ1, apply=True, t=1, r=1, s=1)
                    elif self.fingersNum >= 3:
                        cmds.move(0, 0, 0.5, FingerJ1, r=True)
                        cmds.makeIdentity(FingerJ1, apply=True, t=1, r=1, s=1)
                else:
                    FingerJ0 = FingerList[i - 1][0]
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

                FingerJ2 = Finger[1]
                self.CreatePrixyNode(FingerJ2,
                                     PC=FingerJ1,
                                     mMvoe=[sign * 0.61, 0, 0],
                                     mScale=[0.62, 0.62, 0.62],
                                     lScale=[0.155, 0.155, 0.155],
                                     isConnect=True,
                                     isParent=True)

                FingerJ3 = Finger[2]
                self.CreatePrixyNode(FingerJ3,
                                     PC=FingerJ2,
                                     mMvoe=[sign * 0.61, 0, 0],
                                     mScale=[0.62, 0.62, 0.62],
                                     lScale=[0.155, 0.155, 0.155],
                                     isConnect=True,
                                     isParent=True)

                FingerJTip = Finger[3]
                self.CreatePrixyNode(FingerJTip,
                                     PC=FingerJ3,
                                     mMvoe=[sign * 0.61, 0, 0],
                                     mScale=[0.62, 0.62, 0.62],
                                     lScale=[0.155, 0.155, 0.155],
                                     isConnect=True,
                                     isParent=True)

            cmds.makeIdentity(Wrist, apply=True, t=1, r=1, s=1)

        # Leg
        Hip = self.Proxies_Hips[sideindex]
        self.CreatePrixyNode(Hip,
                             PC=self.Proxies_Root,
                             mMvoe=[sign * 1.72, -0.8, 0],
                             isConnect=True,
                             isParent=True)

        Knee = self.Proxies_Knees[sideindex]
        self.CreatePrixyNode(Knee,
                             PC=Hip,
                             mMvoe=[0, -6.4, 0],
                             mRotate=[0, 180, 90],
                             isConnect=True,
                             isParent=True)

        Ankle = self.Proxies_Ankles[sideindex]
        self.CreatePrixyNode(Ankle,
                             PC=Knee,
                             mMvoe=[0, -6.4, 0],
                             isConnect=True,
                             isParent=True)

        Ball = self.Proxies_Balls[sideindex]
        self.CreatePrixyNode(Ball,
                             PC=Ankle,
                             mMvoe=[0, -1.65, 2.26],
                             isConnect=True,
                             isParent=True)

        Toe = self.Proxies_Toes[sideindex]
        self.CreatePrixyNode(Toe,
                             PC=Ball,
                             mMvoe=[0, 0, 1.7])

        if self.toesNum == 1:
            self.ProxyConnectors(Ball, Toe)

        BallG = Ball + "_GRP"
        cmds.group(n=BallG, em=True)
        cmds.parent(BallG, Ball)
        cmds.parent(Toe, BallG)

        KneeLocator = Knee + "_Locator"
        cmds.spaceLocator(n=KneeLocator)
        PCons = cmds.pointConstraint(Knee, KneeLocator)
        cmds.delete(PCons)
        cmds.parent(KneeLocator, Knee)
        cmds.move(0, 0, 1.5, KneeLocator, r=True)
        cmds.setAttr("%s.v" % KneeLocator, 0)

        # toe num
        cmds.makeIdentity(Ball, apply=True, t=1, r=1, s=1)

        KneeG = Knee + "_GRP"
        cmds.group(n=KneeG, em=True)
        PCons = cmds.pointConstraint(Knee, KneeG)
        cmds.delete(PCons)
        cmds.parent(Knee, KneeG)
        cmds.makeIdentity(KneeG, apply=True, t=1, r=1, s=1)
        cmds.move(0, 0, 0.001, "%s.scalePivot" % KneeG, "%s.rotatePivot" % KneeG, r=True)
        cmds.cycleCheck(e=0)
        cmds.pointConstraint(Hip, Ankle, KneeG, mo=True)
        cmds.cycleCheck(e=1)
        cmds.parent(KneeG, Ankle, self.Main)
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

    def ElbowIndicator(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        # fetch
        Proxies_Elbow = self.Proxies_Elbows[sideindex]
        Proxies_Shoulder = self.Proxies_Shoulders[sideindex]
        Proxies_Wrist = self.Proxies_Wrists[sideindex]

        Proxies_Elbow_GRP = Proxies_Elbow + "_GRP"
        Proxies_ElbowParent = Proxies_Elbow + "_Parent"
        Proxies_ElbowAim = Proxies_Elbow + "_Aim"
        Proxies_ElbowParentUp = Proxies_Elbow + "_ParentUp"
        Proxies_ElbowParentUp_GRP = Proxies_Elbow + "_ParentUp_GRP"

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

        # Hidden
        cmds.setAttr("%s.v" % Proxies_ElbowAim, 0)
        cmds.setAttr("%s.v" % Proxies_ElbowParent, 0)
        cmds.setAttr("%s.v" % Proxies_ElbowParentUp, 0)

        pass

    def KneeIndicator(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        # fetch & name
        Hip = self.Proxies_Hips[sideindex]
        Ankle = self.Proxies_Ankles[sideindex]
        Knee = self.Proxies_Knees[sideindex]

        KneeG = Knee + "_GRP"
        Proxies_KneeParent = Knee + "_Parent"
        Proxies_KneeAim = Knee + "_Aim"
        Proxies_KneeParentUp = Knee + "_ParentUp"
        Proxies_KneeParentUp_GRP = Knee + "_ParentUp_GRP"

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

        # Hidden
        cmds.setAttr("%s.v" % Proxies_KneeAim, 0)
        cmds.setAttr("%s.v" % Proxies_KneeParent, 0)
        cmds.setAttr("%s.v" % Proxies_KneeParentUp, 0)

        pass

    def FootTilt(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        Ankle = self.Proxies_Ankles[sideindex]
        Ball = self.Proxies_Balls[sideindex]
        BallG = Ball + "_GRP"

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
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        Clavicle = "Proxies_" + side + "_Clavicle"
        Shoulder = "Proxies_" + side + "_Shoulder"
        Wrist = "Proxies_" + side + "_Wrist"
        Palm = "Proxies_" + side + "_Palm"
        Hip = "Proxies_" + side + "_Hip"
        Ankle = "Proxies_" + side + "_Ankle"
        Elbow = "Proxies_" + side + "_Elbow"
        Knee = "Proxies_" + side + "_Knee"
        Eye = self.Proxies_Eyes[sideindex]

        if side == "L":
            cmds.transformLimits(Eye, ty=(-0.5, 1), ety=(1, 0))
            cmds.transformLimits(Clavicle, tx=(-1, 1), etx=(1, 0))
            cmds.transformLimits(Shoulder, tx=(-1.5, 1), etx=(1, 0))
            cmds.transformLimits(Wrist, tx=(-6.75, 1), etx=(1, 0))
            cmds.transformLimits(Palm, tx=(-0.6, 1), etx=(1, 0))
            cmds.transformLimits(Hip, tx=(-1.5, 1), etx=(1, 0))
            cmds.transformLimits(Ankle, tx=(-1.5, 1), etx=(1, 0))
            cmds.transformLimits(Elbow, tz=(-1, -0.001), etz=(0, 1))
            cmds.transformLimits(Knee, tz=(0.001, 1), etz=(1, 0))
        else:
            cmds.transformLimits(Eye, ty=(-1, 0.5), ety=(0, 1))
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

    def setRGBColor(self, ctrl, color=(1, 1, 1)):
        rgb = ("R", "G", "B")
        cmds.setAttr(ctrl + ".overrideEnabled", 1)
        cmds.setAttr(ctrl + ".overrideRGBColors", 1)

        for channel, color in zip(rgb, color):
            cmds.setAttr(ctrl + ".overrideColor%s" % channel, color)
