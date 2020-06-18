#import dependencies 
import random
import copy
from timeit import default_timer as timer
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class Hand:
    '''
    This class creates a Texas Holdem 
    '''
    def __init__(self):
        cards = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        suits = ['H','D','S','C']
        self.deck = [(card,suit) for card in cards for suit in suits]
        random.shuffle(self.deck)
        self.selected_hand = []
    def player_1(self):
        '''
        selects two random cards for the player
        '''
        return self.deck[:2]
    def table(self,cards_on_table = 3):
        '''
        places cards_on_table number of random cards on the table

        key word arguments:
        cards_on_table -- Number of cards on the table (0 3 or 4) defualt = 3
        '''
        return self.deck[2:2+cards_on_table], self.deck[2+cards_on_table:]
    def hand_selection(self):
        '''
        input allowing for two specific cards to be selected
        '''
        card_1_value = input('Card 1 value:')
        card_1_suit = input('Card 1 suit:')
        card1 = (int(card_1_value), card_1_suit)
        card_2_value = input('Card 2 value:')
        card_2_suit = input('Card 2 suit:')
        card2 = (int(card_2_value), card_2_suit) 
        self.selected_hand.append(card1)
        self.selected_hand.append(card2)
        return self.selected_hand        

    def table_selection(self, cards_on_table = 3):
        '''
        input allowing for cards_on_table number of cards to be selected to be placed on the table

        key word arguments:
        cards_on_table -- Number of cards on the table (0 3 or 4) defualt = 3
        '''
        on_table = []
        if cards_on_table >= 3:
            table1_value = input('table 1 value:')
            table1_suit = input('table 1 suit:')
            on_table.append((int(table1_value),table1_suit))

            table2_value = input('table 2 value:')
            table2_suit = input('table 2 suit:')
            on_table.append((int(table2_value),table2_suit))
            
            table3_value = input('table 3 value:')
            table3_suit = input('table 3 suit:')
            on_table.append((int(table3_value),table3_suit))
            
        if cards_on_table == 4:
            table1_value = input('table 4 value:')
            table1_suit = input('table 4 suit:')
            on_table.append((int(table4_value),table4_suit))
            
        deck_return = [i for i in self.deck if i != self.selected_hand[0] and i != self.selected_hand[1]]
        deck_return_minus_table = [i for i in deck_return if i not in on_table]
        return [on_table, deck_return_minus_table]
    
    def hand_selection_list(self,cards_in_hand):
        '''
        input allowing for two specific cards to be selected
        
        key word arguments:
        cards_in_hand -- a list of the cards you want in your hand
        '''
        card1 = cards_in_hand[0]
        card2 = cards_in_hand[1]
        self.selected_hand.append(card1)
        self.selected_hand.append(card2)
        return self.selected_hand        

    def table_selection_list(self,cards_on_table):
        '''
        input allowing for cards_on_table number of cards to be selected to be placed on the table

        key word arguments:
        cards_on_table -- a list of cards to appear on the table
        '''            
        deck_return = [i for i in self.deck if i not in self.selected_hand]
        deck_return_minus_table = [i for i in deck_return if i not in cards_on_table]
        return [cards_on_table, deck_return_minus_table]
        
#this probably shouldnt be a class
class Table:
    '''
    This class takes a selected hand and deals two random cards to every player and finishes dealing the remaining deck
    '''
    def __init__(self, player_1, table, player_count = 5):
        self.player_1 = player_1
        self.table = table[0]
        self.player_count = player_count
        self.hands = player_1[0]
        self.remaining_deck = table[1]
        random.shuffle(self.remaining_deck)

    def deal(self):
        '''
        This function deals cards to player_count-1 number of remaining players and deals the remaining cards on the table

        key word arguments:
        player_1 -- Two cards from Hand class that stay constant
        table -- Cards from Hand class that stay constant
        player_count -- the total number of players in this game

        returns a [hands, table_dealt] where hands are the other players two 
        card hands and table_dealt is the 5 cards on the table at the end of the hand
        '''
        remaining_deck_copy = copy.copy(self.remaining_deck)
        hands = [[] for _ in range(self.player_count-1)]
        for _ in range(2): #hands everyone one card and then a second
            for i in range(self.player_count-1):
                hands[i].append(remaining_deck_copy.pop())
        table_dealt = [*self.table, *remaining_deck_copy[-(5-len(self.table)):]]
        return hands, table_dealt

class Hit_Hand:
    '''
    This class returns a boolean value for weather or not the 7 card hand hit each possibity

    key word arguments:
    player_1 -- The two cards the player one is given
    deal -- the 5 cards on the table as well as the other players hands (not used here)
    print_hand -- will print the hand if True (defualt False)
    '''
    def __init__(self, player_1, deal, print_hand = False):
        self.player_1 = player_1
        self.other_players = deal[0]
        self.table = deal[1]
        self.total_hand = [*player_1,*self.table]
        self.suits = [x[1] for x in self.total_hand]
        self.value = [x[0] for x in self.total_hand] #list of cards
        if print_hand == True:
            print('Your Cards:')
            print(self.player_1)
            print('Table:')
            print(self.table)
            
    #this needs to be tested
    def straight_flush(self):
        hand = []
        if (self.suits.count('H') >= 5):
            for card in self.total_hand:
                if card[1] == 'H':
                    hand.append(card[0])
                        
        elif (self.suits.count('S') >= 5):
            for card in self.total_hand:
                if card[1] == 'S':
                    hand.append(card[0])
                    
        elif (self.suits.count('D') >= 5):
            for card in self.total_hand:
                if card[1] == 'D':
                    hand.append(card[0])
                    
        elif (self.suits.count('C') >= 5):
            for card in self.total_hand:
                if card[1] == 'C':
                    hand.append(card[0])
        if len(hand) >= 5:
            #if their is a 14 add a 1 to the begining because Ace is high or low for straight
            cards = list(set(hand))
            if cards.count(14) == 1:
                cards.append(1)
            cards.sort()
            c = 1
            for i in range(len(cards)-1):
                if cards[i] + 1 == cards[i + 1]:
                    c += 1
                elif c >= 5:
                    return True
                else:
                    c = 1
            return (c >= 5)
        return False
    
    def four_of_kind(self):
        c = 0
        for i in set(self.value):
            if self.value.count(i) == 4:
                c += 1
        return (c == 1)
    
    def full_house(self):
        pair = 0
        three = 0
        for i in set(self.value):
            if self.value.count(i) == 2:
                pair += 1
            elif self.value.count(i) >= 3:
                three += 1
        return ((pair >= 1) and (three == 1)) or (three >= 2)
    
    def flush(self):
        return (self.suits.count('H') >= 5) or (self.suits.count('D') >= 5) or \
    (self.suits.count('S') >= 5) or (self.suits.count('C') >= 5)

    def straight(self):
        #if their is a 14 add a 1 to the begining because Ace is high or low for straight
        cards = list(set(self.value))
        if cards.count(14) == 1:
            cards.append(1)
        cards.sort()
        c = 1
        for i in range(len(cards)-1):
            if cards[i] + 1 == cards[i + 1]:
                c += 1
            elif c >= 5:
                return True
            else:
                c = 1
        return (c >= 5)

    def three_of_kind(self):
        c = 0
        for i in set(self.value):
            if self.value.count(i) >= 3:
                c += 1
        return (c >= 1)

    def two_pair(self):
        c = 0
        for i in set(self.value):
            if self.value.count(i) >= 2:
                c += 1
        return (c >= 2)
    
    def pair(self):
        for i in set(self.value):
            if self.value.count(i) >= 2:
                return True
        return False      

    
#identifying the best hand
class Best_Hand:
    '''
    This class returns the best five card hand

    key word arguments:
    player_1 -- The two cards the player one is given
    deal -- the 5 cards on the table as well as the other players hands (not used here)
    print_hand -- will print the hand if True (default False)
    
    ***
    Note: this was designed to be run in order and does not immidiatly identify the best hand but works in conjuction with the top_hand function
    ***
    '''
    def __init__(self, player_1, deal, print_hand = False):
        self.player_1 = player_1
        self.other_players = deal[0]
        self.table = deal[1]
        self.total_hand = [*player_1,*self.table]
        self.suits = [x[1] for x in self.total_hand]
        self.value = [x[0] for x in self.total_hand] #list of cards
        if print_hand == True:
            print('Your Cards:')
            print(self.player_1)
            print('Table:')
            print(self.table)                
            
    #done
    def straight_flush(self):
        hand = []
        if (self.suits.count('H') >= 5):
            for card in self.total_hand:
                if card[1] == 'H':
                    hand.append(card[0])
                        
        elif (self.suits.count('S') >= 5):
            for card in self.total_hand:
                if card[1] == 'S':
                    hand.append(card[0])
                    
        elif (self.suits.count('D') >= 5):
            for card in self.total_hand:
                if card[1] == 'D':
                    hand.append(card[0])
                    
        elif (self.suits.count('C') >= 5):
            for card in self.total_hand:
                if card[1] == 'C':
                    hand.append(card[0])
        if len(hand) >= 5:
            #if their is a 14 add a 1 to the begining because Ace is high or low for straight
            cards = list(set(hand))
            if cards.count(14) == 1:
                cards.append(1)
            cards.sort()
            c = 1
            hand_suited = []
            for i in range(len(cards)-1):
                if (cards[i] + 1) == cards[i + 1]:
                    c += 1
                    if len(hand_suited) == 0:
                        hand_suited.append(cards[i])
                        hand_suited.append(cards[i+1])
                    else:
                        hand_suited.append(cards[i+1])
                elif c >= 5:
                    return hand_suited[-5:]
                else:
                    c = 1
                    hand_suited = []
                    
    def four_of_kind(self):
        hand = []
        for card in self.value:
            if self.value.count(card) == 4:
                hand.append(card)
        if len(hand) == 4:
            high_cards = sorted(self.value)
            if high_cards[-1] != hand[0]:
                hand.append(high_cards[-1])
            else:
                hand.append(high_cards[-5])
            return hand[::-1]
    
    def full_house(self):
        pair_hand = list()
        three_hand = list()
        for card in set(self.value):
            if self.value.count(card) == 2:
                pair_hand.append(card)
            elif self.value.count(card) == 3:
                three_hand.append(card)
        if len(three_hand) == 2:
            return [min(three_hand), min(three_hand), max(three_hand), max(three_hand), max(three_hand)]
        elif len(three_hand) == 1 and len(pair_hand) >= 1:
            return [max(pair_hand),max(pair_hand),max(three_hand),max(three_hand), max(three_hand)]
             
    def flush(self):
        hand = []
        if (self.suits.count('H') >= 5):
            for card in self.total_hand:
                if card[1] == 'H':
                    hand.append(card)
                        
        elif (self.suits.count('S') >= 5):
            for card in self.total_hand:
                if card[1] == 'S':
                    hand.append(card)
                    
        elif (self.suits.count('D') >= 5):
            for card in self.total_hand:
                if card[1] == 'D':
                    hand.append(card)
                    
        elif (self.suits.count('C') >= 5):
            for card in self.total_hand:
                if card[1] == 'C':
                    hand.append(card)
        if len(hand) > 1:
            hand_value = [x[0] for x in hand]
            return sorted(hand_value)[-5:]

    def straight(self):
        #if their is a 14 add a 1 to the begining because Ace is high or low for straight
        cards = list(set(self.value))
        if cards.count(14) == 1:
            cards.append(1)
        cards.sort()
        hand = []
        for i in range(len(cards)-1):
            if (cards[i] + 1) == cards[i + 1]:
                if len(hand) == 0:
                    hand.append(cards[i])
                    hand.append(cards[i+1])
                else:
                    hand.append(cards[i+1])
            if len(hand) >= 5:
                return hand[-5:]
            elif (cards[i] + 1) != cards[i + 1]:
                hand = []
    
    def three_of_kind(self):
        hand = []
        for card in self.value:
            if self.value.count(card) == 3:
                hand.append(card)
        if len(hand) == 3:
            high_cards = []
            for num in sorted(self.value):
                if num != hand[0]:
                    high_cards.append(num)
            hand.append(high_cards[-1])
            hand.append(high_cards[-2])
            return hand[::-1]

    def two_pair(self):
        c = 0
        hand = []
        for card in self.value:
            if self.value.count(card) == 2:
                c += 1
                hand.append(card)
        if (c >= 4):
            top_pairs = sorted(hand)[-4:][::-1]
            high_card = []
            for num in sorted(self.value):
                if num != top_pairs[-3] and num != top_pairs[-1]:
                    high_card.append(num)
            top_pairs.append(high_card[-1])
            return top_pairs[::-1]
        
    def pair(self):
        hand = []
        for card in self.value:
            if self.value.count(card) == 2:
                hand.append(card)
        if len(hand) == 2:
            high_cards = []
            for num in sorted(self.value):
                if num != hand[0]:
                    high_cards.append(num)
            hand.append(high_cards[-1])
            hand.append(high_cards[-2])
            hand.append(high_cards[-3])
            return hand[::-1]
        
    def high_card(self):
        return sorted(self.value)[-5:]
