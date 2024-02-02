import tools
import numpy

#dnkajbdkjsdbakjdbsak
def gesturesName(fingerResult):
    if ((fingerResult == numpy.array([0, 1, 0, 0, 0])).all()):
        return "click"
    elif ((fingerResult == numpy.array([1, 1, 1, 1, 1])).all()):
        return "fist"
    else:
        return "others"


def analize(landmark):
    fingersDegree = numpy.zeros(5)

    fingerVectorDefination = numpy.array([[2, 3, 4], [5, 6, 8], [9, 10, 12],
                                          [13, 14, 16], [17, 18, 20]])

    fingersVector = numpy.zeros((5, 2, 2))
    for i in range(5):
        curDefination = fingerVectorDefination[i]
        vectors = numpy.zeros((3, 2))
        for j in range(3):
            curLandmark = landmark[curDefination[j]]
            vectors[j] = numpy.array([curLandmark.x, curLandmark.y])

        fingersVector[i] = numpy.array(
            [vectors[0] - vectors[1], vectors[2] - vectors[1]])

    for i in range(5):
        fingersDegree[i] = tools.getDegree(fingersVector[i][0],
                                           fingersVector[i][1])

    fingersResult = numpy.zeros(5)
    fingersTriggerDegrees = numpy.array([120, 100, 100, 100, 100])
    for i in range(5):
        if (abs(fingersDegree[i]) < fingersTriggerDegrees[i]):
            fingersResult[i] = 1
        else:
            fingersResult[i] = 0

    print(fingersDegree)

    return fingersResult