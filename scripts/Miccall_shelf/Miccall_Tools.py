# -*- coding: utf-8 -*-

print("Miccall Tool Load ")
import os
import maya.cmds as cmds
import maya.utils

mayaveersion = cmds.about(version=True)

if mayaveersion == "2022":
    import importlib
    from .shelfBase import shelfBase
else:
    import shelfBase

    reload(shelfBase)


def shelf_show():
    Miccall_Tools()


if mayaveersion == "2022":
    class Miccall_Tools(shelfBase):
        def __init__(self):
            super(Miccall_Tools, self).__init__("Miccall")
            self.labelBackground = (0.1322, 0.3344, 0.0393, 1)
            self.build()

        def reimport(self):
            if mayaveersion == "2022":
                command = '%s\n%s\n%s\n%s' % (
                    'import importlib',
                    'from Miccall_shelf import Miccall_Tools',
                    'importlib.reload(Miccall_Tools)',
                    'Miccall_Tools.shelf_show()')
            else:
                command = '%s\n%s\n%s' % (
                    'from Miccall_shelf import Miccall_Tools',
                    'reload(Miccall_Tools)',
                    'Miccall_Tools.shelf_show()')
            exec(command)

        def refreshShelf(self, *args):
            maya.utils.executeDeferred(self.reimport)

        """
        @staticmethod
        def SpringMagic(*args):
            from AnimTools import SpringMagic
            SpringMagic.delete()
            importlib.reload(SpringMagic)
            SpringMagic.create()
        """

        @staticmethod
        def AutoRigging(*args):
            from .Miccall_AutoRigging import AutoRiggingTools
            AutoRiggingTools.delete()
            importlib.reload(AutoRiggingTools)
            AutoRiggingTools.create()

        @staticmethod
        def AnimTool(*args):
            from Miccall_AnimTool import AnimTools
            AnimTools.delete()
            reload(AnimTools)
            AnimTools.create()

        @staticmethod
        def Test(*args):
            print("...Test")

        @staticmethod
        def MetaHuman(*args):
            from .MetaHumanTool import MetaRetarget
            MetaRetarget.delete()
            importlib.reload(MetaRetarget)
            print("...MetaHuman")
            MetaRetarget.create()

        def build(self):
            # Shelf Common Part
            self.addButon(
                "",
                "refresh_shelf.png",
                command=self.refreshShelf,
                doubleCommand=None,
                annotation_str=u'???????????????')

            self.addSeparator()

            self.addButon(
                "",
                "AutoRigging.png",
                command=self.AutoRigging,
                doubleCommand=None,
                annotation_str=u'AutoRigging')

            self.addButon(
                "",
                "AutoRigging.png",
                command=self.AnimTool,
                doubleCommand=None,
                annotation_str=u'Anim')

            self.addButon(
                "",
                "AutoRigging.png",
                command=self.MetaHuman,
                doubleCommand=None,
                annotation_str=u'MetaHuman')

else:
    class Miccall_Tools(shelfBase.shelfBase):
        def __init__(self):
            super(Miccall_Tools, self).__init__("Miccall")
            self.labelBackground = (0.1322, 0.3344, 0.0393, 1)
            self.build()

        def reimport(self):
            command = '%s\n%s\n%s' % (
                'from Miccall_shelf import Miccall_Tools',
                'reload(Miccall_Tools)',
                'Miccall_Tools.shelf_show()')
            exec(command)

        def refreshShelf(self, *args):
            maya.utils.executeDeferred(self.reimport)

        @staticmethod
        def AutoRigging(*args):
            from Miccall_AutoRigging import AutoRiggingTools
            AutoRiggingTools.delete()
            reload(AutoRiggingTools)
            AutoRiggingTools.create()

        @staticmethod
        def AnimTool(*args):
            from Miccall_AnimTool import AnimTools
            AnimTools.delete()
            reload(AnimTools)
            AnimTools.create()

        @staticmethod
        def Test(*args):
            print("...Test")

        @staticmethod
        def MetaHuman(*args):
            from MetaHumanTool import MetaRetarget
            MetaRetarget.delete()
            reload(MetaRetarget)
            print("...MetaHuman")
            MetaRetarget.create()

        def build(self):
            # Shelf Common Part
            self.addButon(
                "",
                "refresh_shelf.png",
                command=self.refreshShelf,
                doubleCommand=None,
                annotation_str=u'???????????????')

            self.addSeparator()

            self.addButon(
                "",
                "AutoRigging.png",
                command=self.AutoRigging,
                doubleCommand=None,
                annotation_str=u'AutoRigging')

            self.addButon(
                "",
                "AutoRigging.png",
                command=self.AnimTool,
                doubleCommand=None,
                annotation_str=u'Anim')

            self.addButon(
                "",
                "AutoRigging.png",
                command=self.MetaHuman,
                doubleCommand=None,
                annotation_str=u'MetaHuman')
