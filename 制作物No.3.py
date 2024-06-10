import tkinter as tk
import random

#盤面
CELL_SIZE = 30
COLS = 10
ROWS = 20
DELAY = 500

#ミノ
MINOS = {
    'I': [((0, 1), (1, 1), (2, 1), (3, 1)), 'cyan'],
    'O': [((0, 0), (0, 1), (1, 0), (1, 1)), 'yellow'],
    'T': [((0, 1), (1, 0), (1, 1), (1, 2)), 'purple'],
    'S': [((0, 1), (0, 2), (1, 0), (1, 1)), 'green'],
    'Z': [((0, 0), (0, 1), (1, 1), (1, 2)), 'red'],
    'J': [((0, 0), (1, 0), (1, 1), (1, 2)), 'blue'],
    'L': [((0, 2), (1, 0), (1, 1), (1, 2)), 'orange']
}

class Tetris(tk.Tk):
    #初期化
    def __init__(self):
        super().__init__()
        self.title('Tetris')
        self.canvas = tk.Canvas(self, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='black')
        self.canvas.pack()
        self.label = tk.Label(self, text="Lines Cleared: 0", font=("Helvetica", 16))
        self.label.pack()
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current_mino = self.new_mino()
        self.mino_pos = [0, 3]
        self.lines_cleared = 0
        self.bind("<Key>", self.key_press)
        self.draw_board()
        self.drop_mino()

#盤面の描画
    def draw_board(self):
        self.canvas.delete('all')
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c]:
                    self.canvas.create_rectangle(
                        c*CELL_SIZE, r*CELL_SIZE,
                        (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                        fill=self.board[r][c],
                        outline='gray'
                    )
        self.draw_mino()
       
    #ミノの生成
    def new_mino(self):
        mino_type = random.choice(list(MINOS.keys()))
        return [MINOS[mino_type][0], MINOS[mino_type][1]]
    
    #ミノの描画
    def draw_mino(self):
        for cell in self.current_mino[0]:
            x, y = cell
            self.canvas.create_rectangle(
                (self.mino_pos[1]+x)*CELL_SIZE, (self.mino_pos[0]+y)*CELL_SIZE,
                (self.mino_pos[1]+x+1)*CELL_SIZE, (self.mino_pos[0]+y+1)*CELL_SIZE,
                fill=self.current_mino[1],
                outline='gray'
            )
    
    #ミノの落下
    def drop_mino(self):
        if not self.check_collision((1, 0)):
            self.mino_pos[0] += 1
        else:
            self.stack_mino()
            self.clear_lines()
            self.current_mino = self.new_mino()
            self.mino_pos = [0, 3]
            if self.check_collision((0, 0)):
                self.game_over()
                return
        self.draw_board()
        self.after(DELAY, self.drop_mino)
    
    #ミノの操作（十字キー）
    def key_press(self, event):
        if event.keysym == "Left":
            if not self.check_collision((0, -1)):
                self.mino_pos[1] -= 1
        elif event.keysym == "Right":
            if not self.check_collision((0, 1)):
                self.mino_pos[1] += 1
        elif event.keysym == "Down":
            if not self.check_collision((1, 0)):
                self.mino_pos[0] += 1
        elif event.keysym == "Up":
            self.rotate_mino()
        self.draw_board()
    
    #衝突の確認
    def check_collision(self, move):
        for cell in self.current_mino[0]:
            x, y = cell
            new_x = self.mino_pos[1] + x + move[1]
            new_y = self.mino_pos[0] + y + move[0]
            if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and self.board[new_y][new_x]):
                return True
        return False
    
    #ミノの回転
    def rotate_mino(self):
        rotated_mino = [(y, -x) for x, y in self.current_mino[0]]
        if not self.check_collision_with_rotated(rotated_mino):
            self.current_mino[0] = rotated_mino
    
    #回転するミノの衝突の確認
    def check_collision_with_rotated(self, rotated_mino):
        for cell in rotated_mino:
            x, y = cell
            new_x = self.mino_pos[1] + x
            new_y = self.mino_pos[0] + y
            if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and self.board[new_y][new_x]):
                return True
        return False
    
    #ミノの定着
    def stack_mino(self):
        for cell in self.current_mino[0]:
            x, y = cell
            self.board[self.mino_pos[0] + y][self.mino_pos[1] + x] = self.current_mino[1]
    
    #揃った行の消去
    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = ROWS - len(new_board)
        #消去した行のカウント
        if lines_cleared > 0:
            new_board = [[0] * COLS for _ in range(lines_cleared)] + new_board
            self.board = new_board
            self.lines_cleared += lines_cleared
            self.label.config(text=f"Lines Cleared: {self.lines_cleared}")
    
    #ゲームーバー
    def game_over(self):
        self.canvas.create_text(
            COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2,
            text="GAME OVER", fill="red", font=("Helvetica", 24)
        )
        self.unbind("<Key>")

if __name__ == '__main__':
    game = Tetris()
    game.mainloop()
