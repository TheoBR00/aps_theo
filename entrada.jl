funcao fatorial(variavel x: Inteiro):Inteiro{
variavel a: Inteiro
a = x
x = x - 1
enquanto(x > 0){
a = a * x
x = x - 1
}
retorna a

}
variavel a: Inteiro
variavel b: Inteiro

a = 5

b = fatorial(a)
printa_ai(b)
