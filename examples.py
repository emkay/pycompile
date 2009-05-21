"""
Example of using if statement.
"""
prog_example1 = ['do',
	['if', ['strlen',""],
		['puts', "IF: The string was not empty"],
		['puts', "ELSE: The string was empty"]
	],
	['if', ['strlen',"Test"],
		['puts', "Second IF: The string was not empty"],
		['puts', "Second IF: The string was empty"]
	]
]
"""
Example of a lambda.
"""
prog_example2 = ['do',
	['call', ['lambda', [], ["printf", "%ld", ["strlen", "Test"]]], [] ]
]

"""
Example of function definition.
"""
prog_example3 = ['defun', 'while', ['cond', 'body'],
			['if', ['apply', 'cond', []], 
				['do', 
					['apply', 'bod', []],
					['while', 'cond', 'body']
				],
				[]
			]
		]
"""
Example of function definition with argument passing.
"""
prog_example4 = ['do', 
	['defun', 'myputs', ['foo'], ['puts', 'foo']],
	['myputs', "TESTING MYPUTS"],
]
