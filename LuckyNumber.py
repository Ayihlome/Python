import random
number = int(input(" Guess the lucky number between 1 to 100: "))
guesses = 1
correct = False
quary = str
redo = bool


# testing the numbers if they are correct
def TestNumber (number):
     correct = False
     guesses = 1
     actualNumber = random.randrange(1,100)
     print (actualNumber)
     while not correct:
      if number > 100 or number < 0:
         number = int(input("The number is not in range, Please try again: "))
         guesses += 1
      elif number > actualNumber: 
         number = int(input("Number is too high, guess again: "))
         guesses += 1
      elif number < actualNumber:
         number = int(input("Number is too low, guess again: "))
         guesses += 1
      elif number == actualNumber:
         correct = True
         print("CORRECT!!!!!")
         print("You did it in " + str(guesses))
# end function

TestNumber(number)
