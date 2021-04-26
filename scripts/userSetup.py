import maya.cmds as cmds

if not cmds.about(batch=True):
    from Miccall_shelf.Miccall_Tools import shelf_show
    cmds.evalDeferred(shelf_show)
