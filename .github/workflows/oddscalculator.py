import numpy as np

# Establishing what cards remain in the deck and featured hands
cardpool = ["Ah","As","Ac","Ad","Kh","Ks","Kc","Kd","Qh","Qs","Qc","Qd","Jh","Js","Jc","Jd","Th","Ts","Tc","Td","9h","9s","9c","9d","8h","8s","8c","8d","7h","7s","7c","7d","6h","6s","6c","6d","5h","5s","5c","5d","4h","4s","4c","4d","3h","3s","3c","3d","2h","2s","2c","2d"]
herohand = input("Enter your hand (e.g. AhKh): ")
villainhand = input("Enter opponent's hand (e.g. QcQs): ")
removecards = [herohand[:2],herohand[2:],villainhand[:2],villainhand[2:]]
currentposition = input("Please enter one of the following to represent where you are in the hand; preflop/flop/turn/river: ")
cardsremaining = 5
if currentposition == "flop":
    cardsremaining = 2
elif currentposition == "turn":
    cardsremaining = 1
elif currentposition == "river":
    cardsremaining = 0 
if cardsremaining < 5:
    runoutplaceholder = input("Enter the runout (e.g. QhJhTh): ")
    for i in range(0, len(runoutplaceholder), 2):
        removecards.append(runoutplaceholder[i:i+2])
deck = [x for x in cardpool if x not in removecards]