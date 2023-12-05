class WallsBody:
    def __init__(self,XY,WH,corridors,blocker = False):
        self.roomXY = XY
        self.roomWH = WH
        self.corridors = corridors
        self.blocker = blocker
