import tcod as libtcod
import tcod.event as event

from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message, MessageLog
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder


def main():
    # 画面サイズの変数
    screen_width = 80
    screen_height = 70

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2

    # 壁とタイルの色を初期化
    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150),
        "light_wall": libtcod.Color(130, 110, 50),
        "light_ground": libtcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, "@", libtcod.green, "player", blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    miya = Entity(0, 0, "C", libtcod.yellow, "miya", blocks=False, render_order=RenderOrder.ACTOR)
    tama = Entity(0, 0, "C", libtcod.white, "tama", blocks=False, render_order=RenderOrder.ACTOR)
    entities = [player, miya, tama]
    # フォントの指定と(libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD）でどのタイプのファイルを読み取るのかを伝える
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    panel = libtcod.console.Console(screen_width, panel_height)


    # ここで実際に画面を作成する、画面サイズとタイトルとフルスクリーンとレンダラーと画面の垂直同期を指定している
    with libtcod.console_init_root(screen_width, screen_height, "libtcod チュートリアル改訂",
                                    fullscreen=False, renderer=libtcod.RENDERER_SDL2, vsync=False
                                    ) as con:

        # ゲームマップの初期化
        game_map = GameMap(map_width, map_height)
        game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, miya, tama, entities,
                          max_monsters_per_room, max_items_per_room)

        # 視覚の計算
        fov_recompute = True

        fov_map = initialize_fov(game_map)

        message_log = MessageLog(message_x, message_width, message_height)


        # ゲームループと呼ばれるもの、ウィンドウを閉じるまでループする
        while True:
            # 視覚の計算
            if fov_recompute:
                recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

            # ループに記述することでマウスの情報を取得し続ける
            mouse = libtcod.event.get_mouse_state()

            # entityをここから呼び出す
            render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                       screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)

            fov_recompute = False

            # 画面上に描画する機能
            libtcod.console_flush()

            # 移動後のentitiesをスペース（" "）で上書きして消す
            clear_all(con, entities)

            # event.get()イテレータをループで回し各キーの押下判定を行う
            for events in libtcod.event.get():
                if events.type == "QUIT":
                    raise SystemExit()

                if events.type == "KEYDOWN":

                    # handle_keysから各種変数を作っていく
                    action = handle_keys(events)

                    move = action.get("move")
                    pickup = action.get("pickup")
                    show_inventory = action.get("show_inventory")
                    exit = action.get("exit")
                    fullscreen = action.get("fullscreen")

                    player_turn_results = []
                    
                    if move and game_state == GameStates.PLAYERS_TURN:
                        dx, dy = move  # action.get("move")で取得した値がdx, dyに代入される
                        
                        # プレイヤーの位置＋dx,dyで移動位置を決める
                        destination_x = player.x + dx
                        destination_y = player.y + dy

                        
                        if not game_map.is_blocked(destination_x, destination_y):
                            target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                            if target:
                                attack_results = player.fighter.attack(target)
                                player_turn_results.extend(attack_results)
                            else:
                                player.move(dx, dy)

                                fov_recompute = True

                            game_state = GameStates.ENEMY_TURN
                    elif pickup and game_state == GameStates.PLAYERS_TURN:
                        for entity in entities:
                            if entity.item and entity.x == player.x and entity.y == player.y:
                                pickup_results = player.inventory.add_item(entity)
                                player_turn_results.extend(pickup_results)

                                break
                        else:
                            message_log.add_message(Message("There is nothing here to pick up.", libtcod.yellow))
                    
                    if show_inventory:
                        previous_game_state = game_state
                        game_state = GameStates.SHOW_INVENTORY

                    if exit:
                        if game_state == GameStates.SHOW_INVENTORY:
                            game_state = previous_game_state
                        else:
                            return False

                    if fullscreen:
                        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

                    for player_turn_result in player_turn_results:
                        message = player_turn_result.get("message")
                        dead_entity = player_turn_result.get("dead")
                        item_added = player_turn_result.get("item_added")

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                        if item_added:
                            entities.remove(item_added)

                            game_state = GameStates.ENEMY_TURN

                    if game_state == GameStates.ENEMY_TURN:
                        for entity in entities:
                            if entity.ai:
                                enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                                for enemy_turn_result in enemy_turn_results:
                                    message = enemy_turn_result.get("message")
                                    dead_entity = enemy_turn_result.get("dead")

                                    if message:
                                        message_log.add_message(message)

                                    if dead_entity:
                                        if dead_entity == player:
                                            message, game_state = kill_player(dead_entity)
                                        else:
                                            message = kill_monster(dead_entity)

                                        message_log.add_message(message)

                                        if game_state == GameStates.PLAYERS_DEAD:
                                            break

                                if game_state == GameStates.PLAYERS_DEAD:
                                    break

                        else:
                            game_state = GameStates.PLAYERS_TURN



# 明示的に実行された時のみmain()関数を実行する
if __name__ == "__main__":
    main()

