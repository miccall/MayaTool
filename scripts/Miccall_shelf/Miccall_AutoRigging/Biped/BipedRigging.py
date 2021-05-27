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
    def __init__(self, ProxyCreator=None, ArmatureCreator=None):
        self.ControllerTool = CT
        self.RiggingTool = RT
        self.ProxyData = ProxyCreator
        self.ArmatureData = ArmatureCreator
        self.name = "Mic"
        self.InitData()
        self.MainRig()
        self.TorsoRig()
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
        TorsoData = []
        Rigger = TorsoRigging.TorsoRigging(ArmatureData=self.ArmatureData, ProxyData=self.ProxyData)
        Rigger.MainProcess2()
        # ROOT Control GRP : 在 hips ，有 hip 和 spline Top 的 定位点

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
        """
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
        """
        pass

    def MainRig(self):
        # Main
        self.MainControl = self.name + "_Main_Ctr"
        self.ControllerTool.MainControl(self.MainControl)
        # ROOT
        self.RootControl = self.name + "Root_Ctr"
        self.ControllerTool.CircleControl(self.RootControl)
        cmds.scale(4, 4, 4, self.RootControl)
        cmds.makeIdentity(self.RootControl, apply=True, s=1)
        self.RootControlGRP = self.RootControl + "_GRP"
        cmds.group(n=self.RootControlGRP)
        cmds.parent(self.RootControlGRP, self.ArmatureData.RootJoint)
        cmds.makeIdentity(apply=False, t=1, s=1)
        cmds.parent(self.RootControlGRP, w=True)
        cmds.delete(self.RootControl, ch=True)
        # MainHip
        self.MainHipsControl = self.name + "_MainHipC"
        self.MainHipsControlGRP = self.MainHipsControl + "_GRP"
        self.ControllerTool.HipsControl(self.MainHipsControl)
        cmds.parent(self.MainHipsControlGRP, self.ArmatureData.RootJoint)
        cmds.makeIdentity(apply=False, t=1, s=1)
        cmds.parent(w=True)
        cmds.scale(3, 2.75, 2.75, self.MainHipsControl)
        cmds.makeIdentity(apply=True, t=0, r=1, s=1)
        pass
