from typing import List

class camion:
    def __init__(self, matricula: str, conductor: str, capacidad_kg: float, descripcion_carga: str ="", rumbo: int = 0, velocidad: int = 0):
        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = float(capacidad_kg)
        self.descripcion_carga = descripcion_carga
        if rumbo <1 or rumbo>359:
            raise ValueError ("ERROR. NO SON VALORES VALIDOS")
        self.rumbo = int(rumbo)
        self.velocidad = int(velocidad)
        self.cajas = []
    
    def __str__(self):
        return (f"Matricula: {self.matricula}\n"
                f"Conductor: {self.conductor}\n"
                f"Capacidad: {self.capacidad_kg} kg\n"
                f"Descripción de la Carga: {self.descripcion_carga}\n"
                f"Rumbo: {self.rumbo} grados\n"
                f"Velocidad: {self.velocidad}\n"
                f"Cajas: {len(self.cajas)}")

    def AñadirCaja(self, Caja):
        self.cajas.append(Caja)

    def setVelocidad (self, n):
        self.velocidad = n
    
    def setRumbo (self, m):
        self.rumbo = m
    
    def claxon (self):
        print("piii")

class Caja:
    def __init__(self, codigo: str, peso_kg: float, descripcion_carga: str, largo: float, ancho: float, altura: float):
        self.codigo = codigo
        self.peso_kg = float(peso_kg)
        self.descripcion_carga = descripcion_carga
        self.largo = float(largo)
        self.ancho = float(ancho)
        self.altura = float(altura)
    
    def __str__(self):
        return (f"Código: {self.codigo}\n"
                f"Peso: {self.peso_kg} kg\n"
                f"Descripción: {self.descripcion_carga}\n"
                f"Descripción de la Carga: {self.descripcion_carga}\n"
                f"Largo: {self.largo}\n"
                f"Áncho: {self.ancho}\n"
                f"Altura: {self.altura}")
    
    

    

if __name__ == "__main__":

# CAJAS    
    caja1 = Caja("7", 8, "Teclados", 20, 30, 40)
    caja2 = Caja("8", 20, "Componentes", 100, 200, 2)
    caja3 = Caja("9", 400, "Zapatos", 10, 20, 30)

# CAMIONES

    camion1 = camion("6605CJW", "Diego", 200,"Escombros", 200, 120)
    camion2 = camion("CA9575BL", "Dani", 300, "ordenadores", 350, 40)
   
    camion1.AñadirCaja(caja1)
    camion1.AñadirCaja(caja2)
    camion1.AñadirCaja(caja3)

    print(camion1)

    camion1.setVelocidad(200)
    camion1.setRumbo(100)
    
    camion2.claxon()
    print(camion1)