# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm

mayaveersion = cmds.about(version=True)
try:
    import PySide2.QtCore as qc
    import PySide2.QtGui as qg
    import PySide2.QtWidgets as qw
    from shiboken2 import wrapInstance
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
except ImportError:
    pm.error('Maya Version Lowed')

if mayaveersion == "2022":
    import importlib
else:
    pass

dialog = None

class AnimTools:
    def __init__(self):
        self.name = "Bony"
        self.KneeIKCs = ["_lKneeIKC","_rKneeIKC"]
        self.LegSwitchCs = ["_lLegSwitchC","_rLegSwitchC"]
        self.ToeIKCs = ["_lToeIKC","_rToeIKC"]
        self.FootIKCs = ["_lFootIKC","_rFootIKC"]

        self.ClavicleCs = ["_lClavicleC","_rClavicleC"]
        self.ShoulderFKCs = ["_lShoulderFKC","_rShoulderFKC"]
        self.ElbowFKCs = ["_lElbowFKC","_rElbowFKC"]
        self.WristFKCs = ["_lWristFKC","_rWristFKC"]

        self.PalmCs = ["_lPalmC","_rPalmC"]
        self.ThumbJ1Cs = ["_lThumbJ1C","_rThumbJ1C"]
        self.ThumbJ2Cs = ["_lThumbJ2C","_rThumbJ2C"]
        self.ThumbJ3Cs = ["_lThumbJ3C","_rThumbJ3C"]
        self.Finger1J1Cs = ["_lFinger1J1C", "_rFinger1J1C"]
        self.Finger1J2Cs = ["_lFinger1J2C", "_rFinger1J2C"]
        self.Finger1J3Cs = ["_lFinger1J3C", "_rFinger1J3C"]
        self.Finger2J1Cs = ["_lFinger2J1C", "_rFinger2J1C"]
        self.Finger2J2Cs = ["_lFinger2J2C", "_rFinger2J2C"]
        self.Finger2J2Cs = ["_lFinger2J3C", "_rFinger2J3C"]
        pass

    def GetLegData(self):
        selectFoot = cmds.ls(sl=True)
        side = selectFoot[0]
        self.currentGetDataSide = side[5]
        if self.currentGetDataSide == "l":
            sideindex = 0
        else:
            sideindex = 1
        # getData
        self.KneeIKC_tx = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".tx")
        self.KneeIKC_ty = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".ty")
        self.KneeIKC_tz = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".tz")
        self.KneeIKC_Follow = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".Follow")
        self.LegSwitchCs_Switch = cmds.getAttr(self.name + self.LegSwitchCs[sideindex] + ".SwitchIkFk")
        self.ToeIKC_rx = cmds.getAttr(self.name + self.ToeIKCs[sideindex] + ".rx")
        self.ToeIKC_ry = cmds.getAttr(self.name + self.ToeIKCs[sideindex] + ".ry")
        self.ToeIKC_rz = cmds.getAttr(self.name + self.ToeIKCs[sideindex] + ".rz")
        self.FootIKC_tx = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".tx")
        self.FootIKC_ty = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".ty")
        self.FootIKC_tz = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".tz")
        self.FootIKC_rx = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".rx")
        self.FootIKC_ry = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".ry")
        self.FootIKC_rz =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".rz")
        self.FootIKC_Stretch =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".Stretch")
        self.FootIKC_KneeLock =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".KneeLock")
        self.FootIKC_footTilt =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".footTilt")
        self.FootIKC_heelBall =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".heelBall")
        self.FootIKC_toeUpDn =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".toeUpDn")
        self.FootIKC_ballSwivel =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".ballSwivel")
        pass

    def GetArmData(self):
        selectArm = cmds.ls(sl=True)
        side = selectArm[0]
        self.currentGetDataSide = side[5]
        if self.currentGetDataSide == "l":
            sideindex = 0
        else:
            sideindex = 1

        self.Clavicle_rx = cmds.getAttr(self.name + self.ClavicleCs[sideindex] + ".rx")
        self.Clavicle_ry = cmds.getAttr(self.name + self.ClavicleCs[sideindex] + ".ry")
        self.Clavicle_rz = cmds.getAttr(self.name + self.ClavicleCs[sideindex] + ".rz")
        self.Shoulder_rx = cmds.getAttr(self.name + self.ShoulderFKCs[sideindex] + ".rx")
        self.Shoulder_ry = cmds.getAttr(self.name + self.ShoulderFKCs[sideindex] + ".ry")
        self.Shoulder_rz = cmds.getAttr(self.name + self.ShoulderFKCs[sideindex] + ".rz")
        self.Shoulder_Orient = cmds.getAttr(self.name + self.ShoulderFKCs[sideindex] + ".ShoulderOrient")
        self.ELbow_ry = cmds.getAttr(self.name + self.ElbowFKCs[sideindex] + ".ry")
        self.Wrist_rx = cmds.getAttr(self.name + self.WristFKCs[sideindex] + ".rx")
        self.Wrist_ry = cmds.getAttr(self.name + self.WristFKCs[sideindex] + ".ry")
        self.Wrist_rz = cmds.getAttr(self.name + self.WristFKCs[sideindex] + ".rz")


        pass

    def setLegMirrorData(self):
        if self.currentGetDataSide == "l":
            mirrorsideindex = 1
        else:
            mirrorsideindex = 0
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".tx" , self.KneeIKC_tx * -1 )
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".ty" , self.KneeIKC_ty)
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".tz" , self.KneeIKC_tz)
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".Follow" , self.KneeIKC_Follow)
        cmds.setAttr(self.name + self.LegSwitchCs[mirrorsideindex] + ".SwitchIkFk" , self.LegSwitchCs_Switch )
        cmds.setAttr(self.name + self.ToeIKCs[mirrorsideindex] + ".rx" , self.ToeIKC_rx )
        cmds.setAttr(self.name + self.ToeIKCs[mirrorsideindex] + ".ry" , self.ToeIKC_ry )
        cmds.setAttr(self.name + self.ToeIKCs[mirrorsideindex] + ".rz" , self.ToeIKC_rz )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".tx" , self.FootIKC_tx * -1 )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".ty" , self.FootIKC_ty * -1 )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".tz" , self.FootIKC_tz * -1 )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".rx" , self.FootIKC_rx )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".ry" , self.FootIKC_ry)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".rz" , self.FootIKC_rz)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".Stretch" , self.FootIKC_Stretch )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".KneeLock" , self.FootIKC_KneeLock)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".footTilt"  , self.FootIKC_footTilt)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".heelBall", self.FootIKC_heelBall)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".toeUpDn", self.FootIKC_toeUpDn)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".ballSwivel", self.FootIKC_ballSwivel)
        pass

    def setArmMirrorData(self):
        if self.currentGetDataSide == "l":
            mirrorsideindex = 1
        else:
            mirrorsideindex = 0

        cmds.setAttr(self.name + self.ClavicleCs[mirrorsideindex] + ".rx" , self.Clavicle_rx)
        cmds.setAttr(self.name + self.ClavicleCs[mirrorsideindex] + ".ry" , self.Clavicle_ry)
        cmds.setAttr(self.name + self.ClavicleCs[mirrorsideindex] + ".rz" , self.Clavicle_rz)
        cmds.setAttr(self.name + self.ShoulderFKCs[mirrorsideindex] + ".rx" , self.Shoulder_rx)
        cmds.setAttr(self.name + self.ShoulderFKCs[mirrorsideindex] + ".ry" , self.Shoulder_ry)
        cmds.setAttr(self.name + self.ShoulderFKCs[mirrorsideindex] + ".rz" , self.Shoulder_rz)
        cmds.setAttr(self.name + self.ShoulderFKCs[mirrorsideindex] + ".ShoulderOrient", self.Shoulder_Orient)
        cmds.setAttr(self.name + self.ElbowFKCs[mirrorsideindex] + ".ry" , self.ELbow_ry)
        cmds.setAttr(self.name + self.WristFKCs[mirrorsideindex] + ".rx" , self.Wrist_rx)
        cmds.setAttr(self.name + self.WristFKCs[mirrorsideindex] + ".ry" , self.Wrist_ry)
        cmds.setAttr(self.name + self.WristFKCs[mirrorsideindex] + ".rz" , self.Wrist_rz)
        pass

    def MirrorLeg(self,side="l"):
        if side == "l":
            sideindex = 0
            mirrorsideindex = 1
        else:
            sideindex = 1
            mirrorsideindex = 0
        # getData
        KneeIKC_tx = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".tx")
        KneeIKC_ty = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".ty")
        KneeIKC_tz = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".tz")
        KneeIKC_Follow = cmds.getAttr(self.name + self.KneeIKCs[sideindex] + ".Follow")
        LegSwitchCs_Switch = cmds.getAttr(self.name + self.LegSwitchCs[sideindex] + ".SwitchIkFk")
        ToeIKC_rx = cmds.getAttr(self.name + self.ToeIKCs[sideindex] + ".rx")
        ToeIKC_ry = cmds.getAttr(self.name + self.ToeIKCs[sideindex] + ".ry")
        ToeIKC_rz = cmds.getAttr(self.name + self.ToeIKCs[sideindex] + ".rz")
        FootIKC_tx = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".tx")
        FootIKC_ty = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".ty")
        FootIKC_tz = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".tz")
        FootIKC_rx = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".rx")
        FootIKC_ry = cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".ry")
        FootIKC_rz =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".rz")
        FootIKC_Stretch =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".Stretch")
        FootIKC_KneeLock =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".KneeLock")
        FootIKC_footTilt =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".footTilt")
        FootIKC_heelBall =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".heelBall")
        FootIKC_toeUpDn =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".toeUpDn")
        FootIKC_ballSwivel =cmds.getAttr(self.name + self.FootIKCs[sideindex] + ".ballSwivel")
        """
        # set mirror Data
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".tx" , KneeIKC_tx * -1 )
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".ty" , KneeIKC_ty)
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".tz" , KneeIKC_tz)
        cmds.setAttr(self.name + self.KneeIKCs[mirrorsideindex] + ".Follow" , KneeIKC_Follow)
        cmds.setAttr(self.name + self.LegSwitchCs[mirrorsideindex] + ".SwitchIkFk" , LegSwitchCs_Switch )
        cmds.setAttr(self.name + self.ToeIKCs[mirrorsideindex] + ".rx" , ToeIKC_rx )
        cmds.setAttr(self.name + self.ToeIKCs[mirrorsideindex] + ".ry" , ToeIKC_ry )
        cmds.setAttr(self.name + self.ToeIKCs[mirrorsideindex] + ".rz" , ToeIKC_rz )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".tx" , FootIKC_tx * -1 )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".ty" , FootIKC_ty * -1 )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".tz" , FootIKC_tz * -1 )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".rx" , FootIKC_rx )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".ry" , FootIKC_ry)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".rz" , FootIKC_rz)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".Stretch" , FootIKC_Stretch )
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".KneeLock" , FootIKC_KneeLock)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".footTilt"  , FootIKC_footTilt)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".heelBall", FootIKC_heelBall)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".toeUpDn", FootIKC_toeUpDn)
        cmds.setAttr(self.name + self.FootIKCs[mirrorsideindex] + ".ballSwivel", FootIKC_ballSwivel)
        """
        pass


# noinspection PyArgumentList
class AnimTools_GUI(MayaQWidgetDockableMixin, qw.QDialog):
    def __init__(self, *args, **kwargs):
        if mayaveersion == 2022:
            super().__init__(*args, **kwargs)
        else:
            super(AnimTools_GUI, self).__init__(*args, **kwargs)
        self.animTool = AnimTools()
        self.setSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)
        self.setWindowTitle('miccall Anim Tools')
        self.DisplayUI()

    def DisplayUI(self):
        self.resize(340, 50)
        self.layout = qw.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        self.Arm_Lb = qw.QLabel("Arm")
        self.layout.addWidget(self.Arm_Lb)

        self.GetArmData_bt = qw.QPushButton("Arm data")
        self.layout.addWidget(self.GetArmData_bt)
        self.GetArmData_bt.clicked.connect(self.GetArmData_Func)

        self.MirrorArm_Bt = qw.QPushButton("Mirror Arm")
        self.layout.addWidget(self.MirrorArm_Bt)
        self.MirrorArm_Bt.clicked.connect(self.MirrorArm_Func)

        self.Leg_Lb = qw.QLabel("Leg")
        self.layout.addWidget(self.Leg_Lb)

        self.GetLegData_bt = qw.QPushButton("Leg data")
        self.layout.addWidget(self.GetLegData_bt)
        self.GetLegData_bt.clicked.connect(self.GetLegData_Func)

        self.MirrorLeg_Bt = qw.QPushButton("Mirror Leg")
        self.layout.addWidget(self.MirrorLeg_Bt)
        self.MirrorLeg_Bt.clicked.connect(self.MirrorLeg_Func)
        self.layout.addStretch(0)

    def MirrorLeg_Func(self):
        self.animTool.setLegMirrorData()
        pass

    def GetLegData_Func(self):
        self.animTool.GetLegData()
        pass

    def MirrorArm_Func(self):
        self.animTool.setArmMirrorData()
        pass

    def GetArmData_Func(self):
        self.animTool.GetArmData()
        pass


def create(docked=True):
    global dialog
    if dialog is None:
        dialog = AnimTools_GUI()
        dialog.show(dockable=docked, floating=False)
    pass


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
    pass

