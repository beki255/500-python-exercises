worked_hour=int(input("enter the total hours worked per week:"))
rank=input("enter your academic rank:")
convert=rank.upper()
if worked_hour>40:
    if convert=="professor":
        overtime=worked_hour -40
        overtimepay=overtime*350*1.5
        totalpay=40*350+overtimepay
    elif convert==" associate professor":
        overtime=worked_hour -40
        overtimepay=overtime*300*1.5
        totalpay=40*300+overtimepay
    elif convert=="assistant professor":
        overtime=worked_hour -40
        overtimepay=overtime*250*1.5
        totalpay=40*250+overtimepay
    elif convert==" lecturer" :
        overtime=worked_hour -40
        overtimepay=overtime*210*1.5
        totalpay=40*210+overtimepay  
else:
     if convert == " professor":
        totalpay=worked_hour*350
     elif convert == " professor":
        totalpay=worked_hour*300
     elif convert == " professor":
        totalpay=worked_hour*250 
     elif convert == " professor":
        totalpay=worked_hour*210   
print(totalpay)
    