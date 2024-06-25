import tkinter as tk
from filter import open_filter_window
from fusionar import fusionar

def launch_filter():
    open_filter_window()

def launch_fusionar():
    fusionar()

# Crear la ventana principal
root = tk.Tk()
root.title("Panel Principal")
root.geometry("300x200")  # Tamaño de la ventana
root.configure(bg="#f0f0f0")  # Color de fondo de la ventana

# Frame principal
frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
frame.grid(row=0, column=0, sticky="nsew")

# Configurar el grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Botón para abrir el filtrador de keywords
filter_button = tk.Button(frame, text="Filtrar", command=launch_filter, font=("Helvetica", 12), bg="#4CAF50", fg="white")
filter_button.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

# Botón para abrir el panel de fusionar
fusionar_button = tk.Button(frame, text="Fusionar", command=launch_fusionar, font=("Helvetica", 12), bg="#2196F3", fg="white")
fusionar_button.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

# Configurar el grid dentro del frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Ejecuta el bucle principal de la ventana
root.mainloop()
