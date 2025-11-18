import tkinter as tk
from tkinter import ttk, messagebox
import pygame

# -----------------------------
# CLASES PROPORCIONADAS
# -----------------------------
class camion:
    def __init__(self, matricula: str, conductor: str, capacidad_kg: float, descripcion_carga: str ="", rumbo: int = 0, velocidad: int = 0):
        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = float(capacidad_kg)
        self.descripcion_carga = descripcion_carga

        if rumbo < 1 or rumbo > 359:
            raise ValueError("NO SON VALORES VALIDOS")
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

    def setVelocidad(self, n):
        self.velocidad = n

    def setRumbo(self, m):
        self.rumbo = m

    def claxon(self):
        pygame.mixer.music.play()

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
                f"Largo: {self.largo}\n"
                f"Áncho: {self.ancho}\n"
                f"Altura: {self.altura}")

# -----------------------------
# PROGRAMA PRINCIPAL TKINTER
# -----------------------------
pygame.init()
pygame.mixer.music.load("claxon.mp3")  # Asegúrate de incluir el archivo

camiones = []
camion_activo = None

# Ventana
root = tk.Tk()
root.title("Gestor de Camiones - VibeCoding")
root.geometry("900x600")

# -----------------------------
# SECCIÓN: NUEVO CAMIÓN
# -----------------------------
frame_nuevo = ttk.LabelFrame(root, text="Crear Camión")
frame_nuevo.pack(side="left", fill="y", padx=10, pady=10)

labels = ["Matrícula", "Conductor", "Capacidad (kg)", "Descripción", "Rumbo (1-359)", "Velocidad"]
entries = {}
for l in labels:
    tk.Label(frame_nuevo, text=l).pack()
    e = tk.Entry(frame_nuevo)
    e.pack()
    entries[l] = e

def crear_camion():
    global camion_activo
    try:
        nuevo = camion(
            entries["Matrícula"].get(),
            entries["Conductor"].get(),
            float(entries["Capacidad (kg)"].get()),
            entries["Descripción"].get(),
            int(entries["Rumbo (1-359)"].get()),
            int(entries["Velocidad"].get())
        )
        camiones.append(nuevo)
        lista_camiones['values'] = [c.matricula for c in camiones]
        messagebox.showinfo("OK", "Camión creado correctamente")
    except Exception as e:
        messagebox.showerror("Error", str(e))

btn_crear = tk.Button(frame_nuevo, text="Crear Camión", command=crear_camion)
btn_crear.pack(pady=10)

# -----------------------------
# SECCIÓN: SELECCIÓN Y CONTROLES
# -----------------------------
frame_ctrl = ttk.LabelFrame(root, text="Control del Camión")
frame_ctrl.pack(side="left", fill="y", padx=10, pady=10)

lista_camiones = ttk.Combobox(frame_ctrl, values=[])
lista_camiones.pack(pady=5)

info = tk.Text(frame_ctrl, width=40, height=10)
info.pack(pady=10)

def actualizar_info():
    global camion_activo
    sel = lista_camiones.get()
    for c in camiones:
        if c.matricula == sel:
            camion_activo = c
            info.delete(1.0, "end")
            info.insert("end", str(c))
            return

btn_seleccionar = tk.Button(frame_ctrl, text="Seleccionar", command=actualizar_info)
btn_seleccionar.pack()

# CONTROLES

vel = tk.Scale(frame_ctrl, from_=0, to=200, label="Velocidad", orient="horizontal")
vel.pack(fill="x")

rum = tk.Scale(frame_ctrl, from_=1, to=359, label="Rumbo", orient="horizontal")
rum.pack(fill="x")

def aplicar_cambios():
    if camion_activo:
        camion_activo.setVelocidad(vel.get())
        camion_activo.setRumbo(rum.get())
        actualizar_info()

btn_aplicar = tk.Button(frame_ctrl, text="Aplicar Cambios", command=aplicar_cambios)
btn_aplicar.pack(pady=5)

# Añadir Caja
frame_caja = ttk.LabelFrame(root, text="Añadir Caja")
frame_caja.pack(side="left", fill="y", padx=10, pady=10)

labels_caja = ["Código", "Peso", "Descripción", "Largo", "Ancho", "Alto"]
entries_caja = {}
for l in labels_caja:
    tk.Label(frame_caja, text=l).pack()
    e = tk.Entry(frame_caja)
    e.pack()
    entries_caja[l] = e

def add_caja():
    if not camion_activo:
        messagebox.showerror("Error", "Selecciona un camión primero")
        return
    nueva = Caja(
        entries_caja["Código"].get(),
        float(entries_caja["Peso"].get()),
        entries_caja["Descripción"].get(),
        float(entries_caja["Largo"].get()),
        float(entries_caja["Ancho"].get()),
        float(entries_caja["Alto"].get())
    )
    camion_activo.AñadirCaja(nueva)
    actualizar_info()

btn_add_caja = tk.Button(frame_caja, text="Añadir Caja", command=add_caja)
btn_add_caja.pack(pady=10)

# Claxon
btn_claxon = tk.Button(root, text="TOCAR CLAXON", bg="yellow", command=lambda: camion_activo.claxon() if camion_activo else None)
btn_claxon.pack(pady=20)

# -----------------------------
# MOVIMIENTO VISUAL
# -----------------------------
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack(side="right", padx=10)
cam_rect = canvas.create_rectangle(120, 120, 180, 180, fill="red")

def animar():
    if camion_activo:
        dx = camion_activo.velocidad * 0.05
        canvas.move(cam_rect, dx, 0)
    canvas.after(50, animar)

animar()
root.mainloop()
