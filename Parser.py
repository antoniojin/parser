# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *
#DIRECTORIO = os.path.join("C:/Users/anton/Desktop/LenguajesProgramacion/practica2/")
DIRECTORIO = os.path.join("C:/Users/USUARIO/parser/")

sys.path.append(DIRECTORIO)

GRADING = os.path.join(DIRECTORIO, 'grading')
FICHEROS = os.listdir(GRADING)

TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(GRADING, fich))
         and fich.endswith(".test")]

class CoolParser(Parser):

    tokens = CoolLexer.tokens

    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LE','<','='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'ISVOID'),
        #('right', 'INT_COMPLEMENT'),
        ('left', '@'),
        ('left', '.'),
        ('right', '~')
    )

    @_('l_class')
    def program(self, p):
        return Programa(p.l_class[-1].linea,p.l_class)

    @_('clase ";"')
    def l_class(self, p):
        return [p.clase]

    @_('l_class clase')
    def l_class(self, p):
        return p.l_class + [p.clase]

    @_('CLASS TYPEID herencia "{" l_feature "}"')
    def clase(self, p):
        return Clase(p.lineno,p.TYPEID,p.herencia,self.nombre_fichero,p.l_feature)

    @_('INHERITS TYPEID')
    def herencia(self, p):
        return p.TYPEID

    @_('empty')
    def herencia(self, p):
        return "OBJECT"

    @_('empty')
    def l_feature(self, p):
        return []

    @_('l_feature feature ";"')
    def l_feature(self, p):
        return p.l_feature + [p.feature]

    @_('OBJECTID "(" formal l_formal ")" ":" TYPEID "{" expr "}" ')
    def feature(self, p):
        return Metodo(p.lineno,p.OBJECTID,p.TYPEID,p.expr,p.l_formal+[p.formal])

    @_('OBJECTID ":" TYPEID inicializador')
    def feature(self, p):
        return Atributo(p.lineno,p.OBJECTID,p.TYPEID,p.inicializador)

    @_('empty')
    def l_formal(self,p):
        return []

    @_('l_formal "," formal')
    def l_formal(self,p):
        return p.l_formal + [p.formal]

    @_('OBJECTID ":" TYPEID')
    def formal(self,p):
        return Formal(p.lineno, p.OBJECTID, p.TYPEID)

    @_('ASSIGN expr')
    def inicializador(self, p):
        return p.expr

    @_('empty')
    def inicializador(self, p):
        return NoExpr(-1)

    @_('')
    def empty(self, p):
        pass

    @_('empty')
    def l_expr(self,p):
        return []

    @_('l_expr "," expr ";"')
    def l_expr(self,p):
        return p.l_expr + [p.expr]

    @_('OBJECTID ASSIGN expr')
    def expr(self, p):
        return Asignacion(p.lineno, p.OBJECTID, p.expr)
    
    @_('expr opcional "." OBJECTID "(" expr l_expr ")" ')
    def expr(self, p):
        if opcional == '':
            return LlamadaMetodo(p.lineno, p.expr, p.OBJECTID, p.l_expr+[p.expr])
        else:
            return LlamadaMetodoEstatico(p.lineno, p.expr, p.TYPEID, p.OBJECTID, p.l_expr+[p.expr])

    @_('empty')
    def opcional(self,p):
        return ''
    
    @_('"@" TYPEID')
    def opcional(self,p):
        return p.TYPEID

    @_('OBJECTID "(" expr l_expr ")"')
    def expr(self, p):
        pass

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        return Condicional(p.expr0,p.expr1,p.expr2)

    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        return Bucle(p.expr0,p.expr1)

    @_('"{" expr l_expr "}"')
    def expr(self, p):
        return l_expr + {expr}

    @_(' LET OBJECTID ":" TYPEID opcional3 opcional4 IN expr ') #TODO
    def expr(self, p):
        pass

    @_('empty')
    def opcional3(self,p):
        pass

    @_('ASSIGN expr')
    def opcional3(self,p):
        return p.expr

    @_('empty')
    def opcional4(self,p):
        pass

    @_('opcional4 "," OBJECTID ":" TYPEID opcional3')
    def opcional4(self,p):
        pass

    @_('CASE expr OF opcional2 ESAC ')
    def expr(self, p):
        Swicht(p.ESAC[-1].linea,p.expr,p.opcional2)

    @_('NEW TYPEID')
    def expr(self, p):
        return Nuevo(p.lineno,p.TYPEID)

    @_('ISVOID expr')
    def expr(self, p):
        return EsNulo(p.lineno,p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return Suma(p.lineno,p.expr0,p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return Resta(p.lineno,p.expr0,p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return Multiplicacion(p.lineno,p.expr0,p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return Menor(p.lineno,p.expr0,p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return Division(p.lineno,p.expr0,p.expr1)

    @_('"~" expr')
    def expr(self, p):
        return Neg(p.lineno,p.expr)

    @_('expr LE expr')
    def expr(self, p):
        return LeIgual(p.lineno,p.expr0,p.expr1)

    @_('expr "=" expr')
    def expr(self, p):
        return Asignacion(p.lineno,p.expr0,p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return Booleano(p.expr.linea,p.expr.value)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('OBJECTID')
    def expr(self, p):
        return Objeto(p.lineno,p.OBJECTID)

    @_('INT_CONST')
    def expr(self, p):
        return Entero(p.lineno,p.INT_CONST)

    @_('STR_CONST')
    def expr(self, p):
        return String(p.lineno,p.STR_CONST)

    @_('BOOL_CONST')
    def expr(self, p):
        return Booleano(p.lineno,p.BOOL_CONST)

    @_('OBJECTID  ";" TYPEID DARROW expr')
    def opcional2(self, p):
        pass

    @_('opcional2 OBJECTID  ";" TYPEID DARROW expr ";"')
    def opcional2(self, p):
        pass
    @_('error ";"')
    def expr(self, p):
        return ErroresSintacticos_CLE(p.lineno,'','','Error')
    def error(self, p):
        pass

for fich in TESTS:
    f = open(os.path.join(GRADING, fich), 'r')
    g = open(os.path.join(GRADING, fich + '.out'), 'r')
    lexer = CoolLexer()
    parser = CoolParser()
    parser.nombre_fichero = fich
    bien = ''.join([c for c in g.readlines() if c and '#' not in c])
    entrada = f.read()
    j = parser.parse(lexer.tokenize(entrada))
    if not j:
        continue
    resultado = '\n'.join([c for c in j.str(0).split('\n')
                         if c and '#' not in c])
    f.close(), g.close()
    if resultado != bien:
        print(f"Revisa el fichero {fich}")



    
