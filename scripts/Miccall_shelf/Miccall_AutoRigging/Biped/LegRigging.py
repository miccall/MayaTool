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


class LegRigging:
    def __init__(self, ResJNT=None):
        self.ResultJoints = ResJNT
        self.FKJoints = self.CreatChain("FK", False)
        self.IKJoints = self.CreatChain("IK", False)
        self.CalulatePos()
        self.IKControl = self.CreateIKControl()
        self.LegControl = self.CreateLegControl()
        self.isNoFilpKneeEnable = False
        self.isPoleVectorKneeEnable = True
        self.SnappableKneefoPoleVectorKneeEnable = True

    def CreateIKControl(self):
        IKControlName = "Leg_L_IK_Ctr"
        CT.IKControl(IKControlName, self.IKJoints[2], self.IKJoints[4])
        return IKControlName
        pass

    def CreateLegControl(self):
        LegControlName = "Leg_L_Main_Ctr"
        FKIKSwitch = "FK_IK_Blend"
        curveMaker = cmds.circle(nr=(0, 1, 0))
        curve = curveMaker[0]
        cmds.rename(curve, LegControlName)

        # Add FK_IK_Blend Attr
        cmds.addAttr(LegControlName, ln=FKIKSwitch, niceName="IK / FK Blend",
                     attributeType="float", defaultValue=1.0, minValue=0.0, maxValue=1)
        cmds.setAttr("%s.%s" % (LegControlName, FKIKSwitch), keyable=True)

        cmds.setAttr("%s.translateX" % LegControlName, self.EndPos[0])
        cmds.setAttr("%s.translateY" % LegControlName, self.EndPos[1])
        cmds.setAttr("%s.translateZ" % LegControlName, self.EndPos[2] - 5)
        cmds.setAttr("%s.scaleX" % LegControlName, 5)
        cmds.setAttr("%s.scaleY" % LegControlName, 5)
        cmds.setAttr("%s.scaleZ" % LegControlName, 5)
        cmds.parentConstraint(self.ResultJoints[2], LegControlName)
        return LegControlName
        pass

    def CalulatePos(self):
        self.StartPos = cmds.xform(self.IKJoints[0], q=1, ws=1, rp=1)
        self.EndPos = cmds.xform(self.IKJoints[2], q=1, ws=1, rp=1)
        pass

    def CreateIK(self, start, end):
        ikHandleName = cmds.ikHandle(sj=start, ee=end, sol="ikRPsolver")
        cmds.rename(ikHandleName[0], "%s_HDL" % start)
        cmds.rename(ikHandleName[1], "%s_Eff" % start)
        cmds.setAttr("%s_HDL.visibility" % start, 0)
        cmds.setAttr("%s_Eff.visibility" % start, 0)
        cmds.parent("%s_HDL" % start, self.IKControl)
        return "%s_HDL" % start

    def CreatChain(self, Attr, OnlyLeg=False):
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
            newChainName = JointNameSplits[0] + "_" + JointNameSplits[1] + "_%s" % Attr + "_JNT"
            cmds.rename(realnamelist[i], newChainName)
            realnamelist[i] = newChainName
        if OnlyLeg:
            cmds.delete("leftToe_%s_IK_JNT" % Attr)
            cmds.delete("leftBall_%s_IK_JNT" % Attr)
            realnamelist.reverse()
            realnamelist.pop()
            realnamelist.pop()
        realnamelist.reverse()
        return realnamelist

    def MainProcess(self):
        self.IKFKSwitch()
        self.LinkIKFK()
        # Create Leg FK Main
        self.CreateFKControl()
        # Create Leg IK Main
        self.LegIKHandle = self.CreateIK(self.IKJoints[0], self.IKJoints[2])

        # distance
        self.LegDistance = cmds.distanceDimension(sp=self.StartPos, ep=self.EndPos)
        self.LegDistanceObjs = cmds.listConnections(self.LegDistance, destination=False)
        cmds.rename(self.LegDistanceObjs[0], "leftLeg_IK_lengthStart_LOC")
        cmds.rename(self.LegDistanceObjs[1], "leftLeg_IK_lengthEnd_LOC")
        self.LegDistanceObjs[0] = "leftLeg_IK_lengthStart_LOC"
        self.LegDistanceObjs[1] = "leftLeg_IK_lengthEnd_LOC"
        cmds.parent(self.LegDistanceObjs[1], self.IKControl)
        cmds.rename(self.LegDistance, "LegDistance")
        self.LegDistance = "LegDistance"
        LegDistanceParent = cmds.listRelatives("LegDistance", parent=True)
        cmds.rename(LegDistanceParent, "LegDistance_Trans")
        cmds.setAttr("%s.visibility" % "LegDistance_Trans", 0)
        cmds.setAttr("%s.visibility" % self.LegDistanceObjs[1], 0)
        # Create Foot IK
        self.CreateIK(self.IKJoints[2], self.IKJoints[3])
        self.CreateIK(self.IKJoints[3], self.IKJoints[4])

        # Create PoleVector Knee
        self.PvIKHandle = self.LegIKHandle
        self.Build_PV()
        # if self.SnappableKneefoPoleVectorKneeEnable:
        #     self.BuildSnappableKnee()
        # set IK FK visiable switch

        # FK Layer
        FK_LayerName = "L_FK_Ctr_Layer"
        cmds.select("Thigh_L_FK_Ctr")
        cmds.createDisplayLayer(name=FK_LayerName, number=1, nr=True)
        cmds.setAttr("%s.displayType" % FK_LayerName, 0)
        cmds.setAttr("%s.color" % FK_LayerName, 18)
        cmds.setAttr("%s.overrideColorRGB" % FK_LayerName, 0, 0, 0)
        cmds.setAttr("%s.overrideRGBColors" % FK_LayerName, 0)
        # IK Layer
        FK_LayerName = "L_IK_Ctr_Layer"
        cmds.select("Leg_L_IK_Ctr")
        cmds.createDisplayLayer(name=FK_LayerName, number=1, nr=True)
        cmds.setAttr("%s.displayType" % FK_LayerName, 0)
        cmds.setAttr("%s.color" % FK_LayerName, 14)
        cmds.setAttr("%s.overrideColorRGB" % FK_LayerName, 0, 0, 0)
        cmds.setAttr("%s.overrideRGBColors" % FK_LayerName, 0)

        # Controller Visiable
        devNode = cmds.shadingNode("plusMinusAverage", asUtility=True)
        cmds.setAttr("%s.operation" % devNode, 2)
        cmds.setAttr("%s.input1D[0]" % devNode, 1)
        cmds.connectAttr("%s.FK_IK_Blend" % self.LegControl, "%s.input1D[1]" % devNode, f=True)
        # 直接连FK 的 vis
        cmds.connectAttr("%s.FK_IK_Blend" % self.LegControl, "Thigh_L_FK_Ctr.visibility", f=True)
        # dev 连 IK 的 vis
        cmds.connectAttr("%s.output1D" % devNode, "Leg_L_IK_Ctr.visibility", f=True)
        cmds.connectAttr("%s.output1D" % devNode, "%s.visibility" % self.IKJoints[0], f=True)

    def LinkAttr(self, Chain1, chain2, Attr, Control, Control_Attr):
        for i in range(0, len(Chain1)):
            BlendNode = 'Blend_%s_%s_%s' % (Chain1[i], chain2[i], Attr)
            cmds.connectAttr('%s.%s' % (Control, Control_Attr), '%s.blender' % BlendNode, f=True)
        pass

    def BlendColor(self, Chain1, chain2, chain3, Attr):
        BlendNodeList = []
        for i in range(0, len(Chain1)):
            blendColorsNode = cmds.shadingNode('blendColors', asShader=True)
            cmds.connectAttr('%s.%s' % (Chain1[i], Attr), '%s.color1' % blendColorsNode, f=True)
            cmds.connectAttr('%s.%s' % (chain2[i], Attr), '%s.color2' % blendColorsNode, f=True)
            cmds.connectAttr('%s.output' % blendColorsNode, '%s.%s' % (chain3[i], Attr), f=True)
            NewName = 'Blend_%s_%s_%s' % (Chain1[i], chain2[i], Attr)
            cmds.rename(blendColorsNode, NewName)
            BlendNodeList.append(NewName)
        return BlendNodeList

    def Build_PV(self):
        self.polePos = RT.calculate_pole_vector(self.IKJoints[0], self.IKJoints[1], self.IKJoints[2])
        self.leftKnee_Pv_LOC = cmds.spaceLocator()
        self.PVControl = "Knee_Pv_Ctr"
        CT.Pyramid(self.PVControl)
        cmds.rename(self.leftKnee_Pv_LOC, "leftKnee_Pv_LOC")
        self.leftKnee_Pv_LOC = "leftKnee_Pv_LOC"
        cmds.setAttr("%s.translateX" % self.leftKnee_Pv_LOC, self.polePos[0])
        cmds.setAttr("%s.translateY" % self.leftKnee_Pv_LOC, self.polePos[1])
        cmds.setAttr("%s.translateZ" % self.leftKnee_Pv_LOC, self.polePos[2])
        cmds.setAttr("%s.visibility" % self.leftKnee_Pv_LOC, 0)
        cmds.setAttr("%s.translateX" % self.PVControl, self.polePos[0])
        cmds.setAttr("%s.translateY" % self.PVControl, self.polePos[1])
        cmds.setAttr("%s.translateZ" % self.PVControl, self.polePos[2])
        cmds.setAttr("%s.scaleX" % self.PVControl, 8)
        cmds.setAttr("%s.scaleY" % self.PVControl, 8)
        cmds.setAttr("%s.scaleZ" % self.PVControl, 8)
        cmds.setAttr("%s.rotateX" % self.PVControl, 90)
        cmds.makeIdentity("%s" % self.leftKnee_Pv_LOC, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity("%s" % self.PVControl, apply=True, t=1, r=1, s=1, n=0)
        self.polePos = cmds.xform("leftKnee_Pv_LOC", q=1, ws=1, rp=1)
        cmds.poleVectorConstraint('%s' % self.leftKnee_Pv_LOC, self.PvIKHandle)
        cmds.parent(self.leftKnee_Pv_LOC, self.PVControl)
        cmds.parent(self.PVControl, self.IKControl)
        pass

    def Build_NoFlip(self):
        # Create spaceLocator
        leftKnee_noFlip_LOC = cmds.spaceLocator()
        cmds.rename(leftKnee_noFlip_LOC, "leftKnee_noFlip_LOC")
        leftKnee_noFlip_LOC = "leftKnee_noFlip_LOC"
        cmds.setAttr("%s.translateX" % leftKnee_noFlip_LOC, self.EndPos[0] + 30)
        cmds.setAttr("%s.translateY" % leftKnee_noFlip_LOC, self.EndPos[1])
        cmds.setAttr("%s.translateZ" % leftKnee_noFlip_LOC, self.EndPos[2])
        cmds.makeIdentity("%s" % leftKnee_noFlip_LOC, apply=True, t=1, r=1, s=1, n=0)

        # make poleVectorConstraint
        cmds.poleVectorConstraint('%s' % leftKnee_noFlip_LOC, self.NoFlipIKHandle)
        cmds.setAttr("%s.twist" % self.NoFlipIKHandle, 90)

        # follow IKControl
        cmds.parent("%s" % leftKnee_noFlip_LOC, self.IKControl)

        # make twist attr
        cmds.group("%s" % leftKnee_noFlip_LOC, name="noFlip_knee_GRP")
        cmds.move(self.EndPos[0], self.EndPos[1], self.EndPos[2], "%s.scalePivot" % "noFlip_knee_GRP",
                  "%s.rotatePivot" % "noFlip_knee_GRP", absolute=True)

        cmds.addAttr(self.IKControl, ln="Knee_Rotate", niceName="Knee Twist",
                     attributeType="float", defaultValue=0.0)
        cmds.setAttr("%s.Knee_Rotate" % self.IKControl, keyable=True)
        cmds.connectAttr('%s.Knee_Rotate' % self.IKControl, '%s.rotateY' % "noFlip_knee_GRP", f=True)
        pass

    def BuildSnappableKnee(self):
        # distance Thigh_To_Pole
        self.Thigh_To_Pole = cmds.distanceDimension(sp=self.StartPos, ep=self.polePos)
        self.Thigh_To_PoleDistanceObjs = cmds.listConnections(self.Thigh_To_Pole, destination=False)
        cmds.rename(self.Thigh_To_Pole, "Thigh_To_Pole_Distance")
        self.Thigh_To_Pole = "Thigh_To_Pole_Distance"
        Thigh_To_Pole_Distance_Parent = cmds.listRelatives(self.Thigh_To_Pole, parent=True)
        cmds.rename(Thigh_To_Pole_Distance_Parent, "Thigh_To_Pole_Dis_Trans")

        # distance Pole_To_Foot
        self.Pole_To_Foot = cmds.distanceDimension(sp=self.polePos, ep=self.EndPos)
        self.Pole_To_FootDistanceObjs = cmds.listConnections(self.Pole_To_Foot, destination=False)
        cmds.rename(self.Pole_To_Foot, "Pole_To_Foot_Distance")
        self.Pole_To_Foot = "Pole_To_Foot_Distance"
        Pole_To_Foot_Distance_Parent = cmds.listRelatives(self.Pole_To_Foot, parent=True)
        cmds.rename(Pole_To_Foot_Distance_Parent, "Pole_To_Foot_Dis_Trans")

        # Stretch to polyvector
        # todo：修改骨骼链
        if self.isNoFilpKneeEnable:
            # 如果开启的话，是需要放到 pv 的骨骼链
            cmds.connectAttr('%s.%s' % ("distance", self.Thigh_To_Pole), '%s.translateX' % BlendNode, f=True)
            cmds.connectAttr('%s.%s' % ("distance", self.Pole_To_Foot), '%s.translateX' % BlendNode, f=True)
        else:
            # 如果没有开启的话，是放到 ik 的骨骼链
            cmds.connectAttr('%s.%s' % ("distance", self.Thigh_To_Pole), '%s.translateX' % BlendNode, f=True)
            cmds.connectAttr('%s.%s' % ("distance", self.Pole_To_Foot), '%s.translateX' % BlendNode, f=True)
        pass

    def IKFKSwitch(self):
        for i in range(len(self.ResultJoints)):
            self.BlendColorNode(i, "rotate")
            self.BlendColorNode(i, "translate")
        pass

    def BlendColorNode(self, i, ConAttr):
        blendColorsNode = cmds.shadingNode('blendColors', asShader=True)
        cmds.connectAttr('%s.%s' % (self.FKJoints[i], ConAttr), '%s.color1' % blendColorsNode, f=True)
        cmds.connectAttr('%s.%s' % (self.IKJoints[i], ConAttr), '%s.color2' % blendColorsNode, f=True)
        cmds.connectAttr('%s.output' % blendColorsNode, '%s.%s' % (self.ResultJoints[i], ConAttr), f=True)
        cmds.select(blendColorsNode, r=True)
        cmds.rename('Blend_%s_%s_%s' % (self.FKJoints[i], self.IKJoints[i], ConAttr))

    def LinkAttrOnce(self, i, ConAttr):
        BlendNode = 'Blend_%s_%s_%s' % (self.FKJoints[i], self.IKJoints[i], ConAttr)
        cmds.connectAttr('%s.%s' % (self.LegControl, "FK_IK_Blend"), '%s.blender' % BlendNode, f=True)

    def LinkIKFK(self):
        for i in range(len(self.ResultJoints)):
            self.LinkAttrOnce(i, "rotate")
            self.LinkAttrOnce(i, "translate")

    def CreateFKControl(self):
        self.FKControlChains = ["Thigh_L_FK_Ctr", "Shin_L_FK_Ctr", "Foot_L_FK_Ctr", "Ball_L_FK_Ctr"]
        self.FKControlChainScale = [11, 9, 7, 5]
        # 为 0 1 2 创建 Curve
        for i in range(0, len(self.FKControlChains)):
            CT.LegFKControl(self.FKControlChains[i], self.FKControlChainScale[i])
            cmds.select(self.FKControlChains[i] + "Shape")
            cmds.select(self.FKJoints[i], add=True)
            mel.eval("parent -r -s")
            cmds.delete(self.FKControlChains[i])
            cmds.rename(self.FKJoints[i], self.FKControlChains[i])

        # Add for Stretch
        cmds.addAttr(self.FKControlChains[0], ln="Lenght", attributeType="double", defaultValue=1.0, minValue=0.0,
                     maxValue=10.0)
        cmds.setAttr("%s.Lenght" % self.FKControlChains[0], keyable=True)
        cmds.addAttr(self.FKControlChains[1], ln="Lenght", attributeType="double", defaultValue=1.0, minValue=0.0,
                     maxValue=10.0)
        cmds.setAttr("%s.Lenght" % self.FKControlChains[1], keyable=True)

        # setDrivenKeyframe
        cmds.setAttr('%s.Lenght' % self.FKControlChains[0], 1)
        cmds.setDrivenKeyframe('%s.translateX' % self.FKControlChains[1],
                               cd='%s.%s' % (self.FKControlChains[0], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % self.FKControlChains[0], 0)
        cmds.setAttr('%s.translateX' % self.FKControlChains[1], 0)
        cmds.setDrivenKeyframe('%s.translateX' % self.FKControlChains[1],
                               cd='%s.%s' % (self.FKControlChains[0], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % self.FKControlChains[0], 1)
        cmds.setAttr('%s.Lenght' % self.FKControlChains[1], 1)
        cmds.setDrivenKeyframe('%s.translateX' % self.FKControlChains[2],
                               cd='%s.%s' % (self.FKControlChains[1], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % self.FKControlChains[1], 0)
        cmds.setAttr('%s.translateX' % self.FKControlChains[2], 0)
        cmds.setDrivenKeyframe('%s.translateX' % self.FKControlChains[2],
                               cd='%s.%s' % (self.FKControlChains[1], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % self.FKControlChains[1], 1)

        cmds.setInfinity('%s.translateX' % self.FKControlChains[1], postInfinite='cycleRelative')
        cmds.setInfinity('%s.translateX' % self.FKControlChains[2], postInfinite='cycleRelative')

        for i in range(0, len(self.FKControlChains)):
            # lock & hide
            cmds.setAttr("%s.translateX" % self.FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.translateY" % self.FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.translateZ" % self.FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.scaleX" % self.FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.scaleY" % self.FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.scaleZ" % self.FKControlChains[i], lock=True, keyable=False, channelBox=False)
        pass
