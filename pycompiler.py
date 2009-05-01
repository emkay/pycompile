def is_list(l):
	return type(l) == type([])

class Compiler:
	
	def __init__(self):
		self.string_constants = {}
		self.seq = 0
		self.PTR_SIZE = 4

	def get_arg(self, a):
		if is_list(a):
			self.compile_exp(a)
			return ['subexpr', False]
		if a in self.string_constants:
			return self.string_constants[a]
		seq = self.seq
		self.seq += 1
		self.string_constants[a] = seq
		return ['strconst', seq]

	def output_constants(self):
		print("\t.section\t.rodata")
		for c,seq in self.string_constants.items():
			print(".LC" + str(seq) + ":")
			print("\t.string \"" + str(c) + "\"")
	
	def compile_exp(self, exp):
		if exp[0] == 'do':
			exp.pop(0)
			map(self.compile_exp, exp)
			return True
				
		call = str(exp[0])
		stack_adjustment = self.PTR_SIZE + int(round((len(exp) - 1 + 0.5) * self.PTR_SIZE / (4.0 * self.PTR_SIZE))) * (4 * self.PTR_SIZE)
		#args = map(self.get_arg, exp[1:])
		#stack_adjustment = self.PTR_SIZE + int(round((len(args)+0.5) * self.PTR_SIZE / (4.0 * self.PTR_SIZE))) * (4 * self.PTR_SIZE)
		if exp[0] != 'do':
			print("\tsubl\t$" + str(stack_adjustment) + ", %esp")
		count = 0
		for a in exp[1:]:
			atype, aparam = self.get_arg(a)
			if exp[0] != 'do':
				if atype == 'strconst':
					param = "$.LC" + str(aparam)
				else:
					param = "%eax"
			if count > 0:
				i = count * self.PTR_SIZE
			else:
				i = ""
			print("\tmovl\t" + str(param) + ", " + str(i) + "(%esp)")
			count += 1
		print("\tcall\t" + str(call))
		print("\taddl\t$" + str(stack_adjustment) + ", %esp")

	def compile(self, exp):
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
		self.compile_exp(exp)
		print("""
	popl	%ecx
	popl	%ebp
	leal	-4(%ecx), %esp
	ret
		""")
		self.output_constants()

"""
prog = ['do',
	['printf', 'Hello'],
	['printf', ' '],
	['printf', 'World']
]
"""
prog = ['printf',"'hello world' takes %ld bytes", ['strlen', "hello world"]]
compiler = Compiler()
compiler.compile(prog)
