from IPython.display import display, Markdown, Latex,Math

class bst():
    def __init__(self):
        self.node=None
        self.left=None
        self.right=None
        
    def append(self,constraint):
        if self.node==None:
            self.node = constraint
            self.left=bst()
            self.right=bst()
        elif constraint[1]<=self.node[1]:
            self.left.append(constraint)
        else: self.right.append(constraint)
        
    def print(self):
        if self.node==None:
            return
        else:
            self.left.print()
            self.print_constraint()
            self.right.print()
            
    def print_constraint(self):
        builder="x_{"+str(self.node[0])+"}=" + str(self.node[1])
        builder+=self.build_linear(self.node[2],self.node[3])
        builder+= "> 0 "
        display(Math(builder))

    def build_linear(self,cons2,cons3):
        builder=""
        for var in cons2:
            builder+='+x_{'+str(var)+'}'
        for var in cons3:
            builder+=' -x_{'+str(var)+'}'
        return builder
    
class constraint():
    def __init__(self,slack,rhs,p,n):
        self.slack=slack
        self.rhs=rhs
        self.p=p
        self.n=n
    
    def __lt__(self, other):
        return self.rhs < other.rhs
    
    def __gt__(self, other):
        return self.rhs > other.rhs
    
    def __eq__(self, other):
        return self.rhs == other.rhs
    
    def __repr__(self):
        builder= ("x_{"+str(self.slack)+"}=" if self.slack>=0 else "W =") + ("" if self.rhs == 0 else str(self.rhs))
        builder+=self.build_linear(self.p,self.n)
        builder+= "> 0 "
        return builder
    
    def __str__(self):
        builder= ("x_{"+str(self.slack)+"}=" if self.slack>=0 else "W =") + ("" if self.rhs == 0 else str(self.rhs))
        builder+=self.build_linear(self.p,self.n)
        if self.slack >=0 : builder+= "> 0 "
        return builder
    
    def build_linear(self,cons2,cons3):
        builder=""
        for var in cons2:
            builder+='+x_{'+str(var)+'}'
        for var in cons3:
            builder+=' -x_{'+str(var)+'}'
        return builder
            
    def __add__(self,other):
        temp=self
        if other.slack in self.p:
            temp.p=self.p.difference({other.slack}).union(other.p)
            temp.n=temp.n.union(other.n)
            removals = temp.p.intersection(temp.n)
            temp.p=temp.p.difference(removals)
            temp.n=temp.n.difference(removals)
            temp.slack=self.slack
            temp.rhs = self.rhs+other.rhs
        elif other.slack in self.n:
            temp.n=self.n.difference({other.slack}).union(other.p)
            temp.p=self.p.union(other.n)
            removals = temp.p.intersection(temp.n)
            temp.p=temp.p.difference(removals)
            temp.n=temp.n.difference(removals)
            temp.slack=self.slack
            temp.rhs = self.rhs-other.rhs
        else :
            temp=self
        return temp
    
        
def build_linear(cons2,cons3):
    builder=""
    for var in cons2:
        builder+='+x_{'+str(var)+'}'
    for var in cons3:
        builder+=' -x_{'+str(var)+'}'
    return builder