class Alojamiento:
    def __init__(self, codigo: str, direccion: str, ciudad: str, precio_por_noche: int, espacio_principal):
        self.codigo = codigo
        self.direccion = direccion
        self.ciudad = ciudad
        self.precio_por_noche = int(precio_por_noche)
        self.espacio_principal = espacio_principal
    
    def __str__(self):
        return (f"Códifo del alojamiento: {self.codigo}\n"
                f"Dirección del alojamiento: {self.direccion}\n"
                f"Ciudad donde se encuentra el alojamiento: {self.ciudad}\n"
                f"Precio por noche: {self.precio_por_noche}\n"
                f"Espacio principal: {self.espacio_principal}")

    def cambiar_precio (self, nuevo_precio):
        if nuevo_precio >= 0:
            self.precio_por_noche = nuevo_precio
        else:
            print("Introduce un número válido")

    def aumentar_precio_porcentaje (self, porcentaje):
        if porcentaje >= 0:
            self.nuevo_precio = self.precio_por_noche * porcentaje
        else:
            print("Dame un número válido")

    def get_precio(self):
        return self.nuevo_precio
