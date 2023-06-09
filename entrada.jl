funcao fatorial(variavel x: Inteiro):Inteiro{
variavel a: Inteiro
a = x
se(a == 0){
a = a + 1
retorna a
}
x = x - 1
enquanto(x > 0){
a = a * x
x = x - 1
}
retorna a
}
variavel a: Inteiro
variavel b: Inteiro

a = leitura()

enquanto(a < 0){
printa_ai("Numero menor que zero! Tente novamente")
a = leitura()
}
b = fatorial(a)
printa_ai(b)
