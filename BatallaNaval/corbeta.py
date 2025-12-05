from plataformanaval import PlataformaNaval

class Corbeta (PlataformaNaval):
    
    def __init__(self, nombre, pais, eslora, desplazamiento, velocidadMaxima, misilesAntibuque: int, autonomiaDias: int):
        super().__init__(nombre, pais, eslora, desplazamiento, velocidadMaxima)
        misilesAntibuque = int(misilesAntibuque)
        autonomiaDias = int(autonomiaDias)
    
    def __str__(self):
        return (f"Misiles Antibuque: {self.misilesAntibuque}\n"
                f"Autonomía en días: {self.autonomiaDias}"
                )
    
    def dispararMisilAntibuque(self):
        if self.misilesAntibuque > 0:
            self.misilesAntibuque =-1
            print("Se ha disparado un misil")
    
    def RealizarPatrulla(self, costera: bool):
        if costera:
            print("Se está realizando una patrulla")
        else:
            print("No se está realizando ninguna patrulla")