from parser import Parser, cargar_tokens, print_ast, save_ast_to_file

if __name__ == '__main__':
    for i in range(1,6):
        print('Archivo ',i)
        archivo = f'./inputs/tokensResults{i}.json'

        tokens = cargar_tokens(archivo)
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            save_ast_to_file(ast, f'./outputs/ast_output{i}.json')
            print("AST generado:")
            print_ast(ast)
        except SyntaxError as e:
            print(str(e))
