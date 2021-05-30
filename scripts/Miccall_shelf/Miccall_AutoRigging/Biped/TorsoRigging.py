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
