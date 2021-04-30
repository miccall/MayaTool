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
    from Biped import LegRigging
    from Biped import TorsoRigging
    reload(ControllerTool)
    reload(RiggingTool)
    reload(LegRigging)
    reload(TorsoRigging)
    from Miccall_shelf.Miccall_AutoRigging.Utility.ControllerTool import ControllerTool as CT
    from Miccall_shelf.Miccall_AutoRigging.Utility.RiggingTool import RiggingTool as RT


class BipedRigging:
    def __init__(self, Creator=None):
        self.ControllerTool = CT
        self.RiggingTool = RT
        self.Creator = Creator
        self.TorsoRig()
        pass

    def LegRig(self):
        Rigger = LegRigging.LegRigging(ResJNT=self.Creator.LegChainNames)
        Rigger.MainProcess()

    def TorsoRig(self):
        Rigger = TorsoRigging.TorsoRigging(ResJNT=self.Creator.TorsoChainNames)
        Rigger.MainProcess()
