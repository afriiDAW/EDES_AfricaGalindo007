# personajes_tk_v2.py
# GUI con Tkinter para manejar Personajes:
# - Selector de personaje, botones (Saltar, Disparar, Medicina, Posicion, Informacion)
# - Crear nuevo personaje con diálogo
# - Dibujos en Canvas + info al lado
# - Música de fondo y sonido de disparo (con archivos.mp3 y pygame)
#  Para instalar pygame:  pip install pygame

import os
import tkinter as tk
from tkinter import ttk, messagebox

# ==== AUDIO (opcional) ========================================================
USE_AUDIO = False
SHOOT_SOUND = None

def init_audio():
    """Inicializa audio si pygame está disponible y hay archivos."""
    global USE_AUDIO, SHOOT_SOUND
    try:
        import pygame
        pygame.mixer.init()
        if os.path.exists("bg_music.mp3"):
            pygame.mixer.music.load("bg_music.mp3")
            pygame.mixer.music.play(-1)  # bucle infinito
        if os.path.exists("shoot.mp3"):
            SHOOT_SOUND = pygame.mixer.Sound("shoot.mp3")
        USE_AUDIO = True
    except Exception:
        USE_AUDIO = False  # sin audio, pero la app sigue

def play_shoot():
    if USE_AUDIO and SHOOT_SOUND is not None:
        try:
            SHOOT_SOUND.play()
        except Exception:
            pass

# ==== MODELO =================================================================
class Personaje:
    def __init__(self, nombre, vidas, flechas, posicionX, posicionY):
        self.nombre = nombre
        self.vidas = vidas
        self.flechas = flechas
        self.posicionX = posicionX
        self.posicionY = posicionY

    def __str__(self):
        return (f"IES RAFAEL ALBERTI Personaje(nombre='{self.nombre}', vidas={self.vidas}, "
                f"flechas={self.flechas}, posicionX={self.posicionX}, "
                f"posicionY={self.posicionY})")

    def medicina(self):
        self.vidas += 1

    def saltar(self, delta_y: int = 30) -> int:
        """
        Incrementa temporalmente Y en +delta_y.
        Devuelve el Y original para que el llamador pueda restaurarlo luego.
        (La temporización/animación la gestiona la GUI).
        """
        y_original = self.posicionY
        self.posicionY += delta_y
        return y_original

    def disparar(self):
        if self.flechas > 0:
            self.flechas -= 1
            return True
        return False

# ==== VISTA / CONTROL =========================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personajes - Videojuego 1º DAM - EDES")
        self.geometry("980x540")
        self.resizable(False, False)

        # Estado
        self.personajes = []        # lista de Personaje
        self.canvas_items = {}      # Personaje -> dict(icon, label)
        self.selected: Personaje | None = None

        # UI
        self._build_ui()

        # Demo: dos personajes iniciales
        self._add_personaje(Personaje("Ana", 3, 2, 50, 100), color="#4CAF50")
        self._add_personaje(Personaje("Luis", 2, 0, 200, 220), color="#2196F3")

        # Audio opcional
        init_audio()

    # ---------- UI ----------
    def _build_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Panel lateral (controles)
        sidebar = ttk.Frame(self, padding=10)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_rowconfigure(99, weight=1)

        ttk.Label(sidebar, text="Personaje activo:").grid(row=0, column=0, sticky="w")
        self.cbo = ttk.Combobox(sidebar, state="readonly", width=24)
        self.cbo.grid(row=1, column=0, pady=5, sticky="w")
        self.cbo.bind("<<ComboboxSelected>>", self.on_select)

        ttk.Separator(sidebar).grid(row=2, column=0, pady=8, sticky="ew")

        # Línea de acciones principales
        ttk.Button(sidebar, text="Saltar (Y temporal +)", command=self.on_saltar).grid(row=3, column=0, pady=4, sticky="ew")
        ttk.Button(sidebar, text="Disparar (flecha)", command=self.on_disparar).grid(row=4, column=0, pady=4, sticky="ew")
        ttk.Button(sidebar, text="Medicina (+1 vida)", command=self.on_medicina).grid(row=5, column=0, pady=4, sticky="ew")

        ttk.Separator(sidebar).grid(row=6, column=0, pady=8, sticky="ew")

        # Movimiento manual X/Y
        move_frame = ttk.LabelFrame(sidebar, text="Mover posición")
        move_frame.grid(row=7, column=0, pady=6, sticky="ew")

        ttk.Button(move_frame, text="X -", command=lambda: self.on_mover(dx=-10, dy=0)).grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        ttk.Button(move_frame, text="X +", command=lambda: self.on_mover(dx=+10, dy=0)).grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        ttk.Button(move_frame, text="Y -", command=lambda: self.on_mover(dx=0, dy=+10)).grid(row=1, column=0, padx=3, pady=3, sticky="ew")
        ttk.Button(move_frame, text="Y +", command=lambda: self.on_mover(dx=0, dy=-10)).grid(row=1, column=1, padx=3, pady=3, sticky="ew")

        ttk.Separator(sidebar).grid(row=8, column=0, pady=8, sticky="ew")

        # Info y crear nuevo
        ttk.Button(sidebar, text="Mostrar info (__str__)", command=self.on_mostrar_info).grid(row=9, column=0, pady=4, sticky="ew")
        ttk.Button(sidebar, text="Nuevo personaje...", command=self.on_new_personaje).grid(row=10, column=0, pady=6, sticky="ew")

        # Lienzo de juego
        self.canvas = tk.Canvas(self, bg="#1e1e1e", width=780, height=520, highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        # Ayuda
        ttk.Label(sidebar, text="Consejos:\n- Selecciona un personaje.\n- Usa los botones.\n- 'Saltar' sube Y y vuelve.\n- X± / Y± mueven la posición.",
                  foreground="#555").grid(row=98, column=0, sticky="sw")

    # ---------- Helpers ----------
    def _world_to_canvas(self, x, y):
        return x, y

    def _draw_personaje(self, p: Personaje, color="#FFC107"):
        x, y = self._world_to_canvas(p.posicionX, p.posicionY)
        r = 18  # radio del icono

        items = self.canvas_items.get(p)
        if items is None:
            body = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
            head = self.canvas.create_oval(x - r//2, y - r - 8, x + r//2, y - r + 8, fill="white", outline="")
            info = self.canvas.create_text(
                x + r + 8, y,
                anchor="w",
                fill="white",
                font=("Segoe UI", 10, "bold"),
                text=self._info_text(p)
            )
            self.canvas_items[p] = {"body": body, "head": head, "info": info, "color": color}
        else:
            dx = x - self._center(items["body"])[0]
            dy = y - self._center(items["body"])[1]
            self.canvas.move(items["body"], dx, dy)
            self.canvas.move(items["head"], dx, dy)
            self.canvas.coords(items["info"], x + r + 8, y)
            self.canvas.itemconfigure(items["info"], text=self._info_text(p))

        # Resalta el seleccionado
        for pj, it in self.canvas_items.items():
            outline = "#FFD54F" if pj is self.selected else ""
            width = 3 if pj is self.selected else 0
            self.canvas.itemconfigure(it["body"], outline=outline, width=width)

    def _center(self, item_id):
        x1, y1, x2, y2 = self.canvas.coords(item_id)
        return (x1 + x2) / 2, (y1 + y2) / 2

    def _info_text(self, p: Personaje):
        return f"{p.nombre}\nPos:({p.posicionX},{p.posicionY})  Vidas:{p.vidas}  Flechas:{p.flechas}"

    def _refresh_all(self):
        for p in self.personajes:
            self._draw_personaje(p, self.canvas_items.get(p, {}).get("color", "#FFC107"))

    def _add_personaje(self, p: Personaje, color="#FFC107"):
        self.personajes.append(p)
        self.canvas_items[p] = None
        self._draw_personaje(p, color=color)
        self.cbo["values"] = [pj.nombre for pj in self.personajes]
        if not self.selected:
            self.selected = p
            self.cbo.set(p.nombre)
        self._refresh_all()

    def _find_by_name(self, name: str) -> Personaje | None:
        for p in self.personajes:
            if p.nombre == name:
                return p
        return None

    # ---------- Eventos ----------
    def on_select(self, _evt=None):
        pj = self._find_by_name(self.cbo.get())
        if pj:
            self.selected = pj
            self._refresh_all()

    def on_saltar(self):
        if not self.selected:
            messagebox.showinfo("Info", "Selecciona un personaje.")
            return
        # Lógica: saltar incrementa Y temporalmente, luego vuelve
        y_original = self.selected.saltar(delta_y=-30)
        self._draw_personaje(self.selected, self.canvas_items[self.selected]["color"])
        # Revertimos tras 250 ms
        self.after(250, self._fin_salto, self.selected, y_original)

    def _fin_salto(self, pj: Personaje, y_original: int):
        # Si el personaje sigue existiendo, restauramos su Y
        if pj in self.personajes:
            pj.posicionY = y_original
            self._draw_personaje(pj, self.canvas_items[pj]["color"])

    def on_medicina(self):
        if not self.selected:
            messagebox.showinfo("Info", "Selecciona un personaje.")
            return
        self.selected.medicina()
        self._draw_personaje(self.selected, self.canvas_items[self.selected]["color"])

    def on_disparar(self):
        if not self.selected:
            messagebox.showinfo("Info", "Selecciona un personaje.")
            return
        ok = self.selected.disparar()
        if ok:
            play_shoot()
        else:
            messagebox.showwarning("Sin flechas", f"{self.selected.nombre} no tiene flechas.")
        self._draw_personaje(self.selected, self.canvas_items[self.selected]["color"])

    def on_mover(self, dx=0, dy=0):
        if not self.selected:
            messagebox.showinfo("Info", "Selecciona un personaje.")
            return
        self.selected.posicionX += dx
        self.selected.posicionY += dy
        self._draw_personaje(self.selected, self.canvas_items[self.selected]["color"])

    def on_mostrar_info(self):
        if not self.selected:
            messagebox.showinfo("Info", "Selecciona un personaje.")
            return
        messagebox.showinfo("Información del personaje", str(self.selected))

    def on_new_personaje(self):
        dlg = NuevoPersonajeDialog(self)
        self.wait_window(dlg)
        if dlg.result is None:
            return
        nombre, vidas, flechas, x, y, color = dlg.result
        if any(p.nombre == nombre for p in self.personajes):
            messagebox.showerror("Error", "Ya existe un personaje con ese nombre.")
            return
        p = Personaje(nombre, vidas, flechas, x, y)
        self._add_personaje(p, color=color)

# ==== DIÁLOGO CREAR PERSONAJE ================================================
class NuevoPersonajeDialog(tk.Toplevel):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.title("Nuevo personaje")
        self.resizable(False, False)
        self.result = None

        frm = ttk.Frame(self, padding=10)
        frm.grid()

        self.var_nombre = tk.StringVar()
        self.var_vidas = tk.StringVar(value="3")
        self.var_flechas = tk.StringVar(value="2")
        self.var_x = tk.StringVar(value="120")
        self.var_y = tk.StringVar(value="120")
        self.var_color = tk.StringVar(value="#FF7043")

        r = 0
        ttk.Label(frm, text="Nombre:").grid(row=r, column=0, sticky="e", padx=4, pady=4); r += 1
        ttk.Entry(frm, textvariable=self.var_nombre, width=24).grid(row=r-1, column=1, padx=4, pady=4)

        ttk.Label(frm, text="Vidas:").grid(row=r, column=0, sticky="e", padx=4, pady=4); r += 1
        ttk.Entry(frm, textvariable=self.var_vidas, width=10).grid(row=r-1, column=1, padx=4, pady=4, sticky="w")

        ttk.Label(frm, text="Flechas:").grid(row=r, column=0, sticky="e", padx=4, pady=4); r += 1
        ttk.Entry(frm, textvariable=self.var_flechas, width=10).grid(row=r-1, column=1, padx=4, pady=4, sticky="w")

        ttk.Label(frm, text="Posición X:").grid(row=r, column=0, sticky="e", padx=4, pady=4); r += 1
        ttk.Entry(frm, textvariable=self.var_x, width=10).grid(row=r-1, column=1, padx=4, pady=4, sticky="w")

        ttk.Label(frm, text="Posición Y:").grid(row=r, column=0, sticky="e", padx=4, pady=4); r += 1
        ttk.Entry(frm, textvariable=self.var_y, width=10).grid(row=r-1, column=1, padx=4, pady=4, sticky="w")

        ttk.Label(frm, text="Color (#RRGGBB):").grid(row=r, column=0, sticky="e", padx=4, pady=4); r += 1
        ttk.Entry(frm, textvariable=self.var_color, width=12).grid(row=r-1, column=1, padx=4, pady=4, sticky="w")

        btns = ttk.Frame(frm)
        btns.grid(row=r, column=0, columnspan=2, pady=10)
        ttk.Button(btns, text="Crear", command=self._ok).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="Cancelar", command=self.destroy).grid(row=0, column=1, padx=5)

        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _ok(self):
        from tkinter import messagebox
        try:
            nombre = self.var_nombre.get().strip()
            if not nombre:
                raise ValueError("Nombre vacío")
            vidas = int(self.var_vidas.get())
            flechas = int(self.var_flechas.get())
            x = int(self.var_x.get())
            y = int(self.var_y.get())
            color = self.var_color.get().strip() or "#FF7043"
        except Exception:
            messagebox.showerror("Error", "Revisa los campos: nombre (texto) y números enteros válidos.")
            return
        self.result = (nombre, vidas, flechas, x, y, color)
        self.destroy()

# ==== MAIN ===================================================================
if __name__ == "__main__":
    App().mainloop()
