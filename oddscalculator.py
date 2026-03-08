import numpy as np

# Establishing what cards remain in the deck
cardpool = ["Ah","As","Ac","Ad","Kh","Ks","Kc","Kd","Qh","Qs","Qc","Qd","Jh","Js","Jc","Jd","Th","Ts","Tc","Td","9h","9s","9c","9d","8h","8s","8c","8d","7h","7s","7c","7d","6h","6s","6c","6d","5h","5s","5c","5d","4h","4s","4c","4d","3h","3s","3c","3d","2h","2s","2c","2d"]
RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def call_cards(s):
    result = []
    for i in range(0, len(s), 2):
        result.append(s[i:i+2])
    return result

hero_hand = call_cards(input("Enter your hand (e.g. AhTh): "))
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
hero_pool = hero_hand + call_cards(runout)
villain_pool = villain_hand + call_cards(runout)

# Creating a hand ranking function which assigns a numeric value to every possible strength
ranking = ["high_card", "pair", "two_pair", "three_of_a_kind", "straight", "flush", "full_house", "four_of_a_kind", "straight_flush", "royal_flush"]
def parse_card(card):
    rank, suit = card[0], card[-1]
    return RANKS[rank], suit

def is_one_pair(cards):
    counts = {}
    for card in cards:
        rank = parse_card(card)[0]
        counts[rank] = counts.get(rank, 0) + 1
    return any(count >= 2 for count in counts.values())

def is_two_pair(cards):
    counts = {}
    for card in cards:
        rank = parse_card(card)[0]
        counts[rank] = counts.get(rank, 0) + 1
    pairs = sum(1 for count in counts.values() if count >= 2)
    return pairs >= 2

def is_three_of_a_kind(cards):
    counts = {}
    for card in cards:
        rank = parse_card(card)[0]
        counts[rank] = counts.get(rank, 0) + 1
    return any(count >= 3 for count in counts.values())

def is_straight(cards):
# Accounting for up and down
    ranks = sorted(set(parse_card(c)[0] for c in cards))
    if 14 in ranks:
        ranks.insert(0, 1)
    count = 1
    for i in range(1, len(ranks)):
        if ranks[i] == ranks[i - 1] + 1:
            count += 1
            if count >= 5:
                return True
        else:
            count = 1
    return False

def is_flush(cards):
    counts = {}
    for card in cards:
        suit = card[-1]
        counts[suit] = counts.get(suit, 0) + 1
    return any(count >= 5 for count in counts.values())

def is_full_house(cards):
    counts = {}
    for card in cards:
        rank = parse_card(card)[0]
        counts[rank] = counts.get(rank, 0) + 1
    values = sorted(counts.values(), reverse = True)
    return values[0] >= 3 and values[1] >=2

def is_four_of_a_kind(cards):
    counts = {}
    for card in cards:
        rank = parse_card(card)[0]
        counts[rank] = counts.get(rank, 0) + 1
    return any(count >= 4 for count in counts.values())

def is_straight_flush(cards):
    by_suit = {}
    for card in cards:
        rank, suit = parse_card(card)
        if suit not in by_suit:
            by_suit[suit] = []
        by_suit[suit].append(rank)

    for ranks in by_suit.values():
        if len(ranks) >= 5 and is_straight([f"{r}x" for r in ranks]):
            return True
        return False
    
def is_royal_flush(cards):
    by_suit = {}
    for card in cards:
        rank, suit = parse_card(card)
        by_suit.setdefault(suit, []).append(rank)
    
    for suit, ranks in by_suit.items():
        if set(range(10,15)).issubset(ranks):
            return True
    return False