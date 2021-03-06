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
    def __init__(self, ResJNT=None, ArmatureData=None, ProxyData=None):
        # 原始的骨骼链
        """
        self.ResultJoints = ResJNT
        self.TorseSplineCount = len(ResJNT)
        """
        self.ArmatureData = ArmatureData
        self.ProxyData = ProxyData
        self.InitData2()

    def InitData(self):
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

    def InitData2(self):
        split = self.ArmatureData.RootJointTemp.split("_")
        split2 = split[0:-1]
        self.name = split[0]
        self.spline = split[1]
        newName = "_".join(split2)
        self.SpineTemp01Joint_FKCtr = newName + "_FKCtr"
        self.SpineTemp01Joint_FKCtr_GRP = self.SpineTemp01Joint_FKCtr + "_GRP"
        self.SpineJoint_FKCtrList = [self.SpineTemp01Joint_FKCtr]
        self.SpineJoint_FKCtrGRPList = [self.SpineTemp01Joint_FKCtr_GRP]
        self.SpineTop_IKCtr = self.name + "_SpineTop_IKCtr"
        self.SpineTop_IKCtr_GRPs = [self.SpineTop_IKCtr + "_GRP", self.SpineTop_IKCtr + "_GRP2"]
        self.SpineMid_IKCtr = self.name + "_SpineMid_IKCtr"
        self.SpineMid_IKCtr_GRPs = [self.SpineMid_IKCtr + "_GRP", self.SpineMid_IKCtr + "_GRP2"]
        self.SplineScale = 1

        self.SpineLengthAimLctr = self.name + "_SpineLengthAimLctr"
        self.SpineLengthTargetLctr = self.name + "_SpineLengthTargetLctr"
        self.HeadLengthAimLctr = self.name + "_HeadLengthAimLctr"
        self.HeadLengthTargetLctr = self.name + "_HeadLengthTargetLctr"
        self.SpineTop_IKCtrOrientLctr = self.SpineTop_IKCtr + "_OrientLctr"

        # Fetch
        self.MainControl = self.name + "_Main_Ctr"
        self.RootControl = self.name + "_Root_Ctr"
        self.RootControlGRP = self.RootControl + "_GRP"
        self.MainHipControl = self.name + "_MainHip_Ctr"
        self.MainHipControlGRP = self.MainHipControl + "_GRP"

        pass

    def Lenght(self):
        cmds.spaceLocator(n=self.SpineLengthAimLctr)
        cmds.spaceLocator(n=self.SpineLengthTargetLctr)
        cmds.parent(self.SpineLengthTargetLctr, self.SpineLengthAimLctr)
        cmds.pointConstraint(self.ProxyData.Proxies_Root, self.SpineLengthAimLctr)
        cmds.aimConstraint(self.ProxyData.Proxies_SpineTop, self.SpineLengthAimLctr,
                           aimVector=[0, 1, 0], upVector=[1, 0, 0], worldUpType="vector", worldUpVector=[1, 0, 0],
                           skip=['y', 'z'])
        cmds.pointConstraint(self.ProxyData.Proxies_SpineTop, self.SpineLengthTargetLctr)
        self.spineLength = cmds.getAttr(self.SpineLengthTargetLctr + ".ty")
        self.spineLength = self.spineLength / 2
        cmds.delete(self.SpineLengthAimLctr)

        cmds.spaceLocator(n=self.HeadLengthAimLctr)
        cmds.spaceLocator(n=self.HeadLengthTargetLctr)
        cmds.parent(self.HeadLengthTargetLctr, self.HeadLengthAimLctr)

        cmds.pointConstraint(self.ProxyData.Proxies_Head, self.HeadLengthAimLctr)
        cmds.aimConstraint(self.ProxyData.Proxies_HeadTip, self.HeadLengthAimLctr,
                           aimVector=[0, 1, 0], upVector=[1, 0, 0], worldUpType="vector", worldUpVector=[1, 0, 0],
                           skip=['y', 'z'])
        cmds.pointConstraint(self.ProxyData.Proxies_HeadTip, self.HeadLengthTargetLctr)
        self.headLength = cmds.getAttr(self.HeadLengthTargetLctr + ".ty")
        cmds.delete(self.HeadLengthAimLctr)
        pass

    def SpineControl(self):
        name = self.name
        spline = self.spline
        controlGroup = ""
        splineList = self.ArmatureData.SpineJointList
        splineList.append(self.ArmatureData.SpineTopJoint)
        for i, controlBone in enumerate(splineList):
            if i == 0:
                # 创建一个 controlname 的控制器给 controlBone 。
                CT.TorsoFKControl(self.SpineTemp01Joint_FKCtr)
                cmds.delete(self.SpineTemp01Joint_FKCtr, ch=True)
                cmds.group(n=self.SpineTemp01Joint_FKCtr_GRP)
                cmds.xform(os=True, piv=[0, 0, 0])
                self.AlignPointPos(self.ArmatureData.RootJointTemp, self.SpineTemp01Joint_FKCtr_GRP)
                cmds.setAttr("%s.scale" % self.SpineTemp01Joint_FKCtr_GRP, (self.SplineScale * 4.5),
                             (self.SplineScale * 1.1),
                             (self.SplineScale * 2.5))
                cmds.makeIdentity(self.SpineTemp01Joint_FKCtr_GRP, apply=True, t=0, s=1, r=1)

                # 处理旋转问题
                controlAlihnLoc = "%s%sAlign_Loc" % (name, spline)
                cmds.spaceLocator(n=controlAlihnLoc)
                self.AlignPointPos(self.ProxyData.Proxies_Root, controlAlihnLoc)
                AimCon = cmds.aimConstraint(self.ProxyData.Proxies_SpineTop, controlAlihnLoc, aimVector=[0, 1, 0],
                                            upVector=[1, 0, 0],
                                            worldUpType="vector", worldUpVector=[1, 0, 0])
                cmds.delete(AimCon)
                OriCon = cmds.orientConstraint(controlAlihnLoc, self.SpineTemp01Joint_FKCtr_GRP)
                cmds.delete(OriCon)
                cmds.delete(controlAlihnLoc)
            else:
                # 复制到其他骨骼
                split = controlBone.split("_")
                split2 = split[0:-1]
                newName = "_".join(split2)
                controlname = newName + "_FKCtr"
                self.SpineJoint_FKCtrList.append(controlname)
                controlGroup = controlname + "_GRP"
                self.SpineJoint_FKCtrGRPList.append(controlGroup)
                cmds.duplicate(self.SpineTemp01Joint_FKCtr_GRP, n=controlGroup, rr=True)
                Pcon = cmds.pointConstraint(controlBone, controlGroup)
                cmds.delete(Pcon)
                cmds.makeIdentity(controlGroup, apply=True, t=1, s=1, r=1)
                cmds.select(controlGroup)
                cmds.pickWalk(d="down")
                cmds.rename(controlname)

        self.SpineTop_FKCtr = self.SpineJoint_FKCtrList[-1]
        self.SpineTop_FKCtr_GRP = self.SpineJoint_FKCtrGRPList[-1]
        pass

    def MainProcess2(self):
        self.Lenght()
        self.SpineControl()
        # spine Top
        controlBone = self.ArmatureData.SpineTopJoint
        CT.SpineTopCOntrol(self.SpineTop_IKCtr)
        Pcon = cmds.pointConstraint(controlBone, self.SpineTop_IKCtr_GRPs[1])
        cmds.delete(Pcon)
        cmds.makeIdentity(self.SpineTop_IKCtr + "_GRP2", apply=True, t=1, s=1, r=1)

        # Mid Curve
        CT.TorsoMidControl(self.SpineMid_IKCtr)

        # Find Mid Joint Ctr
        self.MidJointControl = self.SpineJoint_FKCtrList[1]

        # CONSTRAIN TO FK CONTROLS
        cmds.parentConstraint(self.MidJointControl, self.SpineMid_IKCtr_GRPs[0])
        cmds.pointConstraint(self.SpineTop_FKCtr, self.SpineTop_IKCtr_GRPs[0])

        # CREATE LOCATOR FOR ANGLED SPLINE END
        cmds.spaceLocator(n=self.SpineTop_IKCtrOrientLctr)
        Ocon = cmds.orientConstraint(self.SpineTop_FKCtr, self.SpineTop_IKCtrOrientLctr)
        cmds.delete(Ocon)
        cmds.parentConstraint(self.MainControl, self.SpineTop_IKCtrOrientLctr, mo=True)
        cmds.orientConstraint(self.SpineTop_IKCtrOrientLctr, self.SpineTop_FKCtr, self.SpineTop_IKCtr_GRPs[0])
        cmds.setAttr(self.SpineTop_IKCtrOrientLctr + ".v", 0)
        cmds.parent(self.SpineTop_IKCtrOrientLctr, self.MainControl)

        # Spine Length
        self.SpineStart_Loc = self.name + "_SpineStart_Loc"
        self.SpineEnd_Loc = self.name + "_SpineEnd_Loc"
        cmds.spaceLocator(n=self.SpineStart_Loc)
        cmds.spaceLocator(n=self.SpineEnd_Loc)
        cmds.parent(self.SpineEnd_Loc, self.SpineStart_Loc)
        cmds.pointConstraint(self.RootControl, self.SpineStart_Loc)
        cmds.aimConstraint(self.SpineTop_IKCtr, self.SpineStart_Loc, offset=[0, 0, 0], weight=1, aimVector=[0, 1, 0],
                           upVector=[0, 1, 0], worldUpType="none")
        cmds.pointConstraint(self.SpineTop_IKCtr, self.SpineEnd_Loc)
        self.SpineStart_LocPos = cmds.xform(self.SpineStart_Loc, q=True, ws=True, rp=True)
        self.SpineEnd_LocPos = cmds.xform(self.SpineEnd_Loc, q=True, ws=True, rp=True)

        # Ribbon
        self.Spine_Ribbon = self.name + "_Spine_Ribbon"
        self.Spine_RibbonBlend = self.name + "_Spine_RibbonBlend"
        self.Spine_RibbonBlendShape = self.name + "_Spine_RibbonBlendShape"
        self.spineNum = len(self.SpineJoint_FKCtrList) - 1
        cmds.nurbsPlane(n=self.Spine_Ribbon, p=[0, 0, 0], ax=[0, 0, 1], w=1, lr=3, d=3, u=1, v=self.spineNum, ch=1)
        cmds.rebuildSurface(self.Spine_Ribbon, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=0, kc=0, su=1, du=1, sv=2, dv=3,
                            tol=0.01, fr=0, dir=0)
        cmds.delete(ch=True)
        self.Spine_RibbonClusters = [self.Spine_Ribbon + "_L_Cluster", self.Spine_Ribbon + "_R_Cluster"]
        self.Spine_RibbonClusterGRPs = [self.Spine_RibbonClusters[0] + "_GRP", self.Spine_RibbonClusters[1] + "_GRP"]
        cmds.duplicate(self.Spine_Ribbon, n=self.Spine_RibbonBlend, rr=True)
        self.RibbonCluster("L")
        self.RibbonCluster("R")
        cmds.select(self.Spine_RibbonBlend, self.Spine_Ribbon)
        cmds.blendShape(n=self.Spine_RibbonBlendShape, tc=0)
        cmds.setAttr(self.Spine_RibbonBlendShape + "1." + self.Spine_RibbonBlend, 1)
        cmds.group(self.Spine_RibbonClusters[0], n=self.Spine_RibbonClusterGRPs[0])
        cmds.xform(os=True, piv=[0, 0, 0])
        cmds.group(self.Spine_RibbonClusters[1], n=self.Spine_RibbonClusterGRPs[1])
        cmds.xform(os=True, piv=[0, 0, 0])

        """
        $startPos = `xform -q -ws -rp ("RRA_ROOT")`;
        $EndPos = `xform -q -ws -rp ("RRA_SpineTop")`;
        select ("RRA_Spine"+"??");
        $splineJoints = `ls -sl -type "transform"`;
        $splineSize = `size $splineJoints`;
        select -add ("RRA_SpineTop");
        $splineProxies = `ls -sl`;
        $vertebrae = `size $splineProxies`;
        """
        # region Create Spine Curve
        # create & rebuild Spine Curve
        self.SpineCurve = self.name + "_Spine_Spline_Btm"
        self.SpineCurveTop = self.name + "_Spine_Spline_Top"
        mel.eval("curve -n " + self.SpineCurve + " -d 1 -p %s %s %s -p %s %s %s;" % (
            self.SpineStart_LocPos[0], self.SpineStart_LocPos[1], self.SpineStart_LocPos[2],
            self.SpineEnd_LocPos[0], self.SpineEnd_LocPos[1], self.SpineEnd_LocPos[2]))
        cmds.rebuildCurve(self.SpineCurve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=self.spineNum - 1, d=3,
                          tol=0)
        SpineJointList = [self.ArmatureData.RootJoint]
        SpineJointList += self.ArmatureData.SpineJointList
        # mapping pos
        for i, each in enumerate(SpineJointList):
            SpinePos = cmds.xform(each, q=True, rp=True, ws=True)
            cmds.move(SpinePos[0], SpinePos[1], SpinePos[2], self.SpineCurve + ".cv[%s]" % i, ws=True)

        # normalized
        cmds.select(self.SpineCurve)
        cmds.pickWalk(d="down")
        cmds.rename(self.SpineCurve + "Shape")

        # cut half
        cmds.detachCurve(self.SpineCurve + ".u[0.5]", n=self.SpineCurveTop, ch=0, cos=True, rpo=1)
        cmds.rename(self.SpineCurveTop + "1", self.SpineCurveTop)
        cmds.rebuildCurve(self.SpineCurve, ch=0, rpo=1, rt=0, end=1, kr=1, kcp=0, kep=0, kt=0, s=1, d=3,
                          tol=0.000328084)
        cmds.rebuildCurve(self.SpineCurveTop, ch=0, rpo=1, rt=0, end=1, kr=1, kcp=0, kep=0, kt=0, s=1, d=3,
                          tol=0.000328084)

        # Path followed locator
        SpineJointList.pop()  # last one
        SpineJointList.pop(0)  # first one
        count = len(SpineJointList)
        self.SpineCurveLocList = []

        # Create path loc
        for i, each in enumerate(SpineJointList):
            name = self.name + "_Spine_" + str(i) + "Curve_Loc_GRP"
            nameGRP = name + "_GRP"
            cmds.group(em=True, n=nameGRP)
            self.SpineCurveLocList.append(name)
            mapPath = each + "_MapPath"
            if (i + 1) <= ((count + 1) / 2):
                cmds.pathAnimation(nameGRP, self.SpineCurve, fractionMode=True, follow=False, n=mapPath)
                cmds.cutKey(mapPath, cl=True, at="u")
                v = float(i + 1) / ((count + 1) / 2)
                if v == 1:
                    v = 0.999
                cmds.setAttr(mapPath + ".uValue", v)
            else:
                cmds.pathAnimation(nameGRP, self.SpineCurveTop, fractionMode=True, follow=False, n=mapPath)
                cmds.cutKey(mapPath, cl=True, at="u")
                v = float(float(i + 1) - ((count + 1) / 2)) / ((count + 1) / 2)
                if v == 1:
                    v = 0.999
                cmds.setAttr(mapPath + ".uValue", v)

            cmds.spaceLocator(n=name)
            cmds.parent(name, nameGRP)
            Pcon = cmds.parentConstraint(self.SpineJoint_FKCtrList[i], name)
            cmds.delete(Pcon)

        # constraint
        for CurveLoc in self.SpineCurveLocList:
            CurveLoc += "_GRP"
            cmds.orientConstraint(self.MainHipControl, CurveLoc, mo=True)
            cmds.scaleConstraint(self.MainControl, CurveLoc, mo=True)
            cmds.setAttr(CurveLoc + ".v", 0)

        splineStartPos = cmds.xform(self.ProxyData.Proxies_Root, q=True, ws=True, rp=True)
        splineEndPos = cmds.xform(self.ProxyData.Proxies_SpineTop, q=True, ws=True, rp=True)
        SpineCenterPos = cmds.xform(self.SpineCurveTop + ".cv[0]", q=True, ws=True, t=True)

        # Cluster
        self.SpineCurve_BtmClstr = self.SpineCurve + "_Btm_Cluster"
        self.SpineCurve_TopClstr = self.SpineCurve + "_Top_Cluster"
        self.SpineCurveTop_BtmClstr = self.SpineCurveTop + "_Btm_Cluster"
        self.SpineCurveTop_TopClstr = self.SpineCurveTop + "_Top_Cluster"

        self.SpineCurve_BtmClstrGRP = self.SpineCurve_BtmClstr + "_GRP"
        self.SpineCurve_MidClstrGRP = self.name + "_Spine_Spline_Mid_Cluster_GRP"
        self.SpineCurveTop_TopClstrGRP = self.SpineCurveTop_TopClstr + "_GRP"

        # BTM
        cmds.select(self.SpineCurve + ".cv[0:1]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurve_BtmClstr)
        cmds.group(self.SpineCurve_BtmClstr, n=self.SpineCurve_BtmClstrGRP)
        cmds.xform(os=True, piv=[splineStartPos[0], splineStartPos[1], splineStartPos[2]])
        cmds.parentConstraint(self.MainHipControl, self.SpineCurve_BtmClstrGRP, mo=True)

        # Mid
        cmds.select(self.SpineCurve + ".cv[2:3]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurve_TopClstr)
        cmds.select(self.SpineCurveTop + ".cv[0:1]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurveTop_BtmClstr)
        cmds.group(self.SpineCurve_TopClstr, self.SpineCurveTop_BtmClstr, n=self.SpineCurve_MidClstrGRP)
        cmds.xform(os=True, piv=[SpineCenterPos[0], SpineCenterPos[1], SpineCenterPos[2]])
        cmds.parentConstraint(self.SpineMid_IKCtr, self.SpineCurve_MidClstrGRP)

        # Top
        cmds.select(self.SpineCurveTop + ".cv[2:3]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurveTop_TopClstr)
        cmds.group(self.SpineCurveTop_TopClstr, n=self.SpineCurveTop_TopClstrGRP)
        cmds.xform(os=True, piv=[splineEndPos[0], splineEndPos[1], splineEndPos[2]])
        cmds.parentConstraint(self.SpineTop_IKCtr, self.SpineCurveTop_TopClstrGRP)

        # Vis
        cmds.setAttr(self.SpineCurve_BtmClstr + ".v", 0)
        cmds.setAttr(self.SpineCurve_TopClstr + ".v", 0)
        cmds.setAttr(self.SpineCurveTop_BtmClstr + ".v", 0)
        cmds.setAttr(self.SpineCurveTop_TopClstr + ".v", 0)
        # endregion

        # region Create Spine Control
        self.SpineCurve_Ctr = self.name + "_SpineCurve_01Ctr"
        mel.eval("curve -d 1 -p -4 0 0 -p 4 0 0 -k 0 -k 1 -n " + self.SpineCurve_Ctr + ";")
        cmds.pickWalk(d="down")
        cmds.rename(self.SpineCurve_Ctr + "Shape")
        mel.eval("circle -c 5 0 0 -nr 0 1 0 -ch 0 -n " + self.SpineCurve_Ctr + "2" + ";")
        mel.eval("circle -c -5 0 0 -nr 0 1 0 -ch 0 -n " + self.SpineCurve_Ctr + "3" + ";")
        cmds.parent(self.SpineCurve_Ctr + "2Shape", self.SpineCurve_Ctr + "3Shape", self.SpineCurve_Ctr, r=True, s=True)
        cmds.delete(self.SpineCurve_Ctr + "2", self.SpineCurve_Ctr + "3")
        cmds.setAttr(self.SpineCurve_Ctr + ".scale", 1.25, 1.25, 1.25)
        cmds.makeIdentity(self.SpineCurve_Ctr, apply=True, s=1)

        cmds.setAttr(self.SpineCurve_Ctr + "Shape.overrideEnabled", 1)
        cmds.setAttr(self.SpineCurve_Ctr + "2Shape.overrideEnabled", 1)
        cmds.setAttr(self.SpineCurve_Ctr + "3Shape.overrideEnabled", 1)
        cmds.setAttr(self.SpineCurve_Ctr + "Shape.overrideColor", 27)
        cmds.setAttr(self.SpineCurve_Ctr + "2Shape.overrideColor", 27)
        cmds.setAttr(self.SpineCurve_Ctr + "3Shape.overrideColor", 27)
        # endregion

        # region Spine Control Joint
        self.SpineCurve_TopIK_JNT = self.name + "_SpineCurve_TopIK_JNT"
        self.SpineCurve_BtmIK_JNT = self.name + "_SpineCurve_BtmIK_JNT"
        self.SpineCurve_MidIK_JNT = self.name + "_SpineCurve_MidIK_JNT"

        cmds.select(cl=True)
        cmds.joint(n=self.SpineCurve_TopIK_JNT, p=(0, 2, 0))
        cmds.setAttr(self.SpineCurve_TopIK_JNT + ".radius", 0.5)
        cmds.select(cl=True)
        cmds.joint(n=self.SpineCurve_BtmIK_JNT, p=(0, -2, 0))
        cmds.setAttr(self.SpineCurve_BtmIK_JNT + ".radius", 0.5)
        cmds.select(cl=True)
        cmds.joint(n=self.SpineCurve_MidIK_JNT, p=(0, 0, 0))
        cmds.setAttr(self.SpineCurve_MidIK_JNT + ".radius", 0.5)
        self.RibbonSKinCluster = self.name + "_Spine_RibbonSkinCluster"
        cmds.select(self.Spine_Ribbon, self.SpineCurve_TopIK_JNT, self.SpineCurve_BtmIK_JNT, self.SpineCurve_MidIK_JNT)
        cmds.skinCluster(n=self.RibbonSKinCluster, toSelectedBones=True, ignoreHierarchy=True, mi=3, dr=1, rui=True,
                         bindMethod=0)
        bindPose = cmds.listConnections(self.RibbonSKinCluster, destination=False, source=True, t="dagPose")
        cmds.delete(bindPose)

        self.Spine_Ribbon_GRP = self.name + "_Ribbon_GRP"
        cmds.group(self.SpineCurve_TopIK_JNT, self.SpineCurve_BtmIK_JNT, self.SpineCurve_MidIK_JNT,
                   n=self.Spine_Ribbon_GRP)
        Spine_Length = cmds.xform(self.SpineEnd_Loc, q=True, t=True)
        cmds.setAttr(self.Spine_Ribbon_GRP + ".scale", Spine_Length[1] / 4, Spine_Length[1] / 4, Spine_Length[1] / 4)
        cmds.delete(self.SpineEnd_Loc)
        # CONNECT TO RIG
        cmds.pointConstraint(self.SpineTop_IKCtr, self.SpineCurve_TopIK_JNT)
        cmds.orientConstraint(self.SpineTop_IKCtr, self.SpineTop_FKCtr, self.SpineCurve_TopIK_JNT)
        cmds.parentConstraint(self.SpineMid_IKCtr, self.SpineCurve_MidIK_JNT)
        cmds.pointConstraint(self.MainHipControl, self.SpineCurve_BtmIK_JNT)
        cmds.orientConstraint(self.MainHipControl, self.RootControl, self.SpineCurve_BtmIK_JNT)
        # endregion

        # region Curve for spine length
        SpineRoot_Pos = cmds.xform(self.RootControl, q=True, ws=True, t=True)
        SpineMid_IKJ_Pos = cmds.xform(self.SpineCurve_MidIK_JNT, q=True, ws=True, t=True)
        SpineTop_Pos = cmds.xform(self.SpineCurve_TopIK_JNT, q=True, ws=True, t=True)
        self.SpineCurveLengthCX = self.name + "_SpineCurve_LengthCX"
        mel.eval(
            "curve -n " + self.SpineCurveLengthCX + " -d 3 -p " + str(SpineRoot_Pos[0]) + " " + str(
                SpineRoot_Pos[1]) + " " +
            str(SpineRoot_Pos[2]) + " " +
            "-p " + str((SpineMid_IKJ_Pos[0] - SpineRoot_Pos[0]) / 3.4 + SpineRoot_Pos[0]) + " " +
            str((SpineMid_IKJ_Pos[1] - SpineRoot_Pos[1]) / 3.4 + SpineRoot_Pos[1]) + " " +
            str((SpineMid_IKJ_Pos[2] - SpineRoot_Pos[2]) / 3.4 + SpineRoot_Pos[2]) + " " +

            "-p " + str((SpineMid_IKJ_Pos[0] - SpineRoot_Pos[0]) / 1.35 + SpineRoot_Pos[0]) + " " +
            str((SpineMid_IKJ_Pos[1] - SpineRoot_Pos[1]) / 1.35 + SpineRoot_Pos[1]) + " " +
            str((SpineMid_IKJ_Pos[2] - SpineRoot_Pos[2]) / 1.35 + SpineRoot_Pos[2]) + " " +

            "-p " + str((SpineTop_Pos[0] - SpineMid_IKJ_Pos[0]) / 3.7 + SpineMid_IKJ_Pos[0]) + " " +
            str((SpineTop_Pos[1] - SpineMid_IKJ_Pos[1]) / 3.7 + SpineMid_IKJ_Pos[1]) + " " +
            str((SpineTop_Pos[2] - SpineMid_IKJ_Pos[2]) / 3.7 + SpineMid_IKJ_Pos[2]) + " " +

            "-p " + str((SpineTop_Pos[0] - SpineMid_IKJ_Pos[0]) / 1.4 + SpineMid_IKJ_Pos[0]) + " " +
            str((SpineTop_Pos[1] - SpineMid_IKJ_Pos[1]) / 1.4 + SpineMid_IKJ_Pos[1]) + " " +
            str((SpineTop_Pos[2] - SpineMid_IKJ_Pos[2]) / 1.4 + SpineMid_IKJ_Pos[2]) + " " +

            "-p " + str(SpineTop_Pos[0]) + " " + str(SpineTop_Pos[1]) + " " + str(SpineTop_Pos[2]) + " " +
            "-k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 3 -k 3;")
        cmds.pickWalk(d="down")
        cmds.rename(self.SpineCurveLengthCX + "Shape")
        cmds.select(self.SpineCurveLengthCX)
        cmds.arclen(ch=1)
        curveInfoNode = cmds.listConnections(self.SpineCurveLengthCX + "Shape", t="curveInfo", d=1, s=0)
        self.SpineCurve_LengthInfo = self.name + "_SpineCurve_LengthInfo"
        cmds.rename(curveInfoNode[0], self.SpineCurve_LengthInfo)

        self.SpineCurveLengthCX_Cluster01 = self.SpineCurveLengthCX + "_Cluster01"
        self.SpineCurveLengthCX_Cluster02 = self.SpineCurveLengthCX + "_Cluster02"
        self.SpineCurveLengthCX_Cluster03 = self.SpineCurveLengthCX + "_Cluster03"
        self.SpineCurveLengthCX_Cluster01_GRP = self.SpineCurveLengthCX_Cluster01 + "_GRP"
        self.SpineCurveLengthCX_Cluster02_GRP = self.SpineCurveLengthCX_Cluster02 + "_GRP"
        self.SpineCurveLengthCX_Cluster03_GRP = self.SpineCurveLengthCX_Cluster03 + "_GRP"
        cmds.select(self.SpineCurveLengthCX + ".cv[0:1]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurveLengthCX_Cluster01)
        cmds.select(self.SpineCurveLengthCX + ".cv[2:3]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurveLengthCX_Cluster02)
        cmds.select(self.SpineCurveLengthCX + ".cv[4:5]")
        cmds.cluster(envelope=1)
        cmds.rename(self.SpineCurveLengthCX_Cluster03)

        cmds.connectAttr(self.MainHipControl + ".matrix", self.SpineCurveLengthCX_Cluster01 + "Shape.weightedNode")
        cmds.setAttr(self.SpineCurveLengthCX_Cluster01 + "Cluster.relative", 0)
        cmds.group(em=True, n=self.SpineCurveLengthCX_Cluster01_GRP)
        Pcon = cmds.parentConstraint(self.MainHipControl, self.SpineCurveLengthCX_Cluster01_GRP)
        cmds.delete(Pcon)
        cmds.parent(self.SpineCurveLengthCX_Cluster01, self.SpineCurveLengthCX_Cluster01_GRP)
        cmds.parent(self.SpineCurveLengthCX_Cluster01_GRP, self.MainHipControl)
        cmds.setAttr(self.SpineCurveLengthCX_Cluster01 + ".v", 0)

        cmds.connectAttr(self.SpineMid_IKCtr + ".matrix", self.SpineCurveLengthCX_Cluster02 + "Shape.weightedNode")
        cmds.setAttr(self.SpineCurveLengthCX_Cluster02 + "Cluster.relative", 0)
        cmds.group(em=True, n=self.SpineCurveLengthCX_Cluster02_GRP)
        Pcon = cmds.parentConstraint(self.SpineMid_IKCtr, self.SpineCurveLengthCX_Cluster02_GRP)
        cmds.delete(Pcon)
        cmds.parent(self.SpineCurveLengthCX_Cluster02, self.SpineCurveLengthCX_Cluster02_GRP)
        cmds.parent(self.SpineCurveLengthCX_Cluster02_GRP, self.SpineMid_IKCtr)
        cmds.setAttr(self.SpineCurveLengthCX_Cluster02 + ".v", 0)

        cmds.connectAttr(self.SpineTop_FKCtr + ".matrix", self.SpineCurveLengthCX_Cluster03 + "Shape.weightedNode")
        cmds.setAttr(self.SpineCurveLengthCX_Cluster03 + "Cluster.relative", 0)
        cmds.group(em=True, n=self.SpineCurveLengthCX_Cluster03_GRP)
        Pcon = cmds.parentConstraint(self.SpineTop_FKCtr, self.SpineCurveLengthCX_Cluster03_GRP)
        cmds.delete(Pcon)

        cmds.parent(self.SpineCurveLengthCX_Cluster03, self.SpineCurveLengthCX_Cluster03_GRP)
        cmds.parent(self.SpineCurveLengthCX_Cluster03_GRP, self.SpineTop_IKCtr)
        cmds.setAttr(self.SpineCurveLengthCX_Cluster03 + ".v", 0)

        self.Spine_BtmTX_Loc = self.name + "_Spine_BtmTX_loc"
        cmds.spaceLocator(n=self.Spine_BtmTX_Loc, p=(0, 0, 0))
        cmds.parent(self.Spine_BtmTX_Loc, self.MainControl)
        cmds.pointConstraint(self.SpineMid_IKCtr, self.Spine_BtmTX_Loc)
        self.Spine_TopTX_Loc = self.name + "_Spine_TopTX_loc"
        cmds.spaceLocator(n=self.Spine_TopTX_Loc, p=(0, 0, 0))
        cmds.parent(self.Spine_TopTX_Loc, self.SpineTop_IKCtr)
        cmds.pointConstraint(self.SpineMid_IKCtr, self.Spine_TopTX_Loc)

        # SET DRIVEN KEY
        cmds.setDrivenKeyframe(self.Spine_RibbonClusterGRPs[0] + ".scaleY",
                               currentDriver=self.SpineMid_IKCtr + ".translateX")
        cmds.setDrivenKeyframe(self.Spine_RibbonClusterGRPs[1] + ".scaleY",
                               currentDriver=self.SpineMid_IKCtr + ".translateX")

        cmds.setAttr(self.SpineMid_IKCtr + ".translateX", -4)
        cmds.setAttr(self.Spine_RibbonClusterGRPs[0] + ".scaleY", 0.8)
        cmds.setAttr(self.Spine_RibbonClusterGRPs[1] + ".scaleY", 1.2)

        cmds.setDrivenKeyframe(self.Spine_RibbonClusterGRPs[0] + ".scaleY",
                               currentDriver=self.SpineMid_IKCtr + ".translateX")
        cmds.setDrivenKeyframe(self.Spine_RibbonClusterGRPs[1] + ".scaleY",
                               currentDriver=self.SpineMid_IKCtr + ".translateX")

        cmds.setAttr(self.SpineMid_IKCtr + ".translateX", 4)
        cmds.setAttr(self.Spine_RibbonClusterGRPs[0] + ".scaleY", 1.2)
        cmds.setAttr(self.Spine_RibbonClusterGRPs[1] + ".scaleY", 0.8)

        cmds.setDrivenKeyframe(self.Spine_RibbonClusterGRPs[0] + ".scaleY",
                               currentDriver=self.SpineMid_IKCtr + ".translateX")
        cmds.setDrivenKeyframe(self.Spine_RibbonClusterGRPs[1] + ".scaleY",
                               currentDriver=self.SpineMid_IKCtr + ".translateX")

        cmds.setAttr(self.SpineMid_IKCtr + ".translateX", 0)
        cmds.setAttr(self.Spine_RibbonClusterGRPs[0] + ".scaleY", 1)
        cmds.setAttr(self.Spine_RibbonClusterGRPs[1] + ".scaleY", 1)

        cmds.selectKey(self.Spine_RibbonClusterGRPs[0] + "_scaleY", self.Spine_RibbonClusterGRPs[1] + "_scaleY", k=True)
        cmds.keyTangent(itt="spline", ott="spline")

        self.SpineMid_IKCtr_Btm_Loc = self.name + "_SpineMid_IKCtr_BtmLoc"
        self.SpineMid_IKCtr_Top_Loc = self.name + "_SpineMid_IKCtr_TopLoc"
        self.SpineMid_IKCtr_Btm_Loc_GRP = self.SpineMid_IKCtr_Btm_Loc + "_GRP"
        self.SpineMid_IKCtr_Top_Loc_GRP = self.SpineMid_IKCtr_Top_Loc + "_GRP"
        cmds.spaceLocator(n=self.SpineMid_IKCtr_Btm_Loc)
        cmds.group(self.SpineMid_IKCtr_Btm_Loc, n=self.SpineMid_IKCtr_Btm_Loc_GRP)
        cmds.spaceLocator(n=self.SpineMid_IKCtr_Top_Loc)
        cmds.group(self.SpineMid_IKCtr_Top_Loc, n=self.SpineMid_IKCtr_Top_Loc_GRP)
        Ocon = cmds.orientConstraint(self.SpineMid_IKCtr_GRPs[0], self.SpineMid_IKCtr_Btm_Loc_GRP)
        cmds.delete(Ocon)
        Ocon = cmds.orientConstraint(self.SpineMid_IKCtr_GRPs[0], self.SpineMid_IKCtr_Top_Loc_GRP)
        cmds.delete(Ocon)
        cmds.parent(self.SpineMid_IKCtr_Btm_Loc_GRP, self.MainHipControlGRP)
        cmds.parent(self.SpineMid_IKCtr_Top_Loc_GRP, self.SpineTop_IKCtr_GRPs[0])
        Pcon = cmds.pointConstraint(self.MainHipControl, self.SpineMid_IKCtr_Btm_Loc_GRP)
        cmds.delete(Pcon)
        Pcon = cmds.pointConstraint(self.SpineTop_IKCtr, self.SpineMid_IKCtr_Top_Loc_GRP)
        cmds.delete(Pcon)
        cmds.makeIdentity(self.SpineMid_IKCtr_Btm_Loc_GRP, self.SpineMid_IKCtr_Top_Loc_GRP, apply=True, t=1)
        cmds.pointConstraint(self.MainHipControl, self.SpineMid_IKCtr_Btm_Loc)
        cmds.pointConstraint(self.SpineTop_IKCtr, self.SpineMid_IKCtr_Top_Loc)
        cmds.setAttr(self.SpineMid_IKCtr_Btm_Loc_GRP + ".v", 0)
        cmds.setAttr(self.SpineMid_IKCtr_Top_Loc_GRP + ".v", 0)
        # endregion

        # region CONNECT
        self.SpineMidTranslate_BlendNode = self.name + "_SpineMidTranslate_BlendNode"
        cmds.shadingNode("blendColors", n=self.SpineMidTranslate_BlendNode, asUtility=True)
        cmds.connectAttr(self.SpineMid_IKCtr_Top_Loc + ".translate", self.SpineMidTranslate_BlendNode + ".color1")
        cmds.connectAttr(self.SpineMid_IKCtr_Btm_Loc + ".translate", self.SpineMidTranslate_BlendNode + ".color2")
        cmds.connectAttr(self.SpineMidTranslate_BlendNode + ".output", self.SpineMid_IKCtr_GRPs[1] + ".translate")

        self.SpineMidAimLoc = self.name + "_Spine_MidAimLoc"
        self.SpineMidTargetLoc = self.name + "_Spine_MidTargetLoc"
        self.SpineMidTargetLoc_GRP = self.SpineMidTargetLoc + "_GRP"
        cmds.spaceLocator(n=self.SpineMidAimLoc)
        cmds.spaceLocator(n=self.SpineMidTargetLoc)
        cmds.group(self.SpineMidTargetLoc, n=self.SpineMidTargetLoc_GRP)
        cmds.xform(os=True, piv=(0, 0, 0))
        Pcon = cmds.parentConstraint(self.SpineTop_IKCtr, self.SpineMidTargetLoc_GRP)
        cmds.delete(Pcon)
        cmds.parent(self.SpineMidAimLoc, self.SpineMidTargetLoc_GRP, self.RootControl)
        Pcon = cmds.pointConstraint(self.MainHipControl, self.SpineMidAimLoc)
        cmds.delete(Pcon)
        Pcon = cmds.pointConstraint(self.SpineTop_IKCtr, self.SpineMidTargetLoc)
        cmds.delete(Pcon)
        cmds.makeIdentity(self.SpineMidAimLoc, self.SpineMidTargetLoc, apply=True, t=1, r=1, s=1)
        cmds.setAttr(self.SpineMidAimLoc + ".v", 0)
        cmds.setAttr(self.SpineMidTargetLoc + ".v", 0)

        cmds.connectAttr(self.MainHipControl + ".translate", self.SpineMidAimLoc + ".translate", f=True)
        cmds.connectAttr(self.SpineTop_IKCtr + ".translate", self.SpineMidTargetLoc + ".translate", f=True)
        cmds.aimConstraint(self.SpineMidTargetLoc, self.SpineMidAimLoc, mo=True, weight=1, aimVector=[0, 1, 0],
                           upVector=[0, 1, 0], worldUpType="none", skip="y")
        cmds.connectAttr(self.SpineMidAimLoc + ".rotateX", self.SpineMid_IKCtr_GRPs[1] + ".rotateX")
        cmds.connectAttr(self.SpineMidAimLoc + ".rotateZ", self.SpineMid_IKCtr_GRPs[1] + ".rotateZ")

        self.SpineMid_IKCtr_GRP_BlendNode = self.name + "_SpineMid_IKCtr_GRP_BlendNode"
        cmds.shadingNode("blendColors", n=self.SpineMid_IKCtr_GRP_BlendNode, asUtility=True)
        cmds.connectAttr(self.SpineTop_IKCtr + ".rotate", self.SpineMid_IKCtr_GRP_BlendNode + ".color1", f=True)
        cmds.connectAttr(self.MainHipControl + ".rotate", self.SpineMid_IKCtr_GRP_BlendNode + ".color1", f=True)
        cmds.connectAttr(self.SpineMid_IKCtr_GRP_BlendNode + ".outputG", self.SpineMid_IKCtr_GRPs[1] + ".rotateY",
                         f=True)

        cmds.addAttr(self.SpineMid_IKCtr, ln="SpineLenght", at="double")
        cmds.setAttr(self.SpineMid_IKCtr + ".SpineLenght", e=True, channelBox=True)
        cmds.addAttr(self.MainHipControl, ln="SpineLenght", at="double")
        cmds.setAttr(self.MainHipControl + ".SpineLenght", e=True, channelBox=True)
        cmds.addAttr(self.SpineTop_IKCtr, ln="SpineLenght", at="double")
        cmds.setAttr(self.SpineTop_IKCtr + ".SpineLenght", e=True, channelBox=True)

        self.SpineLength_MDNode = self.name + "_SpineLength_MDNode"
        cmds.shadingNode("multiplyDivide", n=self.SpineLength_MDNode, asUtility=True)
        cmds.setAttr(self.SpineLength_MDNode + ".operation", 2)
        Spine_Length[0] = cmds.getAttr(self.SpineCurve_LengthInfo + ".arcLength")
        cmds.setAttr(self.SpineLength_MDNode + ".input2X", Spine_Length[0])
        cmds.connectAttr(self.SpineCurve_LengthInfo + ".arcLength", self.SpineLength_MDNode + ".input1X", f=True)

        self.SpineLengthCXomp_MDNode = self.name + "_SpineLengthCXomp_MDNode"
        cmds.shadingNode("multiplyDivide", n=self.SpineLengthCXomp_MDNode, asUtility=True)
        cmds.setAttr(self.SpineLengthCXomp_MDNode + ".operation", 2)
        cmds.connectAttr(self.SpineLength_MDNode + ".outputX", self.SpineLengthCXomp_MDNode + ".input1X", f=True)
        cmds.connectAttr(self.MainControl + ".scaleY", self.SpineLengthCXomp_MDNode + ".input2X")

        cmds.connectAttr(self.SpineLengthCXomp_MDNode + ".outputX", self.SpineMid_IKCtr + ".SpineLenght", f=True)
        cmds.connectAttr(self.SpineLengthCXomp_MDNode + ".outputX", self.MainHipControl + ".SpineLenght", f=True)
        cmds.connectAttr(self.SpineLengthCXomp_MDNode + ".outputX", self.SpineTop_IKCtr + ".SpineLenght", f=True)

        self.ExtraNodes = self.name + "_ExtraNodes"
        if cmds.objExists(self.ExtraNodes) is not None:
            cmds.group(em=True, n=self.ExtraNodes)
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.setAttr(self.ExtraNodes + ".inheritsTransform", 0)

        cmds.parent(self.SpineCurveLengthCX, self.Spine_Ribbon, self.Spine_RibbonBlend, self.Spine_RibbonClusters,
                    self.SpineCurveLocList, self.ExtraNodes)

        cmds.setAttr(self.Spine_Ribbon + ".v", 0)
        cmds.setAttr(self.Spine_RibbonBlend + ".v", 0)
        cmds.setAttr(self.Spine_RibbonClusters[0] + ".v", 0)
        cmds.setAttr(self.Spine_RibbonClusters[1] + ".v", 0)
        cmds.setAttr(self.Spine_BtmTX_Loc + ".v", 0)
        cmds.setAttr(self.Spine_TopTX_Loc + ".v", 0)
        cmds.setAttr(self.SpineCurve_BtmIK_JNT + ".v", 0)
        cmds.setAttr(self.SpineCurve_MidIK_JNT + ".v", 0)
        cmds.setAttr(self.SpineCurveLengthCX + ".template", 0)
        cmds.setAttr(self.SpineCurve + ".v", 0)
        cmds.setAttr(self.SpineCurveTop + ".v", 0)

        self.SpineCurve_Ctr_GRP = self.SpineCurve_Ctr + "_GRP"
        cmds.group(self.SpineCurve_Ctr, n=self.SpineCurve_Ctr_GRP)
        print(self.ProxyData.Proxies_SpineList[0])
        Pcon = cmds.pointConstraint(self.ProxyData.Proxies_SpineList[0],self.SpineCurve_Ctr_GRP)
        cmds.delete(Pcon)

        # endregion
        pass

    def RibbonCluster(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        cmds.select(self.Spine_RibbonBlend + ".cv[%s][*]" % (1 - sideindex))
        cmds.cluster(envelope=1)
        cmds.rename(self.Spine_RibbonClusters[sideindex])
        cmds.move(0, 0, 0, self.Spine_RibbonClusters[sideindex] + ".scalePivot",
                  self.Spine_RibbonClusters[sideindex] + ".rotatePivot")

        pass

    def AlignPointPos(self, sou, tar):
        con = cmds.pointConstraint(sou, tar)
        cmds.delete(con)
        pass
