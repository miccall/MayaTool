import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import sys


class ControllerTool:
    @staticmethod
    def pole_vector_Ctrl():
        mel.eval(
            "curve -d 1 -p 0 0.5 0 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p 0 0.5 0 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p 0 0.5 0 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -n \"Pyramid Ctrl\";")
        pass

    @staticmethod
    def threedarrow(name):
        mel.eval(
            "curve -d 1 -p 3 0 0 -p 1 0 -2 -p 1 0 -1 -p -3 0 -1 -p -3 0 1 -p 1 0 1 -p 1 0 2 -p 3 0 0 -p 1 -2 0 -p 1 -1 0 -p -3 -1 0 -p -3 1 0 -p 1 1 0 -p 1 2 0 -p 3 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -n \"%s\";" % name)

    @staticmethod
    def IKControl(name, foot, toe):
        footpos = cmds.xform(foot, q=1, ws=1, rp=1)
        toepos = cmds.xform(toe, q=1, ws=1, rp=1)
        P0 = (2.2955459058998002, -0.07778272499630601, -2.2290949811170773)
        P1 = (0.0, -0.0777745393120915, -3.8159323126431275)
        P2 = (-3.721760705381633, -0.07776750706946273, -2.5127781638489397)
        P3 = (0.10898923590368947, -0.07777453931209143, 5.652038763689961)
        P4 = (-4.778513457825949, -0.07777453931209138, 11.563637300716303)
        P5 = (-0.15685207893522635, -0.07777453931209136, 15.927335226266813)
        P6 = (3.6242324071984866, -0.07778312706102215, 11.995044438076901)
        P7 = (2.4120734093259717, -0.07777453931209143, 5.685210104217603)
        lis = [P0, P1, P2, P3, P4, P5, P6, P7]
        cur = cmds.circle(nr=(0, 1, 0), sw=360)
        for i in range(0, 8):
            cmds.select("%s.cv[%s]" % (cur[0], i))
            ppx = lis[i][0]
            ppy = lis[i][1]
            ppz = lis[i][2]
            cmds.move(ppx, ppy, ppz, r=True)
        cmds.select(cur[0])
        # todo : use foot toe size to calulate Curve
        cmds.move(footpos[0], 0, footpos[2], a=True)
        cmds.scale(2, 2, 2, r=True)
        cmds.makeIdentity(cur[0], apply=True, t=1, r=1, s=1)
        cmds.move(footpos[0], footpos[1], footpos[2], cur[0] + ".scalePivot", cur[0] + ".rotatePivot", absolute=True)
        cmds.rename(cur[0], name)
        pass
