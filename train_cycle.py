# ====================
# 学習サイクルの実行
# ====================

# パッケージのインポート
from dual_network import dual_network
from self_play import self_play
from train_network import train_network
from evaluate_network import evaluate_network
import multiprocessing as mp
from multiprocessing import Pool
import os
import tensorflow as tf
import logging
import warnings
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)
tf.get_logger().setLevel(logging.ERROR)
"""
"""
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.compat.v1.Session(config=config)
"""
if __name__ == "__main__":
    # デュアルネットワークの作成

#dual_network()
#def train__cycle(args):
    #for i in range(10):
        #print('Train', args + i + 1, '========================================')
        # セルフプレイ部
        #self_play()

        # パラメータ更新部
        #train_network()

        # 新ハ゜ラメータ評価部
        #evaluate_network()


#if __name__ == "__main__":
    """
    dual_network()
    p = Pool(mp.cpu_count())
    p.map(train__cycle,range(3))
    p.close()
    """
# デュアルネットワークの作成
    dual_network()
    
    for i in range(2):
        print('Train', i, '========================================')
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
        p.map(train__cycle,range(3))
        p.close()
"""