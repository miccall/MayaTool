# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import sys

mayaveersion = cmds.about(version=True)

if mayaveersion == "2022":
    import importlib

    sys.path.append("..")
    from Miccall_shelf.Miccall_AutoRigging.Utility import ControllerTool
    from Miccall_shelf.Miccall_AutoRigging.Utility import RiggingTool

    importlib.reload(ControllerTool)
    importlib.reload(RiggingTool)
    from Miccall_shelf.Miccall_AutoRigging.Utility.ControllerTool import ControllerTool as CT
    from Miccall_shelf.Miccall_AutoRigging.Utility.RiggingTool import RiggingTool as RT
    from . import LegRigging
    from . import TorsoRigging

    importlib.reload(LegRigging)
    importlib.reload(TorsoRigging)
else:
    from Miccall_shelf.Miccall_AutoRigging.Utility import ControllerTool
    from Miccall_shelf.Miccall_AutoRigging.Utility import RiggingTool
    import LegRigging
    import TorsoRigging

    reload(ControllerTool)
    reload(RiggingTool)
    reload(LegRigging)
    reload(TorsoRigging)
    from Miccall_shelf.Miccall_AutoRigging.Utility.ControllerTool import ControllerTool as CT
    from Miccall_shelf.Miccall_AutoRigging.Utility.RiggingTool import RiggingTool as RT


class BipedRigging:
    def __init__(self, Creator=None):
        self.ControllerTool = CT
        self.RiggingTool = RT
        self.Creator = Creator
        self.InitData()
        self.Armature()
        # self.RiggingTool.CreateDuplicate(self.Creator.root, "IK")
        # self.RiggingTool.CreateDuplicate(self.Creator.root, "FK")
        # Main Control : 在脚底最外层控制器
        # self.TorsoRig()
        # self.LegRig()
        pass

    def LegRig(self):
        # 脚的定位点 。FootInTilt  FootOutTilt FootHeelPivot

        # Leg IK FK GRP

        Rigger = LegRigging.LegRigging(ResJNT=self.Creator.LegChainNames)
        Rigger.MainProcess()

    def TorsoRig(self):
        # ROOT Control GRP : 在hips ，有 hip 和 spline Top 的 定位点

        # Main Hip Control GRP :
        # 1 . Spine Mid IK Control GRP 2_Btm Locator
        # 2 . MId 控制器的定位点
        # 3 . Hip 的控制器

        # Spine?? FK Control GRP

        # Spine Top FK Control GRP

        # Spine Top IK Control GRP 2

        # Spine Mid IK Control GRP

        # SpineStartLctr & SpineSplineBtm & SpineSplineTop

        # SpineSplineTop_ClusterG & SpineSplineMid_ClusterG & SpineSplineBtm_ClusterG

        # Spine_ ribbon Spine GRP
        # 1. Spine Top JNT IK
        # 2. Spine Mid JNT IK
        # 3. Spine Bottom 01 JNT IK

        # ExtraNodes

        # Spine?? Curve Control GRP
        # Spine?? JNT
        pass
        # Rigger = TorsoRigging.TorsoRigging(ResJNT=self.Creator.TorsoChainNames)
        # Rigger.MainProcess()

    def ArmRig(self):
        # Wrist GRP

        # Arm IK FK GRP

        pass

    def JawRig(self):
        pass

    def EyeRig(self):
        pass

    def InitData(self):
        self.Creator.Main
        self.Creator.Proxies_Root
        self.Creator.Proxies_SpineTop
        self.Creator.Proxies_Head
        self.Creator.Proxies_Jaw
        self.Creator.Proxies_JawTip
        self.Creator.Proxies_HeadTip
        self.Creator.Proxies_L_Eye
        self.Creator.Proxies_R_Eye

        self.Proxy_Clavicle = [self.Creator.Proxies_L_Clavicle, self.Creator.Proxies_R_Clavicle]
        self.Proxy_Shoulder = [self.Creator.Proxies_L_Shoulder, self.Creator.Proxies_R_Shoulder]
        self.Proxy_Wrist = [self.Creator.Proxies_L_Wrist, self.Creator.Proxies_R_Wrist]
        self.Proxy_Palm = [self.Creator.Proxies_L_Palm, self.Creator.Proxies_R_Palm]
        self.Proxy_Hip = [self.Creator.Proxies_L_Hip, self.Creator.Proxies_R_Hip]
        self.Proxy_Ankle = [self.Creator.Proxies_L_Ankle, self.Creator.Proxies_R_Ankle]
        self.Proxy_Elbow = [self.Creator.Proxies_L_Elbow, self.Creator.Proxies_R_Elbow]
        self.Proxy_Knee = [self.Creator.Proxies_L_Knee, self.Creator.Proxies_R_Knee]
        self.Proxy_Ball = [self.Creator.Proxies_L_Ball, self.Creator.Proxies_R_Ball]
        self.Proxy_Toe = [self.Creator.Proxies_L_Toe, self.Creator.Proxies_R_Toe]
        pass

    def Armature(self):
        self.name = "Mic"
        name = "Mic"
        self.RootJointTemp = "%s_SpineTemp01_JNT" % name
        self.RootJoint = "%s_Root_JNT" % name
        self.SpineTopJoint = "%s_SpineTop_JNT" % name

        # Create torso Joints Chain
        cmds.select(cl=True)
        cmds.joint(n=self.RootJoint)
        self.AlignPointPos(self.Creator.Proxies_Root, self.RootJoint)
        cmds.select(self.RootJoint)
        cmds.joint(n=self.RootJointTemp)
        self.AlignPointPos(self.Creator.spineProxies[0], self.RootJointTemp)

        spineJoints = [self.RootJointTemp]
        Proxy_spineJoints = self.Creator.spineProxies
        i = 1
        while i < len(Proxy_spineJoints):
            cmds.select(spineJoints[i - 1])
            SpineTemp = "_SpineTemp0"
            JointSuffix = "_JNT"
            spineName = name + SpineTemp + str(i + 1) + JointSuffix
            cmds.joint(n=spineName)
            self.AlignPointPos(Proxy_spineJoints[i], spineName)
            cmds.select(spineName)
            cmds.joint(e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
            spineJoints.append(spineName)
            i += 1
        cmds.select(spineJoints[-1])
        cmds.joint(n=self.SpineTopJoint)
        cmds.joint(e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        # cmds.pointConstraint(self.Creator.Proxies_SpineTop, self.SpineTopJoint)
        self.AlignPointPos(self.Creator.Proxies_SpineTop, self.SpineTopJoint)

        # Create Neck Joints Chain
        self.NeckJointTemp = "%s_NeckTemp01_JNT" % name
        cmds.select(self.SpineTopJoint)
        cmds.joint(n=self.NeckJointTemp)
        cmds.joint(e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        self.AlignPointPos(self.Creator.neckProxies[0], self.NeckJointTemp)

        # Head
        self.HeadJoint = "%s_Head_JNT" % name
        cmds.select(self.NeckJointTemp)
        cmds.joint(n=self.HeadJoint)
        cmds.joint(e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        self.AlignPointPos(self.Creator.Proxies_Head, self.HeadJoint)
        # _HeadTip
        self.HeadTipJoint = "%s_HeadTip_JNT" % name
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.HeadTipJoint)
        cmds.joint(e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        self.AlignPointPos(self.Creator.Proxies_HeadTip, self.HeadTipJoint)
        # Jaw
        self.JawJoint = "%s_Jaw_JNT" % name
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.JawJoint)
        self.AlignPointPos(self.Creator.Proxies_Jaw, self.JawJoint)
        # JawTip
        self.JawTipJoint = "%s_JawTip_JNT" % name
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.JawTipJoint)
        self.AlignPointPos(self.Creator.Proxies_JawTip, self.JawTipJoint)
        # L Eye
        self.LEyeJoint = "%s_L_Eye_JNT" % name
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.LEyeJoint)
        self.AlignPointPos(self.Creator.Proxies_L_Eye, self.LEyeJoint)
        # R Eye
        self.REyeJoint = "%s_R_Eye_JNT" % name
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.REyeJoint)
        self.AlignPointPos(self.Creator.Proxies_R_Eye, self.REyeJoint)

        # Arm
        self.ArmatureArm("L")
        self.ArmatureArm("R")

        # Leg
        self.ArmatureLeg("L")
        self.ArmatureLeg("R")

        # wrist rotate
        lWristRotation = cmds.xform(self.Proxy_Wrist[0], q=True, ro=True)
        lWristRotation = cmds.xform(self.Proxy_Wrist[1], q=True, ro=True)

        # Orient Joints
        cmds.joint(self.RootJoint, e=True, oj="None", secondaryAxisOrient="yup", zso=True)

        pass

    def ArmatureArm(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        # ClavicleJoint
        cmds.select(self.SpineTopJoint)
        ClavicleJoint = self.name + "_" + side + "_Clavicle_JNT"
        cmds.joint(n=ClavicleJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Clavicle[sideindex], ClavicleJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Shoulder[sideindex], ClavicleJoint, aimVector=[1, 0, 0],
                                  upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0],
                                  worldUpObject=self.Proxy_Clavicle[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(ClavicleJoint, apply=True, r=1)

        # ShoulderJoint
        cmds.select(ClavicleJoint)
        ShoulderJoint = self.name + "_" + side + "_Shoulder_JNT"
        cmds.joint(n=ShoulderJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Shoulder[sideindex], ShoulderJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Elbow[sideindex], ShoulderJoint, aimVector=[1, 0, 0],
                                  upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0],
                                  worldUpObject=self.Proxy_Shoulder[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(ClavicleJoint, apply=True, r=1)

        # ElbowJoint
        cmds.select(ShoulderJoint)
        ElbowJoint = self.name + "_" + side + "_Elbow_JNT"
        cmds.joint(n=ElbowJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Elbow[sideindex], ElbowJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Wrist[sideindex], ElbowJoint, aimVector=[1, 0, 0],
                                  upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0],
                                  worldUpObject=self.Proxy_Elbow[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(ClavicleJoint, apply=True, r=1)

        # WristJoint
        cmds.select(ElbowJoint)
        WristJoint = self.name + "_" + side + "_Wrist_JNT"
        cmds.joint(n=WristJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Wrist[sideindex], WristJoint)
        cmds.delete(Pcon)
        cmds.select(ElbowJoint)
        WristDummyJoint = self.name + "_" + side + "_WristDummy_JNT"
        cmds.joint(n=WristDummyJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Wrist[sideindex], WristDummyJoint)
        cmds.delete(Pcon)
        cmds.makeIdentity(WristJoint, WristDummyJoint, apply=True, r=1)

        # Thumb

        # Hand

        # Forearm

        pass

    def ArmatureLeg(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        # HipJoint
        cmds.select(self.RootJoint)
        HipJoint = self.name + "_" + side + "_Hip_JNT"
        cmds.joint(n=HipJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Hip[sideindex], HipJoint)
        cmds.delete(Pcon)

        # KneeJoint
        cmds.select(HipJoint)
        KneeJoint = self.name + "_" + side + "_Knee_JNT"
        cmds.joint(n=KneeJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Knee[sideindex], KneeJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Ankle[sideindex], KneeJoint, aimVector=[1, 0, 0],
                                  upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 0, 1],
                                  worldUpObject=self.Proxy_Knee[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(KneeJoint, apply=True, r=1)

        # Ankle
        cmds.select(KneeJoint)
        AnkleJoint = self.name + "_" + side + "_Ankle_JNT"
        cmds.joint(n=AnkleJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Ankle[sideindex], AnkleJoint)
        cmds.delete(Pcon)
        # Ball
        cmds.select(AnkleJoint)
        BallJoint = self.name + "_" + side + "_Ball_JNT"
        cmds.joint(n=BallJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Ball[sideindex], BallJoint)
        cmds.delete(Pcon)
        # Toe
        cmds.select(BallJoint)
        ToeJoint = self.name + "_" + side + "_Toe_JNT"
        cmds.joint(n=ToeJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Toe[sideindex], ToeJoint)
        cmds.delete(Pcon)

        pass

    def AlignPointPos(self, sou, tar):
        con = cmds.pointConstraint(sou, tar)
        cmds.delete(con)
        pass
