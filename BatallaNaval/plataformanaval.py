class PlataformaNaval:
    def __init__(self, nombre: str, pais: str, eslora: float, desplazamiento: float, velocidadMaxima: float):
        self.nombre = nombre
        self.pais = pais
        self.eslora = float(eslora)
        self.desplazamiento = float(desplazamiento)
        self.velocidadMaxima = float(velocidadMaxima)
    
    def __str__(self):
        return (f"Nombre de la Plataforma: {self.nombre}\n"
                f"País: {self.pais}\n"
                f"Eslora: {self.eslora}\n"
                f"Desplazamiento: {self.desplazamiento}\n"
                f"Velocidad Máxima: {self.velocidadMaxima}")
    
    def Navegar (self, rumbo: float, velocidad: float):
        self.rumbo = float(rumbo)
        self.velocidad = float(velocidad)
    
    def detenerse(self):
        if self.velocidad == 0:
            print("Se ha detenido la plataforma")
    
    def recibirdaño (self, puntos: int):
        self.puntos = int(puntos)
    
    def estaOperativa (self):
        print("La plataforma está operativa")