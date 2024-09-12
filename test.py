import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        # Definición de patrones de tokens
        self.token_patterns = [
            ('KEYWORD', r'\b(int|if|else|return|for)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUMBER', r'\d+(\.\d*)?'),
            ('LITERAL', r'"[^"]*"'),
            ('OPERATOR', r'[+*/=<>-]'),
            ('PUNCTUATION', r'[{}();,]'),
            ('COMMENT', r'//.|/\[\s\S]?\/'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
        ]
        # Inicializamos el contador de tokens por cada tipo
        self.token_count = {token_type: 0 for token_type, _ in self.token_patterns}

    def tokenize(self):
        # Eliminamos comentarios de una o más líneas antes de procesarlo por completo.
        self.source_code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', self.source_code)

        # Dividimos el código fuente en varias líneas, cada línea será procesada.
        lines = self.source_code.split('\n')
        
        # Lista para almacenar los tokens y mostrarlos
        tokens = []
        for line in lines:
            line = line.strip()  # Eliminamos los espacios al inicio y al final de la línea
            if not line:
                continue  # Si encuentra líneas vacías, las ignoramos y continuamos

            while line:
                match = None  # Variable para saber si hicimos match
                
                # Recorremos cada patrón de token
                for token_type, pattern in self.token_patterns:
                    match = re.match(pattern, line)
                    
                    if match:
                        lexeme = match.group(0)
                        if token_type not in ['SKIP', 'NEWLINE']:
                            # Agregamos el token encontrado a la lista de tokens
                            tokens.append((token_type, lexeme))
                            # Incrementamos el contador del tipo de token correspondiente
                            self.token_count[token_type] += 1
                        
                        # Avanzamos a la siguiente parte de la línea eliminando el lexema procesado
                        line = line[len(lexeme):]
                        break

                if not match:
                    # Mostrar mensaje de error o manejar el caso cuando no hay coincidencias
                    tokens.append(("ERROR", line))
                    break
        return tokens

    def get_token_count(self):
        result = "\nResumen de conteo de tokens:\n"
        for token_type, count in self.token_count.items():
            result += f"{token_type}: {count}\n"
        return result

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")
        self.root.geometry("900x650")
        self.root.config(bg="#2C3E50")

        # Crear elementos de la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Título principal
        title_label = tk.Label(self.root, text="Analizador Léxico de Código", bg="#2C3E50", fg="white", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        # Texto de entrada con borde estilizado
        input_frame = tk.Frame(self.root, bg="#34495E", bd=2)
        input_frame.pack(pady=10, padx=20)
        tk.Label(input_frame, text="Ingrese el código a analizar:", bg="#34495E", fg="white", font=("Arial", 14)).pack(anchor="w", padx=10, pady=5)
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10, width=80, font=("Consolas", 12), bd=0, relief="flat")
        self.input_text.pack(padx=10, pady=5)

        # Botones estilizados
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=20)
        analyze_button = tk.Button(button_frame, text="Analizar Código", command=self.analyze_code, bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"), width=18, bd=0, relief="flat")
        analyze_button.grid(row=0, column=0, padx=10)
        file_button = tk.Button(button_frame, text="Cargar desde Archivo", command=self.load_file, bg="#3498DB", fg="white", font=("Arial", 12, "bold"), width=18, bd=0, relief="flat")
        file_button.grid(row=0, column=1, padx=10)

        # Resultado del análisis con borde y colores
        result_frame = tk.Frame(self.root, bg="#34495E", bd=2)
        result_frame.pack(pady=10, padx=20)
        tk.Label(result_frame, text="Resultado del análisis léxico:", bg="#34495E", fg="white", font=("Arial", 14)).pack(anchor="w", padx=10, pady=5)
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80, font=("Consolas", 12), bd=0, relief="flat", state="disabled")
        self.result_text.pack(padx=10, pady=5)

    def analyze_code(self):
        input_code = self.input_text.get("1.0", tk.END).strip()
        if not input_code:
            messagebox.showwarning("Advertencia", "El campo de texto está vacío.")
            return

        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        # Mostrar tokens y conteo
        result = ""
        for token_type, lexeme in tokens:
            result += f"{token_type}: {lexeme}\n"
        result += lexer.get_token_count()

        self.display_result(result)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)

    def display_result(self, result):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state="disabled")

# Crear ventana raíz de la aplicación
root = tk.Tk()
app = LexicalAnalyzerApp(root)
root.mainloop()
