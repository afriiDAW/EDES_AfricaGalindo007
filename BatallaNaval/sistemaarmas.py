class SistemaArmas:
    def __init__(self, numCañones: int, numMisiles: int, numTorpedos: int):
        self.numCañones = int(numCañones)
        self.numMisiles = int(numMisiles)
        self.numTorpedos = int(numTorpedos)
    
    def __str__(self):
        return (f"Número de cañones: {self.numCañones}"
                f"Número de Misiles: {self.numMisiles}"
                f"Número de Torpedos: {self.numTorpedos}")

    def SeleccionarObjetivo (self, idObjetivo: int):
        self.idObjetivo = int(idObjetivo)
    
    def DispararArma(self, tipo:str):
        self.tipo = tipo
        