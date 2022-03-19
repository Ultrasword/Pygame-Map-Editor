from engine import eventhandler



class Test(eventhandler.Event):
    def __init__(self):
        super().__init__({"pressed": "space bar? or a key idk"})