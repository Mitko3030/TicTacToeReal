import tkinter as tk
import random
###Всички нужни променливи
game_running=True
score_red=0
score_blue=0
current_player="X"
winner=False
winner_label=None
current_winner=""
previousWinner=""
game_mode_var="bot"

### Създавам прозореца за игра
screen = tk.Tk()
screen.title("Морски Шах")
screen.geometry("330x420")

### Създава се етикет за заглавието и се поставя
label_tic_tac_toe=tk.Label(screen, text="МОРСКИ ШАХ", font=("Impact", 14))
label_tic_tac_toe.grid(row=0, column=0, columnspan=3, padx=110, pady=10)



### Избирам между бот и човек
game_mode_var = tk.StringVar(value="bot")
player_bot = tk.Radiobutton(screen, text="Срещу Човек", variable=game_mode_var, value="player")
player_person = tk.Radiobutton(screen, text="Срещу Бот", variable=game_mode_var, value="bot")

### Изписвам ги
player_bot.grid(row=8, column=2, padx=10, pady=10)
player_person.grid(row=8, column=0, padx=10, pady=10)


### Два етикета за резултата от играта
label_red_score=tk.Label(screen, text=f"RED SCORE:  {score_red}", fg="#FF0000")
label_blue_score=tk.Label(screen, text=f"BLUE SCORE:  {score_blue}", fg="#0000FF")


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
    global winner_label, game_running, previousWinner

    game_running=False
    winner_label=tk.Label(screen, text=f"Winner is: {current_winner}", fg="green", font=("Arial", 15))
    winner_label.grid(row=5, column=0, columnspan=3, pady=10)
    previousWinner=current_winner




### Функция за рестартиране на играта
def resetBoard():
    global current_player, game_running, winner, winner_label, previousWinner
    game_running = True
    winner = False
    current_player = "X" if previousWinner=="O" else "O"

    if winner_label is not None:
        winner_label.destroy()

    for row in range(3):
        for col in range(3):
            buttons[row][col]["text"] = ""
            buttons[row][col]["fg"] = "black"


### Създавам рестарт бутон и го поставям в прозореца
reset_button = tk.Button(screen, text="Рестарт", command=resetBoard, font=("Arial", 12))
reset_button.grid(row=8, column=1, columnspan=1, pady=10)



### Функция за бота (прави случайни ходове)
def bot_move():
    global current_player, game_running

    if not game_running:
        return

    empty_positions = [(r,c)for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if empty_positions:
        r, c = random.choice(empty_positions)
        buttons[r][c]["text"] = current_player
        buttons[r][c]["fg"] = "blue"

        if checkWin():
            declareWinner()
        else:
            current_player = "X"  # Превключва обратно към играча


### Функция за натискане на бутон
def button_click(row, col):
    global current_player, winner, current_winner


    if buttons[row][col]["text"]=="" and game_running:
        buttons[row][col]["text"]=current_player
        buttons[row][col]["fg"]="red" if current_player=="X" else "blue"

    if checkWin():
        declareWinner()

    else:      # Срещу бот
        if game_mode_var.get() == "bot":  
            current_player = "O"
            bot_move()
        else:  # Двама играчи
            current_player = "O" if current_player == "X" else "X"




### Прозорецът стои отворен постоянно
screen.mainloop()