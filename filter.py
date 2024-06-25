import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import csv

def eliminar_caracteres_invalidos(palabra_clave):
    return ''.join(c for c in palabra_clave if c.isalnum() or c.isspace())

def formatear_valor(valor):
    try:
        return f"{float(valor):.2f}"
    except ValueError:
        return valor

def filtrar_keywords(input_file, output_file, search_engine, column_name='Palabra clave', posicion_column_name='Posición'):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)

        if column_name not in reader.fieldnames:
            messagebox.showerror("Error", f"La columna '{column_name}' no se encontró en el archivo")
            return

        if posicion_column_name not in reader.fieldnames:
            messagebox.showerror("Error", f"La columna '{posicion_column_name}' no se encontró en el archivo")
            return

        fieldnames = ['Palabra clave', 'Clics', 'Impresiones', 'CTR', 'Posición', 'Fuente']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if column_name in row and row[column_name]:
                palabra_clave = eliminar_caracteres_invalidos(row[column_name])
                if (len(palabra_clave) < 80 and 
                    len(palabra_clave.split()) < 10 and
                    '+' not in palabra_clave and 
                    ':' not in palabra_clave):
                    new_row = {
                        'Palabra clave': palabra_clave,
                        'Clics': row.get('Clics', ''),
                        'Impresiones': row.get('Impresiones', ''),
                        'CTR': formatear_valor(row.get('CTR', '')),
                        'Posición': formatear_valor(row.get(posicion_column_name, '')),
                        'Fuente': search_engine
                    }
                    writer.writerow(new_row)

    messagebox.showinfo("Éxito", "El archivo ha sido filtrado y guardado correctamente.")

def open_filter_window():
    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, archivo)

    def procesar_archivo():
        input_file = entry_file_path.get()
        if not input_file:
            messagebox.showerror("Error", "Debe seleccionar un archivo CSV")
            return

        search_engine = search_engine_var.get()
        fecha_actual = datetime.now().strftime("%Y%m%d")
        sugerido_nombre = f"Filtradas_{search_engine}_{fecha_actual}.csv"

        output_file = filedialog.asksaveasfilename(initialfile=sugerido_nombre, defaultextension=".csv",
                                                   filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not output_file:
            messagebox.showerror("Error", "Debe seleccionar una ubicación para guardar el archivo filtrado")
            return filtrar_keywords(input_file, output_file, search_engine)

    app = tk.Toplevel()
    app.title('Filtrador de Keywords')
    app.geometry('600x400')  # Establecer un tamaño fijo para la ventana
    app.configure(bg='#f0f0f0')  # Color de fondo de la ventana

    frame = tk.Frame(app, bg='#f0f0f0')
    frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    label_file_path = tk.Label(frame, text="Ruta del archivo CSV:", bg='#f0f0f0', fg='#333333')
    label_file_path.grid(row=0, column=0, pady=5, sticky='w')

    entry_file_path = tk.Entry(frame, width=60)
    entry_file_path.grid(row=1, column=0, pady=5, padx=(0, 10), sticky='w')

    button_browse = tk.Button(frame, text="Buscar", command=seleccionar_archivo, bg='#4CAF50', fg='white')
    button_browse.grid(row=1, column=1, pady=5, sticky='w')

    frame_engine = tk.Frame(app, bg='#f0f0f0')
    frame_engine.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

    label_search_engine = tk.Label(frame_engine, text="Motor de búsqueda:", bg='#f0f0f0', fg='#333333')
    label_search_engine.grid(row=0, column=0, pady=5, sticky='w')

    search_engine_var = tk.StringVar(value="Bing")
    radio_bing = tk.Radiobutton(frame_engine, text="Bing", variable=search_engine_var, value="Bing", bg='#f0f0f0', fg='#333333')
    radio_bing.grid(row=1, column=0, pady=5, padx=5, sticky='w')
    radio_google = tk.Radiobutton(frame_engine, text="Google", variable=search_engine_var, value="Google", bg='#f0f0f0', fg='#333333')
    radio_google.grid(row=1, column=1, pady=5, padx=5, sticky='w')

    button_process = tk.Button(app, text="Enviar", command=procesar_archivo, bg='#4CAF50', fg='white')
    button_process.grid(row=2, column=0, pady=20, sticky='s')

    # Configurar el comportamiento de las filas y columnas para que se expandan con la ventana
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana raíz
    open_filter_window()
    root.mainloop()