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


class BipedRigging:
    def __init__(self, Creator=None):
        self.ControllerTool = CT
        self.RiggingTool = RT
        print("BipedRigging")
        print(Creator.TorsoChainNames)
        # self.Rigger = LegRigging.LegRigging(ResJNT=self.creator.LegChainNames)
        # self.Rigger.MainProcess()
        # self.Rigger = TorsoRigging.TorsoRigging(ResJNT=self.creator.TorsoChainNames)
        pass
