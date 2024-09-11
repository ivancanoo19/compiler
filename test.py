import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class Lexer:
    def __init__(self, file_path):
        # Abrimos el archivo y leemos su contenido
        with open(file_path, 'r') as file:
            self.source_code = file.read()

        # Definición de patrones de tokens
        self.token_patterns = [
            ('KEYWORD', r'\b(int|if|else|return|for)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUMBER', r'\d+(\.\d*)?'),
            ('LITERAL', r'"[^"]*"'),
            ('OPERATOR', r'[+*/=<>-]'),
            ('DELIMITER', r'[{}();,]'),
            ('COMMENT', r'//.|/\[\s\S]?\/'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
        ]

    def tokenize(self):
        # Eliminamos comentarios de una o más líneas antes de procesarlo por completo.
        self.source_code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', self.source_code)

        # Dividimos el código fuente en varías líneas, cada línea será procesada.
        lines = self.source_code.split('\n')
        
        # Lista para almacenar los tokens y mostrarlos
        tokens = []
        for line in lines:
            # Linea actual
            line = line.strip()     # split elimina los espacios al inicio y al final de la línea
            if not line:
                continue    # Si encuentra lineas vacías, las ignoramos y continuamos

            # A continuación, procesamos cada linea actual hasta que ya
            # no tengamos más lineas que procesar
            while line:
                match = None  # Variable para saber si hicimos match
                
                # Desempaquetamos la lista de tuplas para acceder a cada elemento (tipo, valor) y la recorremos
                for token_type, pattern in self.token_patterns:
                    # re.match para intentar hacer coincidir el patrón con el inicio de la línea
                    match = re.match(pattern, line)
                    
                    if match:
                        # Si el token es un espacio en blanco o salto de línea, lo ignoramos.
                        # Si pertenece a otro tipo de token
                        lexeme = match.group(0)
                        if token_type not in ['SKIP', 'NEWLINE']:
                            # Agregamos el token encontrado a la lista de tokens
                            tokens.append((token_type, lexeme))
                        
                        # Avanzamos a la siguiente parte de la línea eliminando el lexema procesado
                        line = line[len(lexeme):]
                        break

                if not match:
                    # Mostrar mensaje de error o manejar el caso cuando no hay coincidencias
                    print(f"Token no reconocido: {line}")
                    break
        return tokens

# Función para abrir el diálogo y seleccionar el archivo
def seleccionar_archivo():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter y no se vea feo
    archivo = askopenfilename(title="Selecciona el archivo de código para analizar",
                              filetypes=[("Archivos de texto", "*.c *.txt"), ("Todos los archivos", "*.*")])
    return archivo

# Seleccionar el archivo con ventana gráfica que envia a archivos para seleccionar uno compatible
archivo_seleccionado = seleccionar_archivo()

if archivo_seleccionado:
    lexer = Lexer(archivo_seleccionado)
    tokens = lexer.tokenize()
    for t in tokens:
        print(t)
else:
    print("No se seleccionó ningún archivo.")
