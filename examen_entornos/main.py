
# Importación de clases

from alojamiento import Alojamiento
from apartamento import Apartamento
from agencia import Agencia
from casarural import CasaRural
from cliente import Cliente
from espacio import Espacio

# Creo el programa

apartamento = Apartamento(1, "calle inventada", "cádiz", 150, 2, True, Espacio("Salón", 22.5, True))
casarural = CasaRural(2, "calle veintidos 111", "Jeréz", 200, 18, True, Espacio("Estudio", 18.0))

# creo la agencia 

agencia = Agencia("Agencia los alonsistas", "alonsoelmejor@yahoo.com")

alojamimento1 = agencia.agregar_alojamiento(apartamento)
alojamiento2 = agencia.agregar_alojamiento(casarural)

# Creo al cliente

cliente1 = Cliente("Fernando Alonso", "20304R", 611778, apartamento)

cliente = Cliente.reservar(cliente1, alojamimento1)

apartamento = Apartamento.cambiar_precio(Apartamento, 200)
apartamento = Apartamento.aumentar_precio_porcentaje(Apartamento, 10)

print(f"Información completa de la agencia: {agencia}")

# No tengo quitar agencia



