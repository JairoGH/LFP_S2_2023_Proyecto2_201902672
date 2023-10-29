from Abstract.Abstract import Expression

class Registro(Expression):

    def __init__(self, numero, nombre , fila, columna):
        self.nombre = nombre
        self.numero = numero        
        super().__init__(fila, columna)

    def operar(self, no):
        lex = "Registros:" + self.nombre + " = " + self.numero
        return lex

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()