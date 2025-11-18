import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import math

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
        return (f"Matricula: {self.matricula}"

                f"Conductor: {self.conductor}"

                f"Capacidad: {self.capacidad_kg} kg"

                f"Descripción de la Carga: {self.descripcion_carga}"

                f"Rumbo: {self.rumbo} grados"

                f"Velocidad: {self.velocidad}"

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
        return (f"Código: {self.codigo}"
                f"Peso: {self.peso_kg} kg"
                f"Descripción: {self.descripcion_carga}"
                f"Largo: {self.largo}"
                f"Áncho: {self.ancho}"
                f"Altura: {self.altura}")

# -----------------------------
# PROGRAMA PRINCIPAL TKINTER
# -----------------------------
pygame.init()
pygame.mixer.music.load("claxon.mp3")

camiones = []
camion_activo = None

root = tk.Tk()
root.title("Gestor de Camiones - VibeCoding")
root.geometry("1200x700")

# CANVAS GRANDE
canvas = tk.Canvas(root, width=800, height=650, bg="white")
canvas.pack(side="left", padx=10, pady=10)

# Diccionario: matricula → rectángulo en pantalla
rectangulos = {}
textos = {}

# -----------------------------
# SECCIÓN DERECHA
# -----------------------------
panel = ttk.Frame(root)
panel.pack(side="right", fill="y", padx=10)

# Crear camiones
frame_nuevo = ttk.LabelFrame(panel, text="Crear Camión")
frame_nuevo.pack(fill="x", pady=10)

labels = ["Matrícula", "Conductor", "Capacidad (kg)", "Descripción", "Rumbo (1-359)", "Velocidad"]
entries = {}
for l in labels:
    tk.Label(frame_nuevo, text=l).pack()
    e = tk.Entry(frame_nuevo)
    e.pack()
    entries[l] = e

def crear_camion():
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

        # Crear rectángulo en canvas
        rect = canvas.create_rectangle(50, 50, 130, 90, fill="red")
        texto = canvas.create_text(90, 70, text=nuevo.conductor, fill="white")
        rectangulos[nuevo.matricula] = rect
        textos[nuevo.matricula] = texto

        messagebox.showinfo("OK", "Camión creado correctamente")
    except Exception as e:
        messagebox.showerror("Error", str(e))

btn_crear = tk.Button(frame_nuevo, text="Crear Camión", command=crear_camion)
btn_crear.pack(pady=10)

# Selección
frame_ctrl = ttk.LabelFrame(panel, text="Control del Camión")
frame_ctrl.pack(fill="x", pady=10)

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

btn_sel = tk.Button(frame_ctrl, text="Seleccionar", command=actualizar_info)
btn_sel.pack()

# Controles
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

# Claxon
btn_claxon = tk.Button(panel, text="TOCAR CLAXON", bg="pink", command=lambda: camion_activo.claxon() if camion_activo else None)
btn_claxon.pack(pady=20)

# -----------------------------
# ANIMACIÓN
# -----------------------------
def animar():
    for c in camiones:
        rect = rectangulos[c.matricula]
        texto = textos[c.matricula]

        vel = c.velocidad * 0.05
        ang = math.radians(c.rumbo)

        dx = vel * math.cos(ang)
        dy = vel * math.sin(ang)

        canvas.move(rect, dx, dy)
        canvas.move(texto, dx, dy)

        x1, y1, x2, y2 = canvas.coords(rect)

        # Mantener dentro de pantalla
        if x1 < 0: canvas.move(rect, -x1, 0); canvas.move(texto, -x1, 0)
        if y1 < 0: canvas.move(rect, 0, -y1); canvas.move(texto, 0, -y1)
        if x2 > 800: canvas.move(rect, 800-x2, 0); canvas.move(texto, 800-x2, 0)
        if y2 > 650: canvas.move(rect, 0, 650-y2); canvas.move(texto, 0, 650-y2)

    canvas.after(50, animar)

animar()
root.mainloop()
