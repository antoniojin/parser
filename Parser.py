# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
DIRECTORIO = os.path.join("C:/Users/anton/Desktop/LenguajesProgramacion/practica2/")


sys.path.append(DIRECTORIO)

GRADING = os.path.join(DIRECTORIO, 'grading')
FICHEROS = os.listdir(GRADING)

TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(GRADING, fich))
         and fich.endswith(".test")]


class CoolParser(Parser):

    tokens = CoolLexer.tokens
    @_('OBJECTID')
    def expr(self, p):
        pass
