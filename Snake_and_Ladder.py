### Snake and Ladder Game
###Single player game

import os, sys
import random, dictionaries
from dictionaries import *

players = []
started = 0

snake_points = [27, 35, 39, 50, 59, 66, 73, 76, 89, 97, 99]
snake_steps = [7, 5, 3, 34, 46, 24, 12, 63, 67, 86, 26]

ladder_points = [2, 7, 22, 28, 30, 44, 54, 70, 80, 87]
ladder_steps = [23, 29, 41, 77, 32, 58, 69, 90, 83, 93]

###Check if the Snake and Ladder points and steps are matching
if len(snake_points) == len(snake_steps):
    if len(ladder_points) == len(ladder_steps):
        print("Data is correct")
    else:
        print("Data is incorrect")
       
###Get players data
no_of_players = int(input("\nEnter number of players: "))

#if (no_of_players > 6) or (no_of_players < 2):
#    print("\nNumber of players should be between 2 and 6")
#    no_of_players = int(input("\nEnter number of players: "))

for i in range(0,no_of_players):
    player_name = input("Enter player name: ")
    players.append(player_name)

player_data = {players[i]: 0 for i in range(0,len(players))}

print(player_data)

for player in player_data:
    for player_points in player_data.values():
        while (player_points <= 100):
            if started == 0:
                dice = random.randint(1,6)
                print(player,player_points)
            if dice == 6:
                started = 1
        
            if (started == 1):
                dice = random.randint(1,6)
                print("Value before rolling the dice: ",player, player_points)
                player_points += dice
                print("Value after rolling the dice: ",player, dice, player_points)
                for s_point in snake_points:
                    for s_step in snake_steps:
                        if player_points == s_point:
                            print("before snake: ",player, player_points)
                            point_index = snake_points.index(s_point)
                            player_points = snake_steps[point_index]
                            dice = snake_steps[point_index]
                            print("after snake: ",player, player_points)
                for l_point in ladder_points:
                    for l_step in ladder_steps:
                        if player_points == l_point:
                            print("before ladder: ",player, player_points)
                            point_index = ladder_points.index(l_point)
                            player_points = ladder_steps[point_index]
                            dice = ladder_steps[point_index]
                            print("after ladder: ",player, player_points)
            print(player_data)
    