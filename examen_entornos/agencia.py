from alojamiento import Alojamiento
class Agencia:
    def __init__(self, nombre: str, correo_contacto: str):
        self.nombre = nombre
        self.correo_contacto = correo_contacto
        self.lista_alojamientos = []
    
    def __str__(self):
        return (f"Nombre de la agencia: {self.nombre}\n"
                f"Correo de contacto: {self.correo_contacto}\n"
                f"Lista de alojamientos: {self.lista_alojamientos}")

    def agregar_alojamiento(self, alojamiento):
        self.lista_alojamientos.append[alojamiento]
    
    def quitar_alojamiento(codigo):
        pass

    def contar_alojamientos(self):
        return len(self.lista_alojamientos)
    


