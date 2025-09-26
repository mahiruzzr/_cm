import cmath,math

def root3(a,b,c,d):
    b = b/a
    c = c/a
    d = d/a
    x = [0]*3
    p = c - (b**2)/3
    q = (2*(b**3))/27 - (b*c)/3 + d
    j= cmath.sqrt(-1)
    sol = (q/2)**2 + (p/3)**3
    w= (-1+j*cmath.sqrt(3))/2
    if(sol >0):
        u= (-q/2 + cmath.sqrt(sol))**(1/3)
        v= (-q/2 - cmath.sqrt(sol))**(1/3)
        t= u+v
        t1 = u*w + v*w**2
        t2 = u*w**2 + v*w
        x1= t - b/3
        x2= t1 - b/3
        x3 = t2 - b/3
        return (x1,x2,x3)
    if(sol == 0):
        t1 = 2*(-q/2)**(1/3)
        t2 = -(-q/2)**(1/3)
        x1 = t1 - b/3
        x2 = t2 - b/3
        return (x1,x2)
    if(sol < 0):
        p = 2*(-p/3)**0.5
        angle = cmath.acos(-q/2 /((-p/3)**3)**0.5)
        for i in range(3):
            t = p*cmath.cos((angle+2*i*cmath.pi)/3)
            x[i] = t - b/3
        return (x[0],x[1],x[2])

def f(result,a,b,c,d):
    for i in result:    
        y = a*i**3 + b*i**2 + c*i + d
        print(y)

a = int(input())
b = int(input())
c = int(input())
d = int(input())
result = root3(a,b,c,d)
f(result,a,b,c,d)
print("root3:",result)
