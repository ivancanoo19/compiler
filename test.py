import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        
        # token_patterns: lista de tuplas en donde se almacena la clasificación de
        #                 nuestros tokens. Cada tupla tiene el tipo de token y su regex.

        self.token_patterns=[
            ('KEYWORD', r'\b(int|if|else|return|for)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUMBER',   r'\d+(\.\d*)?'),
            ('LITERAL', r'"[^"]*"'),
            ('OPERATOR', r'[+*/=<>-]'),
            ('DELIMITER', r'[{}();,]'),
            ('COMMENT', r'//.|/\[\s\S]?\/'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
        ]

    # 
    #
    # Tokenization
    #
    # 

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
                        if token_type not in ['SKIP', 'NEWLINE']:
                            lexeme = match.group(0)
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

        


source_code = """
int main(){
    int x = 10;
    int i;
    //Este es un comentario

    for(i=0, i<9, i++){
        x=x-1;
        printf("Esta es una iteracion");
    }
    // ESTE ES OTRO COMENTARIO
    if(x==10){
        x = 10 + 5;
        // eSTE ES OTRO COMENTARIO
    }
    
    /* otro comentario
    adsasd
    dadsasd
    DASDas
    */
    else{
        printf("Hola mundo! Este, es un ejemplo.");
        printf("Hola mundo! Este, ejemplo.");
        printf("Hola mundo!");
    }
    return 0;
}
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for t in tokens:
    print(t); 
