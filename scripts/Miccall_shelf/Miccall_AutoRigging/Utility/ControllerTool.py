# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import sys


def ReSetShapeName(name):
    for shape in cmds.listRelatives(name, s=True, f=True) or []:
        print(shape)
        cmds.rename(shape, "%sShape" % name)


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

    @staticmethod
    def LegFKControl(name, sc=5):
        curve = mel.eval(
            "curve -bezier -d 3 -p 0 0.129616 -1 -p 0 0.129616 -1 -p -1.00471 0.129616 -0.920818 -p -1 0.129616 0 -p -0.995291 0.129616 0.920818 -p -2.98023e-08 0.129616 1 -p -2.98023e-08 0.129616 1 -p -2.98023e-08 0.129616 1 -p -2.98023e-08 -0.129616 1 -p -2.98023e-08 -0.129616 1 -p -2.98023e-08 -0.129616 1 -p -0.99465 -0.129616 0.904438 -p -1 -0.129616 0 -p -1.005351 -0.129616 -0.904438 -p 0 -0.129616 -1 -p 0 -0.129616 -1 -p 0 0.129616 -1 -p 0 0.129616 -1 -p 0 0.129616 -1 -k 0 -k 0 -k 0 -k 1 -k 1 -k 1 -k 2 -k 2 -k 2 -k 3 -k 3 -k 3 -k 4 -k 4 -k 4 -k 5 -k 5 -k 5 -k 6 -k 6 -k 6 ;")
        cmds.bezierCurveToNurbs()
        cmds.rename(curve, name)
        # todo: fix rotate
        cmds.setAttr("%s.rotateY" % name, 90)
        cmds.setAttr("%s.rotateX" % name, 90)
        cmds.setAttr("%s.scaleX" % name, sc)
        cmds.setAttr("%s.scaleY" % name, sc)
        cmds.setAttr("%s.scaleZ" % name, sc)
        cmds.makeIdentity("%s" % name, apply=True, t=1, r=1, s=1, n=0)

    @staticmethod
    def Pyramid(name):
        mel.eval(
            "curve -d 1 -p 0 0.5 0 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p 0 0.5 0 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p 0 0.5 0 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -n  \"%s\";" % name)

    @staticmethod
    def IKFKSwitch(name):
        pass

    @staticmethod
    def BoxControl(name):
        mel.eval("curve -d 1 -p 0.5 0.5 0.5 "
                 "-p -0.5 0.5 0.5 "
                 "-p -0.5 0.5 -0.5 "
                 "-p 0.5 0.5 -0.5 "
                 "-p 0.5 0.5 0.5 "
                 "-p 0.5 -0.5 0.5 "
                 "-p 0.5 -0.5 -0.5 "
                 "-p 0.5 0.5 -0.5 "
                 "-p 0.5 -0.5 -0.5 "
                 "-p -0.5 -0.5 -0.5 "
                 "-p -0.5 0.5 -0.5 "
                 "-p -0.5 -0.5 -0.5 "
                 "-p -0.5 -0.5 0.5 "
                 "-p -0.5 0.5 0.5 "
                 "-p -0.5 -0.5 0.5 "
                 "-p 0.5 -0.5 0.5 "
                 "-k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -n \"%s\";" % name)
        ReSetShapeName(name)

    @staticmethod
    def CircleControl(name):
        mel.eval("circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1 -n  \"%s\";" % name)

    @staticmethod
    def FourArror(name):
        mel.eval(
            "curve -d 1 -p 1 0 -3 -p 2 0 -3 -p 0 0 -5 -p -2 0 -3 -p -1 0 -3 -p -1 0 -1 -p -3 0 -1 -p -3 0 -2 -p -5 0 0 -p -3 0 2 -p -3 0 1 -p -1 0 1 -p -1 0 3 -p -2 0 3 -p 0 0 5 -p 2 0 3 -p 1 0 3 -p 1 0 1 -p 3 0 1 -p 3 0 2 -p 5 0 0 -p 3 0 -2 -p 3 0 -1 -p 1 0 -1 -p 1 0 -3 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -n  \"%s\";" % name)
        ReSetShapeName(name)

    @staticmethod
    def MainControl(name):
        mel.eval("circle -n " + name + " -nr 0 1 0 -sw 360 -r 8 -d 3 -ut 0 -tol 0.01 -s 8 -ch 0;")
        Arrow1 = name + "_Arrow1"
        mel.eval(
            "curve -n " + Arrow1 + " -d 1 -p 3 0 8 -p 3 0 9 -p 5 0 9 -p 0 0 12 -p -5 0 9 -p -3 0 9 -p -3 0 8 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 ;")
        cmds.pickWalk(d="down")
        cmds.rename(Arrow1 + "Shape")
        Outer1 = name + "_Outer1"
        mel.eval("circle -n " + Outer1 + " -nr 0 1 0 -sw 48.9 -r 8.545 -d 3 -ut 0 -tol 0.01 -s 8 -ch 0;")
        cmds.rotate(0, 110.55, 0, Outer1, r=True)
        cmds.duplicate(Arrow1, Outer1, rr=True)
        Arrow2 = name + "_Arrow2"
        Outer2 = name + "_Outer2"
        cmds.rotate(0, 90, 0, Arrow2, Outer1, r=True)
        cmds.duplicate(Arrow1, Outer1, rr=True)
        Arrow3 = name + "_Arrow3"
        Outer3 = name + "_Outer3"
        cmds.rotate(0, 180, 0, Arrow3, Outer1, r=True)
        cmds.duplicate(Arrow1, Outer1, rr=True)
        Arrow4 = name + "_Arrow4"
        Outer4 = name + "_Outer4"
        cmds.rotate(0, 270, 0, Arrow4, Outer4, r=True)
        cmds.makeIdentity(name, Arrow1, Arrow2, Arrow3, Arrow4, Outer1, Outer2, Outer3, Outer4, apply=True,
                          r=1)
        cmds.parent(Arrow1 + "Shape", Arrow2 + "Shape", Arrow3 + "Shape", Arrow4 + "Shape", Outer1 + "Shape",
                    Outer2 + "Shape", Outer3 + "Shape", Outer4 + "Shape", name, r=True, s=True)
        cmds.delete(Arrow1, Arrow2, Arrow3, Arrow4, Outer1, Outer2, Outer3, Outer4)
        cmds.move(0, 0, 2, Arrow1 + "Shape.cv[3]", r=True)
        pass

    @staticmethod
    def HipsControl(name):
        mel.eval("circle -n " + name + " -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;")
        cmds.move(0, -0.95, 0, name + ".cv[1]", name + ".cv[5]")
        cmds.move(0, -0.4, 0, name + ".cv[3]", name + ".cv[7]", r=True, os=True, wd=True)
        nameGRP = name + "_GRP"
        cmds.group(name, n=nameGRP)

    @staticmethod
    def TorsoFKControl(name):
        cmds.circle(n=name, c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=1, d=3, ut=0, tol=0.01,
                    s=8,
                    ch=1)
        cmds.move(0, 0, -2.4, "%s.cv[1]" % name,
                  "%s.cv[5]" % name,
                  r=True, os=True, wd=True)
        cmds.move(0, 0, -2.25, "%s.cv[0]" % name,
                  "%s.cv[2]" % name,
                  "%s.cv[4]" % name,
                  "%s.cv[6]" % name, r=True, os=True, wd=True)
        cmds.move(0, 0, -1.8, "%s.cv[3]" % name,
                  "%s.cv[7]" % name,
                  r=True, os=True, wd=True)
        pass

    @staticmethod
    def SpineTopCOntrol(name):
        mel.eval(
            "curve -n " + name + " -d 1 -p 0 -5 0 -p -2 -3 0 -p -1 -3 0 -p -1 -1 0 -p -3 -1 0 -p -3 -2 0-p -5 0 0 -p -3 2 0 -p -3 1 0 -p -1 1 0 -p -1 3 0 -p -2 3 0 -p 0 5 0 -p 2 3 0-p 1 3 0 -p 1 1 0 -p 3 1 0 -p 3 2 0 -p 5 0 0 -p 3 -2 0 -p 3 -1 0 -p 1 -1 0 -p 1 -3 0 -p 2 -3 0 -p 0 -5 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9-k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24;")
        cmds.pickWalk(d="down")
        cmds.rename(name + "Shape")
        cmds.delete(name + "Shape", ch=True)
        cmds.rotate(90, 0, 0, name)
        cmds.makeIdentity(name, apply=True, t=1, s=1, r=1)
        curveG = name + "_GRP"
        curveG2 = name + "_GRP2"
        cmds.group(name, n=curveG)
        cmds.xform(os=True, piv=(0, 0, 0))
        cmds.group(curveG, n=curveG2)
        cmds.xform(os=True, piv=(0, 0, 0))
        pass

    @staticmethod
    def TorsoMidControl(name):
        mel.eval(
            "curve -n " + name + " -d 1 -p 0 0 2.5 -p -1.5 0 1 -p -3.5 0 1 -p -3.5 0 -1 -p 3.5 0 -1 -p 3.5 0 1 -p 1.5 0 1 -p 0 0 2.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;")
        cmds.pickWalk(d="down")
        cmds.rename(name + "Shape")
        cmds.delete(name + "Shape", ch=True)
        cmds.makeIdentity(name, apply=True, t=1, s=1, r=1)
        curveG = name + "_GRP"
        curveG2 = name + "_GRP2"
        cmds.group(name, n=curveG)
        cmds.xform(os=True, piv=(0, 0, 0))
        cmds.group(curveG, n=curveG2)
        cmds.xform(os=True, piv=(0, 0, 0))
        pass


