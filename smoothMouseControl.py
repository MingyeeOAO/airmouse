import mouse
import numpy
import pyautogui
import screeninfo


def mousePosScale(Pos, scale):
    Pos -= 0.5
    Pos *= scale
    Pos += 0.5
    Pos[0] = max(0, min(1, Pos[0]))
    Pos[1] = max(0, min(1, Pos[1]))
    return Pos


class control:

    def __init__(self, smooth=5):
        self.smooth = smooth
        self.screenMonitors = screeninfo.get_monitors()
        self.screenSize = numpy.array(
            (self.screenMonitors[0].width, self.screenMonitors[0].height))
        self.mousePosRecord = numpy.zeros((smooth, 2))

    def speedMove(self):
        if (((self.mousePosRecord[0] - self.mousePosRecord[1])**2).sum()**0.5
                >= 0.005):
            for i in range(1, 5):
                self.mousePosRecord[i] = self.mousePosRecord[0]

    def setPos(self):
        x, y = self.getPos()
        x = int(x)
        y = int(y)
        mouse.move(x, y)

    def getPos(self):
        self.speedMove()
        self.curPos = self.mousePosRecord.sum(axis=0) / self.smooth
        self.curPos = self.curPos * self.screenSize
        return self.curPos

    def pushPos(self, Pos, setPos=True):
        newPos = numpy.array(Pos)
        for i in range(self.smooth - 1, 0, -1):
            self.mousePosRecord[i] = self.mousePosRecord[i - 1]
        self.mousePosRecord[0] = newPos
        if setPos:
            self.setPos()

    def pushDis(self, Dis, setPos=True):
        newPos = numpy.array(Dis + self.mousePosRecord[0])
        self.pushPos(newPos, setPos)

    def mouseDown(self, button):
        pyautogui.mouseDown(button=button)

    def mouseUp(self, button):
        pyautogui.mouseUp(button=button)

    def keyDown(self, button):
        pyautogui.keyDown(button)

    def keyUp(self, button):
        pyautogui.keyUp(button)