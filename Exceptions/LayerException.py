class LayerException(Exception):
    def __init__(self, layerName):
        super().__init__(f"Selecione uma camada valida")
        self.message = f"A camada {layerName} e invalida"
    
    def __str__(self):
        return self.message

class MultipleLayerException(Exception):
    def __init__(self):
        super().__init__(f"Execoes de camadas ocorrerao.")
        self.exceptions = []
    
    def __str__(self):
        exception_messages = "\n".join(e.__str__() for e in self.exceptions)
        return f"Execoes de camadas ocorrerao:\n{exception_messages}"