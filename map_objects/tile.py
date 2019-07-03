class Tile:
    """
    視線や移動をブロックする壁と移動可能なタイルを作成する
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # デフォルトでは壁判定なら視線もブロックする
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False