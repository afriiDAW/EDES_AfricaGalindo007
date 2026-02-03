from plataformanaval import PlataformaNaval
from capitan import Capitan
from corbeta import Corbeta
from fragata import Fragata
from sistemaarmas import SistemaArmas
from sistemasensores import SistemaSensores
from submarino import Submarino
from flota import Flota


plataforma1 = PlataformaNaval("plataforma", "España", 20.2, 200, 300)

# CAPITANES

capitan1 = Capitan ("Dani", "Sargento", 20)
capitan2 = Capitan("Diego", "Cabo", 10)
capitan3 = Capitan ("Selu", "razo", 1)

# FRAGATA, CORBETA Y SUBMARINO

fragata1 = Fragata ("Fragata 1", "España", 100.2, 20, 300, 10, 200, "Ganador")

corbeta1 = Corbeta ("Corbeta1", "Estados Unidos", 100, 200, 500, 20, 10)

submarino1 = Submarino ("Submarino1", "Mexico", 100, 200, 300, 500, "Diesel", 20)


# ASUMIR MANDO

capitan1.asumirMando(fragata1)
capitan2.asumirMando(corbeta1)
capitan3.asumirMando(submarino1)


# SISTEMAS DE ARMAS Y DE SENSORES

SistemaArmas(3, 20, 50)
SistemaSensores(tieneRadar=True, tieneSonar=False)


# CREACION DE FLOTA

flota1 = Flota("Flota del Atlántico", "Atlántico")
flota2 = Flota("Flota del mediterraneo", "Mediterraneo")
# AGREGACION DE PLATAFORMAS

flota1.agregarPlataforma(submarino1)
flota2.agregarPlataforma(fragata1)

# Mostrar información inicial
print("\n--- Información inicial de la flota ---")
for p in flota1.plataformas:
    print(p)
    print(f"Capitán: {p.capitan.nombre}")
    print(f"Sensores: Radar={p.sensores.tieneRadar}, Sonar={p.sensores.tieneSonar}")
    print(p.sensores.escanearSuperficie())
    print(p.sensores.escanearSubmarino())
    print()

# Simulación
print("\n--- Simulación ---")
flota1.ordenarAtaque()
submarino1.navegar(90, 20)
fragata1.recibirDanio(120)
submarino1.sumergirse(200)
fragata1.despegarHelicoptero()

# Estado operativo
print("\n--- Estado operativo ---")
for p in flota1.plataformas:
    estado = "Operativa" if p.estaOperativa() else "No operativa"
    print(f"{p.nombre}: {estado}")