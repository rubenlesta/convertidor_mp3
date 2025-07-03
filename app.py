import tkinter as tk
from tkinter import messagebox
import convertidor  # Importa tu módulo directamente

def descargar():
    entrada = entrada_var.get().strip()
    if not entrada:
        messagebox.showwarning("Entrada vacía", "Por favor introduce una URL o título.")
        return

    estado.set("⏳ Descargando...")
    app.update()

    try:
        # Llama a la función descargar(entrada) de convertidor.py
        convertidor.descargar(entrada)
        estado.set("✅ Descarga completada.")
    except Exception as e:
        estado.set("❌ Error en la descarga.")
        messagebox.showerror("Error", f"La descarga ha fallado.\n{e}")

# Crear ventana principal
app = tk.Tk()
app.title("Descargador YouTube → MP3")
app.geometry("500x200")

# Entrada de texto
entrada_var = tk.StringVar()
tk.Label(app, text="Introduce una URL o título de canción:").pack(pady=5)
tk.Entry(app, textvariable=entrada_var, width=60).pack(pady=5)

# Botón de descarga
tk.Button(app, text="Descargar", command=descargar).pack(pady=10)

# Área de estado
estado = tk.StringVar()
estado.set("Esperando entrada...")
tk.Label(app, textvariable=estado).pack(pady=10)

# Iniciar interfaz
app.mainloop()
