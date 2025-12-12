
class Espacio:
    def __init__(self, nombre_espacio: str, metros_cuadrados: float, ventanas: bool):
        self.nombre_espacio = nombre_espacio
        self.metros_cuadrados = float(metros_cuadrados)
        self.ventanas = ventanas
    
    def __str__(self):
        return (
                f"Nombre del espacio: {self.nombre_espacio}\n"
                f"Metros cuadrados: {self.metros_cuadrados}\n"
                f"Ventanas: {self.ventanas}")

