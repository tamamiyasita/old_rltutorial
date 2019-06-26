class Entity:
    """
    プレイヤー、敵、アイテムなどを表す汎用オブジェクト
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # entityを移動させる関数
        self.x += dx
        self.y += dy

