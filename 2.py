import cmath

def root(a,b,c):
    d= b**2-4*a*c
    if(d>0 or d<0):
        sol1=(-b+cmath.sqrt(d))/(2*a)
        sol2=(-b-cmath.sqrt(d))/(2*a)
        x1=a*sol1**2+b*sol1+c
        x2=a*sol2**2+b*sol2+c
        return (sol1,sol2,x1,x2)
    if(d==0):
        sol1=(-b)/(2*a)
        x1=a*sol1**2+b*sol1+c
        return (sol1,x1)

a = int(input())
b = int(input())
c = int(input())
x1=0
x2=0
result = root(a,b,c)
print(result)
