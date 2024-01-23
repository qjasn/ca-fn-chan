from sympy import *


class EquationUI:
    def __init__(self, equ: str, args="x"):
        _solve = ""
        self.equation = equ
        self.map = {}
        args = args.replace(" ", "")
        for i in args.split(","):
            exec("result = symbols('{}')".format(i))
            self.map[i] = locals()["result"]
        for i in args.split(","):
            _equ = equ.replace(i, 'self.map["{}"]'.format(i))
        self.pares = parse_expr(equ,transformations="all")
        self.latex = latex(self.pares)
        print(str(self.latex))
        for i in args.split(","):
            _solve = _solve + "self.map['{}'],".format(i)
        exec("result = solve(self.pares,({}),dict=True)".format(_solve))
        self.solve = locals()["result"]
        print(self.solve)
