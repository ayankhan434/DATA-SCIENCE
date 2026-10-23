import numpy as np

board = np.zeros((3,3),dtype=int)


#board print karne ke liye 
def print_board(b):
    symbols={0:" ", 1: "X", -1: "0"}
    for r in range(3):
        row=" | ".join(symbols[val] for val in b[r])
        print(" "+ row)
        if r<2:
            print("---+---+---")
    print()

#winner check karne ke liye hai 
def check_winner(b):
    if 3 in np.sum(b,axis=1) or 3 in np.sum(b,axis=0):
        return 'X'
    if -3 in np.sum(b,axis=1) or -3 in np.sum(b,axis=0):
        return '0'
    if np.trace(b)==3 or np.trace (np.fliplr(b))==3:
        return 'X'
    if np.trace(b)==-3 or np.trace(np.fliplr(b))==-3:
        return '0'
    if not 0 in b:
        return 'DRAW'


    return "NONE"


current =1
print("welcome to tic tac tow")




#input / output ke liye from user

while True:

    if current ==1:
        player='X'
    else:
        player='0'


    try:
        row=int(input(player+"  -- Enter row(0,1,2)"))
        col=int(input(player+ " --Enter column(0,1,2)"))

    except ValueError:
        print("please enter numbers only ")
        continue 

    if row <0 or row>2 or col<0 or col>2 :
        print("row and column must be between 0 aND 2")

    if board [row,col]!=0:
        print("cell is allready taken")

    board[row,col]=current
    print_board(board)

    result = check_winner(board)

    if result!="NONE":
        if result == "DRAW":
            print("its a draw")
        else:
            print(result,"wins")

        break

    if current==1:
        current=-1
    else:
        current=1

