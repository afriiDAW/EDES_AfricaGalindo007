class PlataformaNaval:
    def __init__(self, nombre: str, pais: str, eslora: float, desplazamiento: float, VelocidadMaxima: float):
        self.nombre = nombre
        self.pais = pais
        self.eslora = float(eslora)
        self.desplazamiento = float(desplazamiento)
        self.VelocidadMaxima = float(VelocidadMaxima)
    
    def __str__(self):
        return (f"Nombre: {self.nombre}\n"
                f"Pais: {self.pais}\n"
                f"Eslora: {self.eslora}\n"
                f"Desplazamiento: {self.desplazamiento}\n"
                f"Velocidad  Máxima: {self.VelocidadMaxima}\n")

    def navegar(self,rumbo: float, velocidad: float):
        self.rumbo = float(rumbo)
        self.velocidad = float(velocidad)
    
    def detenerse(self):
        self.velocidad = 0
    
    def recibirDanio(self, puntos: int):
        self.puntos = int(puntos)
    
    def estaOperativa(self):
        return self.vida > 0