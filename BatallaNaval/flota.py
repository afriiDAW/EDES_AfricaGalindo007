class Flota:
    def __init__(self,  nombre: str, zonaOperacion: str):
        self.nombre = nombre
        self.zonaOperacion = zonaOperacion
        self.plataformas = []

    def __str__(self):
        return (f"Nombre de la flota: {self.nombre}"
                f"Zona de Operación: {self.zonaOperacion}")
    def agregarPlataforma(self, p):
        self.plataformas.append(p)
        print(f"Plataforma '{p.nombre}' agregada a la flota '{self.nombre}'.")

    def retirarPlataforma(self, p):
        if p in self.plataformas:
            self.plataformas.remove(p)
            print(f"Plataforma '{p.nombre}' retirada de la flota '{self.nombre}'.")
        else:
            print("La plataforma no está en la flota.")

    def ordenarAtaque(self):
        print(f"La flota '{self.nombre}' ordena ataque en la zona '{self.zonaOperacion}'...")
        for plataforma in self.plataformas:
            plataforma.atacar()
    