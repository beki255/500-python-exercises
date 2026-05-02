name=input("please enter your name ")
lab_exam1=int(input(f"{name} enter first lab exam "))
lab_exam2=int(input(f"{name} enter second lab exam "))
if lab_exam1 > 30 and lab_exam2> 30 or lab_exam1 < 30 and lab_exam2 < 30:
   print("you have enter invaild input")
else:
 average=(lab_exam1 + lab_exam2)/2
 if average>=25:
  print(f"congeratulation!!!!{name} your mark {average} is the highest average result")
 else :
     print(f"sorry!!! {name} your mark {average} is the poor average value please read hardly")

 