import math
import numpy


def getVectorLength(vector: numpy.array):
    return ((vector**2).sum())**0.5


def getDegree(vector_a: numpy.array, vector_b: numpy.array):
    cosTheta = (vector_a * vector_b).sum() / (getVectorLength(vector_a) *
                                              getVectorLength(vector_a))
    if (cosTheta > 1):
        cosTheta = 1
    elif (cosTheta < -1):
        cosTheta = -1
    theda = math.acos(cosTheta)
    return math.degrees(theda)
