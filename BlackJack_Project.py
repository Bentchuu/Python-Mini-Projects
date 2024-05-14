import random
players_cards = []
computers_cards = []

def randomizer_player_cards():
    randomizer = True
    while randomizer:
        players_cards.append(random.randint(1,10))
        randomizer = False

def randomizer_computer_cards():
    randomizer = True
    while randomizer:
        computers_cards.append(random.randint(1,10))
        randomizer = False

def initialize_cards():
    for x in range(2):
        randomizer_player_cards()
        randomizer_computer_cards()

initialize_cards()
print(players_cards)
print(computers_cards)