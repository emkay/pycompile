SYMBOLS = ['do', 'defun', 'puts', 'printf', 'strlen']
FUNCTIONS = {}
def is_list(l):
	return type(l) == type([])
def is_int(n):
	return type(n) == type(1)
def is_atom(a):
	return a in SYMBOLS or a in FUNCTIONS.keys()

class Function:
	def __init__(self, args, body):
		self.args = args
		self.body = body

class Scope:
	def __init__(self, compiler, func):
		self.c = compiler
		self.func = func
	
	def get_arg(self, a):
		count = 0
		for arg in self.func.args:
			if arg == a:
				return ['arg', count]
			count += 1
		return ['atom', a]

class Compiler:
	
	def __init__(self, before, after):
		self.DO_BEFORE = before
		self.DO_AFTER = after
		self.string_constants = {}
		self.seq = 0
		self.PTR_SIZE = 4

	def get_arg(self, a, scope=False):
		if is_atom(a):
			return scope.get_arg(a)
		if is_int(a):
			return ['int', a]
		if is_list(a):
			self.compile_exp(a)
			return ['subexpr', False]
		if a in self.string_constants:
			return self.string_constants[a]
		seq = self.seq
		self.seq += 1
		self.string_constants[a] = seq
		return ['strconst', seq]
	
	def defun(self, name, args, body):
		FUNCTIONS[name] = Function(args, body)
		return ['subexpr']
	
	def ifelse(self, cond, if_branch, else_branch):
		self.compile_exp(cond)
		print("\ttestl\t%eax, %eax")
		self.seq += 2
		else_branch_seq = self.seq - 1
		end_if_branch_seq = self.seq
		print("\tje\t.L" + str(else_branch_seq))
		self.compile_exp(if_branch)
		print("\tjmp\t.L" + str(end_if_branch_seq))
		print(".L" + str(else_branch_seq) + ":")
		self.compile_exp(else_branch)
		print(".L" + str(end_if_branch_seq) + ":")


	def output_functions(self):
		for name, func in FUNCTIONS.items():
			print(".globl " + str(name))
			print("\t.type\t" + str(name) + ", @function")
			print(str(name) + ":")
			print("\tpushl\t%ebp")
			print("\tmovl\t%esp, %ebp")
			self.compile_exp(func.body, Scope(self, func))
			print("\tleave")
			print("\tret")
			print("\t.size\t" + str(name) + ", .-" + str(name))

	def output_constants(self):
		print("\t.section\t.rodata")
		for c,seq in self.string_constants.items():
			print(".LC" + str(seq) + ":")
			print("\t.string \"" + str(c) + "\"")
	
	def compile_lambda(self, args, body):
		name = "lambda__" + str(self.seq)
		self.seq += 1
		self.defun(name, args, body)
		print("\tmovl\t$" + str(name) + ",%eax")
		return ['subexpr']
	
	def compile_eval_arg(self, arg, scope=False):
		atype, aparam = self.get_arg(arg, scope)
		if atype == 'strconst':
			return "$.LC" + str(aparam)
		if atype == 'int':
			return "$" + str(aparam)
		if atype == 'atom':
			return str(aparam)
		if atype == 'arg':
			return "\tmovl\t" + str(self.PTR_SIZE * (aparam + 2)) + "(%ebp),%eax"
		return "%eax"
	
	def compile_call(self, func, args):
		function = Function(args, func)
		stack_adjustment = self.PTR_SIZE + int(round(((len(args) + 0.5) * self.PTR_SIZE / (4.0 * self.PTR_SIZE)))) * (4 * self.PTR_SIZE)
		print("\tsubl\t$" + str(stack_adjustment) + ", %esp")
		count = 0
		scope = Scope(self, function)
		for a in args:
			param = self.compile_eval_arg(a, scope)
			if count > 0:
				i = count * 4
			else:
				i = ""
			print("\tmovl\t" + str(param)  + "," + str(i) + "(%esp)")
			count += 1
		res = self.compile_eval_arg(func, scope)
		if res == "%eax":
			res = "*%eax"
		print("\tcall\t" + str(res))
		print("\taddl\t$" + str(stack_adjustment) + ", %esp")
		return ['subexpr']
	
	def compile_do(self, exp):
		map(self.compile_exp, exp)
		return ['subexpr']

	def compile_exp(self, exp, scope=False):
		if not exp or len(exp) == 0:
			return False
		if exp[0] == 'do':
			self.compile_do(exp[1:])
			return True
		if exp[0] == 'defun':
			return self.defun(*exp[1:])
		if exp[0] == 'if':
			return self.ifelse(*exp[1:])
		if exp[0] == 'lambda':
			return self.compile_lambda(*exp[1:])
		if exp[0] == 'call':
			return self.compile_call(exp[1], exp[2])
		return self.compile_call(exp[0], exp[1:])

	def compile_main(self, exp):
		print("""
		.file	"bootstrap.py"
		.text
.globl main
		.type	main, @function
main:
	leal	4(%esp), %ecx
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	movl	%esp, %ebp
	pushl	%ecx
		""")
		main = Function([], [])
		self.compile_exp(exp, Scope(self,main))
		print("""
	popl	%ecx
	popl	%ebp
	leal	-4(%ecx), %esp
	ret
		""")
		self.output_functions()
		self.output_constants()
	
	def compile(self, exp):
		self.compile_main(['do', self.DO_BEFORE, exp, self.DO_AFTER])

DO_BEFORE = []
DO_AFTER = []

prog = ['do', 
	['defun', 'myputs', ['foo'], ['puts', 'foo']],
	['myputs', "TESTING MYPUTS"],
]


compiler = Compiler(DO_BEFORE, DO_AFTER)
compiler.compile(prog)
