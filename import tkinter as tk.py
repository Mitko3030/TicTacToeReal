import tkinter as tk
import winsound
### По-добро качество
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

###Всички нужни променливи
game_running=True
score_red=0
score_blue=0
current_player="X"
winner=False
winner_label=None
current_winner=""
game_mode_var="bot"

### Създавам прозореца за игра и го позиционира в средата на екрана
screen = tk.Tk()
screen.title("Морски Шах")
screen.configure(bg="#222831")
y = (screen.winfo_screenheight() // 5)
x = (screen.winfo_screenwidth() // 3)+100
screen.geometry(f"390x520+{x}+{y}")


### Създава се етикет за заглавието и се поставя
label_tic_tac_toe = tk.Label(screen, text="МОРСКИ ШАХ", font=("Impact", 14), bg="#393E46", fg="white")
label_tic_tac_toe.grid(row=0, column=0, columnspan=3, padx=110, pady=10)



### Избирам между бот и човек
game_mode_var = tk.StringVar(value="bot")
player_bot = tk.Radiobutton(screen, text="Човек", variable=game_mode_var, value="player", font=("Arial", 12), bg="#393E46", fg="white", selectcolor="grey")
player_person = tk.Radiobutton(screen, text="Бот", variable=game_mode_var, value="bot", font=("Arial", 12), bg="#393E46", fg="white", selectcolor="grey")

### Изписвам ги
player_bot.grid(row=8, column=2, padx=10, pady=10)
player_person.grid(row=8, column=0, padx=10, pady=10)


### Два етикета за резултата от играта
label_red_score=tk.Label(screen, text=f"RED SCORE:  {score_red}", fg="#FF2E63", bg="#222831", font=("Impact", 12))
label_blue_score=tk.Label(screen, text=f"BLUE SCORE:  {score_blue}", fg="#08D9D6", bg="#222831", font=("Impact", 12))


###Поставят се двата етикета в прозореца за игра
label_red_score.grid(row=1, column=0, padx=10, pady=10)
label_blue_score.grid(row=1, column=2, padx=10, pady=10)




### Създавам празен лист с бутони и после го запълвам
buttons = []
for row in range(3):
    row_buttons = []
    for col in range(3):
        button = tk.Button(screen, text="", width=6, height=2, font=("Arial", 16),
                           command=lambda r=row, c=col: button_click(r, c))
        button.grid(row=row + 2, column=col, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)







### Функция за проверка за победител
def checkWin():
    global current_winner
    for i in range(3):
        if buttons[i][0].cget("text") == buttons[i][1].cget("text") == buttons[i][2].cget("text") != "":
            current_winner = buttons[i][0].cget("text")
            return True
        if buttons[0][i].cget("text") == buttons[1][i].cget("text") == buttons[2][i].cget("text") != "":
            current_winner=buttons[0][i].cget("text")
            return True
    if buttons[0][0].cget("text") == buttons[1][1].cget("text") == buttons[2][2].cget("text") != "":
        current_winner = buttons[0][0].cget("text")
        return True
    if buttons[0][2].cget("text") == buttons[1][1].cget("text") == buttons[2][0].cget("text") != "":
        current_winner = buttons[0][2].cget("text")
        return True
    return False



### Функция за изписване на победителя
def declareWinner():
    global winner_label, game_running, score_red, score_blue
    game_running=False
    if game_mode_var.get()!="bot":
        winsound.PlaySound("congratulations-deep-voice-172193.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    winner_label=tk.Label(screen, text=f"Winner is: {current_winner}", fg="green", font=("Arial", 15, "bold"), bg="#222831")
    winner_label.grid(row=9, column=0, columnspan=3, pady=10)
    if current_winner=="X":
        score_red+=1
        label_red_score.config(text=f"RED SCORE:  {score_red}")
    elif current_winner=="O":
        score_blue+=1
        label_blue_score.config(text=f"BLUE SCORE:  {score_blue}")
    


### Функция за рестартиране на играта
def resetBoard():
    global current_player, game_running, winner, winner_label
    game_running = True
    winner = False
    current_player="X"

    if winner_label is not None:
        winner_label.destroy()

    for row in range(3):
        for col in range(3):
            buttons[row][col]["text"] = ""
            buttons[row][col]["fg"] = "black"


### Създавам рестарт бутон и го поставям в прозореца
reset_button = tk.Button(screen, text="Рестарт", command=resetBoard, font=("Arial", 12, "bold"), bg="#393E46", fg="white", borderwidth=0)
reset_button.grid(row=8, column=1, columnspan=1, pady=10)




 
### Функция за хода на бота
def bot_move():
    global current_player, game_running
    if not game_running:
        return

    best_score = -float("inf")
    best_move = None

    for r in range(3):
        for c in range(3):
            if buttons[r][c]["text"] == "":
                buttons[r][c]["text"] = "O"
                score = minimax(buttons, 0, False)
                buttons[r][c]["text"] = ""

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    if best_move:
        r, c = best_move
        buttons[r][c]["text"] = "O"
        buttons[r][c]["fg"] = "blue"


        
        
        if checkWin():
            declareWinner()
        else:
            current_player = "X"



### Функция за натискане на бутон
def button_click(row, col):
    global current_player, winner, current_winner


    if buttons[row][col]["text"]=="" and game_running:
        buttons[row][col]["text"]=current_player
        buttons[row][col]["fg"]="red" if current_player=="X" else "blue"

    if checkWin():
        declareWinner()
    elif is_board_full():
        declareDraw()
    else:      # Срещу бот
        if game_mode_var.get() == "bot":  
            current_player = "O"
            screen.after(300, bot_move)
        else:  # Двама играчи
            current_player = "O" if current_player == "X" else "X"  
    



### Функция за проверка за състоянието на играта
def check_winner_state():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]
    return None




### Функция за проверка дали е пълна дъската
def is_board_full():
    return all(buttons[r][c]["text"] != "" for r in range(3) for c in range(3))


def declareDraw():
    global winner_label, game_running
    game_running = False
    winner_label = tk.Label(screen, text="Равенство!", fg="orange", font=("Arial", 15, "bold"), bg="#222831")
    winner_label.grid(row=9, column=0, columnspan=3, pady=10)


### Функция за намиране на най-добрия ход за бота
def minimax(board, depth, is_maximizing, alpha=-float("inf"), beta=float("inf")):
    winner = check_winner_state()
    if winner:
        return 10 - depth if winner == "O" else depth - 10  
    if is_board_full():
        return 0  

    if is_maximizing:
        best_score = -float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c]["text"] == "":
                    board[r][c]["text"] = "O"
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[r][c]["text"] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c]["text"] == "":
                    board[r][c]["text"] = "X"
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[r][c]["text"] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score



### Прозорецът стои отворен постоянно
screen.mainloop()