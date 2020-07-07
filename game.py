# ====================
# 簡易将棋
# ====================

# パッケージのインポート
import random
import math
import multiprocessing as mp
from multiprocessing import Pool

# ゲームの状態
class State:
    # 初期化
    def __init__(self, pieces=None, enemy_pieces=None, depth=0):
        # 方向定数
        self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1),(1, -2),(-1, -2),
                    (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (8, -8),
                    (-1, 1), (-2, 2), (-3, 3), (-4, 4),(-5, 5), (-6, 6), (-7, 7), (-8, 8),
                    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                    (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), (-8, -8),
                    (1, 0), (2, 0),(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                    (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0),(-6, 0), (-7, 0), (-8, 0),
                    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                    (0, -1),(0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (0, -8))
        self.hop = ()
        # 駒の配置
        self.pieces = pieces if pieces != None else [0] * (81 + 3)
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * (81 + 3)
        self.depth = depth
        """
        self.pieces = pieces if pieces != None else [0] * (12 + 3)
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * (12 + 3)
        self.depth = depth
        """
        # 駒の初期配置
        if pieces == None or enemy_pieces == None:
            self.pieces = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           1, 1, 1, 1, 1, 1, 1, 1, 1,
                           0, 2, 0, 0, 0, 0, 0, 3, 0,
                           8, 7, 6, 5, 4, 5, 6, 7, 8,
                           0, 0, 0, 0, 0, 0, 0, 0]
            self.enemy_pieces =[0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0,
                                1, 1, 1, 1, 1, 1, 1, 1, 1,
                                0, 2, 0, 0, 0, 0, 0, 3, 0,
                                8, 7, 6, 5, 4, 5, 6, 7, 8,
                                0, 0, 0, 0, 0, 0, 0, 0]

        self.lose = True
        self.hansoku = False



    # 負けかどうか

    def is_lose(self):

        for i in range(81):

            if self.pieces[i] == 4:  # ライオン存在

                return False



        return True



    #勝ちかどうか

    def is_win(self):

        for i in range(9):

            nifu = 0

            #print(i,":check")

            for j in range(9):

                if self.enemy_pieces[(i+9*j)] == 1:

                    #print(j,(i+9*j),"にあります")

                    nifu = nifu +1



            if nifu >1:

                print("二歩")

                return True

        for i in range(9):

            for j in range(2):

                if self.enemy_pieces[(i + 9 * j)] == 7:

                    print("桂馬の禁じ手")

                    return True

        for i in range(9):

            if self.enemy_pieces[i] == 8 or self.enemy_pieces[i] == 1 :

                print("香車か歩の禁じ手")

                return True



        return False

    # 引き分けかどうか
    def is_draw(self):
        return self.depth >= 300  # 300手

    # ゲーム終了かどうか
    def is_done(self):
        return self.is_lose() or self.is_draw() or self.is_win()

    # デュアルネットワークの入力の2次元配列の取得
    def pieces_array(self):
        # プレイヤー毎のデュアルネットワークの入力の2次元配列の取得
        def pieces_array_of(pieces):
            table_list = []

            for j in range(1, 8):
                table = [0] * 81
                table_list.append(table)
                for i in range(81):
                    if pieces[i] == j:
                        table[i] = 1

            for j in range(1, 8):#持ち駒参照
                flag = 1 if pieces[80 + j] > 0 else 0
                table = [flag] * 81
                table_list.append(table)
            return table_list


        # デュアルネットワークの入力の2次元配列の取得
        return [pieces_array_of(self.pieces), pieces_array_of(self.enemy_pieces)]

    # 駒の移動先と移動元を行動に変換
    def position_to_action(self, position, direction):
        return position * 100 + direction

    # 行動を駒の移動先と移動元に変換
    def action_to_position(self, action):
        return (int(action / 100), action % 100)

    def leg_act(self,inputs):
        actions,p = inputs
        if self.pieces[p] != 0:
            actions.extend(self.legal_actions_pos(p))
            # 持ち駒の配置時
        if self.pieces[p] == 0 and self.enemy_pieces[80 - p] == 0:
            for capture in range(8):  # 持ち駒の参照
                capture = capture + 1
                # print(capture)
                if capture == 1:
                    if p > 8:  # 歩、一段の禁じ手回避
                        # 二歩の回避
                        i = p % 9
                        nifucheck = 0
                        for j in range(9):
                            if self.pieces[(i + 9 * j)] == 1:
                                nifucheck = nifucheck + 1
                        if nifucheck == 0:
                            if self.pieces[80 + capture] > 0:
                                # print("歩回避で座標は",p)
                                # print(self.position_to_action(p, 74 - 1 + capture))
                                actions.append(self.position_to_action(p, 74 - 1 + capture))
                        else:
                            pass
                    else:
                        pass
                # 香車、一段の禁じ手回避したら
                elif capture == 8:
                    if p > 8:
                        if self.pieces[80 + capture] > 0:
                            # print("香車回避",p)
                            # print(self.position_to_action(p, 74 - 1 + capture))
                            actions.append(self.position_to_action(p, 74 - 1 + capture))
                    else:
                        pass
                # 桂馬、一、二段の禁じ手回避したら
                elif capture == 7:
                    if p > 17:
                        if self.pieces[80 + capture] > 0:
                            # print("桂馬回避",p)
                            # print(self.position_to_action(p, 74 - 1 + capture))
                            actions.append(self.position_to_action(p, 74 - 1 + capture))
                    else:
                        pass
                # 歩と香車と桂馬以外は
                else:
                    if self.pieces[80 + capture] > 0:
                        # print("駒うち",p)
                        # print(self.position_to_action(p, 74 - 1 + capture))
                        actions.append(self.position_to_action(p, 74 - 1 + capture))


    # 合法手のリストの取得
    def legal_actions(self):
        #actions = []
        actions = mp.Manager().list()
        p = Pool(mp.cpu_count())
        values = [(actions,x) for x in range(81)]
        p.map(self.leg_act, values)
        p.close()


        """
        for p in range(81):
            # 駒の移動時
            if self.pieces[p] != 0:
                actions.extend(self.legal_actions_pos(p))
            # 持ち駒の配置時
            if self.pieces[p] == 0 and self.enemy_pieces[80 - p] == 0:
                for capture in range(8):#持ち駒の参照
                    capture = capture+1
                    #print(capture)
                    if capture == 1:
                        if p >8 :#歩、一段の禁じ手回避
                            #二歩の回避
                            i = p % 9
                            nifucheck = 0
                            for j in range(9):
                                if self.pieces[(i + 9 * j)] == 1:
                                    nifucheck = nifucheck + 1
                            if nifucheck == 0:
                                if self.pieces[80 + capture] > 0:
                                    #print("歩回避で座標は",p)
                                    #print(self.position_to_action(p, 74 - 1 + capture))
                                    actions.append(self.position_to_action(p, 74 - 1 + capture))
                            else:pass
                        else:pass
                    # 香車、一段の禁じ手回避したら
                    elif capture == 8:
                        if p > 8:
                            if self.pieces[80 + capture] > 0:
                                #print("香車回避",p)
                                #print(self.position_to_action(p, 74 - 1 + capture))
                                actions.append(self.position_to_action(p, 74 - 1 + capture))
                        else: pass
                    # 桂馬、一、二段の禁じ手回避したら
                    elif capture == 7:
                        if p > 17:
                            if self.pieces[80 + capture] > 0:
                                #print("桂馬回避",p)
                                #print(self.position_to_action(p, 74 - 1 + capture))
                                actions.append(self.position_to_action(p, 74 - 1 + capture))
                        else:pass
                    #歩と香車と桂馬以外は
                    else:
                        if self.pieces[80 + capture] > 0:
                            #print("駒うち",p)
                            #print(self.position_to_action(p, 74 - 1 + capture))
                            actions.append(self.position_to_action(p, 74 - 1 + capture))
            """
        #print("actions",actions)
        return actions

    # 駒の移動時の合法手のリストの取得
    def legal_actions_pos(self, position_src):
        actions = []

        # 駒の移動可能な方向
        piece_type = self.pieces[position_src]
        if piece_type > 18:
            piece_type - 18
        directions = []
        if piece_type == 1:  # hu
            directions = [0]
        elif piece_type == 2:  # kaku
            for n in range(4):
                for i in range(8):
                    x = position_src % 9 + self.dxy[9+(8*n)+i+1][0]
                    y = int(position_src / 9) + self.dxy[9+(8*n)+i+1][1]
                    p = x + y * 9
                    # 移動可能時は合法actionとして追加
                    if 0 <= x and x <= 8 and 0 <= y and y <= 8 and self.pieces[p] == 0:
                        directions.append(9+(8*n)+i+1)
                        if self.enemy_pieces[80 - p]!=0:
                            #print("角break")
                            break
                    else:
                        break
        elif piece_type == 3:  # hisya
            for n in range(4):
                for i in range(8):
                    x = position_src % 9 + self.dxy[41+(8*n)+i+1][0]
                    y = int(position_src / 9) + self.dxy[41+(8*n)+i+1][1]

                    p = x + y * 9
                    # 移動可能時は合法actionとして追加
                    if 0 <= x and x <= 8 and 0 <= y and y <= 8 and self.pieces[p] == 0:
                        directions.append(41+(8*n)+i+1)
                        if self.enemy_pieces[80 - p]!=0:
                            break
                    else:
                        break
            #print(directions)
        elif piece_type == 4:  # ou
            directions = [0, 1, 2, 3, 4, 5, 6, 7]
        elif piece_type == 5:  # kin
            directions = [0, 1, 2, 4, 6, 7]
        elif piece_type == 6:  # gin
            directions = [0, 1, 3, 5, 7]
        elif piece_type == 7:  # kei
            directions = [8, 9]
        elif piece_type == 8:  # kyou
            for i in range(8):
                x = position_src % 9 + self.dxy[65 + i+1][0]
                y = int(position_src / 9) + self.dxy[65 + i+1][1]
                p = x + y * 9
                # 移動可能時は合法actionとして追加
                if 0 <= x and x <= 8 and 0 <= y and y <= 8 and self.pieces[p] == 0:
                    directions.append(65 + i + 1)
                    if self.enemy_pieces[80 - p]==0:
                        break
                else:
                    break
        elif piece_type == 11:  # to
            directions = [0, 1, 2, 4, 6, 7]
        elif piece_type == 12:  # uma
            directions = [2,4,6,8]
            for n in range(4):
                for i in range(8):
                    x = position_src % 9 + self.dxy[9+(8*n)+i+1][0]
                    y = int(position_src / 9) + self.dxy[9+(8*n)+i+1][1]
                    p = x + y * 9
                    # 移動可能時は合法actionとして追加
                    if 0 <= x and x <= 8 and 0 <= y and y <= 8 and self.pieces[p] == 0:
                        directions.append(9 + (8 * n) + i + 1)
                        if self.enemy_pieces[80 - p] != 0:
                            break
                    else:
                        break
        elif piece_type == 13:  # ryu
            directions = [1, 3, 5, 7]
            for n in range(4):
                for i in range(8):
                    x = position_src % 9 + self.dxy[41+(8*n)+i+1][0]
                    y = int(position_src / 9) + self.dxy[41+(8*n)+i+1][1]

                    p = x + y * 9
                    # 移動可能時は合法actionとして追加
                    if 0 <= x and x <= 8 and 0 <= y and y <= 8 and self.pieces[p] == 0:
                        directions.append(41 + (8 * n) + i + 1)
                        if self.enemy_pieces[80 - p] != 0:
                            break
                    else:
                        break
        elif piece_type == 16:  # narigin
            directions = [0, 1, 2, 4, 6, 7]
        elif piece_type == 17:  # narikei
            directions = [0, 1, 2, 4, 6, 7]
        elif piece_type == 18:  # narikyou
            directions = [0, 1, 2, 4, 6, 7]

        # 合法手の取得
        for direction in directions:
            # 駒の移動元
            x = position_src % 9 + self.dxy[direction][0]
            y = int(position_src / 9) + self.dxy[direction][1]
            p = x + y * 9

            # 移動可能時は合法手として追加
            if 0 <= x and x <= 8 and 0 <= y and y <= 8 and self.pieces[p] == 0:
                #print(position_src)
                if (p < 27 or position_src < 27) and piece_type < 9:#成りも候補に
                    #print("成りの追加",p,direction)
                    #print(self.position_to_action(p, direction))
                    actions.append(self.position_to_action(p, direction))
                    #print(self.position_to_action(p, direction+10000))
                    actions.append(self.position_to_action(p, direction+10000))
                else:#成りなし
                    #print("成りなし")
                    #print(self.position_to_action(p, direction))
                    actions.append(self.position_to_action(p, direction))


        return actions

    # 次の状態の取得
    def next(self, action):
        #hzkr0 = ('', '歩', '角', '飛', '王', '金', '銀', '桂', '香', '', '', 'と', '馬', '龍', '', '', 'NG', 'KM', 'KY',)

        # 次の状態の作成
        state = State(self.pieces.copy(), self.enemy_pieces.copy(), self.depth + 1)

        if action > 10000:
            action = action-10000
            position_dst, position_src = self.action_to_position(action)
            x = position_dst % 9 - self.dxy[position_src][0]
            y = int(position_dst / 9) - self.dxy[position_src][1]
            position_src = x + y * 9
            """
            print("********************************************")
            if self.depth % 2 == 0:
                #print(position_src)
                #print(state.pieces[position_src])
                print(state.depth, "手*", 9 - position_dst % 9, int(position_dst / 9) + 1,
                      hzkr0[state.pieces[position_src]], "成")
            elif self.depth % 2 == 1:
                #print(position_src)
                #print(state.pieces[position_src])
                print(state.depth, "手：", 9 - (80 - position_dst) % 9, int((80 - position_dst) / 9) + 1,
                      hzkr0[state.pieces[position_src]], "成")
            print("********************************************")
            """
            state.pieces[position_dst] = state.pieces[position_src] + 10
            state.pieces[position_src] = 0

            piece_type = state.enemy_pieces[80 - position_dst]
            if piece_type != 0:
                if piece_type != 4:
                    if piece_type > 8:  # なりごまの処理
                        piece_type = piece_type - 10
                    state.pieces[80 + piece_type] += 1  # 持ち駒+1
                state.enemy_pieces[80 - position_dst] = 0

        else:
            # print(action)
            # 行動を(移動先, 移動元)に変換
            position_dst, position_src = self.action_to_position(action)
            # print(self.dxy[position_src])

            #確認用
            #print(action, position_dst, position_src)

            # 駒の移動
            if position_src < 74:  # dxyの数
                # 駒の移動元
                x = position_dst % 9 - self.dxy[position_src][0]
                y = int(position_dst / 9) - self.dxy[position_src][1]
                position_src = x + y * 9

                # 駒の移動
                """
                if self.depth % 2 == 0:
                    print(state.depth, "手*", 9 - position_dst % 9, int(position_dst / 9) + 1,
                          hzkr0[state.pieces[position_src]])
                elif self.depth % 2 == 1:
                    print(state.depth, "手：", 9 - (80 - position_dst) % 9, int((80 - position_dst) / 9) + 1,
                          hzkr0[state.pieces[position_src]])
                """

                # 歩と香車は、一段目で強制的に成る
                if position_dst < 9 and (state.pieces[position_src] == 1 or state.pieces[position_src] == 8):
                    state.pieces[position_dst] = state.pieces[position_src] + 10
                # 桂馬は、一、二段目で強制的に成る
                elif position_dst < 18 and state.pieces[position_src] == 7:
                    state.pieces[position_dst] = state.pieces[position_src] + 10
                else:
                    state.pieces[position_dst] = state.pieces[position_src]
                state.pieces[position_src] = 0

                # 相手の駒が存在する時は取る
                piece_type = state.enemy_pieces[80 - position_dst]
                if piece_type != 0:
                    if piece_type != 4:
                        if piece_type > 8:  # なりごまの処理
                            piece_type = piece_type - 10
                        state.pieces[80 + piece_type] += 1  # 持ち駒+1
                    state.enemy_pieces[80 - position_dst] = 0

                # 持ち駒の配置
            elif position_src < 82:
                capture = position_src - 73
                xx = position_dst % 9 + 1
                yy = int(position_dst / 9) + 1

                #print(state.depth, "手：", xx, yy, hzkr0[capture], "打")

                state.pieces[position_dst] = capture
                state.pieces[80 + capture] -= 1  # 持ち駒-1






        # 駒の交代
        w = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = w
        #print("一手")
        return state

    # 先手かどうか
    def is_first_player(self):
        return self.depth % 2 == 0

    # 文字列表示
    def __str__(self):
        pieces0 = self.pieces if self.is_first_player() else self.enemy_pieces
        pieces1 = self.enemy_pieces if self.is_first_player() else self.pieces
        hzkr0 = ('', '歩', '角', '飛', '王', '金', '銀', '桂', '香', '','', 'と', '馬', '龍', '', '', 'NG', 'KM', 'KY')
        hzkr1 = ('', 'ふ', 'ｶｸ', 'ﾋｼ', 'ｵｳ', 'ｷﾝ', 'ｷﾞ', 'ｹｲ', 'ｷｮ', '','', 'と', '馬', '龍', '', '', 'NG', 'KM', 'KY')

        # 後手の持ち駒
        str = ' ['
        for i in range(81, 89):
            #print(i)
            if pieces1[i] >= 2: str += ' ' + hzkr1[i - 80]
            if pieces1[i] >= 1: str += ' ' + hzkr1[i - 80]
        str += ' ]\n'

        # ボード
        for i in range(81):
            #print(i)
            if pieces0[i] != 0:
                #print("盤",i,pieces0[i])
                str += '|' + hzkr0[pieces0[i]]
            elif pieces1[80 - i] != 0:
                str += '|' + hzkr1[pieces1[80 - i]]
            else:
                str += '|　'
            if i % 9 == 8:
                str += '|\n'

        # 先手の持ち駒
        str += ' ['
        for i in range(81, 89):
            if pieces0[i] >= 2: str += ' ' + hzkr0[i - 80]
            if pieces0[i] >= 1: str += ' ' + hzkr0[i - 80]
        str += ' ]\n'
        return str


    # ランダムで行動選択
def random_action(state):
    #print("state_legal",state.legal_actions())
    legal_actions = state.legal_actions()
    num = random.randint(0, len(legal_actions) - 1)
    #print(num)
    return legal_actions[num]



# 動作確認
if __name__ == '__main__':
        #for i in range(10):
            # 状態の生成
            state = State()
            # random.seed(2)

            # ゲーム終了までのループ
            while True:
                # ゲーム終了時
                if state.is_done():
                    break

                # 次の状態の取得
                xxx = random_action(state)
                #print("rand",xxx)
                state = state.next(xxx)

                # 文字列表示
                #print(state.pieces)
                #print(state.enemy_pieces)
                print(state)
                print()