# function arguments
# 1.  required or positional argument.

def required(posi):
    print(posi)
required("hello world <--- this is required argument")    
  
  
#2 keyword argument or named argument.
def func(a, b=5, c=10):
    print("a is",a,"and b is",b,"and c is",c)
func(3,7) 
func(25,c=24)   
func(c=50,a=100)

#3 default argument
def func(i,j=100):
    print(i,j)
func(10,33)
#4 variable length non key word argument / VLA postional argument in tuple
def printinfo(arg1,*vartuple):
    print("out put is:")
    print(arg1)
    for var in vartuple:
       print(var)
    return
printinfo(10) 
printinfo(70,60,50)

#4.1 
def sumofnum(*num):
    s=0
    for var in num:
        s=s+var
    print(s) 
sumofnum(1,3,5) 
sumofnum(1,2,3,4,5,6,7)   

#5 variable length keyword argument use in dictionry

def arbitrarykwargs(**kwargs):
    print(kwargs)
    for key,value in kwargs.items():
        print(key,value)
arbitrarykwargs(name="jone", age=25, college="computing")   

     

def arbitrarykwargs(*args,**kwargs):
    print(args)
    for key,value in kwargs.items():
        print(key,value)
arbitrarykwargs(2,3,4,5,name="jone", age=25, college="computing")    


 