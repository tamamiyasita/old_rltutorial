
import tcod as libtcod
from random import randint

from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

from map_objects.rectangle import Rect
from map_objects.tile import Tile
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        # マップを壁で埋めて初期化
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for _ in range(max_rooms):
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

                # 作成した部屋の中心座標を変数に格納
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # 初回はとりあえずplayerが居る最初の部屋の作成だけしてroomsリストに追加しnum_roomsに＋１する
                    player.x = new_x
                    player.y = new_y

                else:
                    # 二回目以降に前の部屋の中心座標を変数prev_x,yに入れる(当然新しい部屋の座標はnew_x,yに入っている)
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # 前の部屋の中心座標と現在の部屋の中心座標からトンネル関数で部屋を彫っていく
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # ここでモンスターたちを部屋に配置する
                self.place_entities(new_room, entities)

                # 新しい部屋をリストに追加する
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, ">", libtcod.white, "Stairs",
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)

        entities.append(down_stairs)

    def create_room(self, room):# newroom(Rect)変数の値をroomに入れる
        # 壁に埋められたtilesマップを四角く掘り出す
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):  # 前作った部屋と現在作った部屋の座標がｘ1とｘ2に入り、
        # ｙ、ｘの座標から横に(max(x1, x2))の位置まで掘る(次のはその逆)
        # つまりこのマップアルゴリズムは横ｘと縦ｙの一本の曲がり角で部屋どうしを繋いでいく感じになる
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        
        """ダンジョンに敵を配置する機能"""
        # モンスターを何体部屋に配置するかランダムに決める
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            "orc": 80,
            "troll": from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
            }

        item_chances = {
            "healing_potion": 35,
            "stone_sword": from_dungeon_level([[5, 4]], self.dungeon_level),
            "wood_shield": from_dungeon_level([[15, 8]], self.dungeon_level),
            "lightning_scroll": from_dungeon_level([[25, 4]], self.dungeon_level),
            "fireball_scroll": from_dungeon_level([[25, 6]], self.dungeon_level),
            "confusion_scroll": from_dungeon_level([[10, 2]], self.dungeon_level)
            }

        for _ in range(number_of_monsters):
            # 部屋のどのあたりにmonsterを配置するかランダムに決める
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # ランダムな場所を選びそこにモンスターとかアイテムとかがなければ配置する
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == "orc":
                    fighter_component = Fighter(hp=10, defense=0, power=3, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, "o", libtcod.desaturated_green, "Orc", blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=26, defense=1, power=4, xp=100)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, "T", libtcod.dark_green, "Troll", blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                # entitiesに格納する
                entities.append(monster)

        for _ in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == "healing_potion":
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, "!", libtcod.violet, "Healing Potion", render_order=RenderOrder.ITEM,
                                  item=item_component)

                elif item_choice == "stone_sword":
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, "/", libtcod.sky, "Stone_Sword", equippable=equippable_component)

                elif item_choice == "wood_shield":
                    equippable_component = Equippable(EquipmentSlots.OFF_HAMD, defense_bones=1)
                    item = Entity(x, y, "[", libtcod.darker_orange, "Wood_Shield", equippable=equippable_component)

                elif item_choice == "fireball_scroll":
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                                          "lift-click a target tile for the fireball, or right-click to cancel.", libtcod.light_cyan),
                                                            damage=22, radius=3)
                    item = Entity(x, y, "#", libtcod.red, "Fireball Scroll", render_order=RenderOrder.ITEM,
                                  item=item_component)

                elif item_choice == "confusion_scroll":
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                                "Left-click an enemy to confuse it, or right-click to cansel.", libtcod.light_cyan))
                    item = Entity(x, y, "#", libtcod.light_pink, "Confusion Scroll", render_order=RenderOrder.ITEM,
                                  item=item_component)

                else:
                    item_component = Item(use_function=cast_lightning, damage=30, maximum_range=5)
                    item = Entity(x, y, "#", libtcod.yellow, "Lightning Scroll", render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)


    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants["max_rooms"], constants["room_min_size"], constants["room_max_size"],
                      constants["map_width"], constants["map_height"], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message("You take a moment to rest, and recover your strength.", libtcod.light_violet))

        return entities