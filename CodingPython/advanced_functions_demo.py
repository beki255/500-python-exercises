'''#python function
#1
def message():
    str="hello world"
    print("great work")
    return str
print(message())
#2
def add():
    a=int(input("enter the first number:"))
    b=int(input("enter a second number:"))
    c=a+b
    print(c)
print("hello")
add()
print("hello world")
#3
def area(l,w):
    a=l*w
    print("the area o0f the rectangle is ", a)
length=int(input("enter the lengthe"))
wid=int(input("enter the lengthe"))
area(length,wid) 

#4
def student(name):
    print(name)
student("abebe")
student("abebe")

#5   RETURN 
def area(l,w):
    a=l*w
    return a
length=int(input("enter the lengthe:"))
wid=int(input("enter the lengthe:"))
ar=area(length,wid)
print("the area 0f the rectangle is ",ar)
 #6 recursion
def fact(n):
    if n>1:
        r=n*fact(n-1)
    else:
        r=1
    return r   
result=fact(5)
print(result)
#7 recursion
def tri_recursion(k):
    if k>0:
        result=k + tri_recursion(k-1)
        print(result)
    else:
        result=0
    return 0
print("recursion example results ")
tri_recursion(6)  '''
#8 main function call other function in the program

def main():
    message()
    print("hello students")
    print("great work")
def message():
    print("bereket")
main()   

 
#9
def change(mylist):
    mylist.append([1,2,3,4])
    print("value in side the function is:",mylist)
    return mylist
mylist=[10,20,30,40]; 
change(mylist)  
print("values out side the function is:",mylist)

#10
def changeme(mylist):
    mylist=[1,2,3,4]
    print("values inside the function:", mylist)
    return 
mylist=[10,20,30,40]  
changeme(mylist) 
print("values outside the functiin:", mylist) 

#11
def increment_func(x):
    x=x+1x=1increment_func(x)print(x)


#12
def increment_func(x):
    x=x+1
    return x
x=1    
print(increment_func(x))
print(x)  


