import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Mod: op.mod,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg, ast.Eq: op.eq, ast.LtE: op.le, ast.Lt: op.lt,
             ast.GtE: op.ge, ast.Gt: op.gt, ast.NotEq: op.ne, ast.And: op.iand,
             ast.Or: op.ior}

def eval_expr(expr):
    '''
    Evaluates strings as mathmatical or conditional expressions.
    '''
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.BoolOp):
        return operators[type(node.op)](eval_(node.values[0]), eval_(node.values[1]))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    elif isinstance(node, ast.Compare):
        return operators[type(node.ops[0])](eval_(node.left), eval_(node.comparators))
    elif isinstance(node, list):
        for n in node:
            return eval_(n)
    elif isinstance(node, ast.IfExp):
        return eval_(node.body) if eval_(node.test) else eval_(node.orelse)
    else:
        raise TypeError(node)

def get_value(expression, values):
    for key, value in values.items():
        var = value
        # print '=================='
        # print 'type: {} | var: {} | is empty unicode: {}'.format(type(var), var, var == u'')
        # print 'expr: {} | var_char: {} | var: {}'.format(expression, v.variable_char, var)
        expression = expression.replace(key, str(var))
    try:
        # print "EXPRESSION", expression
        return eval_expr(expression)
    except ZeroDivisionError:
        return 0

test_values = [
    {'q': '1', 'b': '0'},
    {'q': '50', 'b': '0'},
    {'q': '75', 'b': '0'},
    {'q': '251', 'b': '1'},
    {'q': '300', 'b': '1'},
    {'q': '251', 'b': '0'},
    {'q': '300', 'b': '0'},
    {'q': '1000', 'b': '1'},
    {'q': '1100', 'b': '1'},
    {'q': '1000', 'b': '0'},
    {'q': '1100', 'b': '0'},
]

tests = [
    {
        'name': 'liscenses',
        'expr': "((140 * q) if q < 50 else (175 * q) if q <= 250  else (105 * q) if b == 0 and q < 1000 else (48 * q) if q < 1000 else (101 * 1000) if b == 0 else (46 * 1000)) + (0 if q <= 1000 else 71 * (q - 1000) if b == 0 else 32 * (q - 1000))",
        'values': test_values,
        'expected': [
            140,
            8750,
            13125,
            12048,
            14400,
            26355,
            31500,
            46000,
            49200,
            101000,
            108100,
        ]
    },
    {
        'name': "mobile",
        'expr': "((44 * q) if q <= 50 else (44 * q) if q <= 250 else (31 * q) if b == 0 and q < 1000 else (14 * q) if q < 1000 else (30 * 1000) if b == 0 else (13 * 1000)) + (0 if q <= 1000 else 21 * (q - 1000) if b == 0 else 9 * (q - 1000))",
        'values': test_values,
        'expected': [
            44,
            2200,
            3300,
            3514,
            4200,
            7781,
            9300,
            13000,
            13900,
            30000,
            32100
        ]
    },
    {
        'name': 'pull printing',
        'expr': "((105 * q) if q <= 50 else (105 * q) if q <= 250  else (78 * q) if b == 0 and q < 1000 else (34 * q) if q < 1000 else (75 * 1000) if b == 0 else (33 * 1000)) + (0 if q <= 1000 else 53 * (q - 1000) if b == 0 else 23 * (q - 1000))",
        'values': test_values,
        'expected': [
            105,
            5250,
            7875,
            8534,
            10200,
            19578,
            23400,
            33000,
            35300,
            75000,
            80300
        ]
    },
    {
        'name': "Epic",
        'expr': "(0 if q < 250 else (35 * q) if b == 0 and q < 1000 else (15 * q) if q < 1000 else (34 * 1000) if b == 0 else (14 * 1000)) + (0 if q <= 1000 else 24 * (q - 1000) if b == 0 else 10 * (q - 1000))",
        'values': test_values,
        'expected': [
            0,
            0,
            0,
            3765,
            4500,
            8785,
            10500,
            14000,
            15000,
            34000,
            36400,
        ]
    }
]

for test in tests:
    for i, val_set in enumerate(test['values']):
        val = get_value(test['expr'], val_set)
        if val == test['expected'][i]:
            print "PASSED", val_set, "RECEIVED", val, "EXPECTED", test['expected'][i]
        else:
            print "\tFAILED", val_set, "RECEIVED", val, "EXPECTED", test['expected'][i]
