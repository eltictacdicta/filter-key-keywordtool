import tkinter as tk
from filter import open_filter_window
from fusionar import open_fusionar_window_us

def launch_filter():
    open_filter_window()

def launch_fusionar():
    open_fusionar_window_us()

# Crear la ventana principal
root = tk.Tk()
root.title("Panel Principal")

# Frame principal
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# Botón para abrir el filtrador de keywords
filter_button = tk.Button(frame, text="Filtrar", command=launch_filter)
filter_button.pack(pady=10)

# Botón para abrir el panel de fusionar
fusionar_button = tk.Button(frame, text="Fusionar", command=launch_fusionar)
fusionar_button.pack(pady=10)

# Ejecuta el bucle principal de la ventana
root.mainloop()