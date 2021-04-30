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
        # 原始的骨骼链
        self.ResultJoints = ResJNT
        # 从 thing 到 foot 的 位置
        self.StartPos = cmds.xform(self.ResultJoints[0], q=1, ws=1, rp=1)
        self.EndPos = cmds.xform(self.ResultJoints[2], q=1, ws=1, rp=1)
        # config
        self.isNoFilpKneeEnable = False
        self.isPoleVectorKneeEnable = True
        self.SnappableKneefoPoleVectorKneeEnable = True

    def MainProcess(self):
        # 创建一条 IK 的骨骼链
        self.IKJoints = self.CreatChain("IK", False)
        # 创建一条 FK 的骨骼链
        self.FKJoints = self.CreatChain("FK", False)
        # 创建一个 Base Control
        self.LegControl = self.CreateLegControl()
        # 混合 IK 和 FK
        self.IKFKSwitch()
        self.LinkIKFK()
        # IK 控制器是 一个
        self.IKControl = self.CreateIKControl()
        # FK 控制器是一组
        self.FKControls = self.CreateFKControl()

        # Layer
        self.AddToLayer("Thigh_L_FK_Ctr", 18)
        self.AddToLayer("Leg_L_IK_Ctr", 14)
        self.AddToLayer(self.IKJoints[0], 1)
        self.AddToLayer(self.FKJoints[4], 2)

        # Reverse Foot Roll for IK
        self.BuildFootRollControll()

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
        pass

    def CreatChain(self, Attr, OnlyLeg=False):
        """
            创建腿部的复制骨骼链
            可以只创建腿而不包括脚
        """
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
            # cmds.setAttr("%s.rotateOrder" % newChainName, 3)
            realnamelist[i] = newChainName
        if OnlyLeg:
            cmds.delete("leftToe_%s_IK_JNT" % Attr)
            cmds.delete("leftBall_%s_IK_JNT" % Attr)
            realnamelist.reverse()
            realnamelist.pop()
            realnamelist.pop()
        realnamelist.reverse()
        return realnamelist

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
        cmds.setAttr("%s.tx" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.ty" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.tz" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.rx" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.ry" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.rz" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.sx" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.sy" % LegControlName, keyable=False, channelBox=False, lock=True)
        cmds.setAttr("%s.sz" % LegControlName, keyable=False, channelBox=False, lock=True)
        return LegControlName
        pass

    def CreateIK(self, start, end):
        ikHandleName = cmds.ikHandle(sj=start, ee=end, sol="ikRPsolver")
        cmds.rename(ikHandleName[0], "%s_HDL" % start)
        cmds.rename(ikHandleName[1], "%s_Eff" % start)
        cmds.setAttr("%s_HDL.visibility" % start, 0)
        cmds.setAttr("%s_Eff.visibility" % start, 0)
        cmds.parent("%s_HDL" % start, self.IKControl)
        return "%s_HDL" % start

    def MainProcess2(self):
        # if self.SnappableKneefoPoleVectorKneeEnable:
        #     self.BuildSnappableKnee()
        # set IK FK visiable switch
        pass

    def BuildPoleVector(self):
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
        cmds.setAttr("%s.rx" % self.PVControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ry" % self.PVControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rz" % self.PVControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sx" % self.PVControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % self.PVControl, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % self.PVControl, lock=True, keyable=False, channelBox=False)
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
        FKControlChains = ["Thigh_L_FK_Ctr", "Shin_L_FK_Ctr", "Foot_L_FK_Ctr", "Ball_L_FK_Ctr"]
        FKControlChainScale = [11, 9, 7, 5]
        # 为 0 1 2 创建 Curve
        for i in range(0, len(FKControlChains)):
            CT.LegFKControl(FKControlChains[i], FKControlChainScale[i])
            cmds.select(FKControlChains[i] + "Shape")
            cmds.select(self.FKJoints[i], add=True)
            mel.eval("parent -r -s")
            cmds.delete(FKControlChains[i])
            cmds.rename(self.FKJoints[i], FKControlChains[i])

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

        # Add for Stretch
        cmds.addAttr(FKControlChains[0], ln="Lenght", attributeType="double", defaultValue=1.0, minValue=0.0,
                     maxValue=10.0)
        cmds.setAttr("%s.Lenght" % FKControlChains[0], keyable=True)
        cmds.addAttr(FKControlChains[1], ln="Lenght", attributeType="double", defaultValue=1.0, minValue=0.0,
                     maxValue=10.0)
        cmds.setAttr("%s.Lenght" % FKControlChains[1], keyable=True)

        # setDrivenKeyframe
        cmds.setAttr('%s.Lenght' % FKControlChains[0], 1)
        cmds.setDrivenKeyframe('%s.translateX' % FKControlChains[1],
                               cd='%s.%s' % (FKControlChains[0], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % FKControlChains[0], 0)
        cmds.setAttr('%s.translateX' % FKControlChains[1], 0)
        cmds.setDrivenKeyframe('%s.translateX' % FKControlChains[1],
                               cd='%s.%s' % (FKControlChains[0], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % FKControlChains[0], 1)
        cmds.setAttr('%s.Lenght' % FKControlChains[1], 1)
        cmds.setDrivenKeyframe('%s.translateX' % FKControlChains[2],
                               cd='%s.%s' % (FKControlChains[1], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % FKControlChains[1], 0)
        cmds.setAttr('%s.translateX' % FKControlChains[2], 0)
        cmds.setDrivenKeyframe('%s.translateX' % FKControlChains[2],
                               cd='%s.%s' % (FKControlChains[1], "Lenght"),
                               outTangentType="linear", inTangentType="linear")
        cmds.setAttr('%s.Lenght' % FKControlChains[1], 1)

        cmds.setInfinity('%s.translateX' % FKControlChains[1], postInfinite='cycleRelative')
        cmds.setInfinity('%s.translateX' % FKControlChains[2], postInfinite='cycleRelative')

        for i in range(0, len(FKControlChains)):
            # lock & hide
            cmds.setAttr("%s.translateX" % FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.translateY" % FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.translateZ" % FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.scaleX" % FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.scaleY" % FKControlChains[i], lock=True, keyable=False, channelBox=False)
            cmds.setAttr("%s.scaleZ" % FKControlChains[i], lock=True, keyable=False, channelBox=False)

        return FKControlChains
        pass

    def CreateIKControl(self):
        IKControlName = "Leg_L_IK_Ctr"
        # 控制器
        CT.IKControl(IKControlName, self.IKJoints[2], self.IKJoints[4])
        cmds.setAttr("%s.sx" % IKControlName, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % IKControlName, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % IKControlName, lock=True, keyable=False, channelBox=False)
        self.IKControl = IKControlName
        # IK function
        self.LegIKHandle = self.CreateIK(self.IKJoints[0], self.IKJoints[2])
        # Create Foot IK
        self.FootIKHandle = self.CreateIK(self.IKJoints[2], self.IKJoints[3])
        self.BallIKHandle = self.CreateIK(self.IKJoints[3], self.IKJoints[4])

        # 创建Pole vector
        self.PvIKHandle = self.LegIKHandle
        self.BuildPoleVector()

        return IKControlName
        pass

    def AddToLayer(self, Hierarchy, colorIndex=0):
        # Hierarchy = "Thigh_L_FK_Ctr"
        nameList = Hierarchy.split("_")
        LayerName = nameList[1] + "_" + nameList[2] + "_" + nameList[3] + "_Layer"
        cmds.select(Hierarchy)
        cmds.createDisplayLayer(name=LayerName, number=1, nr=True)
        cmds.setAttr("%s.displayType" % LayerName, 0)
        cmds.setAttr("%s.color" % LayerName, colorIndex)
        cmds.setAttr("%s.overrideColorRGB" % LayerName, 0, 0, 0)
        cmds.setAttr("%s.overrideRGBColors" % LayerName, 0)

    def BuildFootRollControll(self):
        # Add Three Locator
        RollControlLocNames = ["Heel_L_Loc", "Ball_L_Loc", "Toe_L_Loc"]
        # 01
        loc = cmds.spaceLocator(p=(0, 0, 0))
        cmds.rename(loc[0], RollControlLocNames[0])
        Footpos = cmds.xform(self.ResultJoints[2], q=1, ws=1, rp=1)
        cmds.setAttr("%s.tx" % RollControlLocNames[0], Footpos[0])
        cmds.setAttr("%s.ty" % RollControlLocNames[0], 0)
        cmds.setAttr("%s.tz" % RollControlLocNames[0], Footpos[2] - 5)
        # 02
        loc = cmds.spaceLocator(p=(0, 0, 0))
        cmds.rename(loc[0], RollControlLocNames[1])
        Ballpos = cmds.xform(self.ResultJoints[3], q=1, ws=1, rp=1)
        cmds.setAttr("%s.tx" % RollControlLocNames[1], Ballpos[0])
        cmds.setAttr("%s.ty" % RollControlLocNames[1], Ballpos[1])
        cmds.setAttr("%s.tz" % RollControlLocNames[1], Ballpos[2])
        # 03
        loc = cmds.spaceLocator(p=(0, 0, 0))
        cmds.rename(loc[0], RollControlLocNames[2])
        Toepos = cmds.xform(self.ResultJoints[4], q=1, ws=1, rp=1)
        cmds.setAttr("%s.tx" % RollControlLocNames[2], Toepos[0])
        cmds.setAttr("%s.ty" % RollControlLocNames[2], Toepos[1])
        cmds.setAttr("%s.tz" % RollControlLocNames[2], Toepos[2])

        # Adjust Hierarchy
        """
            IKControl
            ├ Heel_L_Loc
            ├─ BallIKHandle
            ├─ Toe_L_Loc
            ├── Ball_L_Loc
            ├─── LegIKHandle
            ├─── FootIKHandle
        """
        cmds.parent(RollControlLocNames[0], self.IKControl)
        cmds.parent(RollControlLocNames[1], RollControlLocNames[2])
        cmds.parent(RollControlLocNames[2], RollControlLocNames[0])
        cmds.parent(self.LegIKHandle, RollControlLocNames[1])
        cmds.parent(self.FootIKHandle, RollControlLocNames[1])
        cmds.parent(self.BallIKHandle, RollControlLocNames[0])

        # Add Attr for Foot Roll Control
        cmds.addAttr(self.IKControl, ln="Roll", niceName="Roll",
                     attributeType="float", defaultValue=0.0)
        cmds.setAttr("%s.%s" % (self.IKControl, "Roll"), keyable=True)

        cmds.addAttr(self.IKControl, ln="BendAngle", niceName="Bend Limite Angle",
                     attributeType="float", defaultValue=45)
        cmds.setAttr("%s.%s" % (self.IKControl, "BendAngle"), keyable=True)

        cmds.addAttr(self.IKControl, ln="StraightAngle", niceName="Toe Straight aAngle",
                     attributeType="float", defaultValue=90)
        cmds.setAttr("%s.%s" % (self.IKControl, "StraightAngle"), keyable=True)

        # Utility calculate
        """
            Name => XXX_XXX
            Variable Name => Name_NodeType
            Node Name == Name_[ L or R ]_NodeType
        """
        Heel_Clamp = cmds.shadingNode("clamp", asUtility=True)
        cmds.rename(Heel_Clamp, "Heel_L_Clamp")
        Heel_Clamp = "Heel_L_Clamp"

        cmds.connectAttr("%s.Roll" % self.IKControl, "%s.inputR" % Heel_Clamp)
        cmds.setAttr("%s.minR" % Heel_Clamp, -70)
        cmds.connectAttr("%s.outputR" % Heel_Clamp, "%s.rx" % RollControlLocNames[0])

        Ball_Zero2Bend_Clamp = cmds.shadingNode("clamp", asUtility=True)
        cmds.rename(Ball_Zero2Bend_Clamp, "Ball_Zero2Bend_Clamp")
        Ball_Zero2Bend_Clamp = "Ball_Zero2Bend_Clamp"

        cmds.connectAttr("%s.Roll" % self.IKControl, "%s.inputR" % Ball_Zero2Bend_Clamp)
        cmds.connectAttr("%s.BendAngle" % self.IKControl, "%s.maxR" % Ball_Zero2Bend_Clamp)

        Ball_02B_PercentRange = cmds.shadingNode("setRange", asUtility=True)
        cmds.rename(Ball_02B_PercentRange, "Ball_02B_PercentRange")
        Ball_02B_PercentRange = "Ball_02B_PercentRange"
        cmds.connectAttr("%s.minR" % Ball_Zero2Bend_Clamp, "%s.oldMinX" % Ball_02B_PercentRange)
        cmds.connectAttr("%s.maxR" % Ball_Zero2Bend_Clamp, "%s.oldMaxX" % Ball_02B_PercentRange)
        cmds.setAttr("%s.minX" % Ball_02B_PercentRange, 0)
        cmds.setAttr("%s.maxX" % Ball_02B_PercentRange, 1)
        cmds.connectAttr("%s.inputR" % Ball_Zero2Bend_Clamp, "%s.valueX" % Ball_02B_PercentRange)

        Foot_InvertPercent = cmds.shadingNode("plusMinusAverage", asUtility=True)
        cmds.rename(Foot_InvertPercent, "Foot_InvertPercent")
        Foot_InvertPercent = "Foot_InvertPercent"
        cmds.setAttr("%s.input1D[0]" % Foot_InvertPercent, 1)
        cmds.setAttr("%s.operation" % Foot_InvertPercent, 2)

        Foot_B2S_Clamp = cmds.shadingNode("clamp", asUtility=True)
        cmds.rename(Foot_B2S_Clamp, "Foot_B2S_Clamp")
        Foot_B2S_Clamp = "Foot_B2S_Clamp"
        cmds.connectAttr("%s.BendAngle" % self.IKControl, "%s.minR" % Foot_B2S_Clamp)
        cmds.connectAttr("%s.StraightAngle" % self.IKControl, "%s.maxR" % Foot_B2S_Clamp)
        cmds.connectAttr("%s.Roll" % self.IKControl, "%s.inputR" % Foot_B2S_Clamp)

        Foot_B2S_PercentRange = cmds.shadingNode("setRange", asUtility=True)
        cmds.rename(Foot_B2S_PercentRange, "Foot_B2S_PercentRange")
        Foot_B2S_PercentRange = "Foot_B2S_PercentRange"
        cmds.connectAttr("%s.minR" % Foot_B2S_Clamp, "%s.oldMinX" % Foot_B2S_PercentRange)
        cmds.connectAttr("%s.maxR" % Foot_B2S_Clamp, "%s.oldMaxX" % Foot_B2S_PercentRange)
        cmds.setAttr("%s.minX" % Foot_B2S_PercentRange, 0)
        cmds.setAttr("%s.maxX" % Foot_B2S_PercentRange, 1)
        cmds.connectAttr("%s.outputR" % Foot_B2S_Clamp, "%s.valueX" % Foot_B2S_PercentRange)
        cmds.connectAttr("%s.outValue.outValueX" % Foot_B2S_PercentRange, "%s.input1D[1]" % Foot_InvertPercent)

        Foot_Roll_Mult = cmds.shadingNode("multiplyDivide", asUtility=True)
        cmds.rename(Foot_Roll_Mult, "Foot_Roll_Mult")
        Foot_Roll_Mult = "Foot_Roll_Mult"
        cmds.connectAttr("%s.outValue.outValueX" % Foot_B2S_PercentRange, "%s.input1X" % Foot_Roll_Mult)
        cmds.connectAttr("%s.inputR" % Foot_B2S_Clamp, "%s.input2X" % Foot_Roll_Mult)
        cmds.connectAttr("%s.outputX" % Foot_Roll_Mult, "%s.rx" % RollControlLocNames[2])

        Ball_percent_Mult = cmds.shadingNode("multiplyDivide", asUtility=True)
        cmds.rename(Ball_percent_Mult, "Ball_percent_Mult")
        Ball_percent_Mult = "Ball_percent_Mult"
        cmds.connectAttr("%s.outValue.outValueX" % Ball_02B_PercentRange, "%s.input1X" % Ball_percent_Mult)
        cmds.connectAttr("%s.output1D" % Foot_InvertPercent, "%s.input2X" % Ball_percent_Mult)

        Ball_Roll_Mult = cmds.shadingNode("multiplyDivide", asUtility=True)
        cmds.rename(Ball_Roll_Mult, "Ball_Roll_Mult")
        Ball_Roll_Mult = "Ball_Roll_Mult"
        cmds.connectAttr("%s.outputX" % Ball_percent_Mult, "%s.input1X" % Ball_Roll_Mult)
        cmds.connectAttr("%s.Roll" % self.IKControl, "%s.input2X" % Ball_Roll_Mult)
        cmds.connectAttr("%s.outputX" % Ball_Roll_Mult, "%s.rx" % RollControlLocNames[1])
