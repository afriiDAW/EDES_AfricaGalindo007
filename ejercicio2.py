import tkinter as tk
from tkinter import messagebox

def celsius_a_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def convertir_temperatura():
    try:
        celsius = float(entry_temp.get())
        fahrenheit = celsius_a_fahrenheit(celsius)
        messagebox.showinfo("Resultado", f"{celsius}°C = {fahrenheit:.2f}°F")
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un valor numérico válido.")

def mostrar_tabla():
    try:
        numero = int(entry_tabla.get())
        tabla = "\n".join([f"{numero} x {i} = {numero * i}" for i in range(1, 11)])
        messagebox.showinfo(f"Tabla del {numero}", tabla)
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un número entero válido.")

def salir():
    ventana.destroy()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Menú principal")
ventana.geometry("350x300")
ventana.config(bg="#e3f2fd")

tk.Label(ventana, text="Conversión de temperatura (°C → °F)", bg="#e3f2fd").pack(pady=5)
entry_temp = tk.Entry(ventana)
entry_temp.pack()
tk.Button(ventana, text="Convertir", command=convertir_temperatura, bg="#64b5f6", fg="white").pack(pady=5)

tk.Label(ventana, text="Tabla de multiplicar", bg="#e3f2fd").pack(pady=10)
entry_tabla = tk.Entry(ventana)
entry_tabla.pack()
tk.Button(ventana, text="Mostrar tabla", command=mostrar_tabla, bg="#4db6ac", fg="white").pack(pady=5)

tk.Button(ventana, text="Salir", command=salir, bg="#ef5350", fg="white").pack(pady=15)

ventana.mainloop()
