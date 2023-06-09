# -*- coding: utf-8 -*-
from importlib.abc import PathEntryFinder
from symtable import Symbol
import sys
import re

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        pass

class Block(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        for filhos in self.children:
            if filhos.__class__.__name__ == "Retorna":
                return filhos.evaluate(st)
            filhos.evaluate(st)

class BinOp(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    
    def evaluate(self, st):

        dir = self.children[0].evaluate(st)
        esq = self.children[1].evaluate(st)
        
        if self.value == "+":
            if dir[0]==esq[0] and dir[0] == "INTEIRO":
                return("INTEIRO", dir[1]+esq[1])
            
        elif self.value == "-":
            if dir[0]==esq[0] and dir[0] == "INTEIRO":
                return("INTEIRO", dir[1]-esq[1])
           
        elif self.value == "*":
            if dir[0]==esq[0] and dir[0] == "INTEIRO":
                return("INTEIRO", dir[1]*esq[1])
            
        elif self.value == "/":
            if dir[0]==esq[0] and dir[0] == "INTEIRO":
                return("INTEIRO", dir[1]//esq[1])
        
        elif self.value == "==":
            return(dir[0], int(dir[1]==esq[1]))
        
        elif self.value == ">":
            if (dir[0] == esq[0] and dir[0] == "INTEIRO") or (dir[0]==esq[0] and dir[0] == "FRASE"):
                return(dir[0], int(dir[1]>esq[1]))
        
        elif self.value == "<":
            if (dir[0]==esq[0] and dir[0] == "INTEIRO") or (dir[0]==esq[0] and dir[0] == "FRASE"):
                return(dir[0], int(dir[1]<esq[1]))
        
        elif self.value == "&&":
            if dir[0]==esq[0] and dir[0] == "INTEIRO":
                return("INTEIRO", int(dir[1] and esq[1]))
        
        elif self.value == "||":
            if dir[0]==esq[0] and dir[0] == "INTEIRO":
                res_2 = dir[1] or esq[1]
                return("INTEIRO", res_2)
        
        elif self.value == ".":
            
            res = str(dir[1]) + str(esq[1])
            return("FRASE", str(res))
        
        
class UnOp(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        if self.value == "+":
            return ("INTEIRO", self.children[0].evaluate(st)[0])
        elif self.value == "-":
            return ("INTEIRO", -self.children[0].evaluate(st)[0])
        elif self.value == "!":
            return ("INTEIRO", int(not self.children[0].evaluate(st)[0]))
        
class Se(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        
        if len(self.children) == 2:
            if self.children[0].evaluate(st)[0]:
                self.children[1].evaluate(st)
        
        elif len(self.children) > 2:
            self.children[2].evaluate(st)


class Enquanto(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        while(self.children[0].evaluate(st)[1]):
            self.children[1].evaluate(st)

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        if type(self.children[0]) == list:
            for i in self.children[0]:
                st.create(i.value, (self.value, self.children[1].value))
        else:
            st.create(self.children[0].value, (self.value, self.children[1].value))
        #print("CRIOU: ", self.children[0].value)

class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        FuncTable.setter(self.children[0].value, self)


class FuncTable():
    
    dic = {}
    
    def getter(key):
        if key not in FuncTable.dic:
            #print("Key errada: ", key)
            raise
            
        return FuncTable.dic[key]
        
    def setter(key, ref):
        FuncTable.dic[key] = ref
        #print("setou 2: ", SymbolTable.dic[key])


class FuncCall(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):

        nome = self.value

        nova_symboltable = SymbolTable()

        ret = FuncTable.getter(nome)
        tipo = ret.value
        
        for i in range(1, len(ret.children) - 1):
            ret.children[i].evaluate(nova_symboltable)
            val = self.children[i-1].evaluate(st)
            
            nova_symboltable.setter(ret.children[i].children[0].value, val)
        
        if len(ret.children)-2 != len(self.children):
            raise
        
        block = ret.children[-1].evaluate(nova_symboltable)
        #print("BLOCK CALL: ", block)

        if tipo != block[0]:
            raise

        return block

class Retorna(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):        
        return self.children.evaluate(st)    
        
class IntVal(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        return ("INTEIRO", self.value)
    
class String(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        return ("FRASE", self.value)

class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        #x = SymbolTable.getter(self.children[0].value)
        for i in self.children[0]:
            st.setter(i.value, (self.children[1].evaluate(st)))


class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        if self.value == "Print":
            print(self.children.evaluate(st)[1])

class Read():
        
    def evaluate(self, st):
        return ("INTEIRO", int(input()))

    
class SymbolTable():
    def __init__(self):
        self.dic = {}
    
    def getter(self, key):
        if key not in self.dic:
            print("KEY ERRADA: ", key)
            raise
        
        return self.dic[key]
        
    def setter(self, key, value):
        if key not in self.dic:
            print("KEY SETTER ERRADA: ", key.value)
            raise
        
        #print("KEY: ", key)
        #print("VALUE: ", value)
        if value[0] == "INTEIRO" and self.dic[key][0] == "FRASE":
            raise Exception("Wrong types in attribution")
        elif value[0] == "FRASE" and self.dic[key][0] == "INTEIRO":
            raise Exception("Wrong types in attribution")

        self.dic[key] = value
        #print("KEY SETADA: ", key)

    def create(self, key, value):
        if key in self.dic:
            print("KEY JÁ FEITA: ", key)
            raise
        
        self.dic[key] = value
        #print("Criou Key: ", key)


class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, st):
        return st.getter(self.value)


class NoOp(Node):
    pass

class Token:
    def __init__(self, value, tipo):
        self.tipo = tipo
        self.value = value

class PrePro:
        
    def filtering(source):
        
        
        comentario = False
        s = ""
        for el in source:

            if el == "#":
                comentario = True

            if comentario == False:
                s += el

            elif comentario == True and el == "\n":
                comentario = False

        return s
                
    
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.nexti = Token(0, "INTEIRO")
        
    def selectNext(self):
        
        list_nums_check = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        list_ops_check = ["+", "-"]
        list_mults_check = ["/", "*"]
        list_par = ["(", ")"]
        reserved = ["printa_ai", "se", "enquanto", "senao", "end","leitura", "Inteiro", "Frase", "variavel", "funcao", "retorna"]
        
        num = ""
        
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position+=1
        
        if self.position == len(self.source):
            self.nexti = Token(1, "EOF")
            return self.nexti
        
        elif self.source[self.position] in list_nums_check:
            num = self.source[self.position]
            self.position += 1
            
            while self.position < len(self.source) and self.source[self.position] in list_nums_check:
                num += self.source[self.position]
                self.position += 1
            
            num = int(num)
            self.nexti = Token(num, "INTEIRO")
                
            
                
        elif self.source[self.position] in list_ops_check and self.source[self.position] == "+":
            self.nexti = Token(self.source[self.position], "PLUS")
            self.position += 1
                
        elif self.source[self.position] in list_ops_check and self.source[self.position] == "-":
            self.nexti = Token(self.source[self.position], "MINUS")
        
            self.position += 1

        elif self.source[self.position] in list_mults_check and self.source[self.position] == "/":
            self.nexti = Token(self.source[self.position], "DIV")
            self.position += 1
            
        elif self.source[self.position] in list_mults_check and self.source[self.position] == "*":
            self.nexti = Token(self.source[self.position], "MULT")
            self.position += 1

        elif self.source[self.position] in list_par and self.source[self.position] == "(":
            self.nexti = Token(self.source[self.position], "A_PARENTESES")
            self.position += 1
        
        elif self.source[self.position] in list_par and self.source[self.position] == ")":
            self.nexti = Token(self.source[self.position], "F_PARENTESES")
            self.position += 1
        
        elif self.source[self.position] == "{":
            self.nexti = Token(self.source[self.position], "ABRE_CHAVES")
            self.position += 1
        
        elif self.source[self.position] == "}":
            self.nexti = Token(self.source[self.position], "FECHA_CHAVES")
            self.position += 1

        elif self.source[self.position] == "\n":
            self.nexti = Token(self.source[self.position], "BARRA_N")
            self.position += 1

        elif self.source[self.position] == "=":
            self.position+=1
            if self.source[self.position] == "=":
                self.nexti = Token(self.source[self.position], "COMPARE")
                self.position += 1
                
            else:
                self.nexti = Token(self.source[self.position], "IGUAL")
            
            
        
        elif self.source[self.position] == ">":
            self.nexti = Token(self.source[self.position], "MAIOR")
            self.position += 1
        
        elif self.source[self.position] == "<":
            self.nexti = Token(self.source[self.position], "MENOR")
            self.position += 1
            
        elif self.source[self.position] == "|":
            self.position+=1
            if self.source[self.position] == "|":
                self.nexti = Token(self.source[self.position], "OR")
                self.position += 1
            
        elif self.source[self.position] == "&":
            self.position+=1
            if self.source[self.position] == "&":
                self.nexti = Token(self.source[self.position], "AND")
                self.position += 1
            
            else:
                raise
        
        elif self.source[self.position] == "!":
            self.nexti = Token(self.source[self.position], "NOT")
            self.position += 1

        elif self.source[self.position] == ":":
            self.nexti = Token(self.source[self.position], "TYPE")
            self.position+=1

        elif self.source[self.position] == ".":
            self.nexti = Token(self.source[self.position], "CONCAT")
            self.position += 1
        
        elif self.source[self.position] == ",":
            self.nexti = Token(self.source[self.position], "VIRGULA")
            self.position += 1
        
        elif self.source[self.position] == '"':
            #string = self.source[self.position]
            self.position+=1
            string = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                if self.source[self.position] == '"':
                    break
                string += self.source[self.position]
                self.position+=1
            self.position += 1
            self.nexti = Token(string, "FRASE")

        elif self.source[self.position].isalpha():
            ident = self.source[self.position]
            self.position += 1
            while self.source[self.position].isalpha() or self.source[self.position] in list_nums_check or self.source[self.position] == "_":
                ident += self.source[self.position]
                self.position += 1
                
            if ident in reserved:
                
                self.nexti = Token(ident, ident.upper())

            else:
                self.nexti = Token(ident, "IDENTIFIER")
   
        else:
            print(self.source[self.position])
            raise Exception("Invalid symbol")
        
        return self.nexti
        
class Parser:
    tokenizer = None
    
    def parseExpression():

        res = Parser.parseTerm()

        while Parser.tokenizer.nexti.tipo == "PLUS" or Parser.tokenizer.nexti.tipo == "MINUS" or Parser.tokenizer.nexti.tipo == "OR":

            if Parser.tokenizer.nexti.tipo == "PLUS":
                Parser.tokenizer.selectNext()

                res = BinOp("+", [res, Parser.parseTerm()])
                
            elif Parser.tokenizer.nexti.tipo == "MINUS":
                Parser.tokenizer.selectNext()
                
                res = BinOp("-", [res, Parser.parseTerm()])

            elif Parser.tokenizer.nexti.tipo == "OR":
                Parser.tokenizer.selectNext()
                
                res = BinOp("||", [res, Parser.parseTerm()])
            
        return res
    

    def relExpr():
        
        res = Parser.parseExpression()
        
        while Parser.tokenizer.nexti.tipo == "COMPARE" or Parser.tokenizer.nexti.tipo == "MAIOR" or Parser.tokenizer.nexti.tipo == "MENOR" or Parser.tokenizer.nexti.tipo == "CONCAT":
            
            if Parser.tokenizer.nexti.tipo == "COMPARE":
                Parser.tokenizer.selectNext()
                
                res = BinOp("==", [res, Parser.parseExpression()])
            
            elif Parser.tokenizer.nexti.tipo == "MAIOR":
                Parser.tokenizer.selectNext()
                
                res = BinOp(">", [res, Parser.parseExpression()])
                
            elif Parser.tokenizer.nexti.tipo == "MENOR":
                Parser.tokenizer.selectNext()
                
                res = BinOp("<", [res, Parser.parseExpression()])

            elif Parser.tokenizer.nexti.tipo == "CONCAT":
                Parser.tokenizer.selectNext()
                
                res = BinOp(".", [res, Parser.parseExpression()])
            
        return res


    def parseTerm():

        res = Parser.parseFactor()

        while Parser.tokenizer.nexti.tipo == "DIV" or Parser.tokenizer.nexti.tipo == "MULT" or Parser.tokenizer.nexti.tipo == "AND":

            if Parser.tokenizer.nexti.tipo == "DIV":
                Parser.tokenizer.selectNext()

                res = BinOp("/", [res, Parser.parseFactor()])
                
            elif Parser.tokenizer.nexti.tipo == "MULT":
                Parser.tokenizer.selectNext()

                res = BinOp("*", [res, Parser.parseFactor()])

            elif Parser.tokenizer.nexti.tipo == "AND":
                Parser.tokenizer.selectNext()
                
                res = BinOp("&&", [res, Parser.parseFactor()])

            else:
                raise
            
        return res
        

    def parseFactor():

        res = 0

        if Parser.tokenizer.nexti.tipo == "INTEIRO":
            
            res = IntVal(Parser.tokenizer.nexti.value, [])
            Parser.tokenizer.selectNext()
            return res
        
        elif Parser.tokenizer.nexti.tipo == "FRASE":
            res = String(Parser.tokenizer.nexti.value, [])
            Parser.tokenizer.selectNext()
            return res
        
        elif Parser.tokenizer.nexti.tipo == "IDENTIFIER":
            name = Parser.tokenizer.nexti.value
            Parser.tokenizer.selectNext()
            
            if Parser.tokenizer.nexti.tipo == "A_PARENTESES":
                Parser.tokenizer.selectNext()
                lista_call = []
                if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                    res = FuncCall(name, lista_call)
                    Parser.tokenizer.selectNext()
                    #print("FEZ NO FUNCCALL")
                    return res  
                lista_call = [Parser.relExpr()]
                #Parser.tokenizer.selectNext()
                while Parser.tokenizer.nexti.tipo == "VIRGULA":
                    Parser.tokenizer.selectNext()
                    lista_call.append(Parser.relExpr())
                    #Parser.tokenizer.selectNext()
                if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                    res = FuncCall(name, lista_call)
                    Parser.tokenizer.selectNext()
                    #print("FEZ NO FUNCCALL")
                    return res            
            
            res = Identifier(name, [])
            return res
        
        elif Parser.tokenizer.nexti.tipo == "PLUS":

            Parser.tokenizer.selectNext()
            res = UnOp("+", [Parser.parseFactor()])
            return res
            
            
        elif Parser.tokenizer.nexti.tipo == "MINUS":

            Parser.tokenizer.selectNext()
            res = UnOp("-", [Parser.parseFactor()])
            return res
        
        elif Parser.tokenizer.nexti.tipo == "NOT":
            Parser.tokenizer.selectNext()
            res = UnOp("!", [Parser.parseFactor()])
            return res
            
        elif Parser.tokenizer.nexti.tipo == "A_PARENTESES":
            Parser.tokenizer.selectNext()

            res = Parser.relExpr()
            
            
            if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                Parser.tokenizer.selectNext()
            
            else:
                raise

            return res
        
        elif Parser.tokenizer.nexti.tipo == "LEITURA":
            Parser.tokenizer.selectNext()
            
            if Parser.tokenizer.nexti.tipo == "A_PARENTESES":
                #print("Parenteses")
                Parser.tokenizer.selectNext()
                
                if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                    Parser.tokenizer.selectNext()
                    
                    res = Read()
                    
                    return res
                    
                else:
                    raise
                    
            else:
                raise
                
        else:
            #print(Parser.tokenizer.nexti.tipo)
            raise


    def parseBlock():

        node = Block('', [])

        while Parser.tokenizer.nexti.tipo != "EOF":
            child = Parser.parseStatement()

            if child != None:
                node.children.append(child)

        return node
    
    
    def parseStatement():

        if Parser.tokenizer.nexti.tipo == "VARIAVEL":
            Parser.tokenizer.selectNext()
        
            if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
                name = Parser.tokenizer.nexti.value
                no = Identifier(Parser.tokenizer.nexti.value, [])
                Parser.tokenizer.selectNext()
                list_ident_2 = [no]
                while Parser.tokenizer.nexti.tipo == "VIRGULA":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
                        no = Identifier(Parser.tokenizer.nexti.value, [])
                        list_ident_2.append(no)
                    Parser.tokenizer.selectNext()
                if Parser.tokenizer.nexti.tipo == "TYPE":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.nexti.tipo == "INTEIRO" or Parser.tokenizer.nexti.tipo == "FRASE":
                        tipo = Parser.tokenizer.nexti.tipo
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.nexti.tipo == "BARRA_N":
                            if tipo == "INTEIRO":
                                no_int = IntVal(0, [])
                                no_var_dec = VarDec(tipo, [list_ident_2, no_int])
                                return no_var_dec
                            elif tipo == "FRASE":
                                no_string = String("", [])
                                no_var_dec = VarDec(tipo, [list_ident_2, no_string])
                                return no_var_dec
                        elif Parser.tokenizer.nexti.tipo == "IGUAL":
                            Parser.tokenizer.selectNext()
                            expr = Parser.relExpr()
                            if Parser.tokenizer.nexti.tipo == "BARRA_N":
                                Parser.tokenizer.selectNext()
                                no_var_dec = VarDec(tipo, [list_ident_2, expr])
                                return no_var_dec
        if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
            name = Parser.tokenizer.nexti.value
            no = Identifier(Parser.tokenizer.nexti.value, [])
            list_ident = [no]
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.nexti.tipo == "VIRGULA":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
                    no = Identifier(Parser.tokenizer.nexti.value, [])
                    list_ident.append(no)
                Parser.tokenizer.selectNext()
            if Parser.tokenizer.nexti.tipo == "IGUAL":
                Parser.tokenizer.selectNext()
                expr = Parser.relExpr()
                #print("EXPR: ", expr)
                if Parser.tokenizer.nexti.tipo == "BARRA_N":
                    Parser.tokenizer.selectNext()
                    return Assignment('', [list_ident, expr])
                
                else:
                    raise
            elif Parser.tokenizer.nexti.tipo == "A_PARENTESES":
                #print("ABRIU")
                Parser.tokenizer.selectNext()
                res = Parser.relExpr()
                
                no_call = FuncCall(name, [res])
                #Parser.tokenizer.selectNext()

                while Parser.tokenizer.nexti.tipo == "VIRGULA":
                    Parser.tokenizer.selectNext()
                    
                    res = Parser.relExpr()
                    no_call.children.append(res)
                    
                    #Parser.tokenizer.selectNext()
                
                if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                    Parser.tokenizer.selectNext()
                    #print("FECHOU PAR")
                
                    if Parser.tokenizer.nexti.tipo == "BARRA_N":
                        Parser.tokenizer.selectNext()
                        #print("FEZ NO CALL")
                        return no_call
        
        elif Parser.tokenizer.nexti.tipo == "RETORNA":
            Parser.tokenizer.selectNext()

            res = Parser.relExpr()
            no_ret = Retorna('', res)

            if Parser.tokenizer.nexti.tipo == "BARRA_N":
                return no_ret
                
        elif Parser.tokenizer.nexti.tipo == "PRINTA_AI":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.nexti.tipo == "A_PARENTESES":
                Parser.tokenizer.selectNext()
                ch = Parser.relExpr()
                
                no_print = Print("Print", ch)
                
                if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.nexti.tipo == "BARRA_N":
                        Parser.tokenizer.selectNext()
                        return no_print
                    
                    else:
                        raise
                    
                else:
                    raise
                    
            else:
                raise

        elif Parser.tokenizer.nexti.tipo == "ENQUANTO":
            
            Parser.tokenizer.selectNext()
                         
            rel = Parser.relExpr()
                
            no_enquanto = Enquanto("enquanto", [rel])

            if Parser.tokenizer.nexti.tipo == "ABRE_CHAVES":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.nexti.tipo == "BARRA_N":

                    Parser.tokenizer.selectNext()
                    res = []
                    while Parser.tokenizer.nexti.tipo != "FECHA_CHAVES":

                        res.append(Parser.parseStatement())
                            
                    no_enquanto = Enquanto("enquanto", [rel, Block("", res)])

                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.nexti.tipo == "BARRA_N":

                        Parser.tokenizer.selectNext()
                            
                        return no_enquanto
                    
                    else:
                        raise

        elif Parser.tokenizer.nexti.tipo == "SE":
            Parser.tokenizer.selectNext()
            
            exp = Parser.relExpr()

            no_if = Se("se", [exp])

            if Parser.tokenizer.nexti.tipo == "ABRE_CHAVES":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.nexti.tipo == "BARRA_N":
                    Parser.tokenizer.selectNext()

                    res = []
                    while Parser.tokenizer.nexti.tipo != "FECHA_CHAVES" and Parser.tokenizer.nexti.tipo != "SENAO":
                        res.append(Parser.parseStatement())

                    no_if = Se("se", [exp, Block("", res)])
                    
                    if Parser.tokenizer.nexti.tipo == "SENAO":
                        Parser.tokenizer.selectNext()
                        
                        if Parser.tokenizer.nexti.tipo == "BARRA_N":
                            Parser.tokenizer.selectNext()
                            el = []
                            while Parser.tokenizer.nexti.tipo != "FECHA_CHAVES":
                                el.append(Parser.parseStatement())
                            Parser.tokenizer.selectNext()
                            no_if.children.append(Block("", el))                                        
                            return no_if
                        
                    else:
                        Parser.tokenizer.selectNext()
                        return no_if
                
                else:
                    raise

        elif Parser.tokenizer.nexti.tipo == "FUNCAO":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
                name_func = Parser.tokenizer.nexti.value
                no = Identifier(Parser.tokenizer.nexti.value, [])
                
                #print("identifier")
                
                no_ident = Identifier(Parser.tokenizer.nexti.value, [])
                no_func = FuncDec(None, [])
                
                no_func.children.append(no_ident)
                
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.nexti.tipo == "A_PARENTESES":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.nexti.tipo == "VARIAVEL":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
                            #variaveis = []
                            #variaveis.append(Parser.tokenizer.nexti.value)
                            arg = Identifier(Parser.tokenizer.nexti.value, [])
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.nexti.tipo == "TYPE":
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.nexti.tipo == "INTEIRO" or Parser.tokenizer.nexti.tipo == "FRASE":
                                    tipo = Parser.tokenizer.nexti.tipo
                                    if tipo == "INTEIRO":
                                        no_int = IntVal(0, [])
                                        no_var_dec = VarDec(tipo, [arg, no_int])
                                        no_func.children.append(no_var_dec)
                                    elif tipo == "FRASE":
                                        no_string = String("", [])
                                        no_var_dec = VarDec(tipo, [arg, no_string])
                                        no_func.children.append(no_var_dec)
                                    Parser.tokenizer.selectNext()
                                    while Parser.tokenizer.nexti.tipo == "VIRGULA":
                                        Parser.tokenizer.selectNext()
                                        if Parser.tokenizer.nexti.tipo == "VARIAVEL":
                                            Parser.tokenizer.selectNext()
                                            if Parser.tokenizer.nexti.tipo == "IDENTIFIER":
                                                arg = Identifier(Parser.tokenizer.nexti.value, [])
                                                #variaveis.append(Parser.tokenizer.nexti.value)
                                                
                                                Parser.tokenizer.selectNext()
                                                if Parser.tokenizer.nexti.tipo == "TYPE":
                                                    Parser.tokenizer.selectNext()
                                                    if Parser.tokenizer.nexti.tipo == "INTEIRO" or Parser.tokenizer.nexti.tipo == "FRASE":
                                                        tipo = Parser.tokenizer.nexti.tipo
                                                        if tipo == "INTEIRO":
                                                            no_int = IntVal(0, [])
                                                            no_var_dec = VarDec(tipo, [arg, no_int])
                                                            no_func.children.append(no_var_dec)
                                                        elif tipo == "FRASE":
                                                            no_string = String("", [])
                                                            no_var_dec = VarDec(tipo, [arg, no_string])
                                                            no_func.children.append(no_var_dec)
                                                        #Parser.tokenizer.selectNext()
                                                        
                                            Parser.tokenizer.selectNext()

                    if Parser.tokenizer.nexti.tipo == "F_PARENTESES":
                        Parser.tokenizer.selectNext()
                        #no_func = FuncDec(name_func, variaveis)
                        if Parser.tokenizer.nexti.tipo == "TYPE":
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.nexti.tipo == "INTEIRO" or Parser.tokenizer.nexti.tipo == "FRASE":
                                tipo_func = Parser.tokenizer.nexti.tipo
                                no_func.value = tipo_func
                                #print("NO_FUNC.VALUE: ", no_func.value)
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.nexti.tipo == "ABRE_CHAVES":
                                    Parser.tokenizer.selectNext()
                                    no_block = Block('', [])
                                    while Parser.tokenizer.nexti.tipo != "FECHA_CHAVES":
                                        block = Parser.parseStatement()
                                        if block.__class__.__name__ != "NoOp":
                                            no_block.children.append(block)
                                        
                                    Parser.tokenizer.selectNext()
                                    if Parser.tokenizer.nexti.tipo == "BARRA_N":
                                        no_func.children.append(no_block)
                                        #no_func = FuncDec(name_func, variaveis, block)
                                        return no_func
                
        elif Parser.tokenizer.nexti.tipo == "BARRA_N":
            Parser.tokenizer.selectNext()
            return NoOp('', [])                   
        
        else:
            print(Parser.tokenizer.nexti.tipo)
            raise

            
    def run(args):
        Parser.tokenizer = Tokenizer(args)
        Parser.tokenizer.selectNext()
        res = Parser.parseBlock()
        if Parser.tokenizer.nexti.tipo != "EOF":
            #print(Parser.tokenizer.nexti.tipo)
            raise
        
        return res


st = SymbolTable()     
args = sys.argv[1]
arq = open(args, 'r')
ast = Parser.run(PrePro.filtering(arq.read()))
ast.evaluate(st)