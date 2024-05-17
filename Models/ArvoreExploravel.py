class ArvoreExploravel:
    id = int(0)
    numero = int(0)
    DAP = 0.0
    H = 0.0
    areaBasal = 0.0
    volume = 0.0
    x = 0.0
    y = 0.0
    z = 0.0

    def __str__(self) -> str:
        return "id:" + str(self.id) + " x:" + str(self.x) + " y:" + str(self.y) + " z:" + str(self.z) 
    