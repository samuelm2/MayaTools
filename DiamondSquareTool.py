import maya.cmds as cmds
from random import uniform



def diamondSquare(sx, sideLength, sr, rFalloff, flattenBelowZero):
    sideEdges=2**sx

    plane = cmds.polyPlane(subdivisionsX=sideEdges, subdivisionsY=sideEdges, height=sideLength, width=sideLength)

    def getVertexPositionY(x, y):
        return cmds.pointPosition(plane[0] + ".vtx[{0}]".format((sideEdges + 1) * y + x))[1]

    def setVertexYPos(x, y, newYPos):
        old = cmds.pointPosition(plane[0] + ".vtx[{0}]".format((sideEdges + 1) * y + x))
        cmds.xform(plane[0] + ".vtx[{0}]".format((sideEdges + 1) * y + x), absolute=True,
                   translation=[old[0], newYPos, old[2]])

    blue = [0, .412, .58]
    green = [.133, .545, .133]
    gray = [.439, .502, .565]
    white = [1, .98, .98]

    def setColor(index):
        vertexStr = plane[0] + ".vtx[{0}]".format(index)
        height = cmds.xform(vertexStr, q=True, translation=True)[1]
        if height <= 0:
            cmds.polyColorPerVertex(vertexStr, colorRGB=blue)
        elif height <= sideLength/40:
            cmds.polyColorPerVertex(vertexStr, colorRGB=green)
        elif height <= sideLength*.085:
            cmds.polyColorPerVertex(vertexStr, colorRGB=gray)
        else:
            cmds.polyColorPerVertex(vertexStr, colorRGB=white)


    def diamondStep(x, y, length, r):
        avgY = (getVertexPositionY(x, y) + getVertexPositionY(x + length, y) + getVertexPositionY(x, y + length) + getVertexPositionY(x + length, y + length)) / 4.
        setVertexYPos(x + length / 2, y + length / 2, avgY + uniform(-r, r))

    def squareStep(x, y, length, r):
        avgYL = (getVertexPositionY(x, y) + getVertexPositionY(x, y + length)) / 2.
        setVertexYPos(x, y + length / 2, avgYL + uniform(-r, r))

        avgYR = (getVertexPositionY(x + length, y) + getVertexPositionY(x + length, y + length)) / 2.
        setVertexYPos(x + length, y + length / 2, avgYR + uniform(-r, r))

        avgYT = (getVertexPositionY(x, y + length) + getVertexPositionY(x + length, y + length)) / 2.
        setVertexYPos(x + length / 2, y + length, avgYT + uniform(-r, r))

        avgYB = (getVertexPositionY(x, y) + getVertexPositionY(x + length, y)) / 2.
        setVertexYPos(x + length / 2, y, avgYB + uniform(-r, r))

    currSideEdges = sideEdges
    currRand = sr

    while currSideEdges > 1:
        for y in range(0, sideEdges, currSideEdges):
            for x in range(0, sideEdges, currSideEdges):
                diamondStep(x, y, currSideEdges, currRand)

        for y in range(0, sideEdges, currSideEdges):
            for x in range(0, sideEdges, currSideEdges):
                squareStep(x, y, currSideEdges, currRand)

        currRand *= 0.5
        currSideEdges /= 2
        cmds.refresh()

    for i in xrange((sideEdges + 1) ** 2):
        setColor(i)
        if flattenBelowZero:
            pos = cmds.pointPosition(plane[0] + ".vtx[{0}]".format(i))
            if pos[1] < 0.:
                cmds.xform(plane[0] + ".vtx[{0}]".format(i), absolute=True, translation=[pos[0], 0, pos[2]])

    cmds.polyOptions(activeObjects=True, colorShadedDisplay=True)

window = cmds.window(title = "Terrain Tool")
cmds.columnLayout()
bvd = cmds.intFieldGrp(label='Vertex Density', value1=6)
btsl = cmds.floatFieldGrp(label='Terrain Side Length', value1=10, precision=2)
bs = cmds.floatFieldGrp(label='Spikiness', value1=2, precision=2)
bsfr = cmds.floatFieldGrp(label='Spikiness Falloff Ratio', value1=0.75, precision=2)
bfv = cmds.checkBoxGrp(label='Flatten Values Below Zero', value1=1)

def runDS(*args):
    vd = cmds.intFieldGrp(bvd, q=True, value1=True)
    tsl = cmds.floatFieldGrp(btsl, q=True, value1=True)
    s = cmds.floatFieldGrp(bs, q=True, value1=True)
    sfr = cmds.floatFieldGrp(bsfr, q=True, value1=True)
    fv = cmds.checkBoxGrp(bfv, q=True, value1=True)
    print(fv)
    diamondSquare(vd, tsl, s, sfr, fv)

button = cmds.button(label='Generate Terrain', command=runDS)
cmds.showWindow( window )
