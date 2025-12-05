from plataformanaval import PlataformaNaval

class Fragata(PlataformaNaval):
    
    def __init__(self, nombre, pais, eslora, desplazamiento, velocidadMaxima, misilesAntiaereos: int, helicopterosEmb: int, rolPrincipal: str):
        super().__init__(nombre, pais, eslora, desplazamiento, velocidadMaxima)
        self.misilesAntiaereos = int(misilesAntiaereos)
        self.helicopterosEmb = int(helicopterosEmb)
        self.rolPrincipal = rolPrincipal
    
    def __str__(self):
        return (f"Misiles Antiaereos: {self.misilesAntiaereos}\n"
                f"Helicopteros Embebidos: {self.helicopterosEmb}\n"
                f"Rol Principal: {self.rolPrincipal}"
        )
    
    def dispararMisilAA(self):
        if self.misilesAntiaereos > 0:
            self.misilesAntiaereos =-1
            print("¡Misil antiaéreo disparado!")
        else:
            print("No quedan misiles")
    
    def despegarHelicoptero(self):
        if self.helicopterosEmb > 0:
            self.helicopterosEmb =-1
            print("Se ha despegado un helicoptero")
