from Abstract.Abstract import Expression

class Dato(Expression):

    def __init__(self, elementos , fila, columna):
        self.elementos = elementos     
        super().__init__(fila, columna)

    def operar(self, no):
        lex = "Registros:" + self.elementos
        return lex

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()