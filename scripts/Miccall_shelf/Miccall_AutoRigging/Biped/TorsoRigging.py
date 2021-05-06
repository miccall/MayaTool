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
        self.BodyGRP = "Body_GRP"
        self.BaseControl = "Base_Ctr"
        self.BodyIKGRP = "Body_IK_GRP"
        self.BodyFKGRP = "Body_FK_GRP"
        self.RootTransform = "Root_Transform"
        self.RootControl = "Root_Ctr"

    def MainProcess(self):
        # 创建一条 IK 的骨骼链
        self.IKJoints = self.GetRigChain("IK")
        # 创建一条 FK 的骨骼链
        self.FKJoints = self.GetRigChain("FK")
        # IK 控制器
        self.CreateIKControl()
        """
        # FK 控制器
        self.CreateFKControl()
        self.LinkRes()
        
        # Main
        self.CreateBaseControl()
        # Layer
        self.AddToLayer(self.BaseControl, 13)
        self.AddToLayer(self.BodyIKGRP, 17)
        self.AddToLayer(self.BodyFKGRP, 18)
        """

    def CreatChain(self, Attr):
        NewChainList = cmds.duplicate(self.ResultJoints, parentOnly=True)
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

    def GetRigChain(self, Attr):
        Chain = []
        for JNT in self.ResultJoints:
            JointNameSplits = JNT.split("_")
            prefix = ""
            for i in range(0, len(JointNameSplits) - 1):
                prefix += JointNameSplits[i] + "_"
            prefix += "%s" % Attr + "_JNT"
            Chain.append(prefix)
        return Chain

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
        cmds.setAttr("%s.inheritsTransform" % self.TorsoIKCurve, 0)
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
        cmds.group(self.IKControls[0], self.ShoulderGRP, self.HipGRP, self.TorsoIKHandle, self.TorsoIKCurve,
                   self.IKControlJoints[0], self.IKControlJoints[1], self.IKJoints[0], n=self.BodyIKGRP)

        cmds.setAttr("%s.sx" % self.IKControls[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % self.IKControls[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % self.IKControls[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sx" % self.IKControls[1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % self.IKControls[1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % self.IKControls[1], lock=True, keyable=False, channelBox=False)

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
            cmds.setAttr("%s.sx" % name, lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.sy" % name, lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.sz" % name, lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.tx" % name, lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.ty" % name, lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.tz" % name, lock=True, keyable=False, channelBox=False)
            self.FKControls.append(name)

        cmds.parentConstraint(self.FKJoints[0], self.HipGRP, mo=True, w=1)
        cmds.parentConstraint(self.FKJoints[self.TorseSplineCount - 1], self.ShoulderGRP, mo=True, w=1)

        cmds.setAttr("%s.sx" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.tx" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ty" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.tz" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rx" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ry" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rz" % self.FKJoints[0], lock=True, keyable=False, channelBox=False)

        cmds.setAttr("%s.sx" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.tx" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ty" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.tz" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rx" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ry" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rz" % self.FKJoints[self.TorseSplineCount - 1], lock=True, keyable=False, channelBox=False)

        cmds.group(self.FKJoints[0], n=self.BodyFKGRP)

    def LinkRes(self):
        # worldMatrix[0] pSphere1.offsetParentMatrix
        # cmds.connectAttr('%s.worldMatrix[0]' % self.IKJoints[0], '%s.offsetParentMatrix' % self.ResultJoints[0], f=True)
        # """
        for i in range(0, len(self.ResultJoints)):
            # cmds.connectAttr('%s.rotate' % self.IKJoints[i], '%s.rotate' % self.ResultJoints[i], f=True)
            # cmds.connectAttr('%s.translate' % self.IKJoints[i], '%s.translate' % self.ResultJoints[i], f=True)
            # cmds.connectAttr('%s.worldMatrix[0]' % self.IKJoints[0], '%s.offsetParentMatrix' % self.ResultJoints[0], f=True)
            cmds.parentConstraint(self.IKJoints[i], self.ResultJoints[i], mo=True, w=1)
        # """

    def CreateBaseControl(self):
        CT.FourArror(self.BaseControl)
        startpos = cmds.xform(self.ResultJoints[0], q=1, ws=1, rp=1)
        cmds.setAttr("%s.rotateOrder" % self.BaseControl, 2)
        cmds.setAttr("%s.sx" % self.BaseControl, 15)
        cmds.setAttr("%s.sy" % self.BaseControl, 15)
        cmds.setAttr("%s.sz" % self.BaseControl, 15)
        cmds.setAttr("%s.tx" % self.BaseControl, startpos[0])
        cmds.setAttr("%s.ty" % self.BaseControl, startpos[1])
        cmds.setAttr("%s.tz" % self.BaseControl, startpos[2])
        cmds.makeIdentity("%s" % self.BaseControl, apply=True, t=1, r=1, s=1, n=0)
        cmds.setAttr("%s.sx" % self.BaseControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % self.BaseControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % self.BaseControl, lock=True, keyable=False, channelBox=False)
        # GRP OTHER
        cmds.group(self.BodyIKGRP, self.BodyFKGRP, n=self.BodyGRP)
        cmds.parentConstraint(self.BaseControl, self.BodyGRP, mo=True, w=1)
        # Root
        cmds.group(self.BodyGRP, self.BaseControl, n=self.RootTransform)
        cmds.setAttr("%s.rotateOrder" % self.RootTransform, 2)
        CT.FourArror(self.RootControl)
        cmds.setAttr("%s.sx" % self.RootControl, 20)
        cmds.setAttr("%s.sy" % self.RootControl, 20)
        cmds.setAttr("%s.sz" % self.RootControl, 20)
        cmds.makeIdentity("%s" % self.RootControl, apply=True, t=1, r=1, s=1, n=0)
        cmds.select("%sShape" % self.RootControl)
        cmds.select("%s" % self.RootTransform, add=True)
        mel.eval("parent -r -s")
        cmds.delete(self.RootControl)
        cmds.rename(self.RootTransform, self.RootControl)
        cmds.setAttr("%sShape.overrideEnabled" % self.RootControl, 1)
        cmds.setAttr("%sShape.overrideRGBColors" % self.RootControl, 1)
        cmds.setAttr("%sShape.overrideColorR" % self.RootControl, 1)
        cmds.setAttr("%sShape.overrideColorG" % self.RootControl, 0)
        cmds.setAttr("%sShape.overrideColorB" % self.RootControl, 1)
        pass

    def AddToLayer(self, Hierarchy, colorIndex=0):
        # Hierarchy = "Thigh_L_FK_Ctr"
        nameList = Hierarchy.split("_")
        LayerName = ""
        for i in range(0, len(nameList) - 1):
            LayerName += nameList[i] + "_"
        LayerName += "Layer"
        cmds.select(Hierarchy)
        cmds.createDisplayLayer(name=LayerName, number=1, nr=True)
        cmds.setAttr("%s.displayType" % LayerName, 0)
        cmds.setAttr("%s.color" % LayerName, colorIndex)
        cmds.setAttr("%s.overrideColorRGB" % LayerName, 0, 0, 0)
        cmds.setAttr("%s.overrideRGBColors" % LayerName, 0)
