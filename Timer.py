class Timer:
        def __init__(self) -> None:
            self.time=0.0
        def getTime(self):
             return round(self.time,2)
        def addTime(self, newTime):
             self.time=self.time+newTime
     
