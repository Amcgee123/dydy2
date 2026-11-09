import random
import os 
 
numberofnumbers = 6
randomm = 8
islive = 1
 
def playgame():
    global randomm, numberofnumbers
 
    print("                               Russian rulet")
    print("play game(1)")
    print("credits(2)")
    print("Close(3)")
    playselect = int(input("  "))
 
    if playselect == 1:
        def playing():
            global randomm, numberofnumbers
 
            print("1 player(1)")
            print("2 player (2)")
            print("Back to main menu(3)")
            noplayers = int(input("  "))
 
            if noplayers == 1:
                while True:                                                                                                 
                    # Player's turn
                    chamber = random.randint(islive, randomm)
                    input("You aim... Press Enter to pull the trigger: ")
                    print(numberofnumbers)
 
                    if chamber == 1:
                        print(" BANG! Live round. You lose!")
                        numberofnumbers = 6
                        randomm = 8
                        playgame()
                        break
                    else:
                        print(" *Click*... Blank round. You're still alive.")
                        randomm -= 1
                        numberofnumbers -= 1
 
                    if numberofnumbers == 0:
                        print(" The last round was live. You lose!")
                        numberofnumbers = 6
                        randomm = 8
                        playgame()
                        break
 
                    # Bot's turn
                    while True:
                        botchamber = random.randint(islive, randomm)
 
                        if botchamber == 1:
                            print("🤖 clanker's turn... 💥 Live round! clanker loses. You win!")
                            numberofnumbers = 6
                            randomm = 8
                            playgame()
                            return
 
                        elif botchamber == 3:
                            print("🤖 clanker pulls the trigger... *click* — Blank round!")
                            break
 
                        elif botchamber == 4:
                            print("🤖 clanker shoots you... it has to go again.")
                            continue
 
                        else:
                            print("🤖 clanker fires a blank and survives.")
                            break
 
            elif noplayers == 2:
                while True:
                    chamber = random.randint(islive, randomm)
                    fire = input("Your turn. Press Enter to fire: ")
 
                    if chamber == 1:
                        print("💥 Live round. You lose!")
                        numberofnumbers = 6
                        randomm = 8
                        playgame()
                        break
                    else:
                        print("🔫 Blank. You survive! Try again.")
                        randomm -= 1
                        numberofnumbers -= 1
 
                    if numberofnumbers == 0:
                        print("💥 Live round. You lose!")
                        numberofnumbers = 6
                        randomm = 8
                        playgame()
                        break
 
            elif noplayers == 3:
                playgame()
 
        playing()
 
    elif playselect == 2:
        print("                          made: by Austin Mcgee")
        print("                          music: By Austin Mcgee")
        print("                           special thanks: you for playing")
        playgame()
 
    elif playselect == 3:
        print("Game closed. Goodbye!")
 
 
playgame()
 