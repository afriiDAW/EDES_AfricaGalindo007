from alojamiento import Alojamiento

class Apartamento (Alojamiento):
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, numero_planta: int, ascensor: bool, espacio_principal):
        super().__init__(codigo, direccion, ciudad, precio_por_noche)
        self.numero_planta = int(numero_planta)
        self.ascensor = ascensor
        self.espacio_principal = espacio_principal
    
    def __str__(self):
        base = super().__str__()
        return (base + "\n"
                f"Número de planta: {self.numero_planta}\n"
                f"Ascensor: {self.ascensor}\n"
                f"Espacio Principal: {self.espacio_principal}")

