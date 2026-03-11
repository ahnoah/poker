from itertools import combinations

# Establishing what cards remain in the deck
cardpool = ["Ah","As","Ac","Ad","Kh","Ks","Kc","Kd","Qh","Qs","Qc","Qd","Jh","Js","Jc","Jd","Th","Ts","Tc","Td","9h","9s","9c","9d","8h","8s","8c","8d","7h","7s","7c","7d","6h","6s","6c","6d","5h","5s","5c","5d","4h","4s","4c","4d","3h","3s","3c","3d","2h","2s","2c","2d"]
RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def call_cards(s):
    result = []
    for i in range(0, len(s), 2):
        result.append(s[i:i+2])
    return result

def parse_card(card):
    rank, suit = card[0], card[-1]
    return RANKS[rank], suit

hero_hand = call_cards(input("Enter hero's hand (e.g. AhTh): "))
villain_hand = call_cards(input("Enter villain's hand (e.g. QcQs): "))

current_position = input("Please enter one of the following to represent where you are in the hand; preflop/flop/turn/river: ")
if current_position == "preflop":
    cards_remaining = 5
elif current_position == "flop":
    cards_remaining = 2
elif current_position == "turn":
    cards_remaining = 1
elif current_position == "river":
    cards_remaining = 0 
else: current_position = input("Please enter a valid position")

if cards_remaining < 5:
    runout = call_cards(input("Enter the runout (e.g. QhJhTh): "))
    remove_cards = hero_hand + villain_hand + runout
    hero_pool = hero_hand + runout
    villain_pool = villain_hand + runout
else: 
    remove_cards = hero_hand + villain_hand
    hero_pool = hero_hand
    villain_pool = villain_hand

deck = [x for x in cardpool if x not in remove_cards]

# Creating a hand ranking function which assigns a numeric value to every possible hand strength
def hand_value(hand):
    ranks = sorted([RANKS[card[0]] for card in hand], reverse = True)
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    suits = [card[-1] for card in hand]
    suit_counts = {}
    for s in suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1
    
    def is_one_pair():
        return any(c >= 2 for c in rank_counts.values())
    
    def is_two_pair():
        return any(1 for c in rank_counts.values() if c >= 2) >= 2
    
    def is_three_of_a_kind():
        return any(c >= 3 for c in rank_counts.values())
    
    def is_four_of_a_kind():
        return any(c >= 4 for c in rank_counts.values())
    
    def is_full_house():
        vals = sorted(rank_counts.values(), reverse = True)
        return vals[0] >= 3 and vals[1] >= 2
    
    def is_flush():
        return any(c >= 5 for c in suit_counts.values())
    
    def is_straight():
        unique = sorted(set(ranks))
        # up and down straights
        if 14 in unique:
            unique.insert(0, 1)
        count = 1
        for i in range(1, len(unique)):
            if unique[i] == unique [i-1] + 1:
                count += 1
                if count >= 5:
                    return True
            else: count = 1
        return False
    
    # straight flush is not as easy as straight and flush, can't easily reuse functions
    def is_straight_flush():
        suit_sort = {}
        for card in hand:
            r, s = parse_card(card)
            suit_sort.setdefault(s, []).append(r)
        for suit_ranks in suit_sort.values():
            if len(suit_ranks) >= 5:
                unique = sorted(set(suit_ranks))
                # up and down again; from here copy of straight function
                if 14 in unique:
                    unique.insert(0, 1)
                count = 1
                for i in range (1, len(unique)):
                    if unique[i] == unique[i - 1] + 1:
                        count += 1
                        if count >= 5:
                            return True
                    else: count = 1
        return False
    
    def is_royal_flush():
        suit_sort = {}
        for card in hand:
            r, s = parse_card(card)
            suit_sort.setdefault(s, []).append(r)
        # can just check equivalence to 10-14
        return any(set(range(10, 15)).issubset(r) for r in suit_sort.values())

    if is_royal_flush():
        value = 9
    elif is_straight_flush():
        value = 8
    elif is_four_of_a_kind():
        value = 7
    elif is_full_house():
        value = 6
    elif is_flush():
        value = 5
    elif is_straight():
        value = 4
    elif is_three_of_a_kind():
        value = 3
    elif is_two_pair():
        value = 2
    elif is_one_pair():
        value = 1
    else:
        value = 0
    by_rank = {}
    hand = sorted([RANKS[card[0]]for card in hand], reverse = True)
    def added_value(hand):
        hold = 0
        for i in range(5):
            hold = hold + .01 ** (i + 1) * hand[i]
        return hold
    value = value + added_value(hand)
    return value

# Comparing hero and villain hand through each iteration to output % chances


hero_wins = 0
villain_wins = 0
total = 0
for i in (combinations(deck, cards_remaining)):
        hero_val = hand_value(hero_pool + list(i))
        villain_val = hand_value(villain_pool + list(i))
        if hero_val > villain_val:
            hero_wins += 1
        elif villain_val > hero_val:
            villain_wins += 1
        total += 1
hero_win_percentage = 100 * hero_wins / total
villain_win_percentage = 100 * villain_wins / total
draw_percentage = 100 - hero_win_percentage - villain_win_percentage

print(f"Hero win %: {hero_win_percentage:.2f} \nVillain win %: {villain_win_percentage:.2f} \nDraw %: {draw_percentage:.2f}")