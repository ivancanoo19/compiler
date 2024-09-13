import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        # Definition of token patterns
        self.token_patterns = [
            ('KEYWORD', r'\b(int|if|else|return|for)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUMBER', r'\d+(\.\d*)?'),
            ('LITERAL', r'"[^"]*"'),
            ('OPERATOR', r'[+*/=<>-]'),
            ('PUNCTUATION', r'[{}();,]'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
        ]
        # Initialize the token count for each type
        self.token_count = {token_type: 0 for token_type, _ in self.token_patterns}

    def tokenize(self):
        # Remove single-line or multi-line comments before processing entirely.
        self.source_code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', self.source_code)

        # Split the source code into multiple lines; each line will be processed.
        lines = self.source_code.split('\n')
        
        # List to store the tokens and display them
        tokens = []
        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces from the line
            if not line:
                continue  # If it finds empty lines, ignore and continue

            while line:
                match = None  # Variable to know if we made a match
                
                # Iterate over each token pattern
                for token_type, pattern in self.token_patterns:
                    match = re.match(pattern, line)
                    
                    if match:
                        lexeme = match.group(0)
                        if token_type not in ['SKIP', 'NEWLINE']:
                            # Add the found token to the list of tokens
                            tokens.append((token_type, lexeme))
                            # Increment the corresponding token type counter
                            self.token_count[token_type] += 1
                        
                        # Move to the next part of the line by removing the processed lexeme
                        line = line[len(lexeme):]
                        break

                if not match:
                    # Display error message or handle the case when no matches are found
                    tokens.append(("ERROR", line))
                    break
        return tokens

    def get_token_count(self):
        result = "\nToken count summary:\n"
        for token_type, count in self.token_count.items():
            result += f"{token_type}: {count}\n"
        return result

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer")
        self.root.geometry("900x650")
        self.root.config(bg="#2C3E50")

        # Create graphical interface elements
        self.create_widgets()

    def create_widgets(self):
        # Main title
        title_label = tk.Label(self.root, text="Code Lexical Analyzer", bg="#2C3E50", fg="white", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        # Input text with stylized border
        input_frame = tk.Frame(self.root, bg="#34495E", bd=2)
        input_frame.pack(pady=10, padx=20)
        tk.Label(input_frame, text="Enter the code to analyze:", bg="#34495E", fg="white", font=("Arial", 14)).pack(anchor="w", padx=10, pady=5)
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10, width=80, font=("Consolas", 12), bd=0, relief="flat")
        self.input_text.pack(padx=10, pady=5)

        # Stylized buttons
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=20)
        analyze_button = tk.Button(button_frame, text="Analyze Code", command=self.analyze_code, bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"), width=18, bd=0, relief="flat")
        analyze_button.grid(row=0, column=0, padx=10)
        file_button = tk.Button(button_frame, text="Load from File", command=self.load_file, bg="#3498DB", fg="white", font=("Arial", 12, "bold"), width=18, bd=0, relief="flat")
        file_button.grid(row=0, column=1, padx=10)

        # Analysis result with border and colors
        result_frame = tk.Frame(self.root, bg="#34495E", bd=2)
        result_frame.pack(pady=10, padx=20)
        tk.Label(result_frame, text="Lexical analysis result:", bg="#34495E", fg="white", font=("Arial", 14)).pack(anchor="w", padx=10, pady=5)
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80, font=("Consolas", 12), bd=0, relief="flat", state="disabled")
        self.result_text.pack(padx=10, pady=5)

    def analyze_code(self):
        input_code = self.input_text.get("1.0", tk.END).strip()
        if not input_code:
            messagebox.showwarning("Warning", "The text field is empty.")
            return

        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        # Display tokens and count
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

# Create root window of the application
root = tk.Tk()
app = LexicalAnalyzerApp(root)
root.mainloop()
