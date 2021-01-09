import random

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}
playing = True

'''
Card class defines individual class in the deck of card
'''
class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank+" of "+self.suit
        
'''
Deck class defines the deck of 52 cards.
It has methods to shuffel the deck of cards and to draw 1 card at a time to distribute cards to the players.
'''
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        all_cards = ''
        for x in self.deck:
            all_cards += '\n'+ x.__str__()
        return 'Cards in deck are : '+ all_cards

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()
        
'''
Hand class is the class to define the cards in playres hand.
it has some methods to add new card and to adjust the value of ace i.e. 1 or 11 depending on the number of aces and total value of cards in hand
'''
class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0   # Sum of values of cards in hand, start with zero value
        self.aces = 0    # Attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
'''
Chips class is the class to define chips player has and what happens when playre loses or wins the bet.
'''
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
#ASK PLAYRE TO BET CHIPS
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('Enter the chips ypou want to bet : '))
        except:
            print('Please enter the integer value.')
        else:
            if chips.total < chips.bet:
                print(f'You don\'t have enough chips to bet, you have {chips.total} chips')
            else:
                break

#IN CASE PLAYER CHOSES TO HIT
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
   
#ASK PLAYER CHOICE TO HIT OF STAND   
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        choice = input('Do you want to hit or stand? [h/s] : ')
        
        if choice[0].lower() == 'h':
            hit(deck,hand)
        
        elif choice[0].lower() == 's':
            print('Playre stands, dealers turn.')
            playing = False
            
        else:
            print('Please enter valid choise [h/s]')
            continue
        break

def show_some(player,dealer):
    print('Dealers cards')
    print('one card is hidden')
    print(dealer.cards[1])
    print('\nPlayres cards')
    for x in player.cards:
        print(x)
    
def show_all(player,dealer):
    print('Dealers cards')
    for x in dealer.cards:
        print(x)
    print('\nPlayres cards')
    for x in player.cards:
        print(x)
        
#TO HANDLE END OF GAME SCENARIO
def player_busts(player,dealer,chips):
    print('Player Busted! Dealer Won.')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player Won!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('Dealer Busted! Player Won.')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('Dealer Won!')
    chips.lose_bet()
    
def push(player,dealer):
    print('It\'s a Tie between dealer and player')
    

#GAME LOGIC
while True:
    # Print an opening statement
    print('WELCOME TO BLACKJACK!!')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    players_hand = Hand()
    players_hand.add_card(deck.deal())
    players_hand.add_card(deck.deal())
    
    dealers_hand = Hand()
    dealers_hand.add_card(deck.deal())
    dealers_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    players_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(players_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(players_hand,dealers_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,players_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(players_hand,dealers_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if players_hand.value > 21:
            player_busts(players_hand,dealers_hand,players_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if players_hand.value <= 21:
        while dealers_hand.value < 17:
            hit(deck,dealers_hand)
    
        # Show all cards
        show_all(players_hand,dealers_hand)
    
        # Run different winning scenarios
        if dealers_hand.value > 21:
            dealer_busts(players_hand,dealers_hand,players_chips)
        elif dealers_hand.value > players_hand.value:
            dealer_wins(players_hand,dealers_hand,players_chips)
        elif dealers_hand.value < players_hand.value:
            player_wins(players_hand,dealers_hand,players_chips)
        else:
            push(players_hand,dealers_hand)
    
    # Inform Player of their chips total 
    print('Player\'s total chips are {}'.format(players_chips.total))
    
    # Ask to play again
    new_game = input('Do you want to play again [y/n]? ')
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('THANK YOU!!')
        break
