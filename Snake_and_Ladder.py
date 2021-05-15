import sys, random
import pandas as pd
import csv

class Snake_Ladder:
    
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
        
    column_name = ['Player_Name', 'Start', 'Current_Value', 'Old_Value', 'Dice_Value']
    player_data = pd.DataFrame(columns = column_name)
    
    def __init__(self):
        
        self.start()
        
    
    #Rules of the game
    def welcome(self):
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
    
    #Get no of player
    def get_player_count(self):
        
        no_of_players = int(input("Enter the number of players: "))
        
        if (no_of_players < 2) or (no_of_players > 6):
            print("""\nNOTE: Minimum number of players = 2
            Maximum number of players = 6""")
            no_of_players = int(input("Enter a valid number of players: "))
        
        self.player_data = pd.DataFrame(0, index = range(no_of_players), columns = self.column_name)
                
        for i in range(0, no_of_players):
            name = input("Enter name of player %d: " %(i+1))
            self.player_data.iloc[i,0] = name
    
    #Roll the dice
    def get_dice_value(self, player):
        
        position = 0
        dice_value = random.randint(1, self.DICE_FACE)
        
        if dice_value == 6:
            position = position + dice_value
            value = input(player + " has got a value '" + str(dice_value) + "' on 1st try. You will get a chance to roll the dice again. Hit enter...")
            dice_value = random.randint(1, self.DICE_FACE)
            if dice_value == 6:
                position = position + dice_value
                value = input(player + " has got a value '" + str(dice_value) + "' on 2nd try also. Now if you get a '" + str(dice_value) + "' on 3rd try as well, you will remain at the same position and wait for your next turn. Hit enter to roll the dice...")
                dice_value = random.randint(1, self.DICE_FACE)
                if dice_value == 6:
                    position = 0
                    print("Oops! " + player + " has got a value '" + str(dice_value) + "' again. You will remain at the same position. Try again on your next turn.")
                else:
                    position = position + dice_value
                    print(player + ", you just escaped a 3rd '6'. It's a: '" + str(dice_value) + "'. Please move ahead by: ",position)
            else:
                position = position + dice_value
                print(player + ", has got a value '" + str(dice_value) + "'. Please move ahead by: ",position)
        else:
            position = position + dice_value
            print("It's a: " + str(dice_value))
        
        return position
    
    #Player hit a snake square
    def snake_value(self, player, old_value, current_value):
        
        print("\nOh no! You have reached the sqaure with a snake." )
        print(player + " will move down the snake from '" + str(old_value) + "' to '" + str(current_value) + "'")
    
    #Player hit a ladder square
    def ladder_value(self, player, old_value, current_value):
        
        print("\nYayy. " + player + " has landed on a square with a ladder.")
        print(player + " will climb up the ladder from '" + str(old_value) + "' to '" + str(current_value) + "'")
    
    #Snake_Ladder check
    def snake_ladder(self, player, current_value, old_value, dice_value):
        
        #Check if value is within MAX_VALUE
        #print(player, current_value, old_value)
        
        if current_value > self.MAX_VALUE:
            print("\nOops! " + player + " will remain at the same position '" + str(old_value) + "' till you get a '" + str(self.MAX_VALUE - old_value) + "'")
            current_value = old_value
            #print("current value is: ", current_value)
        else:
            print(player + " will now move from '" + str(old_value) + "' to '" + str(current_value) + "'")
        
        if current_value in self.snake:
            final_value = self.snake.get(current_value)
            self.snake_value(player, current_value, final_value)
        elif current_value in self.ladder:
            final_value = self.ladder.get(current_value)
            self.ladder_value(player, current_value, final_value)
        else:
            final_value = current_value
    
        return final_value
    
    #Check the winning condition
    def check_win(self, player, position):
        
        if (self.MAX_VALUE == int(position)):
            print("\nYipiee. " + player + " has won the game. Congratulations!")
            return False
        return True
    
    #Game
    def start(self):
        
        self.welcome()
        self.get_player_count()
        
        GAME_STARTED = True
        
        while(GAME_STARTED):
            for i in range(len(self.player_data)):
                
                if self.player_data.iloc[i,1] == 0:
                    value = input("\n" + self.player_data.iloc[i,0] + " will roll the dice to start the game. Hit enter...")
                    dice = random.randint(1, self.DICE_FACE)
                    print("\nDice value for player '" + self.player_data.iloc[i,0] + "' is: '" + str(dice), "'")
                
                    if dice == 6:
                        print(self.player_data.iloc[i,0] + " will enter the game now.")
                        self.player_data.iloc[i,1] = 1
                    else:
                        print(self.player_data.iloc[i,0] + ", your dice value != '6'. Kindly try again on your next turn.")
                
                if (dice == 6) or (self.player_data.iloc[i,1] == 1):
                    value = input("\nIt is " + self.player_data.iloc[i,0] + "'s turn next. Hit enter to roll the dice...")
                    print("\n" + str(self.player_data.iloc[i,0]) + " is rolling the dice...")
                    self.player_data.iloc[i,4] = self.get_dice_value(self.player_data.iloc[i,0])
                    
                    self.player_data.iloc[i,3] = self.player_data.iloc[i,2]
                    self.player_data.iloc[i,2] = self.player_data.iloc[i,2] + self.player_data.iloc[i,4]
                    
                    self.player_data.iloc[i,2] = self.snake_ladder(self.player_data.iloc[i,0], self.player_data.iloc[i,2], self.player_data.iloc[i,3], self.player_data.iloc[i,4])
                    
                    if (self.check_win(self.player_data.iloc[i,0], self.player_data.iloc[i,2]) == False):
                        GAME_STARTED = False
                        break
                print("\nCurrent player status is below\n",self.player_data)
        
        print("\n\nFINAL SCOREBOARD: \n\n",self.player_data)
        
        self.player_data.to_csv('Snake_and_Ladder.csv', mode='a')

#Main function call
if __name__ == "__main__":
    
    Snake_Ladder()
