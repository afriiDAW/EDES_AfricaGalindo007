# videojuego.py
# Ejemplo simple y didáctico de Programación Orientada a Objetos
# Clase Personaje con:
#   - Atributos: nombre, vidas, flechas, posicionX, posicionY
#   - Métodos: medicina(), saltar(), disparar()
#
# Reglas:
#   - medicina(): suma 1 vida
#   - saltar(): mueve un poco en X (por simplicidad, +1)
#   - disparar(): muestra un mensaje y resta 1 flecha (si hay flechas)

class Personaje:
    def __init__(self, nombre, vidas, flechas, posicionX, posicionY):
        self.nombre = nombre
        self.vidas = vidas
        self.flechas = flechas
        self.posicionX = posicionX
        self.posicionY = posicionY

    def medicina(self):
        """Incrementa la vida en 1."""
        self.vidas += 1
        print(f"{self.nombre} toma medicina. Vidas ahora: {self.vidas}")

    def saltar(self):
        """Salta (aquí: avanza un poco en X)."""
        self.posicionX += 1  # 'un poco' = +1 para mantenerlo simple
        print(f"{self.nombre} salta. Nueva posición: X={self.posicionX}, Y={self.posicionY}")

    def disparar(self):
        """Dispara una flecha (si tiene)."""
        if self.flechas > 0:
            self.flechas -= 1
            print(f"{self.nombre} dispara una flecha. Flechas restantes: {self.flechas}")
        else:
            print(f"{self.nombre} no puede disparar: no le quedan flechas.")

# --- Programa principal: crear dos personajes y probar métodos ---
if __name__ == "__main__":
    # Crea dos personajes con valores iniciales sencillos
    p1 = Personaje(nombre="Ana", vidas=3, flechas=2, posicionX=0, posicionY=0)
    p2 = Personaje(nombre="Luis", vidas=2, flechas=0, posicionX=5, posicionY=1)

    # Prueba de  métodos en p1
    print("== Acciones de Ana ==")
    p1.saltar()    # X: 0 -> 1
    p1.disparar()   # flechas: 2 -> 1
    p1.medicina()   # vidas: 3 -> 4

    # Prueba de métodos en p2
    print("\n== Acciones de Luis ==")
    p2.disparar()   # no tiene flechas
    p2.saltar()     # X: 5 -> 6
    p2.medicina()   # vidas: 2 -> 3
