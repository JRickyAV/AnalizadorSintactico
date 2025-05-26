import json
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else {'type': 'EOF', 'value': ''}

    def match(self, expected_type):
        token = self.current_token()
        if token['type'] == expected_type:
            self.pos += 1
            return token
        self.error(f"[Línea {token.get('line', '?')}] Error de sintaxis: Se esperaba {expected_type}, se encontró {token}")
    
    def error(self, message):
        raise SyntaxError(message)

    def parse(self):
        statements = []
        while self.current_token()['type'] != 'EOF':
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        token = self.current_token()
        if token['type'] in ['INT', 'FLOAT', 'CHAR']:
            return self.declaration()
        elif token['type'] == 'IDENTIFIER':
            return self.assignment()
        elif token['type'] == 'WHILE':
            return self.while_loop()
        elif token['type'] == 'FOR':
            return self.for_loop()
        else:
            self.error(f"[Línea {token.get('line', '?')}] Error de sintaxis: Se esperaba declaración o ciclo while")

    def declaration(self):
        tipo = self.match(self.current_token()['type'])['value']
        ident = self.match('IDENTIFIER')['value']

        expr = None
        if self.current_token()['type'] == 'ASSIGN':
            self.match('ASSIGN')
            expr = self.expression()
        
        self.match('SEMICOLON')

        if expr:
            return Assignment(ident, expr)
        else:
            return Declaration(tipo, ident)

    def assignment(self):
        ident = self.match('IDENTIFIER')['value']
        self.match('ASSIGN')
        expr = self.expression()
        self.match('SEMICOLON')
        return Assignment(ident, expr)

    def while_loop(self):
        self.match('WHILE')
        self.match('LPAREN')
        cond = self.expression()
        self.match('RPAREN')
        self.match('LBRACE')
        body = []
        while self.current_token()['type'] != 'RBRACE':
            body.append(self.statement())
        self.match('RBRACE')
        return While(cond, body)
    
    def for_loop(self):
        self.match('FOR')
        self.match('LPAREN')
        init = self.declaration_no_semicolon()
        self.match('SEMICOLON')
        cond = self.expression()
        self.match('SEMICOLON')

        if (self.current_token()['type'] == 'IDENTIFIER' and
            self.tokens[self.pos + 1]['type'] == 'PLUS' and
            self.tokens[self.pos + 2]['type'] == 'PLUS'):
            update = self.parse_increment()
        else:
            update = self.assignment()

        self.match('RPAREN')
        self.match('LBRACE')
        body = []
        while self.current_token()['type'] != 'RBRACE':
            body.append(self.statement())
        self.match('RBRACE')
        return For(init, cond, update, body)


    def declaration_no_semicolon(self):
        tipo = self.match(self.current_token()['type'])['value']
        ident = self.match('IDENTIFIER')['value']

        if self.current_token()['type'] == 'ASSIGN':
            self.match('ASSIGN')
            expr = self.expression()
            return DeclarationWithAssignment(tipo, ident, expr)
        else:
            return Declaration(tipo, ident)



    def parse_increment(self):
        ident = self.match('IDENTIFIER')['value']
        self.match('PLUS')
        self.match('PLUS')
        return UnaryOp('++', Identifier(ident), is_postfix=True)

    def expression(self):
        return self.relational_expression()
    
    def relational_expression(self):
        left = self.expression_arithmetic()
        while self.current_token()['type'] in ['LESS_THAN', 'GREATER_THAN']:
            op = self.match(self.current_token()['type'])['value']
            right = self.expression_arithmetic()
            left = BinaryOp(left, op, right)
        return left

    def expression_arithmetic(self):
        left = self.term()
        while self.current_token()['type'] in ['PLUS', 'MINUS']:
            op = self.match(self.current_token()['type'])['value']
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token()['type'] in ['STAR', 'SLASH']:
            op = self.match(self.current_token()['type'])['value']
            right = self.factor()
            left = BinaryOp(left, op, right)
        return left

    def factor(self):
        token = self.current_token()
        if token['type'] in ['NUMBER', 'FLOAT', 'INT','FLOAT_LITERAL']:
            self.match(token['type'])
            return Number(token['value'])
        elif token['type'] == 'IDENTIFIER':
            self.match('IDENTIFIER')
            return Identifier(token['value'])
        elif token['type'] == 'LPAREN':
            self.match('LPAREN')
            expr = self.expression()
            self.match('RPAREN')
            return expr
        else:
            self.error(f"[Línea {token.get('line', '?')}] Error de sintaxis: Factor inválido, se encontró {token['type']} ({token['value']})")

def print_ast(node, indent=0):
    space = '  ' * indent
    if isinstance(node, Program):
        for stmt in node.statements:
            print_ast(stmt, indent)
    elif isinstance(node, Declaration):
        print(f"{space}Declaración: {node.tipo} {node.identifier}")
    elif isinstance(node, Assignment):
        print(f"{space}Asignación: {node.identifier} =")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, While):
        print(f"{space}While:")
        print_ast(node.condition, indent + 1)
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    elif isinstance(node, BinaryOp):
        print(f"{space}BinOp: {node.op}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, Identifier):
        print(f"{space}Identificador: {node.name}")
    elif isinstance(node, Number):
        print(f"{space}Número: {node.value}")
    elif isinstance(node, For):
        print(f"{space}For:")
        print(f"{space}  Init:")
        print_ast(node.init, indent + 2)
        print(f"{space}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{space}  Update:")
        print_ast(node.update, indent + 2)
        print(f"{space}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 3) 

def cargar_tokens(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def ast_to_dict(node):
    if isinstance(node, Program):
        return {'type': 'Program', 'statements': [ast_to_dict(s) for s in node.statements]}
    elif isinstance(node, Declaration):
        return {'type': 'Declaration', 'tipo': node.tipo, 'identifier': node.identifier}
    elif isinstance(node, Assignment):
        return {'type': 'Assignment', 'identifier': node.identifier, 'expression': ast_to_dict(node.expression)}
    elif isinstance(node, While):
        return {'type': 'While', 'condition': ast_to_dict(node.condition), 'body': [ast_to_dict(s) for s in node.body]}
    elif isinstance(node, BinaryOp):
        return {'type': 'BinaryOp', 'op': node.op, 'left': ast_to_dict(node.left), 'right': ast_to_dict(node.right)}
    elif isinstance(node, Identifier):
        return {'type': 'Identifier', 'name': node.name}
    elif isinstance(node, Number):
        return {'type': 'Number', 'value': node.value}
    elif isinstance(node, For):
        return {'type': 'For', 'init': ast_to_dict(node.init), 'condition': ast_to_dict(node.condition), 'update': ast_to_dict(node.update), 'body': [ast_to_dict(s) for s in node.body]}
    elif isinstance(node, UnaryOp):
        return {'type': 'UnaryOp', 'op': node.op, 'operand': ast_to_dict(node.operand), 'is_postfix': node.is_postfix}
    elif isinstance(node, DeclarationWithAssignment):
        return {'type': 'DeclarationWithAssignment', 'tipo': node.tipo, 'identifier': node.identifier, 'expression': ast_to_dict(node.expression)}
    else:
        return {}
    

def save_ast_to_file(ast, filename):
    ast_dict = ast_to_dict(ast)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(ast_dict, f, ensure_ascii=False, indent=2)