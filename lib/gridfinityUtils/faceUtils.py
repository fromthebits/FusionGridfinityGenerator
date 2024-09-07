import math
import adsk.core, adsk.fusion, traceback
import os

from .const import DEFAULT_FILTER_TOLERANCE
from . import geometryUtils


def minByArea(faces: adsk.fusion.BRepFaces):
    return min(faces, key=lambda x: x.area)

def maxByArea(faces: adsk.fusion.BRepFaces):
    return max(faces, key=lambda x: x.area)

def closestToOrigin(faces: adsk.fusion.BRepFaces):
    origin = adsk.core.Point3D.create(0, 0, 0)
    return min(faces, key=lambda x: min(x.boundingBox.minPoint.distanceTo(origin), x.boundingBox.maxPoint.distanceTo(origin)))

def longestEdge(face: adsk.fusion.BRepFace):
    return max(face.edges, key=lambda x: x.length)

def shortestEdge(face: adsk.fusion.BRepFace):
    return min(face.edges, key=lambda x: x.length)

def isYNormal(face: adsk.fusion.BRepFace):
    return math.isclose(face.boundingBox.minPoint.y, face.boundingBox.maxPoint.y, abs_tol=DEFAULT_FILTER_TOLERANCE)

def isXNormal(face: adsk.fusion.BRepFace):
    return math.isclose(face.boundingBox.minPoint.x, face.boundingBox.maxPoint.x, abs_tol=DEFAULT_FILTER_TOLERANCE)

def isZNormal(face: adsk.fusion.BRepFace):
    return math.isclose(face.boundingBox.minPoint.z, face.boundingBox.maxPoint.z, abs_tol=DEFAULT_FILTER_TOLERANCE)

def getBottomFace(body: adsk.fusion.BRepBody):
    horizontalFaces = [face for face in body.faces if isZNormal(face)]
    return min(horizontalFaces, key=lambda x: x.boundingBox.minPoint.z)

def getTopFace(body: adsk.fusion.BRepBody):
    horizontalFaces = [face for face in body.faces if isZNormal(face)]
    return max(horizontalFaces, key=lambda x: x.boundingBox.minPoint.z)

def getBackFace(body: adsk.fusion.BRepBody):
    verticalFaces = [face for face in body.faces if isYNormal(face)]
    return min(verticalFaces, key=lambda x: x.boundingBox.minPoint.x)

def getFrontFace(body: adsk.fusion.BRepBody):
    verticalFaces = [face for face in body.faces if isYNormal(face)]
    return max(verticalFaces, key=lambda x: x.boundingBox.minPoint.x)

def getRightFace(body: adsk.fusion.BRepBody):
    verticalFaces = [face for face in body.faces if isXNormal(face)]
    return max(verticalFaces, key=lambda x: x.boundingBox.minPoint.y)

def getLeftFace(body: adsk.fusion.BRepBody):
    verticalFaces = [face for face in body.faces if isXNormal(face)]
    return min(verticalFaces, key=lambda x: x.boundingBox.minPoint.y)

def getTopHorizontalEdge(edges: adsk.fusion.BRepEdges):
    horizontalEdges = [edge for edge in edges if geometryUtils.isHorizontal(edge)]
    return max(horizontalEdges, key=lambda x: x.startVertex.geometry.z)

def getBottomHorizontalEdge(edges: adsk.fusion.BRepEdges):
    horizontalEdges = [edge for edge in edges if geometryUtils.isHorizontal(edge)]
    return min(horizontalEdges, key=lambda x: x.startVertex.geometry.z)


def getVerticalEdges(
    faces: adsk.fusion.BRepFaces,
    ):
    filteredEdges: list[adsk.fusion.BRepEdge] = []
    for face in faces:
        for edge in face.edges:
            if geometryUtils.isCollinearToZ(edge):
                filteredEdges.append(edge)
    return filteredEdges
