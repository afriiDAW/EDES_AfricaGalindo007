from alojamiento import Alojamiento
class CasaRural(Alojamiento):
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, metros_jardin: int, chimenea: bool, espacio_principal):
        super().__init__(codigo, direccion, ciudad, precio_por_noche, espacio_principal)
        self.metros_jardin = int(metros_jardin)
        self.chimenea = chimenea
    
    def __str__(self):
        base = super().__str__()

        return (base + "\n"
                f"Metros del Jardín: {self.metros_jardin}\n"
                f"Chimenea: {self.chimenea}\n"
                f"Espacio Principal: {self.espacio_principal}")
    
