prog = ['do',
	['if', ['strlen',""],
		['puts', "IF: The string was not empty"],
		['puts', "ELSE: The string was empty"]
	],
	['if', ['strlen',"Test"],
		['puts', "Second IF: The string was not empty"],
		['puts', "Second IF: The string was empty"]
	]
]
prog = ['do',
	['call', ['lambda', [], ["printf", "%ld", ["strlen", "Test"]]], [] ]
]
prog = ['defun', 'while', ['cond', 'body'],
			['if', ['apply', 'cond', []], 
				['do', 
					['apply', 'bod', []],
					['while', 'cond', 'body']
				],
				[]
			]
		]
