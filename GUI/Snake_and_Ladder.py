import sys, random, signal
import pandas as pd
import csv
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SL_GUI import *

class Snake_Ladder(QWidget):
    
    DICE_FACE = 6
    SLEEP_TIME = 1
    MAX_VALUE = 100
    counter = 0
    
    #Signals
    SL_Signal = pyqtSignal(int,list)
    DICE_VALUE = 1
    return_data = [0]*10
    
    counter = 0
    position = 0
    
    snake = {
    27: 7,
    35: 5,
    39: 3,
    50: 12,
    59: 46,
    66: 24,
    73: 34,
    76: 63,
    89: 67,
    97: 54,
    99: 26
    }
        
    ladder = {
    2: 23,
    9: 21,
    17: 41,
    28: 77,
    30: 32,
    44: 58,
    55: 69,
    72: 91,
    80: 83,
    87: 95
    }
        
    column_name = ['Player_Name', 'Start', 'Current_Value', 'Old_Value', 'Dice_Value']
    player_data = pd.DataFrame(columns = column_name)
    
    #def __init__(self):
    #    pass
        #self.start()
    
    #Signal Handler
    def Handle_GUI_Signal(self, val, data):
        
        if val == GAME_GUI.ROLL_THE_DICE:
            
            index = data[0]
            players_name = data[1]
            no_of_players = len(players_name)
            player_score = data[2]
            start_player = data[3]
            counter = data[4]
            
            #Update the dataframe with no of players and their names
            self.player_data = pd.DataFrame(0, index = range(len(players_name)), columns = self.column_name)
            
            for i in range(0,len(players_name)):
                self.player_data.iloc[i,0] = players_name[i].text()
                self.player_data.iloc[i,1] = int(start_player[i].text())
                self.player_data.iloc[i,2] = int(player_score[i].text())
                self.player_data.iloc[i,3] = int(player_score[i].text())
            self.roll_the_dice(no_of_players, index, start_player, counter)
    
    #Enter the game
    def roll_the_dice(self, no_of_players, current_player_index, start, counter):
        
        current_player_index, next_player_index = self.get_player_index(no_of_players, current_player_index)
        
        self.counter = counter
        
        player_start = int(start[current_player_index-1].text())
        
        current_player = self.player_data.iloc[current_player_index-1,0]
        next_player = self.player_data.iloc[next_player_index-1,0]
        current_player_score = self.player_data.iloc[current_player_index-1,2]
        previous_score = self.player_data.iloc[current_player_index-1,2]
        
        dice_value = random.randint(1, self.DICE_FACE)
        
        SL_message = " "
        winner = " "
        new_score = 0
        
        if player_start == 0:
            if dice_value == 6:
                message = current_player + " has got a " + str(dice_value) + ". You will enter the game now.\n" + next_player + " will roll the dice."
                self.player_index = next_player_index
                player_start = 1
            else:
                message = current_player + ", your value != 6. Kindly try again on your next turn.\n" + next_player + " will roll the dice next."
                self.player_index = next_player_index
        else:
            if (dice_value == 6) and (self.counter == 0):   #Enter level 1
                self.position = self.position + dice_value
                message = current_player + " has got a " + str(dice_value) + " on 1st try. You will get a chance to roll the dice again."
                self.player_index = current_player_index
                self.counter += 1
            
            elif (dice_value != 6) and (self.counter == 0):   #Level 1 and exit
                self.position = self.position + dice_value
                message = current_player + " has got a " + str(dice_value) + ". Move ahead by " + str(self.position) + ".\n" + next_player + " will roll the dice now."
                self.player_index = next_player_index
                current_player_score += self.position
                self.position = 0
                
            elif (dice_value == 6) and (self.counter == 1):   #Enter level 2
                self.position = self.position + dice_value
                message = current_player + " has got a " + str(dice_value) + " on 2nd try also. Now if you get a " + str(dice_value) + " on 3rd try as well, you will remain at the same position and wait for your next turn."
                self.player_index = current_player_index
                self.counter += 1
            
            elif (dice_value != 6) and (self.counter == 1):   #Level 2 and exit
                self.position = self.position + dice_value
                message = current_player + ", has got a value " + str(dice_value) + ". Please move ahead by: " + str(self.position)
                self.player_index = next_player_index
                current_player_score += self.position
                self.position = 0
                self.counter = 0
            
            elif (dice_value == 6) and (self.counter == 2):   #Enter level 3
                self.position = 0
                message = "Oops! " + current_player + " has got a " + str(dice_value) + " again. You will remain at the same position. Try again on your next turn."
                self.player_index = next_player_index
                current_player_score += self.position
                self.counter = 0
            
            elif (dice_value != 6) and (self.counter == 2):   #Level 3 and exit
                self.position = self.position + dice_value
                message = current_player + ", you just escaped a 3rd 6. It's a " + str(dice_value) + ". Please move ahead by: ",self.position
                self.player_index = next_player_index
                current_player_score += self.position
                self.position = 0
                self.counter = 0
        
        if current_player_score in self.snake:
            new_score = self.snake.get(current_player_score)
            SL_message = "Oh no! " + current_player + " has reached the sqaure with a snake. You will move down the snake from " + str(current_player_score) + " to " + str(new_score)
            current_player_score = new_score
            
        if current_player_score in self.ladder:
            new_score = self.ladder.get(current_player_score)
            SL_message = "Yayy. " + current_player + " has landed on a square with a ladder. You will climb up the ladder from " + str(current_player_score) + " to " + str(new_score)
            current_player_score = new_score
            
        if current_player_score > self.MAX_VALUE:
            message = "Oops! " + current_player + " has got a " + str(dice_value) + ". You will remain at the same position " + str(previous_score) + " till you get a " + str(self.MAX_VALUE - previous_score)
            current_player_score = previous_score
        elif current_player_score == self.MAX_VALUE:
            winner = (current_player + " has won the game. Congratulations !")
            
            #Update the DataFrame
            self.player_data.iloc[current_player_index-1,0] = current_player
            self.player_data.iloc[current_player_index-1,1] = player_start
            self.player_data.iloc[current_player_index-1,2] = current_player_score
            self.player_data.iloc[current_player_index-1,3] = previous_score
            self.player_data.iloc[current_player_index-1,4] = dice_value
            
            self.player_data.to_csv('Snake_and_Ladder.csv', mode='a')
        
        self.return_data[0] = player_start
        self.return_data[1] = dice_value
        self.return_data[2] = self.counter
        self.return_data[3] = self.player_index
        self.return_data[4] = current_player_index
        self.return_data[5] = next_player_index
        self.return_data[6] = message
        self.return_data[7] = current_player_score
        self.return_data[8] = SL_message
        self.return_data[9] = winner
        
        self.SL_Signal.emit(self.DICE_VALUE, self.return_data)
    
    #Get player index
    def get_player_index(self, no_of_players, current_player_index):
        
        for no in range(0, no_of_players):
            if current_player_index % no_of_players != 0:
                next_player_index = current_player_index + 1
            else:
                next_player_index = 1
            
        return current_player_index, next_player_index

#Main function call
if __name__ == "__main__":
    
    Snake_Ladder()
