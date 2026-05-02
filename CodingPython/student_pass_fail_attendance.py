attend=int(input(" enter a student attendance:- "))
if attend>=75:
  print(" the student is sufficient for the checking of exam score")
  score=int(input("enter student exam score:- "))
  if score>=50:
     print("you passed the score.")
  else:
     print(" you faild the course due to low score.")
else:
  print("you faild the course due to low attendance")