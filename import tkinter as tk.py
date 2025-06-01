import tkinter as tk


game_running=True
score_red=0
score_blue=0
current_player="X"
winner=False
winner_label=None
current_winner=""
previousWinner=""


screen = tk.Tk()
screen.title("Морски Шах")
screen.geometry("330x420")

###
label_tic_tac_toe=tk.Label(screen, text="МОРСКИ ШАХ", font=("Impact", 14))
label_tic_tac_toe.grid(row=0, column=0, columnspan=3, padx=110, pady=10)


###
label_red_score=tk.Label(screen, text=f"RED SCORE:  {score_red}", fg="#FF0000")
label_blue_score=tk.Label(screen, text=f"BLUE SCORE:  {score_blue}", fg="#0000FF")

###

label_red_score.grid(row=1, column=0, padx=10, pady=10)
label_blue_score.grid(row=1, column=2, padx=10, pady=10)

###

buttons = []
for row in range(3):
    row_buttons = []
    for col in range(3):
        button = tk.Button(screen, text="", width=6, height=2, font=("Arial", 16),
                           command=lambda r=row, c=col: button_click(r, c))
        button.grid(row=row + 2, column=col, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

###

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


###

def declareWinner():
    global winner_label, game_running, previousWinner

    game_running=False
    winner_label=tk.Label(screen, text=f"Winner is: {current_winner}", fg="green", font=("Arial", 15))
    winner_label.grid(row=5, column=0, columnspan=3, pady=10)
    previousWinner=current_winner




###

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


###

reset_button = tk.Button(screen, text="Рестарт", command=resetBoard, font=("Arial", 12))
reset_button.grid(row=6, column=0, columnspan=3, pady=10)

###

def button_click(row, col):
    global current_player, winner, current_winner


    if buttons[row][col]["text"]=="" and game_running:
        buttons[row][col]["text"]=current_player
        buttons[row][col]["fg"]="red" if current_player=="X" else "blue"

    if checkWin():
        declareWinner()
    else:
        current_player="O" if current_player=="X" else "X"
screen.mainloop()