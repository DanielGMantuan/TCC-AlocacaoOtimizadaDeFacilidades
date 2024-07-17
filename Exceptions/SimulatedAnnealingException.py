class SimulatedAnnealingException(Exception):
    def __init__(self, parameter):
        super().__init__(f"Infrorme um {parameter} valido")
        self.message = f"Informe um {parameter} valido"
    
    def __str__(self):
        return self.message

class MultipleSimulatedAnnealingExceptionException(Exception):
    def __init__(self, exceptions):
        self.exceptions = exceptions
        super().__init__("Multiple SA exceptions occurred.")
    
    def __str__(self):
        exception_messages = "\n".join(str(e) for e in self.exceptions)
        return f"Multiple SA exceptions occurred:\n{exception_messages}"