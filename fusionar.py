import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime

def browse_file(entry_widget, file_type):
    if file_type == "csv":
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    elif file_type == "xlsx":
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    else:
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def fusionar_datos(bwmt_file, ubs_file, kwt_file):
    if not bwmt_file or (not ubs_file and not kwt_file):
        messagebox.showerror("Error", "Debe seleccionar al menos dos archivos diferentes para fusionar.")
        return
        
    try:
        bwmt_df = pd.read_csv(bwmt_file, delimiter=',', on_bad_lines='skip')
        fuente = bwmt_df['Fuente'].iloc[0] if 'Fuente' in bwmt_df.columns else 'SinFuente'
        
        merged_df = bwmt_df.copy()
        herramienta = None

        if ubs_file:
            ubs_df = pd.read_csv(ubs_file, delimiter=',', on_bad_lines='skip')
            ubs_df.rename(columns={
                'Palabra clave': 'Palabra clave',
                'Volumen de búsquedas': 'Volumen de búsquedas',
                'CPC': 'CPC',
                'Competition': 'Competition',
                'Paid Difficulty': 'Paid Difficulty',
                'SEO Difficulty': 'SEO Difficulty'
            }, inplace=True)
            ubs_df['CPC'] = ubs_df['CPC'].replace({'€': '', ',': '.'}, regex=True).astype(float)
            merged_df = pd.merge(merged_df, ubs_df, on='Palabra clave', how='outer')
            herramienta = 'Ubersuggest'
            
        if kwt_file:
            kwt_df = pd.read_excel(kwt_file, engine='openpyxl')
            kwt_df.rename(columns={
                'Keywords': 'Palabra clave',
                'Search Volume (Average)': 'Volumen de búsquedas',
                'Average CPC (EUR)': 'CPC',
                'Competition': 'Competition'
            }, inplace=True)
            kwt_df['CPC'] = kwt_df['CPC'].replace({'€': '', ',': '.'}, regex=True).astype(float)
            kwt_df['Paid Difficulty'] = kwt_df['Competition']
            kwt_df['SEO Difficulty'] = pd.NA
            merged_df = pd.merge(merged_df, kwt_df, on='Palabra clave', how='outer')
            herramienta = 'KeywordTool.io'
        
        merged_df['Herramienta'] = herramienta

        # Seleccionar solo las columnas relevantes
        columnas_relevantes = ['Palabra clave', 'Volumen de búsquedas', 'CPC', 'Competition', 'Paid Difficulty', 'SEO Difficulty', 'Fuente', 'Herramienta']
        merged_df = merged_df[columnas_relevantes]

        fecha_actual = datetime.now().strftime("%Y%m%d")
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV Files", "*.csv")],
                                                 initialfile=f"{fuente}-{herramienta}-{fecha_actual}.csv")

        if save_path:
            merged_df.to_csv(save_path, index=False)
            messagebox.showinfo("Éxito", "Archivo fusionado guardado exitosamente.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al fusionar los archivos: {str(e)}")

def fusionar():
    root = tk.Tk()
    root.title("Fusionar Datos")
    root.geometry("700x400")
    
    title_label = tk.Label(root, text="Fusionar Datos BWMT/GSC, Ubersuggest y KeywordTool.io", font=("Helvetica", 16))
    title_label.pack(pady=20)
    
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=10)
    
    tk.Label(frame, text="Datos BWMT/GSC:", font=("Helvetica", 12)).grid(row=0, column=0, pady=(0, 10), sticky="e")
    entry_bwmt = tk.Entry(frame, width=50)
    entry_bwmt.grid(row=0, column=1, pady=(0, 10))
    tk.Button(frame, text="Browse", command=lambda: browse_file(entry_bwmt, "csv")).grid(row=0, column=2, pady=(0, 10))
    
    tk.Label(frame, text="Datos Ubersuggest:", font=("Helvetica", 12)).grid(row=1, column=0, pady=(0, 10), sticky="e")
    entry_ubs = tk.Entry(frame, width=50)
    entry_ubs.grid(row=1, column=1, pady=(0, 10))
    tk.Button(frame, text="Browse", command=lambda: browse_file(entry_ubs, "csv")).grid(row=1, column=2, pady=(0, 10))
    
    tk.Label(frame, text="Datos KeywordTool.io:", font=("Helvetica", 12)).grid(row=2, column=0, pady=(0, 10), sticky="e")
    entry_kwt = tk.Entry(frame, width=50)
    entry_kwt.grid(row=2, column=1, pady=(0, 10))
    tk.Button(frame, text="Browse", command=lambda: browse_file(entry_kwt, "xlsx")).grid(row=2, column=2, pady=(0, 10))
    
    tk.Button(frame, text="Fusionar", font=("Helvetica", 12), command=lambda: fusionar_datos(entry_bwmt.get(), entry_ubs.get(), entry_kwt.get())).grid(row=3, column=1, pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    fusionar()