# ====================
# 人とAIの対戦
# ====================

# パッケージのインポート
#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk
from PIL import Image, ImageTk

# ベストプレイヤーのモデルの読み込み
model = load_model('model/best.h5')

# ゲームUIの定義
class GameUI(tk.Frame):
    # 初期化
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('簡易将棋')

        # ゲーム状態の生成
        self.state = State()
        self.select = -1  # 選択(-1:なし, 0～11:マス, 12～14:持ち駒)

        # 方向定数
        self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, -2), (-1, -2),
                    (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (8, -8),
                    (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (-8, 8),
                    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                    (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), (-8, -8),
                    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                    (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0),
                    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                    (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (0, -8))



        #self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

        # PV MCTSで行動選択を行う関数の生成
        self.next_action = pv_mcts_action(model, 0.0)

        # イメージの準備
        self.images = [(None, None, None, None)]
        for i in range(1, 19):
            image = Image.open('koma_gif/piece{}.gif'.format(i))
            self.images.append((
                ImageTk.PhotoImage(image),
                ImageTk.PhotoImage(image.rotate(180)),
                ImageTk.PhotoImage(image.resize((40, 40))),
                ImageTk.PhotoImage(image.resize((40, 40)).rotate(180))))

        # キャンバスの生成
        self.c = tk.Canvas(self, width=720, height=800, highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 描画の更新
        self.on_draw()

    # 人間のターン
    def turn_of_human(self, event):
        # ゲーム終了時
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 先手でない時
        if not self.state.is_first_player():
            return

        # 持ち駒の種類の取得
        captures = []
        for i in range(8):
            if self.state.pieces[81 + i] >= 2: captures.append(1 + i)
            if self.state.pieces[81 + i] >= 1: captures.append(1 + i)

        # 駒の選択と移動の位置の計算(0-80:マス, 81-88:持ち駒)
        p = int(event.x / 80) + int((event.y - 40) / 80) * 9
        if 40 <= event.y and event.y <= 760:
            select = p
        elif event.x < len(captures) * 40 and event.y > 760:
            select = 81 + int(event.x / 40)
        else:
            return

        # 駒の選択
        if self.select < 0:
            self.select = select
            self.on_draw()
            return

        # 駒の選択と移動を行動に変換
        action = -1
        if select < 81:
            # 駒の移動時
            if self.select < 81:
                action = self.state.position_to_action(p, self.position_to_direction(self.select, p))
            # 持ち駒の配置時
            else:
                action = self.state.position_to_action(p, 74 - 1 + captures[self.select - 81])

        # 合法手でない時
        if not (action in self.state.legal_actions()):
            self.select = -1
            self.on_draw()
            return

        # 次の状態の取得
        self.state = self.state.next(action)
        self.select = -1
        self.on_draw()

        # AIのターン
        self.master.after(1, self.turn_of_ai)

    # AIのターン
    def turn_of_ai(self):
        # ゲーム終了時
        if self.state.is_done():
            return

        # 行動の取得
        action = self.next_action(self.state)

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

    # 駒の移動先を駒の移動方向に変換
    def position_to_direction(self, position_src, position_dst):
        dx = position_dst % 9 - position_src % 9
        dy = int(position_dst / 9) - int(position_src / 9)
        for i in range(74):
            if self.dxy[i][0] == dx and self.dxy[i][1] == dy: return i
        return 0

    # 駒の描画
    def draw_piece(self, index, first_player, piece_type):
        x = (index % 9) * 80 + 20
        y = int(index / 9) * 80 + 40 + 20
        index = 0 if first_player else 1
        self.c.create_image(x, y, image=self.images[piece_type][index], anchor=tk.NW)

    # 持ち駒の描画
    def draw_capture(self, first_player, pieces):
        index, x, dx, y = (2, 0, 40, 760) if first_player else (3, 680, -40, 0)
        captures = []
        for i in range(8):
            if pieces[81 + i] >= 2: captures.append(1 + i)
            if pieces[81 + i] >= 1: captures.append(1 + i)
        for i in range(len(captures)):
            self.c.create_image(x + dx * i, y, image=self.images[captures[i]][index], anchor=tk.NW)

    # カーソルの描画
    def draw_cursor(self, x, y, size):
        self.c.create_line(x + 1, y + 1, x + size - 1, y + 1, width=4.0, fill='#FF0000')
        self.c.create_line(x + 1, y + size - 1, x + size - 1, y + size - 1, width=4.0, fill='#FF0000')
        self.c.create_line(x + 1, y + 1, x + 1, y + size - 1, width=4.0, fill='#FF0000')
        self.c.create_line(x + size - 1, y + 1, x + size - 1, y + size - 1, width=4.0, fill='#FF0000')

    # 描画の更新
    def on_draw(self):
        # マス目
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 720, 800, width=0.0, fill='#EDAA56')
        for i in range(1, 9):
            self.c.create_line(i * 80 + 1, 40, i * 80, 760, width=2.0, fill='#000000')
        for i in range(10):
            self.c.create_line(0, 40 + i * 80, 720, 40 + i * 80, width=2.0, fill='#000000')

        # 駒
        for p in range(81):
            p0, p1 = (p, 80 - p) if self.state.is_first_player() else (80 - p, p)
            if self.state.pieces[p0] != 0:
                self.draw_piece(p, self.state.is_first_player(), self.state.pieces[p0])
            if self.state.enemy_pieces[p1] != 0:
                self.draw_piece(p, not self.state.is_first_player(), self.state.enemy_pieces[p1])

        # 持ち駒
        self.draw_capture(self.state.is_first_player(), self.state.pieces)
        self.draw_capture(not self.state.is_first_player(), self.state.enemy_pieces)

        # 選択カーソル
        if 0 <= self.select and self.select <81:
            self.draw_cursor(int(self.select % 9) * 80, int(self.select / 9) * 80 + 40, 80)
        elif 81 <= self.select:
            self.draw_cursor((self.select - 81) * 40, 760, 40)

# ゲームUIの実行
f = GameUI(model=model)
f.pack()
f.mainloop()


