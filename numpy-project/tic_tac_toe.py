
import streamlit as st
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- RESPONSIVE CUSTOM CSS ----------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

/* Main content container */
.block-container {
    width: 100%;
    max-width: 650px;
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: clamp(0.75rem, 4vw, 2rem);
    padding-right: clamp(0.75rem, 4vw, 2rem);
}

/* Text colors */
h1, h2, h3, p, label {
    color: white !important;
}

/* Game heading */
.game-title {
    text-align: center;
    font-size: clamp(2rem, 7vw, 2.875rem);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
    overflow-wrap: break-word;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: clamp(0.85rem, 3vw, 1rem);
    margin-bottom: clamp(1rem, 4vw, 2rem);
}

/* Status text */
.status {
    text-align: center;
    font-size: clamp(1.1rem, 4vw, 1.4rem);
    font-weight: 700;
    line-height: 1.4;
    margin: clamp(0.75rem, 3vw, 1.25rem) 0;
    overflow-wrap: break-word;
}

/* Board cells */
div.stButton > button {
    width: 100%;
    min-width: 0;
    height: clamp(65px, 16vw, 105px);
    padding: 0;
    border-radius: clamp(10px, 2vw, 16px);
    font-size: clamp(1.5rem, 7vw, 2.5rem);
    font-weight: 800;
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #475569;
    transition: background-color 0.2s ease,
                border-color 0.2s ease;
}

/* Hover effects for mouse devices */
@media (hover: hover) {
    div.stButton > button:hover {
        background-color: #334155;
        border-color: #60a5fa;
        color: white;
    }
}

/* Restart button */
div.stButton > button[kind="primary"] {
    background-color: #2563eb;
    color: white;
    border: 1px solid #3b82f6;
    font-size: clamp(0.95rem, 3vw, 1.1rem);
    font-weight: 700;
    height: auto;
    min-height: 48px;
    padding: 0.65rem 1rem;
}

@media (hover: hover) {
    div.stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8;
        border-color: #60a5fa;
    }
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    margin-top: 1.5rem;
}

/* Small screens */
@media (max-width: 480px) {
    .block-container {
        padding-top: 1.25rem;
        padding-left: 0.65rem;
        padding-right: 0.65rem;
    }

    .subtitle {
        margin-bottom: 1rem;
    }

    div.stButton > button {
        height: clamp(60px, 20vw, 85px);
        border-radius: 10px;
    }
}

/* Reduced motion accessibility */
@media (prefers-reduced-motion: reduce) {
    div.stButton > button {
        transition: none;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- GAME LOGIC ----------
def check_winner(board):

    # Check rows and columns
    for i in range(3):

        row_sum = np.sum(board[i, :])
        col_sum = np.sum(board[:, i])

        if row_sum == 3:
            return "X"

        if row_sum == -3:
            return "O"

        if col_sum == 3:
            return "X"

        if col_sum == -3:
            return "O"

    # Check diagonals
    diagonal1 = np.trace(board)
    diagonal2 = np.trace(np.fliplr(board))

    if diagonal1 == 3 or diagonal2 == 3:
        return "X"

    if diagonal1 == -3 or diagonal2 == -3:
        return "O"

    # Check draw
    if not np.any(board == 0):
        return "DRAW"

    return None


# ---------- RESET GAME ----------
def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.result = None


# ---------- INITIALIZE STATE ----------
if "board" not in st.session_state:
    reset_game()


# ---------- HEADER ----------
st.markdown(
    '<div class="game-title">TIC TAC TOE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Challenge your friend. Make your move!'
    '</div>',
    unsafe_allow_html=True
)


# ---------- GAME STATE ----------
board = st.session_state.board
result = st.session_state.result


# ---------- GAME STATUS ----------
if result == "DRAW":

    st.markdown(
        '<div class="status">🤝 It\'s a Draw!</div>',
        unsafe_allow_html=True
    )

elif result in ("X", "O"):

    st.markdown(
        f'<div class="status">🏆 Player {result} Wins!</div>',
        unsafe_allow_html=True
    )

else:

    player = "X" if st.session_state.current == 1 else "O"

    st.markdown(
        f'<div class="status">🎯 Player {player}\'s Turn</div>',
        unsafe_allow_html=True
    )


# ---------- GAME BOARD ----------
for r in range(3):

    cols = st.columns(3, gap="small")

    for c in range(3):

        value = st.session_state.board[r, c]

        if value == 1:
            symbol = "X"
        elif value == -1:
            symbol = "O"
        else:
            symbol = " "

        with cols[c]:

            clicked = st.button(
                symbol,
                key=f"cell_{r}_{c}",
                disabled=(
                    value != 0
                    or st.session_state.result is not None
                ),
                use_container_width=True
            )

            if clicked:

                # Make the move
                st.session_state.board[r, c] = (
                    st.session_state.current
                )

                # Check winner or draw
                new_result = check_winner(
                    st.session_state.board
                )

                st.session_state.result = new_result

                # Change turn only if game continues
                if new_result is None:
                    st.session_state.current *= -1

                st.rerun()


# ---------- RESTART BUTTON ----------
st.write("")

_, middle, _ = st.columns([1, 2, 1])

with middle:

    st.button(
        "🔄 Restart Game",
        key="restart",
        type="primary",
        use_container_width=True,
        on_click=reset_game
    )


# ---------- FOOTER ----------
st.markdown(
    '<div class="footer">'
    'Built with Python • NumPy • Streamlit'
    '</div>',
    unsafe_allow_html=True
)
