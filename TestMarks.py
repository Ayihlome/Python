testmarks = []

def FinalMark ():
    mark= input("Enter Test mark")
    testmarks.append(mark)


while len(testmarks) < 3:
    FinalMark()

print(testmarks)
# print(testmarks.count)

def CalculateAverage(marks = []):
    total = 0
    for i in range(0, len(marks)):
        mark = int(marks[i])
        total += mark
    
    average = total//len(marks)
    return average

def DetermineGrade (gradelist):
    # print (gradelist)
    if gradelist <=49 & gradelist >= 0:
        print("Learner has Failed")
    
    if gradelist <=59 & gradelist >= 50:
        print ("Learner has Passed")
    
    if gradelist <=69 & gradelist >= 60:
        print ("Learner has Credited")
    
    if gradelist <=79 & gradelist >= 70:
        print ("Learner has Good Marks")
    
    if gradelist <=89 & gradelist >= 80:
        print ("Learner has Very Good Marks")
    
    if gradelist <=100 & gradelist >= 90:
        print ("Learner has a Distinction")


#Calling the function
DetermineGrade(CalculateAverage(testmarks))
print(CalculateAverage(testmarks))

