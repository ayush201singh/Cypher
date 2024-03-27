import speech_recognition as sr
import os
import webbrowser
import win32com.client 
import datetime
from googlesearch import search
import random
import re

speaker = win32com.client.Dispatch("SAPI.SPvoice")

def write(text):
    os.system(f"echo {text}")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "some error occured"

def google(x):

    for i in search(x , tld="com", num=10, stop=10, pause=2):
        print(i)
        continue

def rock_paper_scissor():

    user = input("'r' for rock, 'p' for paper, 's' for scissors: ")
    print(user)
    computer_choice = random.choice(['r','p','s'])
    print(computer_choice)

    if user == computer_choice:
         print("It's a tie")
    
    if (user=="r" and computer_choice=="s") or (user=="s" and computer_choice=="p") or (user=="p" and computer_choice=="r"):
        print("user wins!!")

    else:
        print("compure wins!!!")


class Board():
    def __init__(self, dim_size, num_bombs):

        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #craete the board
        self.board = self.make_new_board() #plant the bombs

        # to keep the track of the explored area
        self.assign_values_to_board()
        self.dug = set()


    def make_new_board(self):
        # make a loop for the rows and columns of the board
        board = [[" " for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc// self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                # to check if the place already has a bomb
                continue

            board[row][col] = "*"
            bombs_planted += 1
        
        return board
    

    def assign_values_to_board(self):
        # after the bombs are planted we will assign the board numbers (0-8) for all the empty spaces
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_surrounding_bombs(r,c)


    def get_num_surrounding_bombs(self, row, col):
        # iterarte through neighbouring positions
        # top left - (r-1,c-1)
        # top middle - (r-1,c)
        # top right - (r-1,c+1)
        # left - (r,c-1)
        # right - (r,c+1)
        # down left - (r+1,c-1)
        # down middle - (r+1,c)
        # down right - (r+1,c+1)

        num_neighbouring_bombs = 0
        for r in range(max(0,row-1) , min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1,col+1)+1):
                if r==row and c== col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == "*":
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

    def dig(self, row, col):

        self.dug.add((row, col)) # keep track of places you dig

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0,row-1) , min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1,col+1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)

        return True
    
    def __str__(self):
        # this is a magic function where if you call print on this object
        # it'll return out what the function returns

        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "


        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
        
        
def minesweeper(dim_size = 10, num_bombs=10):

    board = Board(dim_size, num_bombs)

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0  or col >= board.dim_size:
            print("Invalid location. Try again")
            continue

        safe = board.dig(row,col)
        if not safe:
            # dug a bomb
            break

    if safe:
        print(board)
        print("CONGRATULATIONS, YOU WON THE GAME")
    else:
        print(board)
        print("SORRY GAME OVER :( ")
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        


class lottery():
    ROWS = 3
    COLS = 3

    symbol_count = {"A":2 , "B":3, "C":4, "D":5}

    symbol_value = {"A":5 , "B":4, "C":3, "D":2}

    def check_winnings(columns, lines, bet, values):
        winnings = 0
        winning_lines=[]
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line +1)

        return winnings, winning_lines




    def slot_machine(rows,cols,symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for col in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for row in range(rows):
                value = random.choice(all_symbols)
                current_symbols.remove(value)
                column.append(value)
            columns.append(column)
        
        return columns


    def print_slot_machine(columns):
        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                if i != len(columns)-1:
                    print(column[row], end=" | ")
                else:
                    print(column[row], end="")

            print()



    def deposit():
        while True:
            amount = int(input("enter the amount in digits: $"))
            if amount>0:
                break
            else:
                print("please enter an amount")
        return amount

    MAX_LINES = 3
    MAX_BET = 100
    MIN_BET = 1

    def get_number_of_lines():
        while True:
            lines = int(input("enter the number of lines to bet on (1-"+str(lottery.MAX_LINES)+")?"))
            if lines>=1 and lines<=lottery.MAX_LINES:
                break
            else:
                print("enter valid number of lines")
        return lines

    def get_bet():
        while True:
            amount = int(input("enter the amount you would like to bet on a line? $"))
            if amount>=lottery.MIN_BET and amount<=lottery.MAX_BET:
                break
            else:
                print(f"enter the amount between ${lottery.MIN_BET}-${lottery.MAX_BET}")
        return amount

        
    def spin(balance):
        lines = lottery.get_number_of_lines()
        while True:
            bet = lottery.get_bet()
            total_bet = bet * lines

            if total_bet>balance:
                print(f"you do not have enough balance to bet {bet} on each line, your balance is {balance}")
            
            else:
                break

        print(f"your balance is: {balance}\nnumber of lines to bet on is {lines} \nthe amount you are betting on one line is {bet}\nthe amount you are betting is {total_bet}")
        slots = lottery.slot_machine(lottery.ROWS, lottery.COLS, lottery.symbol_count)
        lottery.print_slot_machine(slots)
        winnings, winning_lines = lottery.check_winnings(slots,lines,bet,lottery.symbol_value)
        print(f"you win {winnings}")
        print(f"you won on line: ", *winning_lines)
        return winnings - total_bet

    def main():
        balance = lottery.deposit()
        while True:
            print(f"Current balance is {balance}")
            game = input("press enter to start game (q to quit)")
            if game== "q":
                break
            balance += lottery.spin(balance) 
        
        print(f"you left with ${balance}")


class guessing():

    def guess(x):
        random_number = random.randint(1,x)
        guess = 0
        while guess!=random_number:
            guess = int(input("enter the number: "))
            if guess<random_number:
                print("Too low, Guess again")
            if guess>random_number:
                print("Too high, guess again")

        print("YAY!!! you have guessed correctly")

    def computer_guess(x):
        low = 1
        high = x
        feedback= " "
        while feedback != "c":
            guess = random.randint(low,high)
            feedback = input(f"is {guess} too high(h), too low(l), or correct (c)?")
            if feedback == "h":
                high = guess-1
            if feedback == "l":
                low = guess+1
            
        print(f"YAY, the computer has guessed correctly")


if __name__== '__main__':
    write("hello, I'm your personal assistant")
    while True:
        print("listening.....")
        query = take_command()
        speaker.Speak(query)

        if "who are you" in query.lower():
            write("I'm your personal AI assistant, I'll help you in your every work.")
            speaker.speak("I'm your personal AI assistant, I'll help you in your every work.")

        sites = [["youtube","https://www.youtube.com/"],["wikipedia", "https://www.wikipedia.org/"], ["neflix", "https://www.netflix.com/browse"], ["google","https://www.google.com/"]]
        for site in sites:  
            if f"open {site[0]}".lower() in query.lower():   
                write(f"opening {site[0]}...")
                webbrowser.open(site[1])
        
        if "play music" in query.lower():
            musicpath = r"C:\Users\ayush\OneDrive\Desktop\anime_song.mp3"
            os.startfile(musicpath)

        if "the time" in query.lower():
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            write(f"the time is {strftime}")
            speaker.speak(f"the time is {hour} hours {min} minute")

        apps = [["cmd" , "C:\WINDOWS\system32\cmd.exe"], ["chrome", "C:\Program Files\Google\Chrome\Application\chrome.exe"], ["spotify", "C:\\Users\\ayush\\AppData\\Roaming\\Spotify\\Spotify.exe"]
                 ]
        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                write(f"opening {app[0]}")
                os.startfile(app[1])
        
        if "google search" in query.lower():
            google(query)

        if "play game rock paper scissor" in query.lower():
            rock_paper_scissor()

        if "play game mine sweeper" in query.lower():
            minesweeper()

        if "play lottery game" in query.lower():
            lottery.main()

        if "exit program" in query.lower():
            break       
        
        guess = [["computer guessing" , guessing.computer_guess(100)], ["guessing", guessing.guess(100)]]
        if f"play {guess[0]} game" in query.lower():
            guess[1]

        
            

        