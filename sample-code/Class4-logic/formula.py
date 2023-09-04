"""
formula.py - propositional formulas for Python
by Robin Wellner
Hereby, I waive all rights to this library, as described at <http://creativecommons.org/publicdomain/zero/1.0/>
Examples:
foo = Atom('foo')
bar = Atom('bar')
disjuction = foo | bar
conjunction = foo & bar
implication = foo >> bar
if_and_only_if = foo << bar
inverse = ~foo
simple_tautology = foo | ~foo
simple_negative_tautology = foo & ~foo
#Valuation:
#Formula.v(true_set)
print(simple_tautology.v({foo}) # prints True
print(negative_tautology.v({foo}) # prints True
print(inverse.v({bar}) # prints True
#Tautology checking:
#Formula.t()
#returns a set of atoms which cause Formula.v to return False (a counterexample)
#or None if the formula is a tautology
print(simple_tautology.t()) # prints None
print(implication.t()) # prints {foo}
"""

class Formula:
	def __invert__(self):
		return Not(self)
	def __and__(self, other):
		return And(self, other)
	def __or__(self, other):
		return Or(self, other)
	def __rshift__(self, other):
		return Implies(self, other)
	def __lshift__(self, other):
		return Iff(self, other)
	def __eq__(self, other):
		return self.__class__ == other.__class__ and self.eq(other)
	def v(self, v):
		raise NotImplementedError("Plain formula can not be valuated")
	def _t(self, left, right):
		while True:
			found = True
			for item in left:
				if item in right:
					return None
				if not isinstance(item, Atom):
					left.remove(item)
					tup = item._tleft(left, right)
					left, right = tup[0]
					if len(tup) > 1:
						v = self._t(*tup[1])
						if v is not None:
							return v
					found = False
					break
			for item in right:
				if item in left:
					return None
				if not isinstance(item, Atom):
					right.remove(item)
					tup = item._tright(left, right)
					left, right = tup[0]
					if len(tup) > 1:
						v = self._t(*tup[1])
						if v is not None:
							return v
					found = False
					break
			if found:
				return set(left)
	def t(self):
		return self._t([], [self])

class BinOp(Formula):
	def __init__(self, lchild, rchild):
		self.lchild = lchild
		self.rchild = rchild
	def __str__(self):
		return '(' + str(self.lchild) + ' ' + self.op+ ' ' + str(self.rchild) + ')'
	def eq(self, other):
		return self.lchild == other.lchild and self.rchild == other.rchild

class And(BinOp):
	op = '∧'
	def v(self, v):
		return self.lchild.v(v) and self.rchild.v(v)
	def _tleft(self, left, right):
		return (left + [self.lchild, self.rchild], right),
	def _tright(self, left, right):
		return (left, right + [self.lchild]), (left, right + [self.rchild])

class Or(BinOp):
	op = '∨'
	def v(self, v):
		return self.lchild.v(v) or self.rchild.v(v)
	def _tleft(self, left, right):
		return (left + [self.lchild], right), (left + [self.rchild], right)
	def _tright(self, left, right):
		return (left, right + [self.lchild, self.rchild]),

class Implies(BinOp):
	op = '→'
	def v(self, v):
		return not self.lchild.v(v) or self.rchild.v(v)
	def _tleft(self, left, right):
		return (left + [self.rchild], right), (left, right + [self.lchild])
	def _tright(self, left, right):
		return (left + [self.lchild], right + [self.rchild]),

class Iff(BinOp):
	op = '↔'
	def v(self, v):
		return self.lchild.v(v) is self.rchild.v(v)
	def _tleft(self, left, right):
		return (left + [self.lchild, self.rchild], right), (left, right + [self.lchild, self.rchild])
	def _tright(self, left, right):
		return (left + [self.lchild], right + [self.rchild]), (left + [self.rchild], right + [self.lchild])

class Not(Formula):
	def __init__(self, child):
		self.child = child
	def v(self, v):
		return not self.child.v(v)
	def __str__(self):
		return '¬' + str(self.child)
	def eq(self, other):
		return self.child == other.child
	def _tleft(self, left, right):
		return (left, right + [self.child]),
	def _tright(self, left, right):
		return (left + [self.child], right),

class Atom(Formula):
	def __init__(self, name):
		self.name = name
	def __hash__(self):
		return hash(self.name)
	def v(self, v):
		return self in v
	def __str__(self):
		return str(self.name)
	__repr__ = __str__
	def eq(self, other):
		return self.name == other.name
