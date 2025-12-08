class Capitan ():
    def __init__(self, nombre, rango, añosexperiencia):
        self.nombre = nombre
        self.rango = rango
        self.añosexperiencia = añosexperiencia
    
    def __str__(self):
        return (f"Nombre del Capitán: {self.nombre}\n"
                f"Rango del Capitán: {self.rango}\n"
                f"Años de Experiencia: {self.añosexperiencia}")
        
    