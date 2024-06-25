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

def formatear_ctr(valor):
    try:
        return f"{float(valor.replace('%', '')):.2f}"
    except ValueError:
        return valor

def filtrar_keywords(input_file, output_file, search_engine):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)

        if search_engine == "Google":
            column_name = 'Consultas principales'
            posicion_column_name = 'Posición'
        elif search_engine == "Bing":
            column_name = 'Palabra clave'
            posicion_column_name = 'Posición media'
        else:
            messagebox.showerror("Error", "Fuente de búsqueda no soportada")
            return

        if column_name not in reader.fieldnames:
            messagebox.showerror("Error", f"La columna '{column_name}' no se encontró en el archivo")
            return

        if posicion_column_name not in reader.fieldnames:
            messagebox.showerror("Error", f"La columna '{posicion_column_name}' no se encontró en el archivo")
            return

        fieldnames = ['Palabra clave', 'Impresiones', 'Clics', 'CTR', 'Posición']
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
                        'Impresiones': row.get('Impresiones', ''),
                        'Clics': row.get('Clics', ''),
                        'CTR': formatear_ctr(row.get('CTR', '')),
                        'Posición': formatear_valor(row.get(posicion_column_name, ''))
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
            return
        
        filtrar_keywords(input_file, output_file, search_engine)

    app = tk.Toplevel()
    app.title('Filtrador de Keywords')
    app.geometry('600x400')
    app.configure(bg='#e0e0e0')

    frame = tk.Frame(app, bg='#e0e0e0')
    frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    label_file_path = tk.Label(frame, text="Archivo CSV", bg='#e0e0e0')
    entry_file_path = tk.Entry(frame, width=50)
    button_browse = tk.Button(frame, text="Buscar", command=seleccionar_archivo)
    label_search_engine = tk.Label(frame, text="Fuente de búsqueda", bg='#e0e0e0')
    search_engine_var = tk.StringVar(value="Google")
    search_engine_options = ["Google", "Bing", "Otros"]
    dropdown_search_engine = tk.OptionMenu(frame, search_engine_var, *search_engine_options)

    button_process = tk.Button(frame, text="Procesar", command=procesar_archivo)

    label_file_path.grid(row=0, column=0, padx=5, pady=5)
    entry_file_path.grid(row=0, column=1, padx=5, pady=5)
    button_browse.grid(row=0, column=2, padx=5, pady=5)

    label_search_engine.grid(row=1, column=0, padx=5, pady=5)
    dropdown_search_engine.grid(row=1, column=1, padx=5, pady=5)

    button_process.grid(row=2, column=0, columnspan=3, pady=20)

    app.mainloop()