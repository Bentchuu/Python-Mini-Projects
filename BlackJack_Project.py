import random
players_cards = []
computers_cards = []


def deal_cards():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    rand_index = int(random.random() * len(cards))
    rand_cards = cards[rand_index]
    return rand_cards

def initialize_cards():
    computers_cards.append(deal_cards())
    for x in range(2):
        players_cards.append(deal_cards())

def calculate_score():
    if sum(players_cards) > sum(computers_cards):
        print("You Win!")
    elif sum(players_cards) < sum(computers_cards):
        print("You Lose!")
    elif sum(players_cards) == sum(computers_cards):
        print("Draw")
    
def get_cards():
    get_card = input("Type 'y' to get another card, type 'n' to pass: ")
    if get_card.lower() == 'y':
        players_cards.append(deal_cards())
        print(f"Your cards: {players_cards}, current score: {sum(players_cards)}")
        print(f"Computer's first card: {sum(computers_cards)}")
        computers_cards.append(deal_cards())
        get_cards()
    elif get_card.lower() == 'n':
        computers_cards.append(deal_cards())
        print(f"Your Final hand: {players_cards}, final score: {sum(players_cards)}")
        print(f"Computer's Final Hand: {computers_cards}, final score: {sum(computers_cards)}")
        calculate_score()

def start_blackjack():
    initialize_cards()
    print(f"Your cards: {players_cards}, current score: {sum(players_cards)}")
    print(f"Computer's first card: {sum(computers_cards)}")
    get_cards()
    

    



start_blackjack()
