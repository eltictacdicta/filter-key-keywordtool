import csv
import codecs

def filtrar_keywords(input_file, output_file):
    with codecs.open(input_file, mode='r', encoding='utf-8-sig') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        print("Columnas disponibles:", fieldnames)  # Imprime los nombres de las columnas
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            # Verifica que no haya campos vacíos o None
            if all(field in row and row[field] for field in fieldnames):
                palabra_clave = row['Palabra clave'].replace(',', ' ')  # Elimina las comas
                if len(palabra_clave) < 80 and len(palabra_clave.split()) < 10:
                    row['Palabra clave'] = palabra_clave
                    writer.writerow(row)

input_file = 'keywords.csv'
output_file = 'keywords-filter.csv'
filtrar_keywords(input_file, output_file)