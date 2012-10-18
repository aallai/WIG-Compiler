# ply lexing

import ply.lex as lex

states = (
	('html', 'exclusive'),
	('tags', 'exclusive'),
	('holes', 'exclusive'),
)

reserved = {
	'service' : 'SERVICE',
	'const' : 'CONST',
	'html' : 'HTML',
	'schema' : 'SCHEMA',
	'int' : 'INT',
	'bool' : 'BOOL',
	'string' : 'STRING',
	'void' : 'VOID',
	'tuple' : 'TUPLE',
	'session' : 'SESSION',
	'show' : 'SHOW',
    'receive' : 'RECEIVE',
	'exit' : 'EXIT',
	'return' : 'RETURN',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'plug' : 'PLUG',
	'true' : 'TRUE',
	'false' : 'FALSE',	
}

# reserved words in html tags
tag_reserved = {
	'input' : 'INPUT',
	'select' : 'SELECT',
}

tokens = [
	'START_HTML_LITERAL', 
	'END_HTML_LITERAL', 
	'INT_LITERAL', 
	'STRING_LITERAL',
	'IDENTIFIER', 
	'META',
	'WHATEVER',
	'START_TAG',
	'START_CLOSE_TAG',
	'END_TAG',
	'START_HOLE',
	'END_HOLE',
	'OR',
	'AND',
	'LSHIFT',
	'EQ',
	'NEQ',
	'LTEQ',
	'GTEQ',
	'TADD',
	'TSUB',
] + reserved.values() + tag_reserved.values()

literals = ('+', '-', '/', '*', '%', '(', ')', '{', '}', '[', ']', '=', '<', '>', ';', ',', '!', '.')

#
# html 
# 

def t_START_HTML_LITERAL(t) :
	'<html>'
	t.lexer.push_state('html')
	return t


def t_html_END_HTML_LITERAL(t) :
	'</html>'
	t.lexer.pop_state()
	return t

t_holes_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_html_META = r'<!--(.|\n)*-->'

t_html_WHATEVER = r'[^<>]+'

def t_html_START_CLOSE_TAG(t) :
	r'</'
	t.lexer.push_state('tags')
	return t

def t_html_START_HOLE(t) :
	r'<\['
	t.lexer.push_state('holes')
	return t

def t_holes_END_HOLE(t) :
	r'\]>'
	t.lexer.pop_state()
	return t

def t_html_START_TAG(t) :
    r'<'
    t.lexer.push_state('tags')
    return t

def t_tags_END_TAG(t) :
    r'>'
    t.lexer.pop_state()
    return t

def t_tags_IDENTIFIER(t) :
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = tag_reserved.get(t.value, 'IDENTIFIER')
    return t

#
# Wig
#

def t_IDENTIFIER(t) :
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'IDENTIFIER')
	return t

def t_INT_LITERAL(t) :
	r'0|([1-9][0-9]*)'
	t.value = int(t.value)
	return t

def t_tags_INITIAL_STRING_LITERAL(t) :
	r'"[^"]*"'
	# get rid of "s	
	t.value = t.value[1:-1]
	return t	

t_EQ = '=='
t_NEQ = '!='
t_LTEQ = '<='
t_GTEQ = '>='
t_AND = '&&'
t_OR = r'\|\|'
t_LSHIFT = '<<'

# tuple add and subtract??
t_TADD = r'\\\+'
t_TSUB = r'\\-'


def t_ANY_newline(t) :
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ANY_ignore = ' \t'

# print token and skip ahead?
def t_ANY_error(t) :
	tok = t.value.split()[0]
	print 'Illegal token ' + tok
	t.lexer.skip(len(tok)) 	

lexer = lex.lex()
 
