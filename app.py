import tkinter as tk
from tkinter import messagebox, ttk
import convertidor  # Tu módulo de descarga
import pygame  # Para reproducir música
import os
from tkinter import PhotoImage  # Para cargar la imagen de la flecha
from send2trash import send2trash  # Para mover archivos a la papelera

# Estilos globales (puedes cambiar estos valores fácilmente)
FONT_FAMILY = "Helvetica"
FONT_SIZE = 12
FONT_COLOR = "black"
BUTTON_FONT_SIZE = 12
BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2
BG_COLOR = "#f0f0f0"  # Fondo claro
BUTTON_COLOR = "#4CAF50"  # Color de fondo de los botones
BUTTON_COLOR_REPRODUCIR = "#2196F3"  # Color del botón de reproducir
BUTTON_COLOR_ELIMINAR = "red"  # Color del botón de eliminar
STATE_COLOR = "black"  # Color del texto de estado

# Inicializa pygame para reproducir música en segundo plano
pygame.mixer.init()

# Función para descargar música
def descargar():
    entrada = entrada_var.get().strip()
    if not entrada:
        messagebox.showwarning("Entrada vacía", "Por favor introduce una URL o título.")
        return

    estado.set("⏳ Descargando...")
    app.update()

    try:
        convertidor.descargar(entrada)
        estado.set("✅ Descarga completada.")
        actualizar_lista_canciones()
    except Exception as e:
        estado.set("❌ Error en la descarga.")
        messagebox.showerror("Error", f"La descarga ha fallado.\n{e}")

# Actualiza la lista de canciones descargadas
def actualizar_lista_canciones():
    canciones_lista.delete(*canciones_lista.get_children())
    for archivo in os.listdir("../mp3"):
        if archivo.endswith(".mp3"):
            # Asumiendo que el formato es "Artista - Canción"
            nombre_cancion = archivo.replace('.mp3', '')  # Eliminar la extensión .mp3

            # Separamos el artista y la canción
            if " - " in nombre_cancion:
                artista, cancion = nombre_cancion.split(" - ", 1)

                # Buscar "ft." o "featuring" y agregar ambos artistas
                if " ft." in artista.lower():
                    artista = artista.replace(" ft.", " ft.").replace(" Feat.", " ft.")
                elif "featuring" in artista.lower():
                    artista = artista.replace(" featuring", " ft.")
            else:
                artista, cancion = "Desconocido", nombre_cancion  # Si no tiene formato, ponlo como desconocido

            # Inserta en la lista con el nuevo formato de artista
            canciones_lista.insert("", "end", values=(artista, cancion))

# Reproduce la canción seleccionada
def reproducir_cancion():
    seleccion = canciones_lista.selection()
    if seleccion:
        cancion = canciones_lista.item(seleccion[0])['values'][1]  # Obtiene solo el nombre de la canción
        pygame.mixer.music.load(f"../mp3/{cancion}.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)

# Función de búsqueda
def buscar_canciones():
    query = busqueda_var.get().lower()
    for item in canciones_lista.get_children():
        values = canciones_lista.item(item, 'values')
        if query in values[0].lower() or query in values[1].lower():
            canciones_lista.item(item, open=True)
        else:
            canciones_lista.item(item, open=False)

# Función para ordenar la lista por columna
def ordenar_lista(columna):
    # Obtener los elementos actuales
    items = canciones_lista.get_children()
    # Ordenar los elementos
    items = sorted(items, key=lambda item: canciones_lista.item(item, 'values')[columna].lower())

    # Reinsertar los elementos ordenados
    for index, item in enumerate(items):
        canciones_lista.move(item, '', index)

# Función para eliminar canción de la lista y moverla a la papelera
def eliminar_cancion():
    seleccion = canciones_lista.selection()
    if seleccion:
        artista = canciones_lista.item(seleccion[0])['values'][0]
        cancion = canciones_lista.item(seleccion[0])['values'][1]

        # Concatenar artista y canción si el artista no es "Desconocido"
        if artista.lower() != "desconocido":
            nombre_archivo = f"{artista} - {cancion}.mp3"
        else:
            nombre_archivo = f"{cancion}.mp3"

        # Ruta completa del archivo
        archivo = os.path.join("../mp3", nombre_archivo)

        if os.path.exists(archivo):
            try:
                send2trash(archivo)  # Mover archivo a la papelera
                messagebox.showinfo("Eliminado", f"La canción {nombre_archivo} ha sido eliminada.")
                actualizar_lista_canciones()  # Actualizar lista después de eliminar
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la canción.\n{e}")
        else:
            messagebox.showerror("Error", f"No se encontró el archivo: {archivo}")

# Crear ventana principal
app = tk.Tk()
app.title("Ritmo Directo")
app.geometry("600x500")
app.configure(bg=BG_COLOR)  # Fondo uniforme claro

# Entrada de texto
entrada_var = tk.StringVar()
tk.Label(app, text="URL o título:", font=(FONT_FAMILY, FONT_SIZE), bg=BG_COLOR, fg=FONT_COLOR).pack(pady=10)
entrada = tk.Entry(app, textvariable=entrada_var, width=40, font=(FONT_FAMILY, FONT_SIZE))
entrada.pack(pady=5)
entrada.config(relief="solid", borderwidth=2, highlightthickness=2, highlightcolor="blue")

# Botón de descarga con esquinas redondeadas
descargar_btn = tk.Button(app, text="Descargar", command=descargar, font=(FONT_FAMILY, BUTTON_FONT_SIZE),
                          bg=BUTTON_COLOR, fg="white", relief="flat")
descargar_btn.pack(pady=15)
descargar_btn.config(borderwidth=0, relief="solid", highlightthickness=0, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

# Área de estado
estado = tk.StringVar()
estado.set("Esperando entrada...")
tk.Label(app, textvariable=estado, font=(FONT_FAMILY, FONT_SIZE), bg=BG_COLOR, fg=STATE_COLOR).pack(pady=10)

# Barra de búsqueda
busqueda_var = tk.StringVar()
busqueda_entrada = tk.Entry(app, textvariable=busqueda_var, width=40, font=(FONT_FAMILY, FONT_SIZE))
busqueda_entrada.pack(pady=10)

# Botón de búsqueda
buscar_btn = tk.Button(app, text="Buscar", command=buscar_canciones, font=(FONT_FAMILY, BUTTON_FONT_SIZE),
                       bg=BUTTON_COLOR_REPRODUCIR, fg="white", relief="flat")
buscar_btn.pack(pady=5)
buscar_btn.config(borderwidth=0, relief="solid", highlightthickness=0, width=10, height=2)

# Treeview para mostrar las canciones descargadas con dos columnas
tk.Label(app, text="Canciones descargadas:", font=(FONT_FAMILY, FONT_SIZE), bg=BG_COLOR, fg=FONT_COLOR).pack(pady=10)

canciones_lista = ttk.Treeview(app, columns=("Artista", "Canción"), show="headings", height=10)
canciones_lista.heading("Artista", text="Artista", command=lambda: ordenar_lista(0))
canciones_lista.heading("Canción", text="Canción", command=lambda: ordenar_lista(1))
canciones_lista.pack(pady=5)

# Frame para los botones de Reproducir, Actualizar y Eliminar
frame_botones = tk.Frame(app)
frame_botones.pack(pady=10)

# Botón para reproducir canción
reproducir_btn = tk.Button(frame_botones, text="Reproducir", command=reproducir_cancion, font=(FONT_FAMILY, BUTTON_FONT_SIZE),
                           bg=BUTTON_COLOR_REPRODUCIR, fg="white", relief="flat")
reproducir_btn.pack(side="left", padx=10)
reproducir_btn.config(borderwidth=0, relief="solid", highlightthickness=0, width=10, height=2)

# Botón de actualizar lista con una imagen de flecha
actualizar_img = PhotoImage(file="flecha.png")  # Asegúrate de tener una imagen llamada "flecha.png"
actualizar_btn = tk.Button(frame_botones, image=actualizar_img, command=actualizar_lista_canciones, relief="flat", bg=BUTTON_COLOR)
actualizar_btn.pack(side="left", padx=10)  # Ponemos el botón a la izquierda de "Reproducir"
actualizar_btn.config(width=30, height=30)  # Hacemos el botón más pequeño

# Botón de eliminar canción con un color rojo
eliminar_btn = tk.Button(frame_botones, text="Eliminar", command=eliminar_cancion, font=(FONT_FAMILY, BUTTON_FONT_SIZE),
                          bg=BUTTON_COLOR_ELIMINAR, fg="white", relief="flat")
eliminar_btn.pack(side="left", padx=10)
eliminar_btn.config(borderwidth=0, relief="solid", highlightthickness=0, width=10, height=2)

# Inicializa la lista de canciones al abrir la app
actualizar_lista_canciones()

# Iniciar la interfaz gráfica
app.mainloop()
