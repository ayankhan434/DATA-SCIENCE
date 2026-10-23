""" import numpy as np

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

 """



import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.game-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

div.stButton > button {
    width: 100%;
    height: 95px;
    border-radius: 16px;
    font-size: 36px;
    font-weight: bold;
    background-color: #1e293b;
    color: white;
    border: 1px solid #475569;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #334155;
    border-color: #60a5fa;
    color: white;
}

div.stButton > button[kind="primary"] {
    background-color: #2563eb;
}

.status {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)


# ---------- GAME LOGIC ----------
def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if abs(np.sum(board[i, :])) == 3:
            return "X" if np.sum(board[i, :]) == 3 else "O"

        if abs(np.sum(board[:, i])) == 3:
            return "X" if np.sum(board[:, i]) == 3 else "O"

    # Check diagonals
    diagonal1 = np.trace(board)
    diagonal2 = np.trace(np.fliplr(board))

    if abs(diagonal1) == 3:
        return "X" if diagonal1 == 3 else "O"

    if abs(diagonal2) == 3:
        return "X" if diagonal2 == 3 else "O"

    # Check draw
    if not np.any(board == 0):
        return "DRAW"

    return None


def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.result = None


# ---------- SESSION STATE ----------
if "board" not in st.session_state:
    reset_game()


# ---------- HEADER ----------
st.markdown(
    '<div class="game-title">TIC TAC TOE</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Challenge your friend. Make your move!</div>',
    unsafe_allow_html=True
)

board = st.session_state.board
result = st.session_state.result

# ---------- GAME STATUS ----------
if result == "DRAW":
    st.markdown(
        '<div class="status">🤝 It is a Draw!</div>',
        unsafe_allow_html=True
    )
elif result:
    st.markdown(
        f'<div class="status">🏆 Player {result} Wins!</div>',
        unsafe_allow_html=True
    )
else:
    player = "X" if st.session_state.current == 1 else "O"
    st.markdown(
        f'<div class="status">🎯 Player {player}’s Turn</div>',
        unsafe_allow_html=True
    )

# ---------- GAME BOARD ----------
for r in range(3):
    cols = st.columns(3, gap="small")

    for c in range(3):
        value = board[r, c]
        symbol = "X" if value == 1 else "O" if value == -1 else "　"

        with cols[c]:
            if st.button(
                symbol,
                key=f"cell_{r}_{c}",
                disabled=(value != 0 or result is not None),
                use_container_width=True
            ):
                st.session_state.board[r, c] = (
                    st.session_state.current
                )

                new_result = check_winner(st.session_state.board)
                st.session_state.result = new_result

                if new_result is None:
                    st.session_state.current *= -1

                st.rerun()

# ---------- RESTART BUTTON ----------
st.write("")

left, middle, right = st.columns([1, 2, 1])

with middle:
    if st.button(
        "🔄 Restart Game",
        type="primary",
        use_container_width=True
    ):
        reset_game()
        st.rerun()

st.write("")
st.caption("Built with Python • NumPy • Streamlit")
