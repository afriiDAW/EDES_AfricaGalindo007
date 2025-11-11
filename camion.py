class camion:
    def __init__(self, matricula, conductor, capacidad_kg, descripcion_carga, rumbo, velocidad, cajas):
        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = capacidad_kg
        self.descripcion_carga = descripcion_carga
        self.rumbo = rumbo
        self.velocidad = velocidad
        self.cajas = cajas
    
    def __str__(self):
        return (f"Matricula: {self.matricula}\n"
                f"Conductor: {self.conductor}\n"
                f"Capacidad: {self.capacidad_kg} kg\n"
                f"Descripción de la Carga: {self.descripcion_carga}\n"
                f"Rumbo: {self.rumbo} grados\n"
                f"Velocidad: {self.velocidad}\n"
                f"Cajas: {self.cajas}")
    