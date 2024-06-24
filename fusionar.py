import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime

def open_fusionar_window_us():
    fusion_window = tk.Toplevel()
    fusion_window.title("Fusionar Datos")

    # Frame principal del panel de fusionar
    frame = tk.Frame(fusion_window, padx=20, pady=20)
    frame.pack()

    # Campo para subir el archivo BWMT o GSC
    label_bwmt_us = tk.Label(frame, text="Datos BWMT o GSC:")
    label_bwmt_us.grid(row=0, column=0, pady=(0, 5), sticky="e")
    entry_bwmt_us = tk.Entry(frame, width=50)
    entry_bwmt_us.grid(row=0, column=1, pady=(0, 5))
    button_bwmt_us = tk.Button(frame, text="Browse", command=lambda: browse_file_us(entry_bwmt_us, "csv"))
    button_bwmt_us.grid(row=0, column=2, pady=(0, 5))

    # Campo para subir el archivo Ubersuggest
    label_ubersuggest = tk.Label(frame, text="Datos Ubersuggest:")
    label_ubersuggest.grid(row=1, column=0, pady=(0, 5), sticky="e")
    entry_ubersuggest = tk.Entry(frame, width=50)
    entry_ubersuggest.grid(row=1, column=1, pady=(0, 5))
    button_ubersuggest = tk.Button(frame, text="Browse", command=lambda: browse_file_us(entry_ubersuggest, "csv"))
    button_ubersuggest.grid(row=1, column=2, pady=(0, 5))

    fusionar_button_us = tk.Button(frame, text="Fusionar", command=lambda: fusionar_datos_us(entry_bwmt_us.get(), entry_ubersuggest.get()))
    fusionar_button_us.grid(row=2, column=1, pady=10)

def browse_file_us(entry_widget, file_type):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", f"*.{file_type}")])
    entry_widget.delete(0)
    entry_widget.insert(0, file_path)

def fusionar_datos_us(bwmt_file, ubersuggest_file):
    if not bwmt_file or not ubersuggest_file:
        messagebox.showerror("Error", "Ambos archivos deben ser seleccionados")
        return
    
    try:
        # Leer archivo CSV de BWMT o GSC
        bwmt_df = pd.read_csv(bwmt_file, delimiter=',', on_bad_lines='skip')
        print(f"Columnas de BWMT/GSC: {bwmt_df.columns.tolist()}")

        # Leer archivo CSV de Ubersuggest
        ubersuggest_df = pd.read_csv(ubersuggest_file)
        ubersuggest_df = ubersuggest_df.rename(columns={
            'No': 'No',
            'Palabra clave': 'Palabra clave',
            'Volumen de búsquedas': 'Volumen de búsquedas',
            'CPC': 'CPC',
            'Competition': 'Competition',
            'Paid Difficulty': 'Paid Difficulty',
            'SEO Difficulty': 'SEO Difficulty'
        })
        print(f"Columnas originales de Ubersuggest: {ubersuggest_df.columns.tolist()}")

        # Asegurarse de que la columna 'Palabra clave' existe en ambos DataFrames
        if 'Palabra clave' not in bwmt_df.columns:
            raise ValueError("La columna 'Palabra clave' no se encuentra en el archivo BWMT/GSC.")
        if 'Palabra clave' not in ubersuggest_df.columns:
            raise ValueError("La columna 'Palabra clave' no se encuentra en el archivo Ubersuggest.")

        # Eliminar espacios en blanco de los nombres de columnas
        bwmt_df.columns = bwmt_df.columns.str.strip()
        ubersuggest_df.columns = ubersuggest_df.columns.str.strip()

        # Imprimir los nombres de las columnas para verificar
        print(f"Columnas finales de BWMT/GSC: {bwmt_df.columns.tolist()}")
        print(f"Columnas finales de Ubersuggest: {ubersuggest_df.columns.tolist()}")

        # Fusionar los datos
        merged_df = pd.merge(bwmt_df, ubersuggest_df, on='Palabra clave', how='outer')

        # Eliminar la columna 'No' si existe
        if 'No' in merged_df.columns:
            merged_df = merged_df.drop(columns=['No'])

        # Mostrar cuadro de diálogo para elegir la ubicación y el nombre del archivo guardado
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            # Guardar el archivo fusionado en la ruta seleccionada
            merged_df.to_csv(save_path, index=False)
            messagebox.showinfo("Éxito", f"Datos fusionados correctamente.\nArchivo guardado como: {save_path}")
        else:
            messagebox.showwarning("Cancelado", "Guardado de archivo cancelado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar los archivos: {e}")
