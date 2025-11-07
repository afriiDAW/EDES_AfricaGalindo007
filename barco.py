class Barco:
    def __init__(self, nombre, posicionX=0, posicionY=0, velocidad=0, rumbo=0, numeroMunicion=10):
        self.nombre = nombre
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.numeroMunicion = numeroMunicion

    def __str__(self):
        return (f"Barco: {self.nombre}\n"
                f"Posición: ({self.posicionX}, {self.posicionY})\n"
                f"Velocidad: {self.velocidad} km/h\n"
                f"Rumbo: {self.rumbo}°\n"
                f"Munición: {self.numeroMunicion}")

    def disparar(self):
        if self.numeroMunicion > 0:
            self.numeroMunicion -= 1
            print(f"{self.nombre} ha disparado . Munición restante: {self.numeroMunicion}")
        else:
            print(f"{self.nombre} no tiene munición")

    def setVelocidad(self, nueva_velocidad):
        if 0 <= nueva_velocidad <= 20:
            self.velocidad = nueva_velocidad
        else:
            print("La velocidad debe estar entre 0 y 20 km/h")

    def setRumbo(self, nuevo_rumbo):
        if 1 <= nuevo_rumbo <= 359:
            self.rumbo = nuevo_rumbo
        else:
            print("El rumbo debe estar entre 1 y 359 grados")


# Pruebas con tres barcos
if __name__ == "__main__":
    barco1 = Barco("El Cano", 10, 20, 5, 90, 3)
    barco2 = Barco("Castilla", 0, 0, 10, 180, 5)
    barco3 = Barco("Perla Negra", 5, 15, 7, 270, 2)

    for barco in [barco1, barco2, barco3]:
        print("\nAntes de disparar:")
        print(barco)
        barco.disparar()
        barco.setVelocidad(15)
        barco.setRumbo(120)
        print("\nDespués de modificar:")
        print(barco)