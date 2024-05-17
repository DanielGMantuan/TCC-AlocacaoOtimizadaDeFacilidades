class Area :
    def __init__(self):
        self.id: int = -1
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
    
    def __str__(self) -> str:
        return "id:" + str(self.id) + " x:" + str(self.x) + " y:" + str(str(self.y)) + " z:" + str(self.z)