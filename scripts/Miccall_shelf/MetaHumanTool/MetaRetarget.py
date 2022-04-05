# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
import maya.api.OpenMaya as om

mayaveersion = cmds.about(version=True)
try:
    import PySide2.QtCore as qc
    import PySide2.QtGui as qg
    import PySide2.QtWidgets as qw
    from shiboken2 import wrapInstance
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
except ImportError:
    pm.error('Maya Version Lowed')

dialog = None


class MetaRetarget:
    def __init__(self, *args, **kwargs):
        if mayaveersion == 2022:
            super(MetaRetarget, self).__init__(*args, **kwargs)
        else:
            super(MetaRetarget, self).__init__(*args, **kwargs)

    def Processing(self):
        pass

    pass


class MetaNewBuild:
    def __init__(self, *args, **kwargs):
        if mayaveersion == 2022:
            super(MetaNewBuild, self).__init__(*args, **kwargs)
        else:
            super(MetaNewBuild, self).__init__(*args, **kwargs)

    def move_constraint(self):
        pass

    def RigLogic(self):
        pass

    pass


class MetaRetarget_GUI(MayaQWidgetDockableMixin, qw.QDialog):
    def __init__(self, *args, **kwargs):
        if mayaveersion == 2022:
            super(MetaRetarget_GUI, self).__init__(*args, **kwargs)
        else:
            super(MetaRetarget_GUI, self).__init__(*args, **kwargs)
        self.setSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)
        self.setWindowTitle('miccall Meta Retarget')
        self.DisplayUI()

    def DisplayUI(self):
        self.resize(340, 50)
        self.layout = qw.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        self.Processing_Bt = qw.QPushButton("Processing")
        self.layout.addWidget(self.Processing_Bt)
        self.Processing_Bt.clicked.connect(self.CreateBiped_Func)

        pass

    def CreateBiped_Func(self):
        print("processing")
        pass


def create(docked=True):
    global dialog
    if dialog is None:
        dialog = MetaRetarget_GUI()
        dialog.show(dockable=docked, floating=False)
    pass


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
    pass
