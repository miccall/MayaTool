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

    importlib.reload(ControllerTool)
    from Miccall_shelf.Miccall_AutoRigging.Utility import RiggingTool

    importlib.reload(RiggingTool)
    from Miccall_shelf.Miccall_AutoRigging.Utility.ControllerTool import ControllerTool as CT
    from Miccall_shelf.Miccall_AutoRigging.Utility.RiggingTool import RiggingTool as RT
else:
    from Miccall_shelf.Miccall_AutoRigging.Utility import ControllerTool

    reload(ControllerTool)
    from Miccall_shelf.Miccall_AutoRigging.Utility import RiggingTool

    reload(RiggingTool)
    from Miccall_shelf.Miccall_AutoRigging.Utility.ControllerTool import ControllerTool as CT
    from Miccall_shelf.Miccall_AutoRigging.Utility.RiggingTool import RiggingTool as RT


class TorsoRigging:
    def __init__(self, ResJNT=None):
        # 原始的骨骼链
        self.ResultJoints = ResJNT
        self.TorseSplineCount = len(ResJNT)
        self.TorsoIKHandle = "Torso_IK_HDL"
        self.TorsoIKEffector = "Torso_IK_Eff"
        self.TorsoIKCurve = "Torso_IK_Curve"
        self.IKControlJoints = ["Torso_IK_Start_CtrJNT", "Torso_IK_End_CtrJNT"]
        self.IKControls = ["Torso_IK_Start_Ctr", "Torso_IK_End_Ctr"]
        self.FKControls = []
        self.HipGRP = "Hip_Const_GRP"
        self.ShoulderGRP = "Shoulder_Const_GRP"

    def MainProcess(self):
        # 创建一条 IK 的骨骼链
        self.IKJoints = self.CreatChain("IK")
        # 创建一条 FK 的骨骼链
        self.FKJoints = self.CreatChain("FK")
        # IK 控制器
        self.CreateIKControl()
        # FK 控制器
        self.CreateFKControl()

    def CreatChain(self, Attr):
        NewChainList = cmds.duplicate(self.ResultJoints[0])
        realname = ""
        realnamelist = []
        for name in NewChainList:
            realname += "|%s" % name
            realnamelist.append(realname)
        NewChainList.reverse()
        realnamelist.reverse()
        for i in range(0, len(realnamelist)):
            JointName = NewChainList[i]
            JointNameSplits = JointName.split("_")
            newChainName = JointNameSplits[0] + "_%s" % Attr + "_JNT"
            cmds.rename(realnamelist[i], newChainName)
            # cmds.setAttr("%s.rotateOrder" % newChainName, 3)
            realnamelist[i] = newChainName
        realnamelist.reverse()
        return realnamelist

    def CreateIKControl(self):
        # Spline IK
        firstJoint = self.IKJoints[0]
        lastJoint = self.IKJoints[self.TorseSplineCount - 1]
        Handle = cmds.ikHandle(sj=firstJoint, ee=lastJoint, sol="ikSplineSolver")
        cmds.rename(Handle[0], self.TorsoIKHandle)
        cmds.rename(Handle[1], self.TorsoIKEffector)
        cmds.rename(Handle[2], self.TorsoIKCurve)
        IKHandleControl = self.CreatChain("IK_Ctr")
        cmds.parent(IKHandleControl[self.TorseSplineCount - 1], w=True)
        cmds.delete(IKHandleControl[1])
        cmds.rename(IKHandleControl[0], self.IKControlJoints[0])
        cmds.rename(IKHandleControl[self.TorseSplineCount - 1], self.IKControlJoints[1])
        influences = [self.IKControlJoints[0], self.IKControlJoints[1]]
        scls = cmds.skinCluster(influences, self.TorsoIKCurve, n='Spine_skinCluster', tsb=True, bm=0, sm=0, nw=1)[0]

        # IK Controller
        CT.BoxControl(self.IKControls[0])
        CT.BoxControl(self.IKControls[1])
        startpos = cmds.xform(self.ResultJoints[0], q=1, ws=1, rp=1)
        endpos = cmds.xform(self.ResultJoints[self.TorseSplineCount - 1], q=1, ws=1, rp=1)
        cmds.setAttr("%s.tx" % self.IKControls[0], startpos[0])
        cmds.setAttr("%s.ty" % self.IKControls[0], startpos[1])
        cmds.setAttr("%s.tz" % self.IKControls[0], startpos[2])
        cmds.setAttr("%s.sx" % self.IKControls[0], startpos[1] / 2)
        cmds.setAttr("%s.sy" % self.IKControls[0], startpos[1] / 4)
        cmds.setAttr("%s.sz" % self.IKControls[0], startpos[1] / 2)
        cmds.setAttr("%s.rotateOrder" % self.IKControls[0], 2)
        cmds.setAttr("%s.tx" % self.IKControls[1], endpos[0])
        cmds.setAttr("%s.ty" % self.IKControls[1], endpos[1])
        cmds.setAttr("%s.tz" % self.IKControls[1], endpos[2])
        cmds.setAttr("%s.sx" % self.IKControls[1], startpos[1] / 2)
        cmds.setAttr("%s.sy" % self.IKControls[1], startpos[1] / 4)
        cmds.setAttr("%s.sz" % self.IKControls[1], startpos[1] / 2)
        cmds.setAttr("%s.rotateOrder" % self.IKControls[1], 2)
        cmds.setAttr("%s.rotateOrder" % self.IKControlJoints[0], 2)
        cmds.setAttr("%s.rotateOrder" % self.IKControlJoints[1], 2)
        cmds.makeIdentity("%s" % self.IKControls[0], apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity("%s" % self.IKControls[1], apply=True, t=1, r=1, s=1, n=0)
        cmds.parentConstraint(self.IKControls[0], self.IKControlJoints[0], mo=True, w=1)
        cmds.parentConstraint(self.IKControls[1], self.IKControlJoints[1], mo=True, w=1)

        # IK Twist
        cmds.setAttr("%s.dTwistControlEnable" % self.TorsoIKHandle, 1)
        cmds.setAttr("%s.dWorldUpType" % self.TorsoIKHandle, 4)
        cmds.setAttr("%s.dWorldUpVectorEndZ" % self.TorsoIKHandle, 1)
        # 将 “ Torso_IK_Start_CtrJNT.worldMatrix[0] ” 连接到 “Torso_IK_HDL.dWorldUpMatrix”
        cmds.connectAttr("%s.worldMatrix[0]" % self.IKControlJoints[0], "%s.dWorldUpMatrix" % self.TorsoIKHandle)
        cmds.connectAttr("%s.worldMatrix[0]" % self.IKControlJoints[1], "%s.dWorldUpMatrixEnd" % self.TorsoIKHandle)

        cmds.group(self.IKControls[0], n=self.HipGRP)
        cmds.group(self.IKControls[1], n=self.ShoulderGRP)
        pass

    def CreateFKControl(self):
        cmds.joint(self.FKJoints[0], e=True, oj="yxz", secondaryAxisOrient="xup", zso=True, ch=True)
        for i in range(1, self.TorseSplineCount - 1):
            print(self.FKJoints[i])
            cmds.setAttr("%s.rotateOrder" % self.FKJoints[i], 1)
            name = "%s_Ctr" % self.FKJoints[i][0:-4]
            CT.CircleControl(name)
            # todo : xform
            cmds.setAttr("%s.scaleX" % name, 20)
            cmds.setAttr("%s.scaleY" % name, 20)
            cmds.setAttr("%s.scaleZ" % name, 20)
            cmds.makeIdentity("%s" % name, apply=True, t=1, r=1, s=1, n=0)
            cmds.select("%sShape" % name)
            cmds.select("%s" % self.FKJoints[i], add=True)
            mel.eval("parent -r -s")
            cmds.delete(name)
            cmds.rename(self.FKJoints[i], name)
            self.FKControls.append(name)

        cmds.parentConstraint(self.FKJoints[0], self.HipGRP, mo=True, w=1)
        cmds.parentConstraint(self.FKJoints[self.TorseSplineCount - 1], self.ShoulderGRP, mo=True, w=1)
