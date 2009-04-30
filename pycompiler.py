class Compiler:
	
	def __init__(self):
		self.string_constants = {}
		self.seq = 0

	def get_arg(self, a):
		if a in self.string_constants:
			return self.string_constants[a]
		seq = self.seq
		self.seq += 1
		self.string_constants[a] = seq
		return seq
	
	def output_constants(self):
		print("\t.section\t.rodata")
		for c,seq in self.string_constants.items():
			print(".LC" + str(seq) + ":")
			print("\t.string \"" + str(c) + "\"")
	
	def compile_exp(self, exp):
		call = str(exp[0])
		temp_args = exp[1:]
		args = map(self.get_arg, temp_args)
		print("\tsubl\t$4,%esp")
		for a in args:
			print("\tmovl\t$.LC" + str(a) + ",(%esp)")
		print("\tcall\t" + str(call))
		print("\taddl\t$4, %esp")

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

prog = ['puts', "Hello World"]
compiler = Compiler()
compiler.compile(prog)

