import tcod as libtcod
import math
import itertools
from render_functions import RenderOrder

class Entity:
    """
    プレイヤー、敵、アイテムなどを表す汎用オブジェクト
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        # entityを移動させる関数
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        # mapの寸法を持つfovマップを作製する
        fov = libtcod.map_new(game_map.width, game_map.height)

        # 現在の地図を毎回スキャンし、全ての壁を歩けないように設定する
        for y1, x1 in itertools.product(range(game_map.height), range(game_map.width)):
            libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                        not game_map.tiles[x1][y1].blocked)

        # 全てのオブジェクトをスキャンして移動させるオブジェクトを確認する
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        my_path = libtcod.path_new_using_map(fov, 1.41)

        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)

        libtcod.path_delete(my_path)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None

