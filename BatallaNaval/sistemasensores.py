class SistemaSensores ():
    def __init__(self, tieneRadar, tieneSonar, rangoDeteccion: float):
        self.tieneRadar = tieneRadar
        self.tieneSonar = tieneSonar
        self.rangoDeteccion = float(rangoDeteccion)
    
    def escanearSuperficie(self):
        print("Escaneando superficie...")

    def escanearSubmarino(self):
        print("Escanenado submarinos...")