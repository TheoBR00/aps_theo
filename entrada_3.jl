funcao concatena(variavel x: Frase):Frase{
variavel a: Frase
a = "numero igual a "
a = a . x
retorna a
}

variavel a: Frase
variavel b: Frase

a = "3"
b = concatena(a)
printa_ai(b)
