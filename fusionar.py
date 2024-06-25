import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def create_ui():
    root = tk.Tk()
    root.title("Fusionar Datos")
    root.geometry("700x250")
    
    # Título Principal
    title_label = tk.Label(root, text="Fusionar Datos BWMT/GSC y Ubersuggest", font=("Helvetica", 16))
    title_label.pack(pady=20)
    
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=10)

    # Campo para subir el archivo BWMT o GSC
    tk.Label(frame, text="Datos BWMT/GSC:", font=("Helvetica", 12)).grid(row=0, column=0, pady=(0, 10), sticky="e")
    entry_bwmt_us = tk.Entry(frame, width=50)
    entry_bwmt_us.grid(row=0, column=1, pady=(0, 10))
    tk.Button(frame, text="Browse", command=lambda: browse_file_us(entry_bwmt_us, "csv")).grid(row=0, column=2, pady=(0, 10))

    # Campo para subir el archivo Ubersuggest
    tk.Label(frame, text="Datos Ubersuggest:", font=("Helvetica", 12)).grid(row=1, column=0, pady=(0, 10), sticky="e")
    entry_ubersuggest = tk.Entry(frame, width=50)
    entry_ubersuggest.grid(row=1, column=1, pady=(0, 10))
    tk.Button(frame, text="Browse", command=lambda: browse_file_us(entry_ubersuggest, "csv")).grid(row=1, column=2, pady=(0, 10))

    # Botón para fusionar los datos
    tk.Button(frame, text="Fusionar", font=("Helvetica", 12), command=lambda: fusionar_datos_us(entry_bwmt_us.get(), entry_ubersuggest.get())).grid(row=2, column=1, pady=20)

def browse_file_us(entry_widget, file_type):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", f"*.{file_type}")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def fusionar_datos_us(bwmt_file, ubersuggest_file):
    if not bwmt_file or not ubersuggest_file:
        messagebox.showerror("Error", "Ambos archivos deben ser seleccionados")
        return

    try:
        bwmt_df = pd.read_csv(bwmt_file, delimiter=',', on_bad_lines='skip')
        ubersuggest_df = pd.read_csv(ubersuggest_file, delimiter=',', on_bad_lines='skip')

        # Renombrar columnas para asegurar la consistencia
        ubersuggest_df.rename(columns={
            'No': 'No',
            'Palabra clave': 'Palabra clave',
            'Volumen de búsquedas': 'Volumen de búsquedas',
            'CPC': 'CPC',
            'Competition': 'Competition',
            'Paid Difficulty': 'Paid Difficulty',
            'SEO Difficulty': 'SEO Difficulty'
        }, inplace=True)

        # Verificar la existencia de la columna 'Palabra clave'
        if 'Palabra clave' not in bwmt_df.columns or 'Palabra clave' not in ubersuggest_df.columns:
            raise ValueError("La columna 'Palabra clave' no se encuentra en uno de los archivos.")

        # Convertir columna CPC de formato €0,00 a 0.00
        ubersuggest_df['CPC'] = ubersuggest_df['CPC'].replace({'€': '', ',': '.'}, regex=True).astype(float)

        # Fusionar los datos
        merged_df = pd.merge(bwmt_df, ubersuggest_df, on='Palabra clave', how='outer')

        # Eliminar la columna 'No' si existe
        if 'No' in merged_df.columns:
            merged_df.drop(columns=['No'], inplace=True)

        # Preguntar la ruta para guardar el archivo fusionado
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        
        # Guardar el DataFrame fusionado como CSV
        if save_path:
            merged_df.to_csv(save_path, index=False)
            messagebox.showinfo("Éxito", "Archivo fusionado guardado exitosamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al fusionar los archivos: {str(e)}")

def main():
    create_ui()
    tk.mainloop()

if __name__ == "__main__":
    main()
