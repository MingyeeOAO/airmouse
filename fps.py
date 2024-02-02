import time
class fps:
    def __init__(self):
        self.lastTime=time.time()
    def get(self):
        curTime=time.time()
        ans = 1/(curTime-self.lastTime)
        self.lastTime=curTime
        return ans