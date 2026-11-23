import random

numberofnumbers = 6
randomm = 8
islive = 1


def reset_state():
    global randomm, numberofnumbers
    numberofnumbers = 6
    randomm = 8


def playgame():
    global randomm, numberofnumbers

    print(" Russian rulet")
    print("play game(1)")
    print("credits(2)")
    print("Close(3)")
    playselect = int(input(" "))

    if playselect == 1:

        while True:
            chamber = random.randint(islive, randomm)
            input("   You aim... Press Enter to pull the trigger: ")

            if chamber == 1:
                print("  BANG! Live round. You lose!")
                reset_state()
                playgame()
                return
            else:
                print("   *Click*... Blank round. You're still alive.")
                randomm -= 1
                numberofnumbers -= 1

            if numberofnumbers == 0:
                print("  The last round was live. You lose!")
                reset_state()
                playgame()
                return

            while True:
                botchamber = random.randint(islive, randomm)

                if botchamber == 1:
                    print("   Robo's turn...   Live round! Robo loses. You win!")
                    reset_state()
                    playgame()
                    return
                elif botchamber == 3:
                    print("   Robo pulls the trigger... *click* — Blank round!")
                    break
                elif botchamber == 4:
                    print("   Robo shoots you... it has to go again.")
                    continue
                else:
                    print("   Robo fires a blank and survives.")
                    break

    elif playselect == 2:

        while True:
            chamber = random.randint(islive, randomm)
            fire = input("Your turn. Press Enter to fire: ")

            if chamber == 1:
                print("  Live round. You lose!")
                reset_state()
                playgame()
                return
            else:
                print("   Blank. You survive! Try again.")
                randomm -= 1
                numberofnumbers -= 1

            if numberofnumbers == 0:
                print("  Live round. You lose!")
                reset_state()
                playgame()
                return

    elif playselect == 3:
        print("Game closed. Goodbye!")
        return

    else:
        print("Invalid option.")
        playgame()


playgame()