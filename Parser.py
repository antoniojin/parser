# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *
DIRECTORIO = os.path.join("C:/Users/anton/Desktop/LenguajesProgramacion/practica2/")
DIRECTORIO = os.path.join("C:/Users/USUARIO/Parse/parser/")

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
        pass

    @_('clase ";"')
    def l_class(self, p):
        pass

    @_('l_class clase')
    def l_class(self, p):
        pass

    @_('CLASS TYPEID herencia "{" l_feature "}"')
    def clase(self, p):
        pass

    @_('INHERITS TYPEID')
    def herencia(self, p):
        pass

    @_('empty')
    def herencia(self, p):
        pass

    @_('empty')
    def l_feature(self, p):
        pass

    @_('l_feature feature ";"')
    def l_feature(self, p):
        pass

    @_('OBJECTID "(" formal l_formal ")" ":" TYPEID "{" expr "}" ')
    def feature(self, p):
        pass

    @_('OBJECTID ":" TYPEID inicializador ')
    def feature(self, p):
        pass

    @_('empty')
    def l_formal(self,p):
        pass

    @_('l_formal "," formal')
    def l_formal(self,p):
        pass

    @_('OBJECTID ":" TYPEID')
    def formal(self,p):
        pass

    @_('ASSIGN expr')
    def inicializador(self, p):
        pass

    @_('')
    def empty(self, p):
        pass

    @_('empty')
    def l_expr(self,p):
        pass

    @_('l_expr "," expr ";"')
    def l_expr(self,p):
        pass

    @_('OBJECTID ASSIGN expr')
    def expr(self, p):
        pass
    
    @_('expr opcional "." OBJECTID "(" expr l_expr ")" ')
    def expr(self, p):
        pass

    @_('empty')
    def opcional(self,p):
        pass
    
    @_('"@" TYPEID')
    def opcional(self,p):
        pass

    @_('OBJECTID "(" expr l_expr ")"')
    def expr(self, p):
        pass

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        pass

    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        pass

    @_('"{" expr l_expr "}"')
    def expr(self, p):
        pass

    @_(' LET OBJECTID ":" TYPEID opcional3 opcional4 IN expr ') #TODO
    def expr(self, p):
        pass

    @_('empty')
    def opcional3(self,p):
        pass

    @_('ASSIGN expr')
    def opcional3(self,p):
        pass

    @_('empty')
    def opcional4(self,p):
        pass

    @_('opcional4 "," OBJECTID ":" TYPEID opcional3')
    def opcional4(self,p):
        pass

    @_('CASE expr OF opcional2 ESAC ')
    def expr(self, p):
        pass

    @_('NEW TYPEID')
    def expr(self, p):
        pass

    @_('ISVOID expr')
    def expr(self, p):
        pass

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
        pass

    @_('expr LE expr')
    def expr(self, p):
        pass

    @_('expr "=" expr')
    def expr(self, p):
        return Asignacion(p.lineno,p.expr0,p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return Booleano(p.expr.lineo,p.expr.value)

    @_('"(" expr ")"')
    def expr(self, p):
        pass

    @_('OBJECTID')
    def expr(self, p):
        return Objeto(p.OBJECTID.lineo,p.OBJECTID.value)

    @_('INT_CONST')
    def expr(self, p):
        return Entero(p.INT_CONST.lineo,p.INT_CONST.value)

    @_('STR_CONST')
    def expr(self, p):
        return String(p.STR_CONST.lineo,p.STR_CONST.value)

    @_('BOOL_CONST')
    def expr(self, p):
        return Booleano(p.BOOL_CONST.lineo,p.BOOL_CONST.value)

    @_('OBJECTID  ";" TYPEID DARROW expr')
    def opcional2(self, p):
        pass

    @_('opcional2 OBJECTID  ";" TYPEID DARROW expr ";"')
    def opcional2(self, p):
        pass


    
