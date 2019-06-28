from random import randint
from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # マップを壁で埋めて初期化
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # ランダムで幅と高さを決める
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # マップの範囲内でランダムな位置の指定
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            # "Rect" クラスで部屋を生成する
            new_room = Rect(x, y, w, h)

            # 部屋と部屋が重複するかの判定
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                # 重複が無ければ部屋を作成
                self.create_room(new_room)

                # 作成した部屋の中心座標
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # playerが居る最初の部屋
                    player.x = new_x
                    player.y = new_y
                else:
                    # 最初の部屋以降部屋と部屋の中心座標どうしをトンネルで繋いでいく
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # 次の二つからランダムに選ぶ
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # 新しい部屋をリストに追加する
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # 四角形のタイルを指定して通過可能にする
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False