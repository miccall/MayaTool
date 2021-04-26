import pymel.core as pm
import importlib

try:
    import PySide2.QtCore as qc
    import PySide2.QtGui as qg
    import PySide2.QtWidgets as qw
    from shiboken2 import wrapInstance
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
except ImportError:
    pm.error('Maya Version Lowed')

from .Biped import Create

importlib.reload(Create)
from .Biped.LegRigging import LegRigging

dialog = None


class AutoRigging_GUI(MayaQWidgetDockableMixin, qw.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)
        self.setWindowTitle('miccall Auto Rigging')
        self.DisplayUI()

    def DisplayUI(self):
        self.resize(250, 200)
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
        pass


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
