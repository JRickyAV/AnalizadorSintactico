class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Declaration(ASTNode):
    def __init__(self, tipo, identifier):
        self.tipo = tipo
        self.identifier = identifier

class Assignment(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class For(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class UnaryOp(ASTNode):
    def __init__(self, op, operand, is_postfix=False):
        self.op = op
        self.operand = operand
        self.is_postfix = is_postfix

class DeclarationWithAssignment(ASTNode):
    def __init__(self, tipo, identifier, expression):
        self.tipo = tipo
        self.identifier = identifier
        self.expression = expression