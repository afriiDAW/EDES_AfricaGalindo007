import tkinter as tk
from tkinter import messagebox
import pygame
from math import cos, sin, radians
from barco import Barco  

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Barcos")
        self.root.geometry("800x600")

        # Inicializar pygame para sonidos
        pygame.mixer.init()
        pygame.mixer.music.load("bg_music.mp3")  # Música de fondo
        pygame.mixer.music.play(-1)
        self.sonido_disparo = pygame.mixer.Sound("shoot.mp3")

        self.canvas = tk.Canvas(root, bg="lightblue", width=600, height=400)
        self.canvas.pack(pady=10)

        self.barcos = []
        self.barco_activo = None

        tk.Button(root, text="Crear Barco", command=self.crear_barco).pack(pady=5)
        self.selector = tk.StringVar()
        self.menu_barcos = tk.OptionMenu(root, self.selector, ())
        self.menu_barcos.pack(pady=5)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Disparar", command=self.disparar).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Aumentar Velocidad", command=lambda: self.cambiar_velocidad(1)).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Disminuir Velocidad", command=lambda: self.cambiar_velocidad(-1)).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Cambiar Rumbo", command=self.cambiar_rumbo).grid(row=0, column=3, padx=5)

        self.actualizar_posiciones()

    def crear_barco(self):
        nombre = f"Barco{len(self.barcos) + 1}"
        nuevo = Barco(nombre)
        self.barcos.append(nuevo)
        self.selector.set(nombre)
        self.actualizar_selector()
        self.barco_activo = nuevo
        print(f"{nombre} creado")

    def actualizar_selector(self):
        menu = self.menu_barcos["menu"]
        menu.delete(0, "end")
        for b in self.barcos:
            menu.add_command(label=b.nombre, command=lambda n=b.nombre: self.seleccionar_barco(n))

    def seleccionar_barco(self, nombre):
        for b in self.barcos:
            if b.nombre == nombre:
                self.barco_activo = b
                self.selector.set(nombre)
                break

    def disparar(self):
        if self.barco_activo:
            self.barco_activo.disparar()
            self.sonido_disparo.play()
        else:
            messagebox.showwarning("Atención", "No hay barco activo")

    def cambiar_velocidad(self, delta):
        if self.barco_activo:
            nueva = self.barco_activo.velocidad + delta
            self.barco_activo.setVelocidad(nueva)
        else:
            messagebox.showwarning("Atención", "Selecciona un barco")

    def cambiar_rumbo(self):
        if self.barco_activo:
            nuevo = (self.barco_activo.rumbo + 45) % 360
            self.barco_activo.setRumbo(nuevo)
        else:
            messagebox.showwarning("Atención", "Selecciona un barco")

    def actualizar_posiciones(self):
        self.canvas.delete("all")
        for b in self.barcos:
            b.posicionX += cos(radians(b.rumbo)) * (b.velocidad / 5)
            b.posicionY += sin(radians(b.rumbo)) * (b.velocidad / 5)
            self.canvas.create_oval(b.posicionX, b.posicionY, b.posicionX + 20, b.posicionY + 20, fill="navy")
            self.canvas.create_text(b.posicionX + 10, b.posicionY - 10, text=b.nombre, fill="black")
        self.root.after(100, self.actualizar_posiciones)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
