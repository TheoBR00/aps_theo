# aps_theo

EBNF LINGUAGEM

FUNC_DEF = "funcao", IDENT, "(", {VARDEC}, ")", ":", TIPO, BLOCK_FUNC;

TIPO = "Inteiro" | "Frase";

COMPARISONS_REL = "==" | "<" | ">" | ".";

COMPARISONS_TERM = "*" | "/" | "&&";

COMPARISONS_EXP = "+" | "-" | "|";

BLOCK_FUNC = (STATEMENT);

RELEXPRESSION = EXPRESSION, {(COMPARISONS_REL), EXPRESSION};

TERM = FACTOR, {(COMPARISONS_TERM), FACTOR};

EXPRESSION = TERM, {(COMPARISONS_EXP), TERM};

FACTOR = NUMERO | STRING | IDENT, {"(", RELEXPRESSION, {",", RELEXPRESSION}, ")"} | ("+"), FACTOR | ("-"), FACTOR | ("!"), FACTOR | "(", RELEXPRESSION, ")" | READLINE | "(", RELEXPRESSION, ")";

STATEMENT = (PRINT, "\n" | ATRIBUIÇÃO, "\n" | RETURN, "\n" | PRINT, "\n"| WHILE, "\n" | IF, "\n" | FUNC_DEF, "\n" | "\n");

ATRIBUIÇÃO = IDENT, {",", IDENT}, "=", RELEXPRESSION;

DECLARACAO_VAR = "variavel", IDENT, {",", IDENT}, ":", TIPO | "variavel", IDENT, {",", IDENT}, ":", TIPO, "=", RELEXPRESSION;

PRINT = "printa_ai", "(", RELEXPRESSION, ")";

LETTER = (a |...|z|A|...|Z);

NUMBER = DIGIT, {DIGIT};

DIGIT = (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9);

STRING = ",{LETTER | NUMBER, {LETTER | NUMBER}},";

IDENT = LETTER ,{LETTER | NUMBER | "_"};

WHILE = "enquanto", "(", RELEXPRESSION, ")", STATEMENT;

IF = "se", "(", RELEXPRESSION, ")", "{", "\n", STATEMENT, {"senao", STATEMENT};

READLINE = "leitura", "(", ")";

RETURN = "retorna", RELEXPRESSION;
