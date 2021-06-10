import sys, signal, random, math
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Snake_and_Ladder import *

class GAME_GUI(QWidget):
    
    DICE_FACE = 6
    prevValue = 0
    name_list = []
    score_list = []
    started_list = []
    GAME_STARTED = 0
    no_of_players = 0
    name = []
    player_index = 1
    counter = 0
    position = 0
    color_list = ["#00FFFF", "#FFB6C1", "#FED8B1", "#98FB98", "#ADD8E6", "white"]
    
    #SIGNALS
    ROLL_THE_DICE = 1
    GUI_Signal = pyqtSignal(int, list)
    data_list = [0]*6
    
    def __init__(self):
        super(GAME_GUI,self).__init__()
        
        self.SL = Snake_Ladder()
        
        #Signal handler
        self.GUI_Signal.connect(self.SL.Handle_GUI_Signal)
        self.SL.SL_Signal.connect(self.Handle_SL_Signal)
        
        self.setFixedSize(1050,850)
        self.setWindowTitle('Snake & Ladder')
        
        self.display()
        
        self.mainlayout = QVBoxLayout(self)
        self.vlayout = QVBoxLayout()
        self.vlayout.setAlignment(Qt.AlignCenter)
        
        self.player_count(self.prevValue)
        
        self.mainlayout.setAlignment(Qt.AlignCenter)
        self.mainlayout.addLayout(self.vlayout)
        
        self.mainlayout.addStretch()
        
        self.setLayout(self.mainlayout)
        self.setContentsMargins(750,155,30,100)
        self.show()
    
    def Handle_SL_Signal(self, val, return_data):
        
        if val == Snake_Ladder.DICE_VALUE:
            start = return_data[0]
            dice_value = return_data[1]
            self.counter = return_data[2]
            self.player_index = return_data[3]
            self.current_player_index = return_data[4]
            next_player_index = return_data[5]
            message = return_data[6]
            current_player_score = return_data[7]
            SL_message = return_data[8]
            winner_message = return_data[9]
            
            current_player = (self.name_list[self.current_player_index-1].text())
            next_player = (self.name_list[next_player_index-1].text())
            
            self.score_list[self.current_player_index-1].setText(str(current_player_score))
            self.started_list[self.current_player_index-1].setText(str(start))
            self.lbl_dice.setText(str(message))
            self.lbl_message.setText(str(SL_message))
            self.winner.setText(str(winner_message))
            
            if self.winner.text() != " ":
                self.lbl_dice.setText(" ")
                self.lbl_message.setText(" ")
                self.roll_the_dice.setEnabled(False)

    def display(self):
        self.display_layout = QFormLayout()
        
        #Headline for the game
        self.headline = QLabel("SNAKE & LADDER", self)
        self.headline.setGeometry(410,10,180,35)
        self.headline.setStyleSheet("background-color : yellow ; border : 3px solid ; border-bottom-color : black ; font-weight: bold")
        self.headline.setFont(QFont('Decorative', 10))
        self.headline.setAlignment(Qt.AlignCenter)
        
        #Rules of the game
        self.rules = QPushButton("Check rules of the game", self)
        self.rules.setGeometry(30,800,230,40)
        self.rules.setStyleSheet("background-color : #5DBB63 ; border : 2px solid ; border-bottom-color : black ; font-weight: bold")
        self.rules.setFont(QFont('Decorative', 10))
        self.rules.clicked.connect(self.rules_click)
        
        #Instructions for snake and ladder
        self.inst_snake = QLabel("SNAKES (red)", self)
        self.inst_snake.setGeometry(30,60,120,30)
        self.inst_snake.setStyleSheet('color: red ; font-weight: bold')
        self.inst_snake.setFont(QFont('Decorative', 9))
        self.inst_snake.setAlignment(Qt.AlignCenter)
        
        self.inst_ladder = QLabel("LADDER (green)", self)
        self.inst_ladder.setGeometry(160,60,140,30)
        self.inst_ladder.setStyleSheet('color: #008000 ;  ; font-weight: bold')
        self.inst_ladder.setFont(QFont('Decorative', 9))
        self.inst_ladder.setAlignment(Qt.AlignCenter)
        
        #Start button
        self.start_btn = QPushButton("START THE GAME", self)
        self.start_btn.setGeometry(800,100,160,30)
        self.start_btn.setStyleSheet("border : 2px solid ; border-bottom-color : black")
        self.start_btn.setFont(QFont('Decorative', 9))
        self.start_btn.clicked.connect(self.start_click)
        
        #No of players text label
        self.lbl_count = QLabel("Number of players in the game:", self)
        self.lbl_count.setGeometry(760,140,250,30)
        self.lbl_count.setFont(QFont('Decorative', 10))
        self.lbl_count.setAlignment(Qt.AlignLeft)
        
        #No of players label
        self.lbl_no = QLabel(self)
        self.lbl_no.setGeometry(990,135,30,30)
        self.lbl_no.setFont(QFont('Decorative', 10))
        self.lbl_no.setAlignment(Qt.AlignCenter)
                                    
        #roll the dice button
        self.lbl_start_msg = QLabel(self)
        self.lbl_start_msg.setGeometry(780,400,210,30)
        self.lbl_start_msg.setFont(QFont('Decorative', 10))
        self.lbl_start_msg.setAlignment(Qt.AlignCenter)
        
        self.roll_the_dice = QPushButton("ROLL THE DICE", self)
        self.roll_the_dice.setGeometry(800,440,150,30)
        self.roll_the_dice.setFont(QFont('Decorative', 10))
        self.roll_the_dice.setStyleSheet("border : 2px solid ; border-bottom-color : black")
        self.roll_the_dice.clicked.connect(self.roll_the_dice_click)
        
        #Print dice value for current player
        self.lbl_dice = QLabel(self)
        self.lbl_dice.setGeometry(740,500,270,100)
        self.lbl_dice.setStyleSheet('color: #008000')
        self.lbl_dice.setFont(QFont('Decorative', 10))
        self.lbl_dice.setAlignment(Qt.AlignCenter)
        self.lbl_dice.setWordWrap(True)
        
        #Print SL message
        self.lbl_message = QLabel(self)
        self.lbl_message.setGeometry(740,600,270,100)
        self.lbl_message.setStyleSheet('color: #800000')
        self.lbl_message.setFont(QFont('Decorative', 10))
        self.lbl_message.setAlignment(Qt.AlignCenter)
        self.lbl_message.setWordWrap(True)
        
        #Print the winner
        self.winner = QLabel(self)
        self.winner.setGeometry(550,800,450,40)
        self.winner.setFont(QFont('Decorative', 10))
        self.winner.setStyleSheet("background-color : #C0C0C0 ; border : 3px solid ; border-bottom-color : black ; color : black ; font-weight: bold")
        self.winner.setAlignment(Qt.AlignCenter)
        
        #Add Widgets to the layout
        #self.display_layout.addWidget(self.start_btn)
        #self.display_layout.addWidget(self.lbl_count)
        #self.display_layout.addWidget(self.lbl_no)
        #self.display_layout.addWidget(self.lbl_roll)
        #self.display_layout.addWidget(self.lbl_dice)
    
    def player_count(self,value):
        self.player_name_layout = QGridLayout()
        
        for i in range(0,self.prevValue):
            self.player_name_layout.removeWidget(self.name_list[i])
            self.player_name_layout.removeWidget(self.score_list[i])
            self.player_name_layout.removeWidget(self.started_list[i])
            self.name_list[i].deleteLater()
            self.score_list[i].deleteLater()
            self.started_list[i].deleteLater()
        self.name_list = []
        self.score_list = []
        self.started_list = []
        
        for i in range(0,len(self.name)):
            self.player_name = QLineEdit()
            self.player_name.setFixedSize(130,25)
            self.player_name.setEnabled(False)
            self.player_name.setAlignment(Qt.AlignCenter)
            self.player_name.setStyleSheet("background-color: %s ; color: black" % self.color_list[i])
            self.player_name.setText(self.name[i])
            self.player_name_layout.addWidget(self.player_name,i,0)
            self.name_list.append(self.player_name)
            
            self.player_score = QLineEdit()
            self.player_score.setFixedSize(40,25)
            self.player_score.setEnabled(False)
            self.player_score.setAlignment(Qt.AlignCenter)
            self.player_score.setStyleSheet("background-color: %s ; color: black" % self.color_list[i])
            self.player_score.setText(str(0))
            self.player_name_layout.addWidget(self.player_score,i,1)
            self.score_list.append(self.player_score)
            
            self.player_started = QLineEdit()
            self.player_started.setFixedSize(30,25)
            self.player_started.setEnabled(False)
            self.player_started.setAlignment(Qt.AlignCenter)
            self.player_started.setVisible(False)
            self.player_started.setText(str(0))
            self.player_name_layout.addWidget(self.player_started,i,2)
            self.started_list.append(self.player_started)
            
        self.vlayout.addLayout(self.player_name_layout)
        self.prevValue = value
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        
        self.xlength = 70
        y_off = (self.xlength * 11) - 50
        x_off = 70
        n = 10
        for x in range(0,10):
            for y in range(0,10):
                if (y % 2) == 0:
                    x_off = 30
                    rect = QRect(x_off + (x * self.xlength), y_off - (y * self.xlength), self.xlength, self.xlength)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter, str((n * y) + x + 1))
                else:
                    x_off = (self.xlength * 10) - 40
                    rect = QRect(x_off - (x * self.xlength), y_off - (y * self.xlength), self.xlength, self.xlength)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter, str((n * y) + x + 1))
        
        
        #Snakes
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawLine(485,630,550,740)   #27:8
        painter.drawLine(415,560,345,740)   #35:5
        painter.drawLine(135,560,205,740)   #39:3
        painter.drawLine(695,490,625,670)   #50:12
        painter.drawLine(205,350,135,390)   #63:59
        painter.drawLine(410,360,275,600)   #66:24
        painter.drawLine(550,280,485,530)   #73:34
        painter.drawLine(340,280,200,460)   #76:43
        painter.drawLine(620,210,480,320)   #89:67
        painter.drawLine(270,140,480,390)   #97:54
        painter.drawLine(130,140,415,600)   #99:26
        
        #Ladders
        painter.setPen(QPen(QColor("#008000"), 4, Qt.SolidLine))
        painter.drawLine(135,740,205,630)   #2:23
        painter.drawLine(620,740,65,630)   #9:21
        painter.drawLine(555,670,625,560)   #13:32
        painter.drawLine(275,670,65,490)   #17:41
        painter.drawLine(550,600,270,280)   #28:77
        painter.drawLine(275,530,205,420)   #37:58
        painter.drawLine(550,460,625,350)   #48:69
        painter.drawLine(65,320,205,210)   #61:83
        painter.drawLine(625,250,695,140)   #72:91
        painter.drawLine(485,250,410,140)   #74:95
        
        if self.GAME_STARTED == 1:
            self.move_pointer(painter)
            self.update()

    def move_pointer(self, painter):
        
        y_off= 770
        #Player pointers in the game
        for i in range(0,len(self.name)):
            if (self.started_list[i].text() == '1') and (int(self.score_list[i].text()) != 0):
                value = int(self.score_list[i].text())
                if (value % 10 == 0) and ((int(math.log10(value)+1)) == 2):
                    number = [int(i) for i in str(value)]
                    y = number[0]
                    x = number[1]
                    if (y % 2) == 0:
                        x_base = 50
                        painter.setPen(Qt.black)
                        painter.setBrush(QColor(self.color_list[i]))
                        painter.setFont(QFont('Decorative', 5))
                        painter.drawEllipse(x_base + (i * 5) + (x * 70),y_off - ((y-1) * 70),15,15)
                    else:
                        x_base = 670
                        painter.setPen(Qt.black)
                        painter.setBrush(QColor(self.color_list[i]))
                        painter.setFont(QFont('Decorative', 5))
                        painter.drawEllipse(x_base + (i * 5) - (x * 70),y_off - ((y-1) * 70),15,15)
                elif (int(math.log10(value)+1)) == 1:
                    x = value
                    y = 0
                    if (y % 2) == 0:
                        x_base = -20
                        painter.setPen(Qt.black)
                        painter.setBrush(QColor(self.color_list[i]))
                        painter.setFont(QFont('Decorative', 5))
                        painter.drawEllipse(x_base + (i * 5) + (x * 70),y_off - (y * 70),15,15)
                    else:
                        x_base = 670
                        painter.setPen(Qt.black)
                        painter.setBrush(QColor(self.color_list[i]))
                        painter.setFont(QFont('Decorative', 5))
                        painter.drawEllipse(x_base + (i * 5) - (x * 70),y_off - (y * 70),15,15)
                elif (int(math.log10(value)+1)) == 2:
                    number = [int(i) for i in str(value)]
                    y = number[0]
                    x = number[1]
                    if (y % 2) == 0:
                        x_base = -30
                        painter.setPen(Qt.black)
                        painter.setBrush(QColor(self.color_list[i]))
                        painter.setFont(QFont('Decorative', 5))
                        painter.drawEllipse(x_base + (i * 5) + (x * 70),y_off - (y * 70),15,15)
                    else:
                        x_base = 750    
                        painter.setPen(Qt.black)
                        painter.setBrush(QColor(self.color_list[i]))
                        painter.setFont(QFont('Decorative', 5))
                        painter.drawEllipse(x_base + (i * 5) - (x * 70),y_off - (y * 70),15,15)
                elif (int(math.log10(value)+1)) == 3:
                    painter.setPen(Qt.black)
                    painter.setBrush(QColor(self.color_list[i]))
                    painter.setFont(QFont('Decorative', 5))
                    painter.drawEllipse(40,140,15,15)
            elif self.started_list[i].text() == '1':
                painter.setPen(Qt.black)
                painter.setBrush(QColor(self.color_list[i]))
                painter.setFont(QFont('Decorative', 5))
                painter.drawEllipse(10,y_off - (i * 20),15,15)

    def start_click(self):
        self.GAME_STARTED = 0
        self.start_btn.setText("RESTART THE GAME")
        
        temp, ok = QInputDialog.getInt(self, "select input dialog", "Enter number of players:")
        if ok:
            self.no_of_players = int(temp)
            self.name = [self.no_of_players] * 0
            
            while (self.no_of_players < 2) or (self.no_of_players > 6):
                self.count_msg()
                temp = QInputDialog.getText(self, "integer input dialog", "Enter number of players:")
                self.no_of_players = int(temp[0])
            self.SL.player_data = pd.DataFrame(0, index = range(self.no_of_players), columns = self.SL.column_name)
            
            for i in range(0, self.no_of_players):
                name_temp, ok = QInputDialog.getText(self, "select input dialog", "Enter name of player no %d: "%(i+1))
                
                if ok:
                    if str(name_temp) == '':
                        self.name.append("Player " + str(i+1))
                    else:
                        self.name.append(str(name_temp))
            
            self.player_count(self.no_of_players)
            self.lbl_no.setText(str(self.no_of_players))
            self.lbl_start_msg.setText(self.name[0] + " will start the game.")
            self.winner.setText(" ")
            self.roll_the_dice.setEnabled(True)
            self.GAME_STARTED = 1

    def rules_click(self):
        msg = QMessageBox()
        msg.setWindowTitle("RULES OF THE GAME")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText("""         WELCOME TO SNAKE & LADDER GAME
        
        Below are the rules of the game:
            
        1. The number of players in this game should neither be less than 2 nor more than 6.
        2. Each player will start the game from position '0'.
        3. To start the game, the player has to roll a value '6' on the dice for the first time. This value is used only to enter the game.
        4. If a player lands on the lower numbered square of a ladder, the player will climb the ladder till the upper numbered square of the ladder.
        5. If a player lands on the upper numbered square of a snake, the player will momve down till the lower numbered sqaure of the snake.
        6. If any player gets a value equal to 100, he/she wins the game. If on rolling the dice, the value becomes greater than 100, the player has to wait on the current value till he/she gets a number resulting in final value equal to 100.
            
                            Enjoy the game !
        """)
        retval = msg.exec_()
    
    def count_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("ALERT")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText("NOTE: Minimum number of players = 2 and maximum number of players = 6. Enter a valid number of players.")
        retval = msg.exec_()
    
    def roll_the_dice_click(self):
        self.lbl_start_msg.setText('')
        
        self.data_list[0] = self.player_index
        self.data_list[1] = self.name_list
        self.data_list[2] = self.score_list
        self.data_list[3] = self.started_list
        self.data_list[4] = self.counter
        
        self.GUI_Signal.emit(self.ROLL_THE_DICE, self.data_list)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    Gui = GAME_GUI()
    sys.exit(app.exec_())