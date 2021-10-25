import random

us = 0
bs = 0

# Introduction
print("Welcome to ROCK, PAPER , SCISSOR")
print("The rule to winning is ->")
print("Rock beats scissor, scissor beats paper and paper beats rock")

# Getting player name
print()
player_name = input("Enter your name : ")

print()
# Getting name of opponent
while True:
    namec = input("Would you like to name your opponent (default name is bot) (enter y/n) : ")
    if namec == "y":
        bot_name = input("Enter name of opponent : ")
        break
    elif namec == "n":
        bot_name = "bot"
        break
    else:
        print("Enter correct response")
        print()

moves = ['rock', 'paper', 'scissor']


def check_winning():
    if us > bs:
        print("You are currently winning, nice going.")
    elif us < bs:
        print("You are currently losing, but don't lose hope, tables might turn around soon.")
    elif us == bs:
        print("You score is currently tied with that of", bot_name, ",the match is neck to neck.")


def printing_score():
    print(player_name, "score :", us)
    print(bot_name, "score :", bs)


def tie_display():
    print("That's a tie. What a coincidence!!")
    print("Score remains unchanged, so score is ->")
    printing_score()
    check_winning()


print()
print("Let's begin!!")
print()

while True:
    user_input = input("Enter your move : ")
    bot_input = random.choice(moves)
    print(bot_name, " entered :", bot_input)
    print()

    if user_input == "rock" and bot_input == "rock":
        tie_display()

    elif user_input == "rock" and bot_input == "paper":
        print("You lost")
        bs = bs + 1
        print(bot_name, "gained 1 point, so score is ->")
        printing_score()
        check_winning()

    elif user_input == "rock" and bot_input == "scissor":
        print("You won")
        us = us + 1
        print("You gained 1 point, so score is ->")
        printing_score()
        check_winning()

    elif user_input == "paper" and bot_input == "rock":
        print("You won")
        us = us + 1
        print("You gained 1 point, so score is ->")
        printing_score()
        check_winning()

    elif user_input == "paper" and bot_input == "paper":
        tie_display()

    elif user_input == "paper" and bot_input == "scissor":
        print("You lost")
        bs = bs + 1
        print(bot_name, "gained 1 point, so score is ->")
        printing_score()
        check_winning()

    elif user_input == "scissor" and bot_input == "rock":
        print("You lost")
        bs = bs + 1
        print(bot_name, "gained 1 point, so score is ->")
        printing_score()
        check_winning()

    elif user_input == "scissor" and bot_input == "paper":
        print("You won")
        us = us + 1
        print("You gained 1 point, so score is ->")
        printing_score()
        check_winning()

    elif user_input == "scissor" and bot_input == "scissor":
        tie_display()

    else:
        print("Enter correct move")

    con = input("Want to continue game (y/n) : ")
    if con == "n":
        break
print("The game is now finished.")
print("The final result is given below ->")
printing_score()
if us > bs:
    print("You have officially defeated", bot_name, "!!! Congratulations on your victory")
elif us < bs:
    print("Unfortunately you lost the game. But its alright. There is always a next time.")
elif us == bs:
    print("The final result is a tie. It seems that both you and", bot_name, "are equally good at this game.")
