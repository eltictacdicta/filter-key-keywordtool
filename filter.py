import csv
import codecs
import re
import unidecode
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def eliminar_caracteres_invalidos(palabra_clave):
    caracteres_validos = r'\w\s!@#$%^&*()_\-+=~`|{}[\]:;"\'<>,.?/'
    palabra_clave_sin_acentos = unidecode.unidecode(palabra_clave)
    palabra_clave_limpia = re.sub(r'[^' + caracteres_validos + ']', ' ', palabra_clave_sin_acentos)
    return palabra_clave_limpia

def formatear_valor(valor):
    try:
        if isinstance(valor, str) and '%' in valor:
            valor_decimal = float(valor.strip('%'))
            return f"{valor_decimal:.2f}%"
        else:
            valor_decimal = float(valor)
            return f"{valor_decimal:.2f}"
    except ValueError:
        return "Valor no válido"

def filtrar_keywords(input_file, output_file, search_engine):
    column_name = 'Palabra clave' if search_engine == 'Bing' else 'Consultas principales'
    posicion_column_name = 'Posición media' if search_engine == 'Bing' else 'Posición'

    with codecs.open(input_file, mode='r', encoding='utf-8-sig') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)

        if column_name not in reader.fieldnames:
            messagebox.showerror("Error", f"La columna '{column_name}' no se encontró en el archivo")
            return

        if not posicion_column_name:
            messagebox.showerror("Error", "No se encontró ninguna columna de posición en el archivo")
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
            return

        filtrar_keywords(input_file, output_file, search_engine)

    app = tk.Toplevel()
    app.title('Filtrador de Keywords')

    frame = tk.Frame(app)
    frame.pack(padx=20, pady=20, fill=tk.X)

    label_file_path = tk.Label(frame, text="Ruta del archivo CSV:")
    label_file_path.pack(pady=5, anchor='w')

    entry_file_path = tk.Entry(frame, width=60)
    entry_file_path.pack(pady=5, side=tk.LEFT, padx=(0, 10))

    button_browse = tk.Button(frame, text="Buscar", command=seleccionar_archivo)
    button_browse.pack(pady=5, side=tk.LEFT)

    frame_engine = tk.Frame(app)
    frame_engine.pack(padx=20, pady=20, fill=tk.X)

    label_search_engine = tk.Label(frame_engine, text="Motor de búsqueda:")
    label_search_engine.pack(pady=5, anchor='w')

    search_engine_var = tk.StringVar(value="Bing")
    radio_bing = tk.Radiobutton(frame_engine, text="Bing", variable=search_engine_var, value="Bing")
    radio_bing.pack(pady=5, side=tk.LEFT, padx=5)
    radio_google = tk.Radiobutton(frame_engine, text="Google", variable=search_engine_var, value="Google")
    radio_google.pack(pady=5, side=tk.LEFT, padx=5)

    button_process = tk.Button(app, text="Enviar", command=procesar_archivo)
    button_process.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana raíz
    open_filter_window()
    root.mainloop()

