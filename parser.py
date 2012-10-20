import ply.yacc as yacc
from lexer import tokens
from tree import *

precedence = (
    ('left', 'LSHIFT', 'TADD', 'TSUB'), # no idea what these do
    ('left', 'AND', 'OR'),
    ('nonassoc', '=', 'EQ', 'NEQ', '<', '>', 'LTEQ', 'GTEQ'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', '!'),
    ('right', 'UMINUS'),
)

def p_error(p) :
    print 'Syntax error at line ' + str(p.lineno) + ' on token ' + p.value 

# for the non-empty productions
def build_list(p, offset=0) :
    if len(p) > 2 :
        return [p[1]] + p[2 + offset]
    else :
        return [p[1]]

# for possibly empty productions
# None value denotes the empty production
def build_empty(p) :
    if len(p) > 1 :
        return p[1]
    else :
        return None

# I'm adding a variables production, this creates shift/reduce conflicts but
# simplifies the grammar. 
def p_service(p) :
    '''
    service : SERVICE '{' htmls schemas variables functions sessions '}'
    '''    
    p[0] = Service(*p[3:-1])


def p_htmls(p) :
    '''
    htmls : html 
          | html htmls
    '''
    p[0] = build_list(p)

def p_html(p) :  
    '''
    html : CONST HTML IDENTIFIER '=' START_HTML_LITERAL nehtmlbodies END_HTML_LITERAL ';'
    '''
    p[0] = HTML(p[3], p[6])

def p_emptyhtml(p) :
    '''
    html : CONST HTML IDENTIFIER '=' START_HTML_LITERAL END_HTML_LITERAL ';'
    '''
    p[0] = HTML(p[3], None)

def p_nehtmlbodies(p) :
    '''
    nehtmlbodies : htmlbody
                   | htmlbody nehtmlbodies
    '''
    p[0] = build_list(p)

def p_tag(p) :
    '''
    htmlbody : START_TAG IDENTIFIER attributes END_TAG  
    '''
    p[0] = Tag(p[2], p[3])

def p_closing_tag(p) :
    '''
    htmlbody : START_CLOSE_TAG IDENTIFIER END_TAG 
    '''
    p[0] = ClosingTag(p[2])

def p_hole(p) :
    '''
    htmlbody : START_HOLE IDENTIFIER END_HOLE
    '''
    p[0] = Hole(p[2])

def p_whatever(p) :
    '''
    htmlbody : WHATEVER
    '''
    p[0] = Whatever(p[1])

def p_meta(p) :
    '''
    htmlbody : META
    '''
    p[0] = Meta(p[1])

def p_forminput(p) :
    '''
    htmlbody : START_TAG INPUT attributes END_TAG
    '''
    p[0] = FormInput(p[3])

def p_select(p) :
    '''
    htmlbody : START_TAG SELECT attributes END_TAG nehtmlbodies START_CLOSE_TAG SELECT END_TAG
    '''
    p[0] = FormSelect(p[3], p[5])

def p_emptyselect(p) :
    '''
    htmlbody : START_TAG SELECT attributes END_TAG START_CLOSE_TAG SELECT END_TAG
    '''
    p[0] = FormSelect(p[3], None)

# skipping inputattrs since it allows arbitrary attributes anyways
def p_attributes(p) :
    '''
    attributes : 
               | neattributes
    '''
    p[0] = build_empty(p)

def p_neattributes(p) :
    '''
    neattributes : attribute
                 | attribute neattributes
    '''
    p[0] = build_list(p)

def p_attribute(p) :
    '''
    attribute : attr
              | attr '=' attr
    '''
    if len(p) > 2 :
        p[0] = Attribute(p[1], p[3])
    else :
        p[0] = Attribute(p[1], None)

def p_attr(p) :
    '''
    attr : IDENTIFIER
         | STRING_LITERAL
    '''
    p[0] = p[1]

def p_schemas(p) :
    '''
    schemas :
            | neschemas
    '''
    p[0] = build_empty(p)

def p_neschemas(p) :
    '''
    neschemas : schema
              | schema neschemas
    '''
    p[0] = build_list(p)

def p_schema(p) :
    '''
    schema : SCHEMA IDENTIFIER '{' fields '}'    
    '''

def p_fields(p) :
    '''
    fields : 
           | nefields
    '''
    p[0] = build_empty(p)

def p_nefields(p) :
    '''
    nefields : field
             | field nefields
    '''
    p[0] = build_list(p)

def p_field(p) :
    '''
    field : simpletype IDENTIFIER ';'
    '''
    p[0] = Field(p[2], p[1])

def p_variables(p) :
    '''
    variables :
              | nevariables
    '''
    p[0] = build_empty(p)

def p_nevariables(p) :
    '''
    nevariables : variable
                | variable nevariables
    '''
    p[0] = build_list(p)

def p_variable(p) :
    '''
    variable : type identifiers ';'
    '''
    p[0] = Variables(p[2], p[1])

def p_identifiers(p) :
    '''
    identifiers : IDENTIFIER
                | IDENTIFIER ',' identifiers
    '''
    p[0] = build_list(p, 1)    

def p_simpletype(p) :
    '''
    simpletype : INT 
               | BOOL 
               | STRING 
               | VOID
    '''
    p[0] = Type(p[1])

def p_type(p) :
    '''
    type : simpletype
         | TUPLE IDENTIFIER
    '''
    if len(p) > 2 :
        p[0] = Type(p[1], p[2])
    else :
        p[0] = p[1]

def p_functions(p) :
    '''
    functions :
              | nefunctions
    '''
    p[0] = build_empty(p)

def p_nefunction(p) :
    '''
    nefunctions : function
                | function nefunctions
    '''
    p[0] = build_list(p)

def p_function(p) :
    '''
    function : type IDENTIFIER '(' arguments ')' compoundstm
    '''
    p[0] = Function(p[1], p[2], p[4], p[6])

def p_arguments(p) :
    '''
    arguments :
              | nearguments
    '''
    p[0] = build_empty(p)

def p_nearguments(p) :
    '''
    nearguments : argument
                | argument ',' nearguments
    '''
    p[0] = build_list(p, 1)

def p_argument(p) :
    '''
    argument : type IDENTIFIER
    '''
    p[0] = Argument(p[1], p[2])

def p_sessions(p) :
    '''
    sessions : session
             | session sessions
    '''
    p[0] = build_list(p)

def p_session(p) :
    '''
    session : SESSION IDENTIFIER '(' ')' compoundstm
    '''
    p[0] = Session(p[2], p[5])

def p_stms(p) :
    '''
    stms :
         | nestms
    '''
    p[0] = build_empty(p)

def p_nestms(p) :
    '''
    nestms : stm
           | stm nestms
    '''
    p[0] = build_list(p)

def p_estm(p) :
    '''
    stm : ';'
    '''
    pass

def p_show(p) :
    '''
    stm : SHOW document receive ';'
    '''
    p[0] = Show(p[2], p[3])

def p_exit(p) :
    '''
    stm : EXIT document ';'
    '''
    p[0] = Exit(p[2])

def p_return(p) :
    '''
    stm : RETURN ';'
        | RETURN exp ';'
    '''
    if len(p) > 3 :
        p[0] = Return(p[3])
    else :
        p[0] = Return(None)


def p_if(p) :
    '''
    stm : IF '(' exp ')' stm
    '''
    p[0] = If(p[3], p[5])

def p_ifelse(p) :
    '''
    stm : IF '(' exp ')' stm ELSE stm 
    '''
    p[0] = IfEsle(p[3], p[5], p[7])


def p_while(p) :
    '''
    stm : WHILE '(' exp ')' compoundstm
    '''
    p[0] = While(p[3], p[5])

def p_blockexpstm(p) :
    '''
    stm : compoundstm
        | exp ';'
    '''
    p[0] = p[1]


def p_document(p) :
    '''
    document : IDENTIFIER
             | PLUG IDENTIFIER '[' plugs ']'
    '''
    if len(p) > 2 :
        p[0] = Document(p[2], p[4])
    else :
        p[0] = Document(p[1], None)

def p_receive(p) :
    '''
    receive :
            | RECEIVE '[' inputs ']'
    '''
    p[0] = Receive(p[3])

def p_block(p) :
    '''
    compoundstm : '{' variables stms '}'
    '''
    p[0] = Block(p[2], p[3])

def p_plugs(p) :
    '''
    plugs : plug
          | plug ',' plugs
    '''
    p[0] = build_list(p, 1)

def p_plug(p) :
    '''
    plug : IDENTIFIER '=' exp
    '''
    p[0] = Plug(p[1], p[3])

def p_inputs(p) :
    '''
    inputs :
           | neinputs
    '''
    p[0] = build_empty(p)

def p_neinputs(p) :
    '''
    neinputs : input
             | input ',' neinputs
    '''
    p[0] = build_list(p)

def p_input(p) :
    '''
    input : lvalue '=' IDENTIFIER
    '''
    p[0] = Input(p[1], p[2])

def p_binexp(p) :
    '''
    exp : lvalue '=' exp
        | exp EQ exp
        | exp NEQ exp
        | exp '<' exp
        | exp '>' exp
        | exp LTEQ exp
        | exp GTEQ exp
        | exp '+' exp
        | exp '-' exp
        | exp '*' exp
        | exp '/' exp
        | exp '%' exp
        | exp AND exp
        | exp OR exp
        | exp LSHIFT exp
    '''
    p[0] = BinaryExp(p[1], p[2], p[3])

# no idea what these do, im assuming they work on tuples?
def p_tuplebinaryexp(p) :
    '''
    exp : exp TADD IDENTIFIER
        | exp TADD '(' identifiers ')'
        | exp TSUB IDENTIFIER
        | exp TSUB '(' identifiers ')'
    '''
    if len(p) > 4 :
        p[0] = TupleBinaryExp(p[1], p[2], p[4])
    else :
        p[0] = TupleBinaryExp(p[1], p[2], p[3])

def p_unaryexp(p) :
    '''
    exp : '-' exp %prec UMINUS
        | '!' exp
    '''
    p[0] = UnaryExp(p[1], p[2])

def p_lval(p) :
    '''
    exp : lvalue
    '''
    p[0] = p[1]

def p_call(p) :
    '''
    exp : IDENTIFIER '(' exps ')'
    '''
    p[0] = Call(p[1], p[3])

def p_stringliteral(p) :
    '''
    exp : STRING_LITERAL
    '''
    p[0] = p[1]

def p_boolliteral(p) :
    '''
    exp : TRUE
        | FALSE
    '''
    if p[1] == 'true' :
        p[0] = True
    else :
        p[0] = False

def p_intliteral(p) :
    '''
    exp : INT_LITERAL
    '''
    p[0] = int(p[1])

def p_tupleliteral(p) :
    '''
    exp : TUPLE '{' fieldvalues '}'
    '''
    p[0] = Tuple(p[3])

def p_group(p) :
    '''
    exp : '(' exp ')'
    '''
    p[0] = p[2]

def p_exps(p) :
    '''
    exps :
         | neexps
    '''
    p[0] = build_empty(p)

def p_neexps(p) :
    '''
    neexps : exp
           | exp ',' neexps
    '''
    p[0] = build_list(p, 1)

def p_lvalue(p) :
    '''
    lvalue : IDENTIFIER
           | IDENTIFIER '.' IDENTIFIER
    '''
    p[0] = ''.join(p[1:])

def p_fieldvalues(p) :
    '''
    fieldvalues :
                | nefieldvalues
    '''
    p[0] = build_empty(p)

def p_nefieldvalues(p) :
    '''
    nefieldvalues : fieldvalue
                  | fieldvalue ',' fieldvalues
    '''
    p[0] = build_list(p, 1)


def p_fieldvalue(p) :
    '''
    fieldvalue : IDENTIFIER '=' exp
    '''
    p[0] = FieldValue(p[1], p[3])


parser = yacc.yacc()

