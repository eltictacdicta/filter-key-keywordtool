import csv
import codecs
import re
import unidecode


def eliminar_caracteres_invalidos(palabra_clave):
    # Definir los caracteres válidos permitidos por AdWords
    caracteres_validos = r'\w\s!@#$%^&*()_\-+=~`|{}[\]:;"\'<>,.?/'
    
    # Eliminar acentos de la palabra clave
    palabra_clave_sin_acentos = unidecode.unidecode(palabra_clave)
    
    # Reemplazar caracteres inválidos con un espacio
    palabra_clave_limpia = re.sub(r'[^' + caracteres_validos + ']', ' ', palabra_clave_sin_acentos)
    
    return palabra_clave_limpia

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

                palabra_clave = eliminar_caracteres_invalidos(row['Palabra clave'])
                if (len(palabra_clave) < 80 and 
                    len(palabra_clave.split()) < 10 and
                    '+' not in palabra_clave and 
                    ':' not in palabra_clave):
                    row['Palabra clave'] = palabra_clave
                    writer.writerow(row)

input_file = 'keywords.csv'
output_file = 'keywords-filter.csv'
filtrar_keywords(input_file, output_file)