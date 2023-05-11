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
%token IDENT
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
%token PONTO_VIRGULA
%token VIRGULA
%token enquanto
%token SE
%token SE_NAO
%token END
%token PRINT
%token READ


%%

chama_block: ABRE_CHAVES BLOCK_FUNC
  ;

chama_ident 
  : IDENT chama_ident_2
  ;

tipo
  : INT 
  | STRING
  ;

chama_ident_2 
  : VIRGULA chama_ident
  | IGUAL REL_EXP PONTO_VIRGULA
  ;

vardec : var chama_ident_2 ":" tipo
  ;

chama_state : END
            | SE_NAO chama_state
            | STATEMENT_FUNC chama_state
            ;

BLOCK_FUNC : FECHA_CHAVES
            | STATEMENT_FUNC BLOCK_FUNC

STATEMENT_FUNC : chama_ident
                | vardec
                | PRINT ABRE_PAR REL_EXP FECHA_PAR PONTO_VIRGULA
                | enquanto ABRE_PAR REL_EXP FECHA_PAR chama_state
                | BLOCK_FUNC
                | SE ABRE_PAR REL_EXP FECHA_PAR chama_state
                ;

REL_EXP : EXPRESSION
         | EXPRESSION MAIOR EXPRESSION
         | EXPRESSION MENOR EXPRESSION
         | EXPRESSION COMPARE EXPRESSION
         ;

EXPRESSION : TERM
            | TERM PLUS TERM
            | TERM MINUS TERM
            | TERM OR TERM
            ;

TERM : FACTOR
      | FACTOR MULT FACTOR
      | FACTOR DIV FACTOR
      | FACTOR AND FACTOR
      ;

FACTOR: INTVAL
      | IDENT
      | PLUS FACTOR
      | MINUS FACTOR
      | NOT FACTOR
      | ABRE_PAR REL_EXP FECHA_PAR
      | READ ABRE_PAR FECHA_PAR

%%