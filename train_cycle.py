# ====================
# 学習サイクルの実行
# ====================

# パッケージのインポート
from dual_network import dual_network
from self_play import self_play
from train_network import train_network
from evaluate_network import evaluate_network



# デュアルネットワークの作成
dual_network()

for i in range(10):
    print('Train', i , '========================================')
    # セルフプレイ部
    self_play()

    # パラメータ更新部
    train_network()

    # 新ハ゜ラメータ評価部
    evaluate_network()

"""
def train__cycle(args):
    for i in range(10):
        print('Train',args+i+1,'========================================')
        # セルフプレイ部
        self_play()

        # パラメータ更新部
        train_network()

        # 新ハ゜ラメータ評価部
        evaluate_network()

if __name__ == "__main__":
    dual_network()
    p = Pool(mp.cpu_count())
    p.map(train__cycle,range(5))
    p.close()
"""
