import flet as ft

# Check for win conditions
def check_winner(b):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)             # Diagonals
    ]
    for x, y, z in lines:
        if b[x] and b[x] == b[y] == b[z]:
            return b[x]
    if "" not in b:
        return "Tie"
    return None

# Minimax algorithm for the Pro Bot (AI is "O", Human is "X")
def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner == "O": return 1
    if winner == "X": return -1
    if winner == "Tie": return 0

    if is_maximizing:
        best_score = -1000
        for i in range(9):
            if b[i] == "":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for i in range(9):
            if b[i] == "":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = ""
                best_score = min(score, best_score)
        return best_score

def find_best_move(b):
    best_score = -1000
    move = -1
    for i in range(9):
        if b[i] == "":
            b[i] = "O"
            score = minimax(b, False)
            b[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def main(page: ft.Page):
    page.title = "Tic Tac Toe - Vs Pro Bot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 500

    board = [""] * 9
    status_text = ft.Text("Your turn (X)", size=16, weight=ft.FontWeight.BOLD)
    grid_buttons = []

    def reset_game(e):
        nonlocal board
        board = [""] * 9
        status_text.value = "Your turn (X)"
        for btn in grid_buttons:
            btn.text = ""
            btn.disabled = False
        page.update()

    def make_ai_move():
        move = find_best_move(board)
        if move != -1:
            board[move] = "O"
            grid_buttons[move].text = "O"
            grid_buttons[move].disabled = True

        res = check_winner(board)
        if res:
            end_game(res)
        else:
            status_text.value = "Your turn (X)"
            page.update()

    def end_game(res):
        for btn in grid_buttons:
            btn.disabled = True
        if res == "Tie":
            status_text.value = "It's a Tie!"
        else:
            status_text.value = f"Player {res} Wins!"
        page.update()

    def handle_click(e):
        idx = int(e.control.data)
        if board[idx] == "" and status_text.value.startswith("Your"):
            board[idx] = "X"
            e.control.text = "X"
            e.control.disabled = True
            
            res = check_winner(board)
            if res:
                end_game(res)
            else:
                status_text.value = "Bot thinking..."
                page.update()
                page.run_task(delayed_ai_move)

    async def delayed_ai_move():
        import asyncio
        await asyncio.sleep(0.3)
        make_ai_move()

    for i in range(9):
        btn = ft.ElevatedButton(
            text="",
            data=i,
            width=90,
            height=90,
            on_click=handle_click,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        grid_buttons.append(btn)

    grid = ft.GridView(
        runs_count=3,
        max_extent=100,
        spacing=5,
        run_spacing=5,
        width=300,
        height=300,
        controls=grid_buttons
    )

    reset_btn = ft.ElevatedButton("Restart Game", on_click=reset_game)

    page.add(
        ft.Column(
            [status_text, grid, reset_btn],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)
