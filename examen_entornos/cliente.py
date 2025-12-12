from alojamiento import Alojamiento
class Cliente:
    def __init__(self, nombre: str, dni: str, telf: int, alojamiento_actual):
        self.nombre = nombre
        self.dni = dni
        self.telf = int(telf)
        self.alojamiento_actual = alojamiento_actual
    
    def __str__(self):
        return (f"Nombre del cliente: {self.nombre}\n"
                f"DNI del cliente: {self.dni}\n"
                f"Teléfono del cliente: {self.telf}")
    
    def reservar(self, alojamiento):
        self.alojamiento_actual = alojamiento
    

    def cancelar_reserva (self):
        self.alojamiento_actual = "ninguno"


    def mostrar_reserva(self):
        if self.alojamiento_actual != "ninguno":
            print(f"Información del alojamiento: {Alojamiento}")
        else:
            print("Has cancelado la reserva")   
    
