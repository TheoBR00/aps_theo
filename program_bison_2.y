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
%token PRINT
%token READ


%%

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

chama_block: ABRE_CHAVES BLOCK_FUNC
  ;

vardec : var chama_ident_2 DOIS_PONTOS tipo
  ;

chama_exp : EXPRESSION
          | EXPRESSION chama_exp
          ;

chama_term : TERM
            | TERM chama_term

chama_factor : FACTOR
              | FACTOR chama_factor

BLOCK_FUNC : FECHA_CHAVES
            | STATEMENT_FUNC BLOCK_FUNC

STATEMENT_FUNC : chama_ident
                | vardec
                | PRINT ABRE_PAR REL_EXP FECHA_PAR PONTO_VIRGULA
                | enquanto ABRE_PAR REL_EXP FECHA_PAR STATEMENT_FUNC
                | BLOCK_FUNC
                | SE ABRE_PAR REL_EXP FECHA_PAR STATEMENT_FUNC
                | SE ABRE_PAR REL_EXP FECHA_PAR STATEMENT_FUNC SE_NAO STATEMENT_FUNC
                ;

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
      | IDENT
      | PLUS FACTOR
      | MINUS FACTOR
      | NOT FACTOR
      | ABRE_PAR REL_EXP FECHA_PAR
      | READ ABRE_PAR FECHA_PAR

%%