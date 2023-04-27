%{
    #include <iostream>
    #include <stdio.h>
    #include <string.h>

    #include "program_bison.tab.h"

    extern "C" int yylex(void);

    using namespace std;

    void count(void);

    
%}

%%

"+"             return PLUS;
"-"             { return MINUS;}
"*"             { return MULT;}
"/"             { return DIV;}

"||"            { return OR;}
"&&"            { return AND;}

"="             { return IGUAL;}
"=="            { return COMPARE;}
">"             { return MAIOR;}
"<"             { return MENOR;}
"!"             { return NOT;}

"{"             { return ABRE_CHAVES;}
"}"             { return FECHA_CHAVES;}
"("             { return ABRE_PAR;}
")"             { return FECHA_PAR;}

variavel        { return var;}
int             { return INT;}
String          { return STRING;}

enquanto        { return enquanto;}
se              { return SE;}
se_nao          { return SE_NAO;}
[ \t\n]         ;

Print           {return PRINT;}
Read            {return READ;}


1-9[0-9]+          { return NUM;}
a-zA-Z[a-zA-Z0-9]*    { return IDENT;}
"[a-zA-Z0-9]*"    { return STRINGVAL;}
.               ;
%%
