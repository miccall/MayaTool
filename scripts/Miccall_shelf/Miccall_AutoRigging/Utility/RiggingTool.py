# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import sys


class RiggingTool:
    @staticmethod
    def calculate_pole_vector(p1, p2, p3, poleDistance=1):
        """
        This function takes 3 PyMEL PyNodes as inputs.
        Creates a pole vector position at a "nice" distance away from a triangle of positions.
        Normalizes the bone lengths relative to the knee to calculate straight ahead
        without shifting up and down if the bone lengths are different.
        Returns a pymel.core.datatypes.Vector
        @url : https://gist.github.com/chris-lesage/0fcc9a344f2096cf6c82a353cb735b3e
        """
        p1 = pm.PyNode(p1)
        p2 = pm.PyNode(p2)
        p3 = pm.PyNode(p3)

        vec1 = p1.getTranslation(space='world')  # "hips"
        vec2 = p2.getTranslation(space='world')  # "knee"
        vec3 = p3.getTranslation(space='world')  # "ankle"

        # 1. Calculate a "nice distance" based on average of the two bone lengths.
        legLength = (vec2 - vec1).length()
        kneeLength = (vec3 - vec2).length()
        distance = (legLength + kneeLength) * 0.5 * poleDistance

        # 2. Normalize the length of leg and ankle, relative to the knee.
        # This will ensure that the pole vector goes STRAIGHT ahead of the knee
        # Avoids up-down offset if there is a length difference between the two bones.
        vec1norm = ((vec1 - vec2).normal() * distance) + vec2
        vec3norm = ((vec3 - vec2).normal() * distance) + vec2

        # 3. given 3 points, calculate a pole vector position
        mid = vec1norm + (vec2 - vec1norm).projectionOnto(vec3norm - vec1norm)

        # 4. Move the pole vector in front of the knee by the "nice distance".
        midPointer = vec2 - mid
        poleVector = (midPointer.normal() * distance) + vec2

        return poleVector

    @staticmethod
    def CreateDuplicate(Root, Attr):
        NewChainList = cmds.duplicate(Root, renameChildren=True)
        for JNT in NewChainList:
            JointNameSplits = JNT.split("_")
            prefix = ""
            for i in range(0, len(JointNameSplits) - 1):
                prefix += JointNameSplits[i] + "_"
            prefix += "%s" % Attr + "_JNT"
            cmds.rename(JNT, prefix)
        pass
