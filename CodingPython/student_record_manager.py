def main():
    menu()
    ch=int(input())
    if ch==1:
        writedata()
    elif ch==2:
        readdata() 
    elif ch==3:
        deletedata() 
    elif ch==4:
        updatedata()  
    elif ch==5:
        searchdata()
    elif ch==6:
        exit()
    else:           
        print(" invaild input")
    main()    
def writedata():
    id=input("enter student id: ")
    name=input("enter student name: ")
    age=input("enter student age: ")
    studlist=[id,name,age]
    with open("st.txt",'a') as rf:
        for std in studlist:
            rf.writelines(std)
            rf.writelines("\t")
        rf.writelines("\n") 
def readdata():
    with open("st.txt", 'r') as rf:
        print(rf.read())
def deletedata():
    deleid=input("enter deltebby id:")
    with open("st.txt",'r')as rf:
        lines=rf.readlines()
    updatedlist=[]
    for line in lines:
        if not line.startswith(deleid):
            updatedlist.append(lines)
    with open("st.txt" , 'w') as wf:
        wf.writelines(updatedlist) 
    if len(lines)==len(updatedlist):
        print("id not found") 
    else: 
        print("record is delted")   
def updatedata():
    pass
def searchdata():
    pass
def menu():
  print('''
   choose the following option
   ========================================
   ========================================
   
   1.writedata of student
   2.readdata  of student
   3.deletedata of student
   4.updatedata of student
   5.searchdata of student
   6.exit
   
   =========================================
    
      ''')
main()