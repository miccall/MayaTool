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


class BipedArmatureCreator:
    def __init__(self, ProxyCreator):
        self.name = "Mic"
        self.Creator = ProxyCreator
        self.InitData()
        pass

    def InitData(self):
        self.Proxy_Clavicle = self.Creator.Proxies_Clavicles
        self.Proxy_Shoulder = self.Creator.Proxies_Shoulders
        self.Proxy_Wrist = self.Creator.Proxies_Wrists
        self.Proxy_Palm = self.Creator.Proxies_Palms
        self.Proxy_Hip = self.Creator.Proxies_Hips
        self.Proxy_Ankle = self.Creator.Proxies_Ankles
        self.Proxy_Elbow = self.Creator.Proxies_Elbows
        self.Proxy_Knee = self.Creator.Proxies_Knees
        self.Proxy_Ball = self.Creator.Proxies_Balls
        self.Proxy_Toe = self.Creator.Proxies_Toes

        self.RootJointTemp = "%s_SpineTemp01_JNT" % self.name
        self.RootJoint = "%s_Root_JNT" % self.name
        self.SpineTopJoint = "%s_SpineTop_JNT" % self.name
        self.NeckJointTemp = "%s_NeckTemp01_JNT" % self.name
        self.HeadJoint = "%s_Head_JNT" % self.name
        self.HeadTipJoint = "%s_HeadTip_JNT" % self.name
        self.JawJoint = "%s_Jaw_JNT" % self.name
        self.JawTipJoint = "%s_JawTip_JNT" % self.name
        self.EyeJoints = []
        self.Joint_Clavicles = []
        self.Joint_Shoulders = []
        self.Joint_Wrists = []
        self.Joint_WristDummys = []
        self.Joint_Palms = []
        self.Joint_Forearms = []
        self.Joint_Hips = []
        self.Joint_Ankles = []
        self.Joint_Elbows = []
        self.Joint_Knees = []
        self.Joint_Balls = []
        self.Joint_Toes = []
        self.InitDataSide("L")
        self.InitDataSide("R")

        pass

    def InitDataSide(self, side):
        Eye = self.name + "_" + side + "_Eye_JNT"
        self.EyeJoints.append(Eye)

        ClavicleJoint = self.name + "_" + side + "_Clavicle_JNT"
        self.Joint_Clavicles.append(ClavicleJoint)

        ShoulderJoint = self.name + "_" + side + "_Shoulder_JNT"
        self.Joint_Shoulders.append(ShoulderJoint)

        ElbowJoint = self.name + "_" + side + "_Elbow_JNT"
        self.Joint_Elbows.append(ElbowJoint)

        WristJoint = self.name + "_" + side + "_Wrist_JNT"
        self.Joint_Wrists.append(WristJoint)

        WristDummyJoint = self.name + "_" + side + "_WristDummy_JNT"
        self.Joint_WristDummys.append(WristDummyJoint)

        Palm = self.name + "_" + side + "_Palm_JNT"
        self.Joint_Palms.append(Palm)

        Forearm = self.name + "_" + side + "_Forearm_JNT"
        self.Joint_Forearms.append(Forearm)

        HipJoint = self.name + "_" + side + "_Hip_JNT"
        self.Joint_Hips.append(HipJoint)

        KneeJoint = self.name + "_" + side + "_Knee_JNT"
        self.Joint_Knees.append(KneeJoint)

        AnkleJoint = self.name + "_" + side + "_Ankle_JNT"
        self.Joint_Ankles.append(AnkleJoint)

        BallJoint = self.name + "_" + side + "_Ball_JNT"
        self.Joint_Balls.append(BallJoint)

        ToeJoint = self.name + "_" + side + "_Toe_JNT"
        self.Joint_Toes.append(ToeJoint)
        pass

    def MainProcessing(self):
        # Create torso Joints Chain
        cmds.select(cl=True)
        cmds.joint(n=self.RootJoint)
        self.AlignPointPos(self.Creator.Proxies_Root, self.RootJoint)
        cmds.select(self.RootJoint)
        cmds.joint(n=self.RootJointTemp)
        self.AlignPointPos(self.Creator.Proxies_SpineList[0], self.RootJointTemp)
        self.SpineJointList = [self.RootJointTemp]
        Proxy_spineJoints = self.Creator.Proxies_SpineList
        i = 1
        while i < len(Proxy_spineJoints):
            cmds.select(self.SpineJointList[i - 1])
            SpineTemp = "_SpineTemp0"
            JointSuffix = "_JNT"
            spineName = self.name + SpineTemp + str(i + 1) + JointSuffix
            cmds.joint(n=spineName)
            self.AlignPointPos(Proxy_spineJoints[i], spineName)
            cmds.select(spineName)
            self.SpineJointList.append(spineName)
            i += 1
        cmds.select(self.SpineJointList[-1])
        cmds.joint(n=self.SpineTopJoint)
        # cmds.pointConstraint(self.Creator.Proxies_SpineTop, self.SpineTopJoint)
        self.AlignPointPos(self.Creator.Proxies_SpineTop, self.SpineTopJoint)

        # Create Neck Joints Chain
        # todo : only once neck
        cmds.select(self.SpineTopJoint)
        cmds.joint(n=self.NeckJointTemp)
        self.AlignPointPos(self.Creator.Proxies_NeckList[0], self.NeckJointTemp)

        # Head
        cmds.select(self.NeckJointTemp)
        cmds.joint(n=self.HeadJoint)
        self.AlignPointPos(self.Creator.Proxies_Head, self.HeadJoint)
        # _HeadTip

        cmds.select(self.HeadJoint)
        cmds.joint(n=self.HeadTipJoint)
        self.AlignPointPos(self.Creator.Proxies_HeadTip, self.HeadTipJoint)
        # Jaw
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.JawJoint)
        self.AlignPointPos(self.Creator.Proxies_Jaw, self.JawJoint)
        # JawTip
        cmds.select(self.HeadJoint)
        cmds.joint(n=self.JawTipJoint)
        self.AlignPointPos(self.Creator.Proxies_JawTip, self.JawTipJoint)

        # other
        self.ArmatueSide("L")
        self.ArmatueSide("R")

        # Orient
        cmds.joint(self.RootJoint, e=True, oj="none", secondaryAxisOrient="yup", zso=True)
        cmds.joint(self.SpineJointList, e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        cmds.joint(self.SpineTopJoint, e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        cmds.joint(self.NeckJointTemp, e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        cmds.joint(self.HeadJoint, e=True, oj="xyz", secondaryAxisOrient="zdown", zso=True)
        cmds.joint(self.HeadTipJoint, e=True, oj="none", secondaryAxisOrient="yup", zso=True)
        self.OrientJoints("L")
        self.OrientJoints("R")
        pass

    def ArmatueSide(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        cmds.select(self.HeadJoint)
        cmds.joint(n=self.EyeJoints[sideindex])
        self.AlignPointPos(self.Creator.Proxies_Eyes[sideindex], self.EyeJoints[sideindex])

        # Arm
        self.ArmatureArm(side)

        # Leg
        self.ArmatureLeg(side)
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
        ClavicleJoint = self.Joint_Clavicles[sideindex]
        cmds.joint(n=ClavicleJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Clavicle[sideindex], ClavicleJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Shoulder[sideindex], ClavicleJoint, aimVector=[1 * sign, 0, 0],
                                  upVector=[0, 1 * sign, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0],
                                  worldUpObject=self.Proxy_Clavicle[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(ClavicleJoint, apply=True, r=1)

        # ShoulderJoint
        cmds.select(ClavicleJoint)
        ShoulderJoint = self.Joint_Shoulders[sideindex]
        cmds.joint(n=ShoulderJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Shoulder[sideindex], ShoulderJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Elbow[sideindex], ShoulderJoint, aimVector=[1 * sign, 0, 0],
                                  upVector=[0, 1 * sign, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0],
                                  worldUpObject=self.Proxy_Shoulder[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(ClavicleJoint, apply=True, r=1)

        # ElbowJoint
        cmds.select(ShoulderJoint)
        ElbowJoint = self.Joint_Elbows[sideindex]
        cmds.joint(n=ElbowJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Elbow[sideindex], ElbowJoint)
        cmds.delete(Pcon)
        Acon = cmds.aimConstraint(self.Proxy_Wrist[sideindex], ElbowJoint, aimVector=[1 * sign, 0, 0],
                                  upVector=[0, 1 * sign, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0],
                                  worldUpObject=self.Proxy_Elbow[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(ClavicleJoint, apply=True, r=1)

        # WristJoint
        cmds.select(ElbowJoint)
        WristJoint = self.Joint_Wrists[sideindex]
        cmds.joint(n=WristJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Wrist[sideindex], WristJoint)
        cmds.delete(Pcon)
        cmds.select(ElbowJoint)
        WristDummyJoint = self.Joint_WristDummys[sideindex]
        cmds.joint(n=WristDummyJoint)
        Pcon = cmds.parentConstraint(self.Proxy_Wrist[sideindex], WristDummyJoint)
        cmds.delete(Pcon)
        if side == "R":
            cmds.rotate(180, 0, 0, WristJoint, WristDummyJoint, r=True, os=True)
        cmds.makeIdentity(WristJoint, WristDummyJoint, apply=True, r=1)

        # Thumb
        cmds.select(cl=True)
        cmds.select("Proxies_" + side + "_Thumb??")
        ThumbList = cmds.ls(sl=True, objectsOnly=True)
        count = len(ThumbList)
        tips = "Proxies_" + side + "_ThumbJTip"
        ThumbList.append(tips)
        ThumbJNT_list = []
        cmds.select(cl=True)
        for i in range(0, count + 1):
            if i > 0:
                cmds.select(ThumbJNT_list[i - 1])
            namesp = ThumbList[i].split("_")
            newName = self.name + "_" + side + "_" + namesp[2] + "_JNT"
            cmds.joint(n=newName)
            ThumbJNT_list.append(newName)
            Pcon = cmds.parentConstraint(ThumbList[i], newName)
            cmds.delete(Pcon)
        cmds.parent(ThumbJNT_list[0], WristJoint)
        cmds.parent(WristJoint, w=True)

        # Hand
        cmds.select(cl=True)
        cmds.select("Proxies_" + side + "_Finger_*_J1")
        FingerList = cmds.ls(sl=True, objectsOnly=True)
        FingersFirstJointList = []
        for Finger in FingerList:
            cmds.select(Finger)
            name = Finger[0:-1]
            cmds.select(name + "?")
            jointlist = cmds.ls(sl=True)
            tip = name + "Tip"
            jointlist.append(tip)
            cmds.select(WristJoint)
            i = 0
            FinList = []
            for jo in jointlist:
                namesp = jo.split("_")  # Proxies_L_Finger_1_J1
                newName = self.name + "_" + side + "_" + namesp[2] + namesp[3] + namesp[4] + "_JNT"
                if i > 0:
                    cmds.select(FinList[i - 1])
                else:
                    FingersFirstJointList.append(newName)
                cmds.joint(n=newName)
                Pcon = cmds.parentConstraint(jointlist[i], newName)
                cmds.delete(Pcon)
                FinList.append(newName)
                i += 1

        # Palm
        cmds.select(WristJoint)
        Palm = self.Joint_Palms[sideindex]
        cmds.joint(n=Palm)
        Pcon = cmds.parentConstraint(self.Proxy_Palm[sideindex], Palm)
        cmds.delete(Pcon)
        if side == "R":
            cmds.rotate(180, 0, 0, Palm, r=True, os=True)
        cmds.makeIdentity(Palm, apply=True, r=1)
        for Finger in FingersFirstJointList:
            cmds.parent(Finger, Palm)

        # Forearm
        cmds.select(cl=True)
        Forearm = self.Joint_Forearms[sideindex]
        cmds.joint(n=Forearm)
        Pcon = cmds.parentConstraint(WristJoint, ElbowJoint, Forearm)
        cmds.delete(Pcon)
        cmds.parent(Forearm, ElbowJoint)
        if side == "R":
            cmds.rotate(180, 0, 0, Forearm, r=True, os=True)
        cmds.makeIdentity(Forearm, apply=True, r=1)
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
        HipJoint = self.Joint_Hips[sideindex]
        cmds.joint(n=HipJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Hip[sideindex], HipJoint)
        cmds.delete(Pcon)

        # KneeJoint
        cmds.select(HipJoint)
        KneeJoint = self.Joint_Knees[sideindex]
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
        AnkleJoint = self.Joint_Ankles[sideindex]
        cmds.joint(n=AnkleJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Ankle[sideindex], AnkleJoint)
        cmds.delete(Pcon)
        # Ball
        cmds.select(AnkleJoint)
        BallJoint = self.Joint_Balls[sideindex]
        cmds.joint(n=BallJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Ball[sideindex], BallJoint)
        cmds.delete(Pcon)
        # Toe
        cmds.select(BallJoint)
        ToeJoint = self.Joint_Toes[sideindex]
        cmds.joint(n=ToeJoint)
        Pcon = cmds.pointConstraint(self.Proxy_Toe[sideindex], ToeJoint)
        cmds.delete(Pcon)
        pass

    def AlignPointPos(self, sou, tar):
        con = cmds.pointConstraint(sou, tar)
        cmds.delete(con)
        pass

    def OrientJoints(self, side):
        sign = 1
        sideindex = 0
        if side == "L":
            sign = 1
            sideindex = 0
        else:
            sign = -1
            sideindex = 1

        HipJoint = self.Joint_Hips[sideindex]
        KneeJoint = self.Joint_Knees[sideindex]
        AnkleJoint = self.Joint_Ankles[sideindex]
        ForearmJoint = self.Joint_Forearms[sideindex]
        WristJoint = self.Joint_Wrists[sideindex]
        WristDummyJoint = self.Joint_WristDummys[sideindex]
        ToeJoint = self.Joint_Toes[sideindex]
        Clavicle = self.Joint_Clavicles[sideindex]

        # HipJoint
        cmds.parent(KneeJoint, w=True)
        Acon = cmds.aimConstraint(self.Proxy_Knee[sideindex], HipJoint, aimVector=[1, 0, 0],
                                  upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 0, 1],
                                  worldUpObject=self.Proxy_Knee[sideindex])
        cmds.delete(Acon)
        cmds.makeIdentity(HipJoint, apply=True, r=1)
        cmds.parent(KneeJoint, HipJoint)

        KneeLength = cmds.xform(KneeJoint, q=True, t=True)
        AnkleLength = cmds.xform(AnkleJoint, q=True, t=True)
        cmds.select(AnkleJoint)
        cmds.joint(e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)

        # FOREARM
        cmds.setAttr("%s.jointOrient" % ForearmJoint, 0, 0, 0)

        # Thumb
        cmds.select("Mic_" + side + "_ThumbJ?_JNT")
        ThumbJNT_list = cmds.ls(sl=True)
        for thumb in ThumbJNT_list:
            cmds.select(thumb)
            cmds.joint(e=True, oj="xzy", secondaryAxisOrient="xdown", ch=True, zso=True)

        # FIX WRIST ORIENTATIONS
        Ocon = cmds.orientConstraint(WristJoint, WristDummyJoint)
        cmds.delete(Ocon)
        cmds.makeIdentity(WristDummyJoint, apply=True, t=1, r=1, s=1)

        # Toe
        cmds.select(ToeJoint)
        cmds.joint(e=True, oj="none", ch=True, zso=True)
        cmds.rotate(0, 90, 0, ToeJoint)
        cmds.makeIdentity(HipJoint, apply=True, r=1)
        cmds.select(cl=True)

        # Fix right side
        if side == "R":
            Clavicle_R_Orient = cmds.getAttr("%s.jointOrient" % Clavicle)
            Hip_R_Orient = cmds.getAttr("%s.jointOrient" % HipJoint)
            cmds.setAttr("%s.jointOrientX" % HipJoint, Hip_R_Orient[0][0] * -1)
            cmds.setAttr("%s.jointOrientY" % HipJoint, Hip_R_Orient[0][1] * -1)
            cmds.setAttr("%s.jointOrientZ" % HipJoint, Hip_R_Orient[0][2] + 180)

            cmds.select(KneeJoint, hi=True)
            reOrientJoints = cmds.ls(sl=True)
            for currentJoint in reOrientJoints:
                currentOrient = cmds.getAttr(currentJoint + ".jointOrient")
                currentPos = cmds.getAttr(currentJoint + ".tx")
                cmds.setAttr("%s.jointOrientX" % currentJoint, currentOrient[0][0] * -1)
                cmds.setAttr("%s.jointOrientY" % currentJoint, currentOrient[0][1] * -1)
                cmds.setAttr("%s.tx" % currentJoint, currentPos * -1)

        pass
