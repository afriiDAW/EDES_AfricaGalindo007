from plataformanaval import PlataformaNaval

class Submarino (PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, VelocidadMaxima, profundidadMaxima: int, tipoPropulsion: str, tubosLanzatorpedos: int):
        super().__init__(nombre, pais, eslora, desplazamiento, VelocidadMaxima)
        self.profundidadMaxima = int(profundidadMaxima)
        self.tipoPropulsion = tipoPropulsion
        self.tubosLanzatorpedos = int(tubosLanzatorpedos)
    
    def __str__(self, profundidadMaxima, tipoPropulsion, tubosLanzatorpedos):
        return (f"Profundidad Máxima: {profundidadMaxima}\n"
                f"Tipo de Porpulsión: {tipoPropulsion}\n"
                f"Tubos Lanza Torpedos: {tubosLanzatorpedos}")
    
    def sumergirse(self, profundidad: int):
        self.profundidad = int(profundidad)
    
    def emerger(self):
        self.profundidad = 0 
    
    def lanzarTorpedo ():
        pass

        