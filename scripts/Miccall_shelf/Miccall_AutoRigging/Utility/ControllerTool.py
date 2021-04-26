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
    def threedarrow():
        mel.eval(
            "curve -d 1 -p 3 0 0 -p 1 0 -2 -p 1 0 -1 -p -3 0 -1 -p -3 0 1 -p 1 0 1 -p 1 0 2 -p 3 0 0 -p 1 -2 0 -p 1 -1 0 -p -3 -1 0 -p -3 1 0 -p 1 1 0 -p 1 2 0 -p 3 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -n \"Three D Control\";")
