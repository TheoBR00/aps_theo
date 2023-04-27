%{
    #include <iostream>
    using namespace std;

    extern int yyparse();
    extern "C" int yylex(void);
    extern FILE **yyin;

    void yyerror(const char *s){
        fprintf (stderr, "erro: %s\n", s);
    }
%}

%union{
    int num;
    char *nomes;
}

%token PLUS
%token MINUS
%token MULT
%token DIV
%token var
%token INT
%token STRING
%token STRINGVAL

%token INTVAL
%token OR
%token AND
%token IGUAL
%token COMPARE
%token MAIOR
%token MENOR
%token NOT
%token ABRE_CHAVES
%token FECHA_CHAVES
%token ABRE_PAR
%token FECHA_PAR
%token enquanto
%token SE
%token SE_NAO
%token PRINT
%token READ

%type <nomes> STRING var STRINGVAL
%type <num> INTVAL PRINT
%type <nomes> PLUS MINUS MULT DIV
%type <nomes> OR AND
%type <nomes> IGUAL COMPARE MAIOR MENOR NOT
%type <nomes> ABRE_CHAVES FECHA_CHAVES ABRE_PAR FECHA_PAR
%type <nomes> enquanto SE SE_NAO
%type <nomes> STATEMENT_FUNC


%%

tipo: INT | STRING

arg_func: ""
        | vardec
        | vardec "," arg_func

ident : IDENT

chama_ident : ident
            | ident "," chama_ident

vardec : var chama_ident ":" tipo

chama_state: STATEMENT_FUNC
            | STATEMENT_FUNC chama_state

chama_exp : EXPRESSION
          | EXPRESSION chama_exp

chama_term : TERM
            | TERM chama_term

chama_factor : FACTOR
              | FACTOR chama_factor

function-def : tipo STRINGVAL ABRE_PAR arg_func FECHA_PAR BLOCK_FUNC

BLOCK_FUNC : ABRE_CHAVES chama_state FECHA_CHAVES

STATEMENT_FUNC : ident "=" REL_EXP ";"
                | PRINT ABRE_PAR REL_EXP FECHA_PAR ';'
                | enquanto ABRE_PAR REL_EXP FECHA_PAR STATEMENT_FUNC
                | BLOCK_FUNC
                | SE ABRE_PAR REL_EXP FECHA_PAR STATEMENT_FUNC
                | SE ABRE_PAR REL_EXP FECHA_PAR STATEMENT_FUNC SE_NAO STATEMENT_FUNC

REL_EXP : EXPRESSION COMPARE chama_exp
        | EXPRESSION MAIOR chama_exp
        | EXPRESSION MENOR chama_exp

EXPRESSION : TERM                       
            | TERM PLUS TERM            
            | TERM MINUS chama_term     
            | TERM OR chama_term        

TERM : FACTOR
      | FACTOR MULT chama_factor
      | FACTOR DIV chama_factor
      | FACTOR AND chama_factor

FACTOR: INTVAL
      | ident
      | PLUS FACTOR
      | MINUS FACTOR
      | NOT FACTOR
      | ABRE_PAR REL_EXP FECHA_PAR
      | READ ABRE_PAR FECHA_PAR

%%
