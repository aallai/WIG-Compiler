
# for now i'm going with a joos style dummy AST, so I can start
# writing and testing the parser

# should probably add a baseclass later with linenos

class Service(object) :
	
	def __init__(self, htmls, schemas, variables, functions, sessions) :
		self.htmls = htmls
		self.schemas = schemas
		self.variables = variables
		self.functions = functions
		self.sessions = sessions


class HTML(object) :
	
	def __init__(self, identifier, body) :
	
		'Body is a list of HTML elements'
		
		self.identifier = identifier
		self.body = body


class Tag(object) :
	
	'HTML opening tag.'

	def __init__(self, identifier, attrs) :
		
		'attrs is a list of HTML attributes'
		self.identifier = identifier
		self.attrs = attrs

class ClosingTag(object) :
	
	'HTML closing tag, i.e. </script>'

	def __init__(self, identifier) :
		self.identifier = identifier

class Hole(object) :

	'WIG hole, i.e. <[ var ]>'

	def __init__(self, identifier) :
		self.identifier = identifier

class Whatever(object) :

	'The "whatever" production from the grammar.'

	def __init__(self, value) :
		'Value is the string the lexer matched'
		self.value = value

class Meta(object) :

	'HTML comment'

	def __init__(self, value) :
		'Value is the lexed string'
		self.value = value

class FormInput(object) :

	def __init__(self, attrs) :
		'attrs is a list of HTML attributes'
		self.attrs = attrs

class FormSelect(object) :

	'HTML select tag'

	def __init__(self, attrs, body) :
		'Body is a list of HTML elements'
		self.attrs = attrs
		self.body = body

class Attribute(object) :

	'HTML tag attribute'	
	
	def __init__(self, name, value) :

		'Value can be None'

		self.name = name
		self.value = value

class Schema(object) :

	def __init__(self, identifier, fields) :
		self.identifier = identifier
		self.fields = fields

class Field(object) :

	def __init__(self, identifier, type_) :
		self.identifier = identifier
		self.type_ = type_


class Variables(object) :

	'Declaration of one or more vars of same type.'
	
	def __init__(self, identifiers, type_) :
		'identifiers is a list'
		self.identifiers = identifiers
		self.type_ = type_

class Type(object) :

	'Simple and tuple types'

	def __init__(self, type_, identifier=None) :
		'The tuple type has an identifier which probably refers to the schema.'
		self.type_ = type_
		self.identifier = identifier

class Function(object) :

	def __init__(self, type_, identifier, args, body) :
		self.identifier = identifier
		self.type_ = type_
		self.args = args
		self.body = body

class Argument(object) :

	def __init__(self, type_, identifier) :
		self.type_ = type_
		self.identifier = identifier


class Session(object) :
	
	def __init__(self, identifier, body) :
		self.identifier = identifier
		self.body = body

class Show(object) :

    def __init__(self, doc, recv) :
        'doc van be a plug or  html const, recv can be None'
        self.doc = doc
        self.recv = recv


class Exit(object) :

    def __init__(self, doc) :
        self.doc = doc

class Return(object) :
    
    def __init__(self, exp) :
        'exp can be None'
        self.exp = exp

class If(object) :

    def __init__(self, exp, block) :
        self.exp = exp
        self.block = block

class IfElse(object) :

    def __init__(self, exp, if_block, else_block) :
        self.exp = exp
        self.if_block = if_block
        self.esle_block = else_block

class While(object) :
    
    def __init__(self, exp, block) :
        self.exp = exp
        self.block = block

class Document(object) :

    def __init__(self, identifier, plugs) :
        'plugs can be None'
        self.identifier = identifier
        self.plugs = plugs

class Receive(object) :
    
    def __init__(self, inputs) :
        self.inputs = inputs


class Block(object) :

    def __init__(self, variables, stms) :
        'Both potentially empty'
        self.variables = variables
        self.stms = stms

class Plug(object) :

    def __init__(self, identifier, exp) :
        self.identifier = identifier
        self.exp = exp

class Input(object) :
    
    def __init__(self, lval, identifier) :
        self.lval = lval
        self.identifier = identifier

class BinaryExp(object) :

    def __init__(self, left, op, right) :
        self.left = left
        self.right = right
        self.op = op

# tuples?
class TupleBinaryExp(object) :

    def __init__(self, exp, op, identifiers) :
        self.exp = exp
        self.op = op
        self.identifiers = identifiers

class UnaryExp(object) :
    
    def __init__(self, op, exp) :
        self.op = op
        self.exp = exp


class Call(object) :

    def __init__(self, func, args) :
        'args are unevalutated exps'
        self.func = func
        self.args = args

class Tuple(object) :

    'Tuple literal'

    def __init__(self, fieldvalues) :
           self.fieldvalues = fieldvalues

class FieldValue(object) :
    
    'Tuple literal field'

    def __init__(self, identifier, exp) :
        self.identifier = identifier
        self.exp = exp

