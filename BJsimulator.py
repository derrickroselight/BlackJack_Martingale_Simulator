#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 05:31:40 2020

@author: Light
"""

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns 

main_table = pd.read_csv('/Users/Light/PythonData/BlackJack/Main_Strategy_Table.txt', sep=" ",index_col = 0,engine='python')
ace_table = pd.read_csv('/Users/Light/PythonData/BlackJack/Ace_Strategy_Table.txt', sep=" ",index_col = 0,engine='python')
ace2_table = pd.read_csv('/Users/Light/PythonData/BlackJack/Ace2_Strategy_Table.txt', sep=" ",index_col = 0,engine='python')
pair_table = pd.read_csv('/Users/Light/PythonData/BlackJack/Pair_Strategy_Table.txt', sep=" ",index_col = 0,engine='python')

blackjack = set(['A',10])
d_hand = []
p_hand = []
num_decks = 1
card_types = ['A',2,3,4,5,6,7,8,9,10,10,10,10]
player_results = []
deposit_curve = []
deposit = 128
bet = 1

# Make a deck
def make_decks(num_decks, card_types):
    new_deck = []
    for i in range(num_decks):
        for j in range(4):
            new_deck.extend(card_types)
    random.shuffle(new_deck)
    return new_deck

dealer_cards = make_decks(num_decks, card_types)


# This function lists out all permutations of ace values in the
# array sum_array.
# For example, if you have 2 aces, there are 4 permutations:
#     [[1,1], [1,11], [11,1], [11,11]]
# These permutations lead to 3 unique sums: [2, 12, 22]
# Of these 3, only 2 are <=21 so they are returned: [2, 12]
def get_ace_values(temp_list):
    sum_array = np.zeros((2**len(temp_list), len(temp_list)))
    # This loop gets the permutations
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2**n * 0.5)
        for rep in range(int(sum_array.shape[0]/half_len/2)):
            sum_array[rep*2**n : rep*2**n+half_len, i]=1
            sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i]=11
    # Only return values that are valid (<=21)
    return list(set([int(s) for s in np.sum(sum_array, axis=1)\
                     if s<=21]))
        
def ace_values(num_aces):
    temp_list = []
    for i in range(num_aces):
        temp_list.append([1,11])
    return get_ace_values(temp_list)

# Total up value of hand
def total_up(hand):
    aces = 0
    total = 0
    
    for card in hand:
        if card != 'A':
            total += card
        else:
            aces += 1
    
    # Call function ace_values to produce list of possible values
    # for aces in hand
    ace_value_list = ace_values(aces)
    final_totals = [i+total for i in ace_value_list if i+total<=21]
    
    if final_totals == []:
        return min(ace_value_list) + total
    else:
        return max(final_totals)
    
def Let_us_play(stacks):
   global dealer_cards, d_hand, p_hand, p1_hand, p2_hand, split, bet, result
   #balance = 255    
   #players = 1  
   #dealer_card_feature = []
   #player_card_feature = []
   #player_results = []
   for stack in range(stacks):
    
        result = 0
        split = 0
        #curr_player_result = 0
        dealer_cards = make_decks(num_decks, card_types)
        #p = player, d = dealer
        d_hand = []
        p_hand = []

        # Deal FIRST card
        p_hand.append(dealer_cards.pop(0))
        d_hand.append(dealer_cards.pop(0))
        # Deal SECOND card
        p_hand.append(dealer_cards.pop(0))
        d_hand.append(dealer_cards.pop(0))
        

        ### Pair in hand ###
        if(p_hand[0] == p_hand[1]):
            #print('Pair')
            Pair = pair_table.loc[str(p_hand[0]), str(d_hand[0])]
            if(Pair == 'D'):
                #print('Pair_D')
                p_hand.append(dealer_cards.pop(0))
                bet *= 2
                battle(p_hand,d_hand)
                
            elif(Pair == 'P'):
                #print('Pair_P')
                split = 1
                p1_hand = [p_hand[0]]
                p2_hand = [p_hand[1]]
                p1_hand.append(dealer_cards.pop(0))
                p2_hand.append(dealer_cards.pop(0))
                check_ace(p1_hand)
                check_ace(p2_hand)
                
            elif(Pair == 'H'):
                #print('Pair_H')
                p_hand.append(dealer_cards.pop(0))
                check_ace(p_hand)
                
            elif(Pair == 'S'):
                #print('Pair_S')
                battle(p_hand,d_hand)
                
        ### Check A in Hand ###
        elif('A' in p_hand):
            #print("Ace")
            Ace = ace_table.loc[wo_ace_total_up(p_hand), str(d_hand[0])]
            if(Ace == 'D'):
                #print('Ace_D') 
                p_hand.append(dealer_cards.pop(0))
                bet *= 2
                battle(p_hand,d_hand)
                
            elif(Ace == 'S'):
                #print('Ace_S')
                battle(p_hand,d_hand)
                
            elif(Ace == 'H'):
                #print('Ace_H')    
                p_hand.append(dealer_cards.pop(0))
                check_ace(p_hand)

        ### Main Table ###
        else:
            #print('Main')
            Main = main_table.loc[total_up(p_hand), str(d_hand[0])]
            if(Main == 'D'):
                #print('Main_D')
                p_hand.append(dealer_cards.pop(0))
                bet *= 2
                battle(p_hand,d_hand)
                
            elif(Main == 'S'): 
                #print('Main_S')
                battle(p_hand,d_hand)
                
            elif(Main == 'H'):   
                #print('Main_H')
                p_hand.append(dealer_cards.pop(0))
                check_ace(p_hand)
                
        if deposit >= 200 :
             print('Enough')
             break
        elif bet > 128:
             print('Game Over')
             break
         
     
                
def wo_ace_total_up(p_hand):
    woa_hand = p_hand.copy()
    woa_hand.remove('A')
    rep = [1 if x == 'A' else x for x in woa_hand]
    return sum(rep)

def check_ace(p_hand):
    global dealer_cards, d_hand, split, bet
    if ('A' in p_hand):
        if(wo_ace_total_up(p_hand) >= 11):
            if(total_up(p_hand) > 21):
                battle(p_hand,d_hand) 
                
            elif(main_table.loc[total_up(p_hand), str(d_hand[0])] == 'S'): 
                battle(p_hand,d_hand)
                
            else:
                #print('Hard_Ace_H')
                p_hand.append(dealer_cards.pop(0))
                check_ace(p_hand)
                
        elif(len(p_hand) == 2 and ace_table.loc[wo_ace_total_up(p_hand), str(d_hand[0])] == 'D'):  
            #print('2_Ace_D')
            bet *= 2
            p_hand.append(dealer_cards.pop(0))
            battle(p_hand,d_hand)
            
        elif(ace2_table.loc[wo_ace_total_up(p_hand), str(d_hand[0])] == 'S'):  
            battle(p_hand,d_hand)    
            
        else:
             #print('2_Ace_H')
             p_hand.append(dealer_cards.pop(0))
             check_ace(p_hand)
             
    elif (total_up(p_hand) > 21):
        battle(p_hand,d_hand)
        
    else:
        if(main_table.loc[total_up(p_hand), str(d_hand[0])] == 'S'): 
            battle(p_hand,d_hand)
        elif(len(p_hand) == 2 and main_table.loc[total_up(p_hand), str(d_hand[0])] == 'D'): 
            #print('2_Main_D')
            bet *= 2
            p_hand.append(dealer_cards.pop(0))
            battle(p_hand,d_hand)
        else:
            #print('2_Main_H')
            p_hand.append(dealer_cards.pop(0))
            check_ace(p_hand)
       
def battle(p_hand, d_hand):  
        global dealer_cards, bet, result, player_results, deposit, deposit_curve
        while (total_up(d_hand) < 17):
            d_hand.append(dealer_cards.pop(0)) 
        """
        print(len(dealer_cards))    
        print('dealer')
        for x in range(len(d_hand)): 
             #print(d_hand[x], end = ' ')     
        print(total_up(d_hand))
        
        print('player')
        for x in range(len(p_hand)): 
             print(p_hand[x], end = ' ')
        print(total_up(p_hand))
        """
        if (split == 0 and set(p_hand) == blackjack and set(d_hand) == blackjack):
            #print("Tie Tie Tie!")
            result = 'Tie'
            
        elif (split == 0 and set(p_hand) == blackjack):
            #print("BlackJack")
            result = 'BJ'
            
        elif set(d_hand) == blackjack:
            #print("You Lose!") 
            result = 'L' 
            
        elif total_up(p_hand) >= 22:
            #print("You Lose!")
            result = 'L'
            
        elif total_up(d_hand) >= 22:
            #print("You Win!") 
            result = 'W'
            
        elif total_up(p_hand) > total_up(d_hand):
            #print("You Win!")
            result = 'W'
            
        elif total_up(p_hand) == total_up(d_hand):
            #print("Tie Tie Tie!")
            result = 'Tie'
            
        elif total_up(p_hand) < total_up(d_hand):
            #print("You Lose!")   
            result = 'L'
            
        #print(result)
        #print('') 
        if result == 'BJ':
            deposit = deposit + 1.5 * bet
            bet = 1
        elif result == 'W':
            deposit = deposit + 1 * bet
            bet = 1
        elif result == 'Tie':
            deposit = deposit
        elif result == 'L':
            deposit = deposit - bet
            bet *= 2
            
            
        if deposit < 0 or bet > 128:
            deposit = -999999999999999
        deposit_curve.append(deposit)    
        player_results.append(result)
       
Let_us_play(200) 

deposit_curve = deposit_curve[:-1]
data = pd.DataFrame(deposit_curve)
ax = sns.lineplot(data=data)
plt.show()



