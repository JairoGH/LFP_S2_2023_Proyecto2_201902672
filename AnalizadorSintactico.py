from Errores.Errores import *
from Instrucciones.DeclaracionClaves import *
from Instrucciones.Imprimir import *
from Instrucciones.Imprimirln import *
from Instrucciones.Registros import *
from Instrucciones.Datos import *

global n_linea
global n_columna
global lista_lexemas_sintacticos
global instrucciones_sintacticas


lista_errores = []


def instrucciones_sintactico(lista_lexemas):

    while lista_lexemas:

        lista_registros = [] 
        lexema = lista_lexemas.pop(0)


        if lexema.operar(None) == 'Claves':
            lista_elementos = []
            palabra_reservada = lexema
            igual = lista_lexemas.pop(0)
            if igual.operar(None) == '=':
                corchete_izq = lista_lexemas.pop(0)
                if corchete_izq.operar(None) == '[':
                    while lista_lexemas:
                        lex = lista_lexemas.pop(0)
                        if lex.operar(None) == '"':
                            continue
                        elif lex.operar(None) == ',':
                            continue
                        elif lex.operar(None) == ']':
                            return DeclaracionClaves(palabra_reservada.lexema, lista_elementos, lex.getFila(), lex.getColumna())
                        else:
                            lista_elementos.append(lex.lexema)
            else: #! para detectar errores sintácticos
                print("Error sintactico en la declaracion de claves")
                lista_errores.append(Errores(igual.lexema,"Sintactico", igual.getFila(), igual.getColumna()))
                while lista_lexemas:
                    lex = lista_lexemas.pop(0)
                    lista_errores.append(Errores(lex.lexema, "Sintactico",lex.getFila(), lex.getColumna()))
                    if lex.operar(None) == ']':
                        print("Final de la declaracion de claves")
                        #break

        
        if lexema.operar(None) == 'imprimir':
            lexema = lista_lexemas.pop(0)
            if lexema.operar(None) == '(':
                comillas = lista_lexemas.pop(0)
                if comillas.operar(None) == '"':
                    texto = lista_lexemas.pop(0)
                    comillas = lista_lexemas.pop(0)
                    if comillas.operar(None) == '"':
                        parentesis = lista_lexemas.pop(0)
                        if parentesis.operar(None) == ')':
                            punto_coma = lista_lexemas.pop(0)
                            if punto_coma.operar(None) == ';':
                                return Imprimir(texto.lexema, lexema.getFila(), lexema.getColumna())
            
                else:
                    print("Error sintactico en imprimir")
                    lista_errores.append(Errores(comillas.lexema,"Sintactico", comillas.getFila(), comillas.getColumna()))
                    while lista_lexemas:
                        lex = lista_lexemas.pop(0)
                        lista_errores.append(Errores(lex.lexema, "Sintactico",lex.getFila(), lex.getColumna()))
                        if lex.operar(None) == ';':
                            print("Final de la impresion")
                            break




        if lexema.operar(None) == 'Registros':
            igual = lista_lexemas.pop(0)
            if igual.operar(None) == '=':
                corchete_izq = lista_lexemas.pop(0)
                if corchete_izq.operar(None) == '[':
                    llave_izq = lista_lexemas.pop(0)
                    if llave_izq.operar(None) == '{':
                        lista_registros = []
                        while lista_lexemas:
                            registro = {}
                            while lista_lexemas:
                                lex = lista_lexemas.pop(0)
                                if lex == '':
                                    break
                                elif lex.operar(None) == ',':
                                    continue
                                elif lex.operar(None) == '}':
                                    lista_registros.append(registro)
                                elif lex.operar(None) == ']':
                                    return Registro(lista_registros, lex.getFila(),lista_elementos, lex.getColumna())
                                    
                                else:
                                    lista_elementos.append(lex.lexema)
            else: #! para detectar errores sintácticos
                print("Error sintáctico en la declaración de Registros")
                lista_errores.append(Errores(igual.lexema,"Sintactico", igual.getFila(), igual.getColumna()))
                while lista_lexemas:
                    lex = lista_lexemas.pop(0)
                    lista_errores.append(Errores(lex.lexema, "Sintactico",lex.getFila(), lex.getColumna()))
                    if lex.operar(None) == ']':
                        print("Final de la declaracion de Registros")
                        #break

        if lexema.operar(None) == 'datos':
            lexema = lista_lexemas.pop(0)
            if lexema.operar(None) == '(':
                parentesis = lista_lexemas.pop(0)
                if parentesis.operar(None) == ')':
                    punto_coma = lista_lexemas.pop(0)
                    if punto_coma.operar(None) == ';':
                        return Dato(lexema.lexema, lexema.getFila(), lexema.getColumna())



        if lexema.operar(None) == 'imprimirln':
            lexema = lista_lexemas.pop(0)
            if lexema.operar(None) == '(':
                comillas = lista_lexemas.pop(0)
                if comillas.operar(None) == '"':
                    texto = lista_lexemas.pop(0)
                    comillas = lista_lexemas.pop(0)
                    if comillas.operar(None) == '"':
                        parentesis = lista_lexemas.pop(0)
                        if parentesis.operar(None) == ')':
                            punto_coma = lista_lexemas.pop(0)
                            if punto_coma.operar(None) == ';':
                                return Imprimirln(texto.lexema, lexema.getFila(), lexema.getColumna())
            
            else: #! para detectar errores sintácticos
                print("Error sintáctico en la declaración de claves")
                lista_errores.append(Errores(igual.lexema,"Sintáctico", igual.getFila(), igual.getColumna()))
                while lista_lexemas:
                    lex = lista_lexemas.pop(0)
                    lista_errores.append(Errores(lex.lexema, "Sintáctico",lex.getFila(), lex.getColumna()))
                    if lex.operar(None) == ';':
                        print("Final de imprimirln")
                        break
