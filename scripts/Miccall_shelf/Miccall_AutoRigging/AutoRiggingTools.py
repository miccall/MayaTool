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
    from .Biped import Create

    importlib.reload(Create)
    from .Biped import LegRigging

    importlib.reload(LegRigging)
else:
    from Biped import Create

    reload(Create)
    from Biped import LegRigging

    reload(LegRigging)

dialog = None


class AutoRigging_GUI(MayaQWidgetDockableMixin, qw.QDialog):
    def __init__(self, *args, **kwargs):
        if mayaveersion == 2022:
            super().__init__(*args, **kwargs)
        else:
            super(AutoRigging_GUI, self).__init__(*args, **kwargs)
        self.setSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)
        self.setWindowTitle('miccall Auto Rigging')
        self.DisplayUI()

    def DisplayUI(self):
        self.myScriptJobID = cmds.scriptJob(event=["SelectionChanged", self.TestCallBack])
        self.resize(340, 50)
        self.layout = qw.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        self.CreateBiped_Bt = qw.QPushButton("Create Biped")
        self.layout.addWidget(self.CreateBiped_Bt)
        self.CreateBiped_Bt.clicked.connect(self.CreateBiped_Func)

        self.Test_Bt = qw.QPushButton("Test")
        self.layout.addWidget(self.Test_Bt)
        self.Test_Bt.clicked.connect(self.Test_Func)

        pass

    def CreateBiped_Func(self):
        self.creator = Create.CreateBipedJoints()
        pass

    def Test_Func(self):
        self.Rigger = LegRigging.LegRigging(ResJNT=self.creator.LegChainNames)
        self.Rigger.MainProcess()
        pass

    def TestCallBack(self):
        objs = cmds.ls(sl=True)
        if len(objs) > 0:
            current = objs[0]
            print("%s : ss " % current)

    def closeEvent(self, *args):
        super(MayaDockWindow, self).closeEvent(*args)
        # print("closeEvent")
        self.close()

    def hideEvent(self, *args):
        # print("Close Window")
        cmds.scriptJob(kill=self.myScriptJobID)
        return


def create(docked=True):
    global dialog
    if dialog is None:
        dialog = AutoRigging_GUI()
        dialog.show(dockable=docked, floating=False)
    pass


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
    pass
