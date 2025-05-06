import math

class Expr:
    "A symbolic expression."
    
    def __add__(self, other):
        return Add(self, other)
    def __sub__(self, other):
        return Sub(self, other)
    def __mul__(self, other):
        return Mul(self, other)
    def __pow__(self, other):
        return Pow(self, other)
    def __truediv__(self, other):
        return Div(self, other)
    def __repr__(self):
        return str(self)

    def _repr_latex_(self):
        """Jupyter hook to render LaTeX automatically in notebooks."""
        return f"${self.latex()}$"

    def eval(self):
        return self


######################################################
#  SYMBOLS
######################################################



class Symbol(Expr):
    """
    A symbolic element.
    """
    def __init__(self, name, value=1):
        self.name = name
        self.value = value

    def __str__(self):
        if self.value >= 0:
            if self.value == 1:
                return f'{self.name}'
            else:
                return f'{self.value}{self.name}'
        else:
            if self.value == -1:
                return f'(-{self.name})'
            else:
                return f'({self.value}{self.name})'

    def latex(self): 
        if self.value >= 0:
            if self.value == 1:
                return f'{self.name}'
            else:
                return f'{self.value}{self.name}'
        else:
            if self.value == -1:
                return f'(-{self.name})'
            else:
                return f'({self.value}{self.name})'
            

    def eval(self):
        return self


def S(symbol):
    """ Returns a symbolic element. """
    return Symbol(symbol)





class Constant(Expr):
    """ A symbolic constant element. """
    def __init__(self, name: str, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name

    def latex(self):
        return self.name
    
    def eval(self):
        return self.value


PI = Constant('π', math.pi)
PHI = Constant('𝛗', (1 + math.sqrt(5))/2)
E = Constant('e', math.e)
TAU = Constant('𝛕', math.tau)

class Number(Expr):
    """ A symbolic number element."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value >= 0:
            return str(self.value)
        else:
            return str(f'({self.value})')

    def latex(self):
        if self.value >= 0:
            return str(self.value)
        else:
            return str(f'({self.value})')

    def eval(self):
        return self

def N(number):
    return Number(number)
    
def symbolify_number(x):
    if isinstance(x, Expr):
        return x
    if isinstance(x, (int, float)):
        return Number(x)
    raise TypeError

######################################################
#  OPERATIONS
######################################################




class Add(Expr):
    """ A symbolic addition"""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} + {self.right})"
    def latex(self):
        return f"({self.left.latex()} + {self.right.latex()})"


    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)

        elif isinstance(left, Symbol) and isinstance(right, Symbol):
            if left.name == right.name:
                result = left.value - right.value
                if result == 0:
                    return Number(result)
                else:
                    return Symbol(left.name, value=left.value + right.value)

        elif isinstance(left, Symbol) and isinstance(right, Number):
            if right.value == 0:
                return left
            else:
                return(Add(left, right))
        elif isinstance(left, Number) and isinstance(right, Symbol):
            if left.value == 0:
                return right
            else:
                return Add(left, right)

        return(Add(left, right))


    def solve_for(self, symbol, lhs, rhs):
        # for x + 1
        if isinstance(self.left, Symbol) and self.left.name == symbol.name:
            l = symbol
            r = rhs - self.right
            return l.eval(), r.eval()

        # for 1 + x
        if isinstance(self.right, Symbol) and self.right.name == symbol.name:
            l = symbol
            r = rhs - self.left
            return l.eval(), r.evla()

        # for 1 + 1
        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return self.eval()

        # MUL + 1
        if isinstance(self.left, Mul):
            self.left = self.left.eval()
            return lhs, rhs

        raise NotImplementedError("Cannot isolate symbol in this expression")






class Sub(Expr):
    """ A symbolic subtraction."""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return f"({self.left} - {self.right})"
    def latex(self):
        return f"{self.left.latex()} - {self.right.latex()}"
    
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if isinstance(left, Number) and isinstance(right, Number):
            return Add(Number(left.value), Number(right.value * -1))
        
        elif isinstance(left, Symbol) and isinstance(right, Symbol):
            return Add(Symbol(left.name, left.value), Symbol(right.name, right.value * -1))

        elif isinstance(left, Symbol) and isinstance(right, Number):
            return Add(Symbol(left.name, left.value), Number(right.value * -1))

        elif isinstance(left, Number) and isinstance(right, Symbol):
            return Add(Number(left.value), Symbol(right.name, right.value * -1))
            
        return(Sub(left, right))


    def solve_for(self, symbol, lhs, rhs):
        # for x - 1
        if isinstance(self.left, Symbol) and self.left.name == symbol.name:
            l = symbol
            r = rhs + self.right
            return l.eval(), r.eval()
        
        # for 1 - x
        if isinstance(self.right, Symbol) and self.right.name == symbol.name:
            l = self.left
            r = rhs - symbol
            return l.eval(), r.eval()

        # for 1 - 1
        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return self.eval()

        raise NotImplementedError("Cannot isolate symbol in this expression")



class Mul(Expr):
    """ A symbolic multiplication."""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return f"({self.left} * {self.right})"
    def latex(self):
        return f"({self.left.latex()} \\cdot {self.right.latex()})"

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)

        elif isinstance(left, Number) and isinstance(right, Symbol):
            return Symbol(right.name, right.value * left.value)

        elif isinstance(left, Symbol) and isinstance(right, Number):
            return Symbol(left.name, left.value * right.value)


        return Mul(left, right)

    def solve_for(self, symbol, lhs, rhs):
        # for x * 1  = 4
        if isinstance(self.left, Symbol) and self.left.name == symbol.name:
            l = self.left
            r = rhs / self.right
            return l.eval(), r.eval()
        # for 1 * x = 4
        if isinstance(self.right, Symbol) and self.right.name == symbol.name:
            l = self.right
            r = rhs / self.left
            return l.eval(), r.eval()



class Div(Expr):
    """ A symbolic division """
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    def __str__(self):
        return f"({self.numerator} / {self.denominator})"
    def latex(self):
        return f"\\frac{{{self.numerator.latex()}}}{{{self.denominator.latex()}}}"

    def eval(self):
        numerator = self.numerator.eval()
        denominator = self.denominator.eval()
        if isinstance(numerator, Number) and isinstance(denominator, Number):
            return Number(numerator.value / denominator.value)
        return Div(numerator, denominator)



class Pow(Expr):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent
    def __str__(self):
        return f"({self.base} ** {self.exponent})"
    def latex(self):
        return f"{self.base.latex()}^{{{self.exponent.latex()}}}"







######################################################
#  EQUATIONS
######################################################

class Equation(Expr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs  # Left-hand side expression
        self.rhs = rhs  # Right-hand side expression

    def __repr__(self):
        return f"{self.lhs} = {self.rhs}"

    def latex(self):
        return f"{self.lhs} = {self.rhs}"
    
    def solve(self, symbol):

        if isinstance(self.rhs, Symbol):
            self.lhs = self.lhs.eval()
        elif isinstance(self.lhs, Symbol):
            self.rhs = self.rhs.eval()

        # Solve the left
        # ADD
        elif isinstance(self.lhs, Add):
            if isinstance(self.lhs.right, Number) and isinstance(self.lhs.left, Number):
                self.lhs = self.lhs.evl()
            else:
                self.lhs, self.rhs = self.lhs.solve_for(symbol, self.lhs, self.rhs)
        
        # SUB
        elif isinstance(self.lhs, Sub):
            if isinstance(self.lhs.right, Number) and isinstance(self.lhs.left, Number):
                self.lhs = self.lhs.evl()
            else:            
                self.lhs, self.rhs = self.lhs.solve_for(symbol, self.lhs, self.rhs)
       
        # MUL
        elif isinstance(self.lhs, Mul):
            if isinstance(self.lhs.right, Number) and isinstance(self.lhs.left, Number):
                self.lhs = self.lhs.evl()
            else:  
                self.lhs, self.rhs = self.lhs.solve_for(symbol, self.lhs, self.rhs)
        
        elif isinstance(self.lhs, Symbol):
            pass



        # Solve the right
        # ADD
        elif isinstance(self.rhs, Add):
            if isinstance(self.rhs.right, Number) and isinstance(self.rhs.left, Number):
                self.lhs = self.lhs.evl()
            else: 
                self.rhs, self.lhs =  self.rhs.solve_for(symbol, self.rhs, self.lhs)
        # SUB
        elif isinstance(self.rhs, Sub):
            if isinstance(self.rhs.right, Number) and isinstance(self.rhs.left, Number):
                self.lhs = self.lhs.evl()
            else: 
                self.rhs, self.lhs = self.rhs.solve_for(symbol, self.rhs, self.lhs)
        # MUL
        elif isinstance(self.rhs, Mul):
            if isinstance(self.rhs.right, Number) and isinstance(self.rhs.left, Number):
                self.lhs = self.lhs.eval()
            else:   
                self.rhs, self.lhs = self.rhs.solve_for(symbol, self.rhs, self.lhs)

        else:

            raise NotImplementedError("Equation solving only implemented for simple additions.")


def EQ(lhs, rhs):
    return Equation(lhs, rhs)








class SIN(Expr):

    def __init__(self, angle):
        self.angle = angle
        
    def __str__(self):
        return f'sin(a)'
    
    def latex(self):
        return f'\\sin({{{self.angle.latex()}}})'
    
    def eval(self):
        return math.sin(self.angle.value)

class COS(Expr):

    def __init__(self, angle):
        self.angle = angle
        
    def __str__(self):
        return f'cos(a)'
    
    def latex(self):
        return f'\\cos({{{self.angle.latex()}}})'
    
    def eval(self):
        return math.cos(self.angle.value)

class TAN(Expr):

    def __init__(self, angle):
        self.angle = angle
        
    def __str__(self):
        return f'tan(a)'
    
    def latex(self):
        return f'\\tan({{{self.angle.latex()}}})'
    
    def eval(self):
        return math.tan(self.angle.value)