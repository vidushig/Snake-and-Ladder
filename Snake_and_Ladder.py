### Snake and Ladder Game
### Multiple player game

              
                           
                          

import random, time, sys
           

DICE_FACE = 6
SLEEP_TIME = 1
MAX_VALUE = 100

snake = {
27: 7,
35: 5,
39: 3,
50: 34,
59: 46,
66: 24,
73: 12,
76: 63,
89: 67,
97: 86,
99: 26
}

ladder = {
2: 23,
7: 29,
22: 41,
28: 77,
30: 32,
44: 58,
54: 69,
70: 90,
80: 83,
87: 93
}

#Rules of the game
def welcome():
    
    print("Welcome to Snake & Ladder Game")
    print("""
    
    Below are the rules of the game.
    
    1. The number of players in this game should neither be less than 2 nor more than 6.
    2. Each player will start the game from position '0'.
    3. To start the game, the player has to roll a value '6' on the dice for the first time. This value is used only to enter the game.
    4. If a player lands on the lower numbered square of a ladder, the player will climb the ladder till the upper numbered square of the ladder.
    5. If a player lands on the upper numbered square of a snake, the player will momve down till the lower numbered sqaure of the snake.
    6. If any player gets a value equal to 100, he/she wins the game. If on rolling the dice, the value becomes greater than 100, the player has to wait on the current value till he/she gets a number resulting in final value equal to 100.
    
    Enjoy the game !
    """)

#Get player data
def get_player_names():
    
    players = []
    
    no_of_players = int(input("Enter the number of players: "))
    
    if (no_of_players < 2) or (no_of_players > 6):
        print("""\nNOTE: Minimum number of players = 2
        Maximum number of players = 6""")
        no_of_players = int(input("Enter a valid number of players: "))
    
    for i in range(0, no_of_players):
        name = input("Enter the name of player no %d: " %(i+1))
        players.append(name)
    
    return players

#Roll the dice
def get_dice_value():
    dice_value = random.randint(1, DICE_FACE)
    print("\nIt's a '" + str(dice_value) + "'")
    
    return dice_value

#Player hit a snake square
def snake_value(player, old_value, current_value):
    print("\nOh no! You have reached the sqaure with a snake." )
    print(player + " will move down the snake from '" + str(old_value) + "' to '" + str(current_value) + "'")

#Player hit a ladder square
def ladder_value(player, old_value, current_value):
    print("\nYayy. " + player + " has landed on a square with a ladder.")
    print(player + " will climb up the ladder from '" + str(old_value) + "' to '" + str(current_value) + "'")

#Final value based on snake / ladder
def snake_ladder(player, current_value, dice_value):
    
    old_value = current_value
    current_value = current_value + dice_value
    
    #Check if value is within MAX_VALUE
    if current_value > MAX_VALUE:
        current_value = old_value
        print("\nOops! " + player + " will remain at the same position '" + str(old_value) + "' till " + player + " gets '" + str(MAX_VALUE - old_value) + "'")
    else:
        print("\n" + player + " will now move from '" + str(old_value) + "' to '" + str(current_value) + "'")
    
    if current_value in snake:
        final_value = snake.get(current_value)
        snake_value(player, current_value, final_value)
    elif current_value in ladder:
        final_value = ladder.get(current_value)
        ladder_value(player, current_value, final_value)
    else:
        final_value = current_value
    
    return final_value

#Check the winning condition
def check_win(player, position):
    
    if (MAX_VALUE == int(position)):
        print("\nYipiee. " + player + " has won the game. Congratulations!")
        return False
    return True

#Game
def start_the_game():
    
    welcome()
    
    player_list = get_player_names()
    
    player_data = {player_list[i]: 0 for i in range(0, len(player_list))}
    player_position = 0
    GAME_STARTED  = True
    
    while (GAME_STARTED):

        for player, player_points in player_data.items():
        
            value = input("\nIt is " + player + "'s turn next. Hit enter to roll the dice...")
            print("\n" + player + " is rolling the dice...")
            dice_value = get_dice_value()
            player_data[player] = snake_ladder(player, player_data[player], dice_value)
            
            if (check_win(player, player_data[player]) == False):
                GAME_STARTED = False
                break
    print("\nHere is the scoreboard: ",player_data)

#Main function
if __name__ == "__main__":
                                                                        
                                             
                                               
                                                    
                                                                          
                                                                      
                                                                     
                                                            
                                                                         
                              
    
    start_the_game()