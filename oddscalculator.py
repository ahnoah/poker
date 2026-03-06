import numpy as np

# Establishing what cards remain in the deck
cardpool = ["Ah","As","Ac","Ad","Kh","Ks","Kc","Kd","Qh","Qs","Qc","Qd","Jh","Js","Jc","Jd","Th","Ts","Tc","Td","9h","9s","9c","9d","8h","8s","8c","8d","7h","7s","7c","7d","6h","6s","6c","6d","5h","5s","5c","5d","4h","4s","4c","4d","3h","3s","3c","3d","2h","2s","2c","2d"]

def call_cards(s):
    result = []
    for i in range(0, len(s), 2):
        result.append(s[i:i+2])
    return result

hero_hand = call_cards(input("Enter your hand (e.g. AhKh): "))
villain_hand = call_cards(input("Enter opponent's hand (e.g. QcQs): "))

current_position = input("Please enter one of the following to represent where you are in the hand; preflop/flop/turn/river: ")
cards_remaining = 5
if current_position == "flop":
    cards_remaining = 2
elif current_position == "turn":
    cards_remaining = 1
elif current_position == "river":
    cards_remaining = 0 

if cards_remaining < 5:
    runout = input("Enter the runout (e.g. QhJhTh): ")
remove_cards = hero_hand + villain_hand + call_cards(runout)
deck = [x for x in cardpool if x not in remove_cards]



