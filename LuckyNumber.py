import random
number = int(input(" Guess the lucky number between 1 to 100: "))
luckyNumber = random.randrange(1,100)
guesses = 1
correct = False

# print(luckyNumber)

# testing the numbers if they are correct
while not correct:
    if number > 100 or number < 0:
         number = int(input("The number is not in range, Please try again: "))
         guesses += 1
    elif number > luckyNumber: 
         number = int(input("Number is too high, guess again: "))
         guesses += 1
    elif number < luckyNumber:
         number = int(input("Number is too low, guess again: "))
         guesses += 1
    elif number == luckyNumber:
         correct = True
         print("CORRECT!!!!!")
         print("You did it in " + str(guesses))
      
    
     


